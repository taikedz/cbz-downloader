import shutil
import os
import feedback

class CBZArchive:
    """ CBZ Archive maker

    A Comic Book ZIP file is simply a Zip/deflate file containing the pages; readers
    will display them typically in file name string order.
    """

    def __init__(self, folder):
        """Create a new CBZArchive object against the folder containing pages"""
        self.folder = os.path.abspath(folder)

    def compile(self, remove_dir=False):
        """ Compile a CBZ file from the target folder

        remove_dir : whether to remove the source directory once the CBZ is created
        """
        # Target folder does not exist, or no files in target folder (someone's "clever" syntax)
        if (
          not os.path.isdir(self.folder) or
          len([name for name in os.listdir(self.folder) if os.path.isfile(self.folder+os.path.sep+name)]) == 0
          ):
            return

        feedback.info("  Compiling CBZ for %s"%self.folder)
        shutil.make_archive(self.folder, "zip", self.folder)
        shutil.move(self.folder+".zip", self.folder+".cbz")

        if remove_dir:
            shutil.rmtree(self.folder)
