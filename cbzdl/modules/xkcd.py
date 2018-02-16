import web
import re
import feedback
import ComicEngine

# Edit this to list the valid domains for the site
valid_domains = ['xkcd.com']

block_size = 512

class ComicSite(web.WebResource):

    def __ini__(self, url):
        self.validateUrl(url)

        web.WebResource.__init__(self, url)
        self.domain = web.extractDomain()

    def validateUrl(self, url):
        """ If you want to rewrite the URL before accessing it, modify this section
        """
        return url

class Comic(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getTitle(self):
        return "xkcd"

    def getComicLowerName(self):
        return "xkcd"

    def getChapterUrls(self):
        # 1. Get latest
        # 2. iterate in blocks of (block_size) until max is reached
        # 3. Return list of URLs at starts of blocks
        pass

class Chapter(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getChapterNumber(self):
        global block_size
        n = int( re.match(".+/([0-9]+)$", self.url).group(1) )
        return (n - (n % block_size))/block_size # Yes, first chapter will be chapter 0 :-)

    def getPageUrls(self):
        # If possible, detect dynamic/interactive comics, and avoid including them
        pass

class Page(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getPageNumber(self):
        pass

    def getImageUrl(self):
        # include download failure catching at this level ; if interactive/dynamic comic is detected
        # return a placeholder image URL instead
        pass
