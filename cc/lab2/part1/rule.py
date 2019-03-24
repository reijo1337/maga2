class Rule(object):
    """
    Правило вывода для грамматики
    """
    def __init__(self, left_part, right_part):
        """
        Конструктор
        :type right_part: str
        :type left_part: str
        """
        self.left_part = left_part
        self.right_part = right_part.split(' ')

    def __eq__(self, other):
        """
        :type other: Rule
        """
        if self.left_part == other.left_part and self.right_part == other.right_part:
            return True
        return False

    def __hash__(self):
        return hash(self.left_part + '->' + ' '.join(self.right_part))
