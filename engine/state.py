import os
import pickle
import filesys
import feedback
import ComicEngine

state_file_name = "state.data"

class DownloaderState:

    def __init__(self, stated_source):
        state_file_name = "state.data"
        feedback.debug("Source: %s" % stated_source)

        self.__state_data = None

        if os.path.isdir(stated_source):
            self.__state_file = os.path.sep.join([stated_source, state_file_name])
            self.load()
            self.cengine = ComicEngine.determineFrom( self.get("url") )

        else:
            self.cengine = ComicEngine.determineFrom(stated_source)
            feedback.debug("Comic engine: %s" % self.cengine.__name__)

            comic_dir = self.cengine.Comic(stated_source).getComicLowerName()
            feedback.debug('Comic dir: %s' % comic_dir)

            self.__state_file = os.path.sep.join([comic_dir, state_file_name])
            self.set("url", stated_source)

    def __ensureStateStore(self):
        filesys.ensureDirectoryFor(self.__state_file)

    def initialize(self):
        """ Initialize state.

        If data existed, it is discarded.

        Does not commit to file.
        """
        self.__state_data = {}

    def load(self):
        """ (Re-)loads the data from file
        """
        if os.path.isfile(self.__state_file):
            with open(self.__state_file, 'rb') as fh:
                self.__state_data = pickle.load(fh)
        else:
            self.initialize()

    def commit(self):
        if self.__state_data:
            self.__ensureStateStore()
            with open(self.__state_file, 'wb') as fh:
                pickle.dump(self.__state_data, fh)
        else:
            raise ComicStateError("No data to save")

    def has(self, key):
        try:
            self.get(key)
            return True
        except ComicStateError:
            return False

    def get(self, key):
        if not self.__state_data:
            self.load()

        if not key in self.__state_data.keys():
            raise ComicStateError("No such key [%s] (store is [%s])" % (key, self.__state_file) )

        return self.__state_data[key]

    def set(self, key, value):
        if not self.__state_data:
            self.load()

        self.__state_data[key] = value
        self.commit()

class ComicStateError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
