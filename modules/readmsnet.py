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
valid_domains = ['readms.net']
recommended_delay = 0

class ComicSite(web.WebResource):

    def __init__(self, url):
        url = self.validateUrl(url)

        web.WebResource.__init__(self, url)
        self.domain = web.getUrlComponents(url, 2)

    def validateUrl(self, url):
        """ If you want to rewrite the URL before accessing it, modify this section
        """
        return url
        #return 

class Comic(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, re.sub("/r/([^/]+).*", "/manga/\\1", url) )
        feedback.debug(self.url)
        self.name = self.getComicLowerName()

    def getComicLowerName(self):
        res = util.regexGroup("https://readms.net/manga/([^/]+)", self.url)
        feedback.debug(": "+res)
        return res

    def getChapterUrls(self):
        dom = self.getDomObject()
        alinks = dom.cssselect("table tr td a")

        chaplinks = []

        for elem_a in alinks:
            href = elem_a.attrib['href']
            if re.match("/r/%s" % self.name, href):
                chaplinks.append("https://readms.net"+href)

        util.naturalSort(chaplinks, ".+/%s/([0-9.]+)/.+")

        return chaplinks

class Chapter(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)
        self.name = self.getChapterLowerName()

    def getChapterLowerName(self):
        cname = util.regexGroup("https://readms.net/r/([^/]+)", self.url)
        return "%s_chapter-%s" % (cname, self.getChapterNumber().zfill(3) )

    def getChapterNumber(self):
        cnum = util.regexGroup("https://readms.net/r/[^/]+/([0-9.]+)", self.url)
        feedback.debug("Return chapter number: %s" % cnum)
        return cnum

    def getPageUrls(self):

        base_chapter_url = util.regexGroup("https://readms.net(/r/.+)/[0-9.]+$", self.url)
        feedback.debug("Base URL : "+base_chapter_url)

        dom = self.getDomObject()

        pageurls = []

        links = dom.cssselect("ul.dropdown-menu li a")

        for elem_a in links:
            href = elem_a.attrib['href']
            if re.match(base_chapter_url, href):
                pageurls.append("https://readms.net" + href)

        return pageurls
                

class Page(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getPageNumber(self):
        return util.regexGroup(".+/([0-9]+)", self.url)

    def getImageUrl(self):
        src = self.getDomObject().get_element_by_id("manga-page").attrib['src']
        if src[:2] == '//':
            return "https:"+src
        else:
            return "https://%s/%s"%(self.domain, src)
