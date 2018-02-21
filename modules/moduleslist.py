import filesys
import feedback

modules_dir = filesys.getParentDir(__file__)

feedback.debug("Modules from %s" % modules_dir)

module_files = filesys.listDir(modules_dir, "[a-zA-Z0-9]+.py$")

feedback.debug("Got files %s"%module_files)

engine_files = []

for i in range(len(module_files)):
    file_name = module_files[i]
    if file_name == "example_module.py" or file_name == "moduleslist.py":
        continue

    engine_files.append( "modules.%s" % file_name[:-3] )

# To be done:
# https://www.manga.club
