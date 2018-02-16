import shutil
import os
import feedback

class CBZArchive:

    def __init__(self, folder):
        self.folder = os.path.abspath(folder)

    def compile(self, remove_dir=False):
        if not os.path.isdir(self.folder) or len([name for name in os.listdir(self.folder) if os.path.isfile(self.folder+os.path.sep+name)]) == 0:
            return

        feedback.info("  Compiling CBZ for %s"%self.folder)
        shutil.make_archive(self.folder, "zip", self.folder)
        shutil.move(self.folder+".zip", self.folder+".cbz")

        if remove_dir:
            shutil.rmtree(self.folder)
