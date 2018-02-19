import re
import feedback

def regexGroup(pattern, target, group=1):
    m = re.match(pattern, target)

    if m:
        return m.group(group)

def naturalSort(array, keypattern='.*?([0-9]+)', group=1):
    """ Use a natural sorting on first number,
    
    Or by the string identified by the pattern match group
    """
    def naturalSortKey(string):
        m = re.match(keypattern, string)
        if m:
            if re.match("^[0-9]+$", m.group(group) ):
                return int(m.group(group)) # number
            return m.group(group) # targeted group
        return string # string in general


    array.sort(key=naturalSortKey)
