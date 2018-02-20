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

# Edit this to list the valid domains for the site
valid_domains = ['www.mangareader.net']

class ComicSite(web.WebResource):

    def __ini__(self, url):
        url = self.validateUrl(url)

        web.WebResource.__init__(self, url)
        self.domain = web.getUrlComponents(url, 2)

    def validateUrl(self, url):
        """ If you want to rewrite the URL before accessing it, modify this section
        """
        return url

class Comic(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)
        self.name = self.getComicLowerName()

    def getComicLowerName(self):
        return util.regexGroup("http://%s/([^/]+)"%self.domain, self.url)

    def getChapterUrls(self):
        doc = self.getDomObject()
        chapters = doc.get_element_by_id("chapterlist").cssselect("tr td a")
        urls = []

        for chap in chapters:
            link = chap.attrib["href"]
            chapter_num = util.regexGroup("/%s/([0-9.]+)$"%self.name, link)
            if chapter_num:
                urls.append("%s/%s"%(self.url, chapter_num) )

        util.naturalSort(urls)

        return urls


class Chapter(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getChapterLowerName(self):
        return util.regexGroup("http://%s/([^/]+)"%self.domain, self.url) + "_c" + self.getChapterNumber()

    def getChapterNumber(self):
        return util.regexGroup(".+/([0-9.]+)$", self.url).zfill(4)

    def getPageUrls(self):
        doc = self.getDomObject()
        options = doc.cssselect("#selectpage select option")
        urls = []

        for opt in options:
            path = opt.attrib["value"]
            urls.append("http://%s%s" % (self.domain, path))

        util.naturalSort(urls, ".+/([0-9]+)$")

        return urls

class Page(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getPageNumber(self):
        return util.regexGroup(".+/([0-9]+)$", self.url)

    def getImageUrl(self):
        return self.getDomObject().get_element_by_id("img").attrib['src']
