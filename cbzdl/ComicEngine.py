import re
import importlib

# ==================================================
# Add your engine modules to this list !
engine_files = [
    "modules.MangaFox",
#    "modules.MangaHere",
#    "modules.MangaReader",
    "modules.Mangakakalot"
    ]

def getAvailableEngineFiles():
    # TODO Automate discovery?

    return engine_files

class ComicError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

def getUrlComponents(comic_url):
    matched = re.match("^([a-z0-9]+)://([a-zA-Z0-9.-]+)(.+)$", comic_url)

    if matched:
        return matched.group(2)

def determineFrom(comic_url):
    domain = getUrlComponents(comic_url)

    if domain == None:
        ComicError("Invalid URL")

    for engine_file in getAvailableEngineFiles():
        cengine = importlib.import_module(engine_file)
        if domain in cengine.valid_domains:
            return cengine

    raise ComicError("Unknown handler for %s"%domain)
