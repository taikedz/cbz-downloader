import re
import feedback

def regexGroup(pattern, target, group=1):
    """ Given a pattern and a string, return capturing group 1 by default
    """
    m = re.match(pattern, target)

    if m:
        return m.group(group)

def naturalSort(array, keypattern='.*?([0-9]+)', group=1):
    """ Use a natural sorting on first number in the string,
    
    Or, specify a pattern, and matching using the contents of the capturing group as the key
    """
    def naturalSortKey(string):
        m = re.match(keypattern, string)
        if m:
            gv = m.group(group)
            if re.match("^[0-9]+(\\.[0-9]+)?$", gv ):
                # number, expect possibility of floats from custom strings
                return float(gv)
            # Simply the plain targeted group
            return gv

        # Return the original string, for something to compare on
        return string


    array.sort(key=naturalSortKey)
