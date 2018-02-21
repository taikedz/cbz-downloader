""" An example of a module file

To create a new module:

* Copy this to the cbzdl/modules folder
* Flesh out your copy of the file
* Edit ComicEngine.py and add your module to the list
"""

import web
import util
import re
import feedback
import ComicEngine
import base64

# Edit this to list the valid domains for the site
valid_domains = ['manga-here.io']

class ComicSite(web.WebResource):

    def __init__(self, url):
        url = self.validateUrl(url)

        web.WebResource.__init__(self, url)
        self.domain = web.getUrlComponents(url, 2)

    def validateUrl(self, url):
        """ If you want to rewrite the URL before accessing it, modify this section
        """
        return re.sub("^http:","https:",url)

class Comic(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)
        self.name = self.getComicLowerName()

    def getComicLowerName(self):
        return util.regexGroup("https://%s/([^/]+)" % self.domain, self.url)

    def getChapterUrls(self):
        doc = self.getDomObject()
        chapters = doc.get_element_by_id("list_chapter").cssselect(".row span a")

        urls = []

        for elem_a in chapters:
            path = elem_a.attrib['href']
            if re.match("/%s/chapter-[0-9.]+" % self.name, path):
                urls.append("https://%s%s"%(self.domain, path) )

        util.naturalSort(urls, ".+/chapter-([0-9.]+)$")

        return urls

class Chapter(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getChapterLowerName(self):
        return "%s-chapter-%s" % (
            util.regexGroup("https://%s/([^/]+)" % self.domain, self.url),
            self.getChapterNumber().zfill(4)
            )

    def getChapterNumber(self):
        return util.regexGroup(".+/chapter-([0-9.]+)", self.url)

    def getPageUrls(self):
        doc = self.getDomObject()

        image_nodes = doc.cssselect("img.fullsizable")

        page_urls = []
        # All pages are in one page - encode them and stuff them in a bogus query string
        i = 1
        for img in image_nodes:
            imgurl = img.attrib['src']
            feedback.debug(imgurl)
            pagenum = i
            i += 1

            if re.match(".+/nextchap.png", imgurl):
                continue

            page_urls.append("%s?u=%s&n=%s"%(self.url , base64.urlsafe_b64encode(imgurl.encode("utf-8")).decode("utf-8"), pagenum) )

        return page_urls

class Page(ComicSite):

    def __init__(self, url):
        ComicSite.__init__(self, url)
        self.pagenum = util.regexGroup(".+n=([0-9]+)", self.url)
        self.imgurl = base64.urlsafe_b64decode( util.regexGroup(".+u=([^&]+)", self.url) ).decode("utf-8")

    def getPageNumber(self):
        return self.pagenum

    def getImageUrl(self):
        return self.imgurl

