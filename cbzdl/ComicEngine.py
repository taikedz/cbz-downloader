import importlib
import web

import modules.moduleslist

""" Module to determine which module to use, given a URL
"""

def getAvailableEngineFiles():
    "Get the list of module files"
    return modules.moduleslist.engine_files

class ComicError(Exception):
    "Standard cbzdl error"

    def __init__(self, message):
        Exception.__init__(self, message)

def determineFrom(comic_url):
    """ Return a download module determined by the URL
    """

    scheme, domain, path = web.getUrlComponents(comic_url)

    if domain == None:
        ComicError("Invalid URL")

    for engine_file in getAvailableEngineFiles():
        cengine = importlib.import_module(engine_file)
        if domain in cengine.valid_domains:
            return cengine

    raise ComicError("Unknown handler for %s"%domain)
