import os
import feedback

def ensureDirectoryFor(filepath):
    parent_dir = getParentDir(filepath)
    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

def getParentDir(path):
    abspath = os.path.abspath(path)
    i = abspath.rfind(os.path.sep)
    if i < 1:
        raise ValueError(ValueError)
    feedback.debug("Containing dir: %s"%abspath[:i])
    return abspath[:i]
