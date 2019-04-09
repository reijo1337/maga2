from syntax_tree import Tree


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

    def __lt__(self, other):
        return len(self.right_part) < len(other.right_part)

    def __len__(self):
        return len(self.right_part)

    def __eq__(self, other):
        """
        :type other: Rule
        """
        if self.left_part == other.left_part and self.right_part == other.right_part:
            return True
        return False

    def __hash__(self):
        return hash(self.left_part + '->' + ' '.join(self.right_part))

    def __str__(self):
        return f'{self.left_part}->{" ".join(self.right_part)}'

    def non_terminals_count(self, non_terminals):
        """
        Количество нетерминалов в правой части
        """
        count = 0
        for ch in self.right_part:
            if ch in non_terminals:
                count = count+1
        return count

    def has_terminals(self, non_terminals):
        for ch in self.right_part:
            if ch not in non_terminals and ch != 'eps':
                return True
        return False

    def check(self, string, i, non_terminals, grammar, tree, depth=0):
        """

        :type tree: Tree
        """
        original = i.val()
        prefix = ''
        for tab in range(depth):
            prefix = prefix + ' '
        for right in self.right_part:
            child = Tree(cargo=right)
            tree.childs.append(child)
            if i.val() == len(string):
                tree.childs.remove(child)
                return True
            if right in non_terminals:
                if not grammar.check_rules_for_non_terminal(non_terminal=right, string=string, i=i, tree=child, depth=depth):
                    i.set(original)
                    tree.childs.clear()
                    return False
            elif right == string[i.val()]:
                print(prefix + f'Успешно обработали симовл {string[i.val()]} при позиции i={i.val()}')
                i.inc()
            else:
                print(prefix + f'Ошибка при i={i.val()} и соотвественном символе {string[i.val()]}')
                print(prefix + f'Правило {self} \n')
                i.set(original)
                tree.childs.clear()
                return False
        print(prefix + f'Подходит правило {self}\n')
        return True

