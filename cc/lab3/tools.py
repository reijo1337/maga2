def list_compare(a, b):
    if len(a) != len(b):
        return False
    inter = set(a).intersection(b)
    if len(inter) != len(a):
        return False
    return True


class Integer(object):
    def __init__(self, i):
        self.i = i

    def inc(self):
        self.i = self.i + 1

    def val(self):
        return self.i
