from part1.rule import Rule
from tools import list_compare


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
        self.eps = 'eps'

    def __eq__(self, other):
        """
        Перегрузка сравнения
        :type other: Grammar
        """
        if self.start != other.start:
            return False
        if not list_compare(self.non_terminals, other.non_terminals) or \
                not list_compare(self.terminals, other.terminals) or \
                not list_compare(self.rules, other.rules):
            return False
        return True

    def add_non_terminal(self, non_terminal):
        self.non_terminals.append(non_terminal)

    def add_terminal(self, terminal):
        self.terminals.append(terminal)

    def add_rule(self, left_part, right_part):
        if not self.rule_part_correct(left_part) or not self.rule_part_correct(right_part):
            raise ValueError("В правиле присутствет недопустимый (не)терминал\n"
                             "Правило: " + left_part + "->" + right_part)
        self.rules.append(Rule(left_part, right_part))

    def rule_part_correct(self, part):
        for ch in part.split(' '):
            if (ch not in self.non_terminals) and (ch not in self.terminals) and (ch != self.eps):
                return False
        return True

    def add_start(self, start):
        self.start = start

    def load_from_file(self, filename):
        """
        Создание грамматики по файлу
        :param filename: имя файла
        """
        self.non_terminals.clear()
        self.terminals.clear()
        self.rules.clear()
        self.start = ""
        with open(filename) as file:
            non_terminals = file.readline().replace('\n', '').split(' ')
            for non_terminal in non_terminals:
                self.non_terminals.append(non_terminal)
            terminals = file.readline().replace('\n', '').split(' ')
            for terminal in terminals:
                self.terminals.append(terminal)
            rules_count = int(file.readline().replace('\n', ''))
            for _ in range(rules_count):
                rule_parts = file.readline().replace('\n', '').split('->')
                self.add_rule(left_part=rule_parts[0], right_part=rule_parts[1])
            self.start = file.readline().replace('\n', '')

    def save_to_file(self, filename):
        """
        Сохранение грамматики в файл
        :param filename: имя файла
        """
        with open(filename, 'w') as f:
            f.write(" ".join(self.non_terminals))
            f.write('\n')
            f.write(" ".join(self.terminals))
            f.write('\n')
            f.write(str(len(self.rules)))
            f.write('\n')
            for rule in self.rules:
                f.write(f'{rule.left_part}->{" ".join(rule.right_part)}')
                f.write('\n')
            f.write(self.start)
