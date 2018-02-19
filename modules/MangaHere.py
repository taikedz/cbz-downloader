""" An example of a module file

To create a new module:

* Copy this to the cbzdl/modules folder
* Flesh out your copy of the file
* Edit ComicEngine.py and add your module to the list
"""

import web
import re
import feedback
import ComicEngine
import util

# Edit this to list the valid domains for the site
valid_domains = ['mangahere.co', 'mangahere.cc','www.mangahere.co', 'www.mangahere.cc']

class ComicSite(web.WebResource):

    def __ini__(self, url):
        url = self.validateUrl(url)

        web.WebResource.__init__(self, url)
        self.domain = web.extractDomain(url)

    def validateUrl(self, url):
        """ If you want to rewrite the URL before accessing it, modify this section
        """
        return re.sub("^https?://(%s)/"%("|".join(valid_domains)), "http://www.mangahere.cc/")

class Comic(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getComicLowerName(self):
        return re.match(".+/manga/([^/]+)", self.url).group(1)

    def getChapterUrls(self):
        doc = self.getDomObject()
        chapter_links = doc.cssselect("li span a")
        urls = []

        for a in chapter_links:
            if "href" not in a.attrib.keys():
                continue

            link = a.attrib['href']
            if re.match("//.+?/manga/[^/]+/c[0-9.]+/", link):
                urls.append("http:"+link)

        util.naturalSort(urls)

        return urls

class Chapter(ComicSite):
    
    def __init__(self, url):
        if re.match(".+/[0-9]+\\.html", url) or url[-1] == '/':
            url = url[:url.rfind('/') ]

        ComicSite.__init__(self, url)

    def getChapterNumber(self):
        return int( re.match(".+?/c([0-9.]+)$", self.url).group(1) )

    def getChapterLowerName(self):
        parts = re.match(".+/manga/([^/]+)/(c[0-9.]+)", self.url)
        return "%s_c%s" % (parts.group(1), parts.group(2) )

    def getPageUrls(self):
        doc = self.getDomObject()
        div = doc.get_element_by_id("top_chapter_list").getparent()
        options = div.cssselect("select option")
        urls = []

        for opt in options:
            pagenum = opt.text_content()

            if re.match("^[0-9]+$", pagenum):
                urls.append( "%s/%i.html" % (self.url, int(pagenum) ) )

        util.naturalSort(urls)

        return urls

class Page(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getPageNumber(self):
        return re.match(".+/([0-9]+).html$", self.url).group(1)

    def getImageUrl(self):
        return self.getDomObject().get_element_by_id("image").attrib['src']