import os
import feedback

def ensureDirectoryFor(filepath):
    """ Ensures a parent directory and its path exist
    """
    parent_dir = getParentDir(filepath)
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

def getParentDir(path):
    """ Get the parent directory of a path

    Returns an absolute path
    """
    abspath = os.path.abspath(path)
    i = abspath.rfind(os.path.sep)

    if i == 0:
        return "/"
    elif i < 0:
        raise ValueError("Nothing above root")

    feedback.debug("Containing dir: %s"%abspath[:i])
    return abspath[:i]
