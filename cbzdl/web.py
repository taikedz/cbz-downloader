#!/usr/bin/python3

""" Web-related utilities and classes.
"""

import urllib.request
import urllib.error
from lxml.html import parse as parseHTML
import filesys
import io
import re
import os
import time
import gzip
import ComicEngine
import feedback

useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

class WebResource:
    """ A WebResource is identified by its URL
    """
    def __init__(self, url):
        self.url = url
        self.domain = getUrlComponents(url, 2)
        self.pagedata = None
        self.response = None

    def saveTo(self, filepath):
        rawdata = self.getData()

        filesys.ensureDirectoryFor(filepath)

        fh = open(filepath, 'wb')
        fh.write(rawdata)
        fh.close()

    def decompress(self):
        if self.getHeader("Content-Encoding") == "gzip":
            self.pagedata = gzip.decompress(self.pagedata)

    def load(self):
        """ Loads the page data if not yet already done.

        On 500-class errors, retries up to 3 times.

        class implementors should not need to call this method.
        """
        if self.pagedata == None:
            global useragent
            retries = 3
            while retries > 0:
                feedback.debug(self.url)
                try:
                    req = urllib.request.Request(
                        self.url,
                        data=None,
                        headers={
                            'User-Agent': useragent
                        }
                    )
                    self.response = urllib.request.urlopen(req)
                    self.pagedata = self.response.read()
                    self.response.close()

                    if self.pagedata != None:
                        self.decompress()
                        feedback.debug("Succesfully downloaded %s"%self.url)
                        return
                    else:
                        raise ComicEngine.ComicError("No data obtained!")
                except ConnectionResetError as e:
                    if retries > 0:
                        print("Peer reset connection - retrying ...")
                        retries -= 1
                        time.sleep(2)
                        continue
                    
                    raise DownloadError("Could not load %s\n%s"%(self.url, str(e)), self.url )

                except urllib.error.HTTPError as e:
                    if httpCodeClass(e.code) == 500 and retries > 0:
                        feedback.warn("# HTTP %i error - retrying ..."%e.code)
                        retries -= 1
                        time.sleep(2)
                        continue
                    if httpCodeClass(e.code) == 400:
                        raise DownloadError("Request error: %i" % e.code, self.url, e.code)
                    
                    raise DownloadError("Could not load %s\n%s"%(self.url, str(e)), self.url, e.code )

    def getHeader(self, header):
        self.load()
        return self.response.getheader(header)

    def getData(self):
        """ Loads remote data, and returns the data as raw bytes
        """
        self.load()
        return self.pagedata

    def getSource(self, encoding="utf-8"):
        """ Loads remote data, and returns the data as decoded text, by default using UTF-8 encoding
        """
        self.load()
        try:
            return self.pagedata.decode(encoding)
        except UnicodeDecodeError as e:
            self.saveTo("dump.txt")
            raise e

    def getDomObject(self):
        return parseHTML(io.StringIO(self.getSource() ) ).getroot()


    def searchInSource(self, pattern, group=0):
        """ Filter source lines on pattern
        """
        text_lines = self.getSourceLines()
        matching_lines = []

        for line in text_lines:
            matched = re.match(pattern, line)
            if matched:
                matching_lines.append(matched.group(group) )

        if len(matching_lines) > 0:
            return matching_lines
        return None

    def getSourceLines(self, matching=None):
        """ Get source data as a series of lines. Lines do not include line terminator sequence.
        """
        sourcedata = self.getSource()
        sourcedata = re.split("(\\r|\\n|\\r\\n)", sourcedata)

        if matching:
            return self.filter(souredata, matching)
        else:
            return sourcedata

    def getUrl(self):
        """ Return the URL the object is configured with
        """
        return self.url

    def getExtension(self):
        self.load()

        extension = mapExtension( self.getHeader("content-type") )

        if extension == None:        
            return "bmp"
        return extension

def mapExtension(content_type):
    extensions = {
        "image/jpeg" : "jpg",
        "image/png" : "png",
        "image/gif" : "gif"
    }
    
    if content_type in extensions.keys():
        return extensions[content_type]

def getUrlComponents(comic_url, group=0):
    """ Extract the copmonents of a URL

    If group == 0 , returns a tuple of (scheme, domain, path)

    Else each group number returns:
    1 - scheme
    2 - domain
    3 - path
    """
    m = re.match("^([a-z0-9]+)://([a-zA-Z0-9.-]+)(.*?)$", comic_url)

    if m:
        if group == 0:
            return m.group(1), m.group(2), m.group(3)
        elif group > 3:
            raise ComicEngine.ComicError("No such group %i"%group)
        return m.group(group)

    raise ValueError("Not a valid url: %s" % comic_url)

def httpCodeClass(num):
    """ Given a HTTP code, return the denomination
    (100, 200, 300, 400, or 500)
    """
    x = num % 100
    return num - x

class DownloadError(Exception):

    def __init__(self, message, url, code=0):
        Exception.__init__(self, message)
        self.code = code
        self.url = url
