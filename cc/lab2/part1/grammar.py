from part1.rule import Rule


class Grammar(object):
    """
    Класс для представления грамматик
    """
    def __init__(self):
        """
        Конструктор
        """
        self.non_terminals = []
        self.terminals = []
        self.rules = []
        self.start = ""

    def add_non_terminal(self, non_terminal):
        self.non_terminals.append(non_terminal)

    def add_terminal(self, terminal):
        self.terminals.append(terminal)

    def add_rule(self, left_part, right_part):
        if not self.rule_part_correct(left_part) or not self.rule_part_correct(right_part):
            raise ValueError("В правиле присутствет недопустимый (не)терминал")
        self.rules.append(Rule(left_part, right_part))

    def rule_part_correct(self, part):
        for ch in part:
            if (ch not in self.non_terminals) and (ch not in self.terminals):
                return False
        return True

    def add_start(self, start):
        self.start = start

    def load_from_file(self, filename):
        """
        Создание грамматики по файлу
        :param filename: имя файла
        """
        with open(filename) as file:
            non_terminals = file.readline().split(' ')
            for non_terminal in non_terminals:
                self.non_terminals.append(non_terminal)
            terminals = file.readline().split(' ')
            for terminal in terminals:
                self.terminals.append(terminal)
            rules_count = int(file.readline())
            for _ in range(rules_count):
                rule_parts = file.readline().split('->')
                self.add_rule(left_part=rule_parts[0], right_part=rule_parts[1])
            self.start = file.readline()

    def save_to_file(self, filename):
        """
        Сохранение грамматики в файл
        :param filename: имя файла
        """
        with open(filename) as f:
            f.write(" ".join(self.non_terminals))
            f.write(" ".join(self.terminals))
            f.write(str(len(self.rules)))
            for rule in self.rules:
                f.write(f'{rule.left_part}->{rule.right_part}')
            f.write(self.start)
