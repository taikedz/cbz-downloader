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

"""

Usage:

Download a comic, optionally specifying start/end chapters

If a directory is specified, will try to download from the last registered chapter.

    cbzdl { URL | COMICDIR } [-s START] [-e END] [-d DELAY]

Re-attempt the download of the missing pages of a chapter.

    cbzdl CHAPDIR [-d DELAY]

"""

step_delay = 1
ch_start = 0
ch_end = 9000

def url_display(url):
    if len(url) > 60:
        return "%s ... %s"%(url[:30],url[-30:])
    return url

def downloadPage(cengine, page_url, chapter_dir):
    feedback.info("    Fetch %s"%url_display(page_url) )
    page        = cengine.Page(page_url)

    image_url   = page.getImageUrl()
    resource    = web.WebResource(image_url)
    image_file  = os.path.sep.join( [chapter_dir, 'page_' + page.getPageNumber().zfill(4) + '.' + resource.getExtension()] )

    resource.saveTo(image_file)

def downloadChapter(cengine, chapter_url, comic_dir):
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

    feedback.info("  Get %s"%chapter_url)

    page_urls   = chapter.getPageUrls()
    chapter_dir = os.path.sep.join([comic_dir, chapter.getChapterLowerName()])

    errors = 0
    feedback.breakpoint("Page URLs: %s"%str(page_urls))
    for url in page_urls:
        try:
            downloadPage(cengine, url, chapter_dir)
        except ComicEngine.ComicError as e:
            feedback.warn("Oops : %s"%str(e) )
            errors += 1
        except urllib.error.URLError:
            feedback.warn("Could not download %s"%url)
            errors += 1

        time.sleep(step_delay)

    if errors == 0:
        feedback.debug("  Compiling to CBZ ...")
        try:
            cbz.CBZArchive(chapter_dir).compile(remove_dir=True)
        except Exception as e:
            feedback.warn( str(e) )
            errors += 1

    return errors

def downloadComic(cengine, comic_url):
    feedback.info("Downloading %s"%comic_url)

    comic        = cengine.Comic(comic_url)
    chapter_urls = comic.getChapterUrls()
    comic_dir    = comic.getComicLowerName()

    failed_chapters = []
    for url in chapter_urls:
        feedback.breakpoint("Get chapter %s"%url)
        errors = downloadChapter(cengine, url, comic_dir)

        if errors == 'max':
            # exceeded max chapter
            break

        elif errors > 0:
            feedback.warn("Failed %s"%url)
            failed_chapters.append(url)

    return failed_chapters

def parseArguments():

    parser = argparse.ArgumentParser(sys.argv, description="Download a comic")
    parser.add_argument("url", type=str, help="The URL of the comic to download")
    parser.add_argument("-s", "--start", action="store", default=0, type=int, help="Minimum chapter to start from")
    parser.add_argument("-e", "--end", action="store", default=9000, type=int, help="Maximum chapter to include (up to 9000)")
    parser.add_argument("-d", "--delay", action='store', type=int, default=1, help="Delay to introduce during download (seconds)")
    parser.add_argument("-v", "--verbose", action='store_true', help="Verbose mode")

    return parser.parse_args()

def extractUrl(url):
    if not os.path.isdir(url):
        return url

    sourceurl_file = os.path.sep.join([url, "source.url"])

    if os.path.isfile(sourceurl_file):
        fh = open(sourceurl_file, 'r')
        url = fh.read().strip()
        fh.close()
    else:
        raise ComicEngine.ComicError("No source.url file in %s"%url)

    return url

def saveUrl(cengine, url):
    comic_dir = cengine.Comic(url).getComicLowerName()
    sourceurl_file = os.path.sep.join([comic_dir, "source.url"])

    filesys.ensureDirectoryFor(sourceurl_file)
    fh = open(sourceurl_file, 'w')
    fh.write(url)
    fh.close()

def main():
    global step_delay
    global ch_start
    global ch_end

    args       = parseArguments()
    comic_url  = extractUrl(args.url)

    step_delay = args.delay
    ch_start   = args.start
    ch_end     = args.end
    feedback.debug_mode = args.verbose

    cengine = ComicEngine.determineFrom(comic_url)
    saveUrl(cengine, comic_url)

    failed = downloadComic(cengine, comic_url)

    if len(failed) > 0:
        feedback.error("Failed:")
        for f in failed:
            feedback.error("# "+f)

if __name__ == "__main__":
    main()
