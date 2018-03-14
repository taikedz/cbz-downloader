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
valid_domains = ['www.mangapanda.com']
recommended_delay = 1

class ComicSite(web.WebResource):

    def __init__(self, url):
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
        return util.regexGroup("https://%s/([^/]+)" % self.domain, self.url)

    def getChapterUrls(self):
        dom = self.getDomObject()
        chapters = dom.get_element_by_id("chapterlist").cssselect("td a")

        urls = []

        for elem_a in chapters:
            path = elem_a.attrib['href']
            if re.match("/%s/[0-9.]+" % self.name, path):
                urls.append("https://%s%s"%(self.domain, path) )

        util.naturalSort(urls, ".+/([0-9.]+)$")

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
        return util.regexGroup(".+/([0-9.]+)", self.url)

    def getPageUrls(self):
        doc = self.getDomObject()
        options = doc.cssselect("#selectpage select option")

        urls = []

        for option in options:
            urls.append("https://%s%s"%( self.domain, option.attrib['value'] ))

        return urls

class Page(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getPageNumber(self):
        return util.regexGroup(".+/([0-9]+)$", self.url)

    def getImageUrl(self):
        doc = self.getDomObject()
        img = doc.get_element_by_id("img")
        return img.attrib['src']
