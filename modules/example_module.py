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
valid_domains = ['example.com', 'm.example.com']

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

    def getComicLowerName(self):
        pass

    def getChapterUrls(self):
        pass

class Chapter(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getChapterLowerName(self):
        pass

    def getChapterNumber(self):
        pass

    def getPageUrls(self):
        pass

class Page(ComicSite):
    
    def __init__(self, url):
        ComicSite.__init__(self, url)

    def getPageNumber(self):
        pass

    def getImageUrl(self):
        pass
