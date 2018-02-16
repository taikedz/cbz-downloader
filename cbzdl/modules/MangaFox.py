import web
import re
import feedback
import ComicEngine

valid_domains = ['fanfox.net', 'm.fanfox.net']

class ComicSite(web.WebResource):

    def __ini__(self, url):
        self.validateUrl(url)

        web.WebResource.__init__(self, url)
        self.domain = web.extractDomain()

    def validateUrl(self, url):
        """ If you want to rewrite the URL before accessing it, modify this section
        """
        return re.sub("https?://m.", "http://", url)

def getMangabasePath(url):
    return re.match("(.+?/manga/[^/]+/)",url).group(1)
    
def array_fix(items, pre="", post=""):
    for i in range(len(items) ):
        items[i] = "%s%s%s" % (pre, items[i], post)

class Comic(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getTitle(self):
        titlepat = ".+/manga/([^/]+)"
        m = re.match(titlepat, self.url)
        if m:
            return m.group(1)

        raise ComicEngine.ComicError("Could not extract title from '%s' using '%s'"%(url, titlepat))

    def getComicLowerName(self):
        return re.match(".+/manga/([^/]+)", self.url).group(1)

    def getChapterUrls(self):
        feedback.debug("domain: "+str(web.getDomain(self.url)))
        urls = self.searchInSource(""".+<a href="(//%s/manga/%s/[^"]+)"""%(web.getDomain(self.url),self.getTitle() ), group=1)

        if urls == None:
            raise ComicEngine.ComicError("No URLs returned from %s"%self.url)

        array_fix(urls, pre="http:")
       
        # Because getting from basic main page
        urls.reverse()
        feedback.debug(urls)
        return urls

class Chapter(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getChapterNumber(self):
        # FIXME what about when volumes have same-numbered chpaters ??
        return re.match(".+/c([0-9.]+)/", self.url).group(1)

    def getChapterLowerName(self):
        chapter_lower = "%s%s%s" % ( Comic(self.url).getLowerName() , "_chapter-" , self.getChapterNumber() )
        return chapter_lower

    def getBaseChapterUrl(self):
        i = self.url.rfind('/')
        return self.url[:i]

    def getPageUrls(self):
        # FIXME shoddy
        pagecount = self.searchInSource("^\\s*of\\s+([0-9]+)", group=1)
        if pagecount == None:
            self.saveTo("dump.bin")
            raise ComicEngine.ComicError("Could not obtain page count!")
        pagecount = int(pagecount[0])

        pagenums = list(range(pagecount+1))[1:]
        base_chapter_url = self.getBaseChapterUrl()

        array_fix(pagenums, pre=base_chapter_url+"/",post=".html")

        feedback.debug("Page urls: "+str(pagenums) )
        return pagenums

class Page(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getPageNumber(self):
        return re.match(".+/([0-9]+)\\.html$", self.url).group(1)

    def getImageUrl(self):
        images = self.searchInSource(""".+<img\\s[^>]+id="image"\\s[^>]+""")
        if len(images) != 1:
            raise ComicEngine.ComicError("Could not isolate key image: %s"%str(images))
        m = re.match( """.+\\bsrc="([^"]+)""", images[0])
        if not m:
            raise ComicEngine.ComicError("Could not extract image URL")

        feedback.debug(m.group(1) )
        return m.group(1)
