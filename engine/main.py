#!/usr/bin/env python3

import filesys
import ComicEngine
import urllib.error
import argparse
import sys
import re
import os
import time
import feedback
import web
import cbz
import state

"""

Usage:

Download a comic, optionally specifying start/end chapters

If a directory is specified, will try to download from the last registered chapter.

    cbzdl { URL | COMICDIR } [-s START] [-e END] [-d DELAY]

Re-attempt the download of the missing pages of a chapter.

    cbzdl CHAPDIR [-d DELAY]

"""

step_delay = 1
ch_start = -1
ch_end = 9000

def abbreviateUrl(url, max=60):
    """ Reduce long URLs for screen display
    """
    if len(url) > max:
        mid = int( (max - 5)/2 )
        return "%s ... %s"%(url[:mid],url[-mid:])
    return url

def downloadPage(cengine, page_url, chapter_dir):
    """ Download an individual page

    Takes care of zero-padding page numbers
    """
    feedback.info("    Fetch %s"%abbreviateUrl(page_url) )
    page        = cengine.Page(page_url)

    image_url   = page.getImageUrl()
    resource    = web.WebResource(image_url)
    # TODO pre-detect existing pages, don't re-download
    image_file  = os.path.sep.join( [chapter_dir, 'page_' + page.getPageNumber().zfill(4) + '.' + resource.getExtension()] )

    resource.saveTo(image_file)

def downloadChapter(cengine, chapter_url, comic_dir):
    """ Kicks off the page downloads for a chapter

    Checks whether chapter number is within specified bounds
    
    On completion, if there were no page download errors, attempts CBZ creation

    Returns number of errors encountered
    """
    feedback.debug("Start on %s ..."%chapter_url)

    global step_delay
    global ch_start
    global ch_end

    chapter     = cengine.Chapter(chapter_url)
    chapter_num = float(chapter.getChapterNumber() )
    
    if chapter_num < ch_start:
        return 0
    elif chapter_num > ch_end:
        return 'max'
    
    # IF no start was specified THEN use the last success as base
    if ch_start == -1 and chapter_num <= dlstate.get("last"):
        return 0

    feedback.info("  Get %s"%chapter_url)

    page_urls   = chapter.getPageUrls()
    if page_urls == None:
        return ['%s not a valid chapter'%chapter_num]

    chapter_dir = os.path.sep.join([comic_dir, chapter.getChapterLowerName()])

    feedback.info("    %i pages"%len(page_urls))

    failed_urls = []
    for url in page_urls:
        try:
            downloadPage(cengine, url, chapter_dir)
        except ComicEngine.ComicError as e:
            feedback.warn("Oops : %s"%str(e) )
            failed_urls.append(url)
        except urllib.error.URLError as e:
            feedback.warn("Could not download %s"%url)
            failed_urls.append(url)
        except web.DownloadError as e:
            feedback.warn("%i : %s"%(e.code,str(e)) )
            failed_urls.append(url)

        time.sleep(step_delay)

    if len(failed_urls) == 0:
        feedback.debug("  Compiling to CBZ ...")
        try:
            cbz.CBZArchive(chapter_dir).compile(remove_dir=True)
            dlstate.set("last", chapter_num) # Inequivocable success !
        except Exception as e:
            feedback.warn( str(e) )
            errors += 1

    return failed_urls

def downloadComic(cengine, comic_url):
    """ Downloads the chapters of a comic

    Displays any failed chapters after execution
    """
    feedback.info("Downloading %s"%comic_url)

    comic        = cengine.Comic(comic_url)
    chapter_urls = comic.getChapterUrls()
    comic_dir    = comic.getComicLowerName()

    feedback.info("  %i chapters (total)" % len(chapter_urls))

    failed_chapters = {}
    for url in chapter_urls:
        failed_urls = downloadChapter(cengine, url, comic_dir)

        if failed_urls == 'max':
            # exceeded max chapter
            break

        elif failed_urls == 0:
            continue # not reached min chapter

        elif len(failed_urls) > 0:
            feedback.warn("Failed %s"%url)
            failed_chapters[url] = failed_urls

    return failed_chapters

def parseArguments():

    parser = argparse.ArgumentParser(sys.argv, description="Download a comic")
    parser.add_argument("url", type=str, help="The URL of the comic to download")
    parser.add_argument("-s", "--start", action="store", default=-1, type=float, help="Minimum chapter to start from")
    parser.add_argument("-e", "--end", action="store", default=9000, type=float, help="Maximum chapter to include (up to 9000)")
    parser.add_argument("-d", "--delay", action='store', type=int, default=-1, help="Delay to introduce during download (seconds)")
    parser.add_argument("-v", "--verbose", action='store_true', help="Verbose mode")
    parser.add_argument("-f", "--failed", action='store_true', help="Check for failed items")
    parser.add_argument("-l", "--last", action='store_true', help="Display last successfully downloded chapter")

    return parser.parse_args()

def checkSpecialCases(keyword):
    global dlstate

    if keyword == "modules":
        print(ComicEngine.getAvailableModuleNames() )
        exit(0)

def checkState(args):
    if args.failed:
        if dlstate.has("failed_chapters") and dlstate.get("failed_chapters") != None:
            feedback.warn(str(dlstate.get("failed_chapters") ) )
        else:
            feedback.info("No failures to report.")
        exit(0)
    elif args.last:
        if dlstate.has("last"):
            feedback.info(str(dlstate.get("last") ) )
        else:
            feedback.info("No failures to report.")
        exit(0)

def initializeState():
    if ch_start != -1:
        dlstate.set("last", ch_start)

    try:
        dlstate.get("last")
    except state.ComicStateError as e:
        dlstate.set("last", -1)

    # TODO manage failed chapters in state file instead of initializing on each run
    dlstate.set("failed_chapters", None)

def main():
    global step_delay
    global ch_start
    global ch_end
    global dlstate

    args = parseArguments()
    feedback.debug_mode = args.verbose

    checkSpecialCases(args.url)

    dlstate = state.DownloaderState(args.url)
    checkState(args)

    ch_start = args.start
    ch_end = args.end

    initializeState()

    try:
        cengine = dlstate.cengine
        comic_url = dlstate.get("url")

        if args.delay >= 0:
            step_delay = args.delay

        elif 'recommended_delay' in dir(cengine):
            step_delay = cengine.recommended_delay

        else:
            step_delay = 1

        feedback.debug("Delay chosen: %i" % step_delay)

        failed = downloadComic(cengine, comic_url)

    except ComicEngine.ComicError as e:
        feedback.fail(str(e) )

    if len(failed) > 0:
        feedback.error("Failed:")
        for chapter in failed:
            feedback.error("# %s"%chapter )

        dlstate.set("failed_chapters", failed)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        feedback.fail("(abort)")
