#!/usr/bin/python3

class Comic:
    """ A Comic is defined by URL, from which its chapter URLs can be derived
    """
    def __init__(self, url, ComicHandler, ChapterHandler, PageHandler):
        #self.data = web.WebResource(url).getData(mode=web.STRING)
        self.url = url
        self.comicHandler = ComicHandler
        self.chapterHandler = ChapterHandler
        self.pageHandler = PageHandlers

    def download(self, start=None, end=None):
        comicHandler()

class Chapter:
    """ A chapter is defined by URL, from which its page URLs can be derived
    """
    def __init__(self, url):
        self.data = web.WebResource(url).getData(mode=web.STRING)

    def getPageUrls(self, PageHandler):
        pass
        

class Page:
    """ A page is defined by URL, from which its image URL can be derived
    """
    def __init__(self, url, PageHandler):
        self.url = url

    def getImageUrl(self):
        pass
