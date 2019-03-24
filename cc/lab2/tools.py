def list_compare(a, b):
    if len(a) != len(b):
        return False
    inter = set(a).intersection(b)
    if len(inter) != len(a):
        return False
    return True
