import re


pattern = re.compile(r'(?<!^)(?=[A-Z])')
def to_snake_case(name):
    return pattern.sub('_', name).lower()


def remove_dupes(l):
    """
    Remove duplicates from list inplace.
    """
    i = 0
    while i < len(l):
        if l[i] in l[:i]:
            del l[i]
        else:
            i += 1
