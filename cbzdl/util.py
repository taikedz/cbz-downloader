import re

def natural_sort(array, keypattern='.*?([0-9]+)', group=1):
    """ Use a natural sorting on first number,
    
    Or by the string identified by the pattern match group
    """
    def natural_sort_key(string):
        m = re.match(keypattern, string)
        if m:
            if re.match("^[0-9]+$", m.group(group) ):
                return int(m.group(group)) # number
            return m.group(group) # targeted group
        return string # string in general


    array.sort(key=natural_sort_key)
