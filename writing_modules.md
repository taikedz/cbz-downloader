# Essential API for module writing

The core CBZ Downloader in `cbzdl/` takes care of managing chapter downloads and CBZ assembling ; support for individual sites must be added by modules.

To add a new module, copy the `modules/example_module.py` file into a new file in the `modules/` folder, and adjust it for the site you want.

The `WebResource` class in `cbzdl/web.py` provides some utilities for fetching pages and data, so all you need to do is take care of extracting the relevant portions of the site you are scraping. See the existing modules for examples.

You can deploy new modules from the local `modules/` folder by running

	./install.sh modules

The following are some API notes pertinent specifically to the writing of new modules.

Implementors are encouraged to read the source of existing modules. The simplest to date is the one for `MangaReader.net`. `MangaFox.py` and `Mangakakalot.py` have more complex page listing functions, owing to their pages' respective structures.

## Module structure

This is the basic essential methods that module implementors must provide. All classes here are direct or indirect subclasses of `web.WebResource` (see below)


```python
class ComicSite(web.WebResource):
    def validateUrl(self, url):
```


ComicSite serves as a common base for the module's resource classes. Particularly, it exposes a `validateUrl()` method that can be used to ensure a URL passed to any of its children is acceptable, and has the option to return a re-written version. Handy when converting `m.example.com` links to `example.com` ones.

```python
class Comic(ComicSite):
    def getComicLowerName(self):
    def getChapterUrls(self):
```

The `Comic` class represents the main page of a comic, from which it can derive a full chapter listing. The comic's lower-case name is used for creating the local download main directory, and should only be composed of letters, numbers, and the characters in: `. _ -`

```python
class Chapter(ComicSite):
    def getChapterLowerName(self):
    def getChapterNumber(self):
    def getPageUrls(self):
```

The `Chapter` class repesents a chapter webpage from which all reading page URLs can be derived. The lowercase name and the number for creating its specifc download folder and naming the CBZ file. The chapter number should be a string for further manipulation.

```python
class Page(ComicSite):
    def getPageNumber(self):
    def getImageUrl(self):
```

The `Page` class represents a reading page, in which the image URL can be found. The page number MUST be retruend as a string so that it can be zero-filled by the download routine.


## Utility APIs

### `web.WebResource`

All objects in the comic module are subclasses of the WebResource class.

The following are useful methods they expose

`saveTo(filepath):` - save the resource's contents to the specified file.

`decompress():` - if the downloaded content was transferred compressed, decompress it and replace the compressed data in the object

`getHeader(header):` - get the header content, e.g. `myobj.getHeader("Content-Type")`

`getData():` - get the raw data bytes

`getSource(encoding="utf-8"):` get the data decoded as UTF-8 data by default

`getDomObject():` - get a DOM-like  document object for the source -- see online help for `lxml.html.HtmlEntity`

`searchInSource(pattern, group=0):` - a rudimentary line-oriented search. Matches `pattern` against each line of the source; returns an array of all the matching lines, or of the specified capture group

`getSourceLines(matching=None):` - get the basic source lines

`getUrl():` - get the URL configured on the WebResource

`getExtension():` - get a file extension appropriate for the type (only tries to figure out image file extensions)

### `util`

Basic utility functions

`util.regexGroup(pattern, string, group=1)` - supply a regular expression with a capturing group, and a string to match against, and get the capturing group 1 by default

`util.naturalSort(list, pattern='.*?([0-9]+)', group=1)` - naturally sort, where a number is involved, sort numerically

### `web`

Basic web-related utility functions

`web.getUrlComponents(comic_url, group=0):` - get (scheme, domain, path) components from the URL, or individual component (specify group 1, 2 or 3)

`web.httpCodeClass(num):` - get the HTTP code class (e.g. `code 503 ---> class 500`)

### `feedback`

The `feedback` library allows you to write some additional feedback to the output (by default, stderr), distinguished by colour.

It is possible to turn on debug messages with the `-v` flag during `cbzdl` runtime.

`breakpoint(message):` - if debug mode is on, interrupt the execution and print a message

`fail(message, code=1):` - print a red message, and exit with code

`error(message):` - print a red message

`warn(message):` - print a yellow message

`info(message):` - print a green message

`debug(message):` - if debug mode is on, print a blue message

