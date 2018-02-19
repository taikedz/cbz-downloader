import web
import util
import re
import feedback
import ComicEngine

valid_domains = ['fanfox.net', 'm.fanfox.net']

class ComicSite(web.WebResource):

    def __init__(self, url):
        url = self.validateUrl(url)

        web.WebResource.__init__(self, url)
        self.domain = web.extractDomain(url)

    def validateUrl(self, url):
        """ If you want to rewrite the URL before accessing it, modify this section
        """
        return re.sub("https?://m.", "http://", url)

class Comic(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)
        self.name = self.getComicLowerName()
        self.domain = web.extractDomain(self.url)

    def getComicLowerName(self):
        return re.match(".+/manga/([^/]+)", self.url).group(1)

    def getChapterUrls(self):
        feedback.debug("domain: "+str(self.domain))

        doc = self.getDomObject()
        #obj_a = doc.get_elements_by_tag_name("a")
        obj_a = doc.cssselect("a")
        
        urls = []
        for item in obj_a:
            if not "href" in item.attrib.keys():
                continue
            m = re.match("""(//%s/manga/%s/[^"]+)"""%(self.domain,self.name ), item.attrib["href"])
            if not m:
                continue
            target_url = "http:"+m.group(1)
            if not target_url in urls:
                urls.append(target_url)

        if len(urls) < 1:
            raise ComicEngine.ComicError("No URLs returned from %s"%self.url)

        util.natural_sort(urls) # I've seen one series which was a load of "chapter 1" in different volumes... how to deal with that ?
        feedback.debug(urls)
        return urls

class Chapter(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getChapterNumber(self):
        # FIXME what about when volumes have same-numbered chapters ??
        return re.match(".+/c([0-9.]+)/", self.url).group(1)

    def getChapterLowerName(self):
        chapter_lower = "%s%s%s" % ( Comic(self.url).name , "_chapter-" , self.getChapterNumber() )
        return chapter_lower

    def getBaseChapterUrl(self):
        """ Chapters are defined by their first page, so the base has to be the parent
        """
        i = self.url.rfind('/')
        return self.url[:i]

    def getPageUrls(self):

        doc = self.getDomObject()
        top_bar = doc.get_element_by_id("top_bar")
        #options = top_bar.get_elements_by_tag_name("option")
        options = top_bar.cssselect("option")
        urls = []
        base_url = self.getBaseChapterUrl()

        for option in options:
            m = re.match("^[0-9]+$", option.attrib["value"])
            if not m:
                continue
            v = int(m.group(0))
            if v < 1:
                continue

            urls.append( "%s/%i.html" % (base_url, v) )

        util.natural_sort(urls, ".+/c([0-9.]+)/")
        return urls

class Page(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getPageNumber(self):
        return re.match(".+/([0-9]+)\\.html$", self.url).group(1)

    def getImageUrl(self):
        doc = self.getDomObject()
        img = doc.get_element_by_id("image")
        return img.attrib['src']
