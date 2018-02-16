""" An example of a module file

To create a new module:

* Copy this to the cbzdl/modules folder
* Flesh out your copy of the file
* Edit ComicEngine.py and add your module to the list
"""

import web
import re
import base64
import feedback
import ComicEngine

# Edit this to list the valid domains for the site
valid_domains = ['mangakakalot.com']

class ComicSite(web.WebResource):

    def __ini__(self, url):
        self.validateUrl(url)

        web.WebResource.__init__(self, url)

    def validateUrl(self, url):
        """ If you want to rewrite the URL before accessing it, modify this section
        """
        return re.sub("^https:", "http:", url.lower() )

class Comic(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)
        self.lowername = re.match("http://%s/manga/([^/]+)"%(self.domain), self.url).group(1)

    def getTitle(self):
        return self.searchInSource("<h1>(.+)</h1>", group=1)

    def getComicLowerName(self):
        return self.lowername

    def getChapterUrls(self):
        urls = self.searchInSource(".+(http://%s/chapter/%s/[^\"]+)"%(self.domain, self.lowername), group=1)
        urls.reverse()
        return urls

class Chapter(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getChapterNumber(self):
        return re.match(".+/chapter_(.+)$", self.url).group(1)

    def getChapterLowerName(self):
        comicname = re.match(".+/chapter/([^/]+)", self.url).group(1)
        return "%s_ch%s" % (comicname, self.getChapterNumber().zfill(3) )

    def getPageUrls(self):
        document = self.getDomObject()
        image_nodes = document.get_element_by_id("vungdoc").getchildren()

        page_urls = []
        # All pages are in one page - encode them and stuff them in a bogus query string
        i = 1 # counter... hopefully pages always come in-order...!
        for img in image_nodes:
            imgurl = img.attrib['src']
            feedback.debug(imgurl)
            pagenum = i #re.match(".+?([0-9]+)\\.[a-z]+$", imgurl).group(1)
            i += 1

            if re.match(".+/nextchap.png", imgurl):
                continue

            page_urls.append("%s?u=%s&n=%s"%(self.url , base64.urlsafe_b64encode(imgurl.encode("utf-8")).decode("utf-8"), pagenum) )

        return page_urls


class Page(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)
        self.pagenum = re.match(".+n=([0-9]+)", self.url).group(1)
        self.imgurl = base64.urlsafe_b64decode( re.match(".+u=([^&]+)", self.url).group(1) ).decode("utf-8")

    def getPageNumber(self):
        return self.pagenum

    def getImageUrl(self):
        return self.imgurl
