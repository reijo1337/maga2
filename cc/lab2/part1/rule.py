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
        self.right_part = right_part
