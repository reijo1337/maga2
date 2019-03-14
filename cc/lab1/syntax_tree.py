import os
from graphviz import Digraph


CHAR_EMPTY = chr(1)
CHAR_ENDMARK = '#'
available_chars = 'abcdefghijklmnopqrstuvwxyz'
operands = '()*|.+'
position = 1


class Tree:
    """
    Узел дерева
    """

    def __init__(self, cargo, left=None, right=None, pos=None):
        self.cargo = cargo
        self.left = left
        self.right = right
        self.pos = pos

    def __str__(self):
        return str(self.cargo)


def print_tree_postorder(tree):
    """
    Вывод дерева
    :param tree: Дерево
    """
    if tree is None:
        return
    print_tree_postorder(tree.left)
    print_tree_postorder(tree.right)
    print(f'{firstpos(tree)} ({tree}) {lastpos(tree)}')


def convert_regex_to_list(regex):
    """
    Преобразует строку с регулярным выражением в список лексем для построения синтаксического дерева
    :param regex: регулярное выражение
    :return: список лексем
    """
    global position
    if not isinstance(regex, str):
        raise ValueError(f'Регулярное выражение должно быть строкой, а оно типа {type(regex)}')
    ret = list()
    prev = ''
    need_dot = available_chars + '*+'
    for ch in regex:
        if ch not in available_chars + operands:
            raise ValueError(
                f'Регулярное выражение должно содержать только буквы и символы \'(,),*,|\'. Есть символ {ch}')
        if ch in available_chars:
            position = position + 1
        if prev in need_dot and ch in available_chars + '(':
            ret.append('.')
        ret.append(ch)
        prev = ch
    ret.append('.')
    ret.append(CHAR_ENDMARK)
    position = position + 1
    ret = ret[1:] if ret[0] == '.' else ret
    ret.reverse()
    return ret


def get_token(token_list, expected):
    """
    Функция сравнивает ожидаемую лексему с первой в списке.
    :param token_list: список лексем
    :param expected: ожидаемая лексема
    :return: Если первая лексема списка и ожидаемая лексема равны, то первая лексема удаляется из списка, и функция
    возвращает True. В противном случае возвращается False
    """
    if len(token_list) == 0:
        return False
    elif token_list[0] == expected:
        del token_list[0]
        return True
    else:
        return False


def get_char(token_list):
    global position
    """
    Формирует вершину дерева из первого элемента списка, если тот не является операндом
    :param token_list: список лексем
    :return: вершина дерева Tree, если первый элемент не операнд, или None
    """
    if get_token(token_list, ')'):
        x = get_sum(token_list)  # get the subexpression
        get_token(token_list, '(')  # remove the closing parenthesis
        return x
    else:
        x = token_list[0]
        if x not in available_chars + CHAR_ENDMARK:
            return None
        token_list[0:1] = []
        position = position - 1
        return Tree(x, None, None, position)


def get_product(token_list):
    # a = get_iter(token_list)
    # if get_token(token_list, '.'):
    #     b = get_sum(token_list)
    #     return Tree('.', b, a)
    # else:
    #     return a
    a = get_iter(token_list)
    if get_token(token_list, '|'):
        b = get_char(token_list)
        return Tree('|', b, a)
    else:
        return a


def get_sum(token_list):
    # a = get_product(token_list)
    # if get_token(token_list, '|'):
    #     b = get_sum(token_list)
    #     return Tree('|', b, a)
    # else:
    #     return a
    a = get_product(token_list)
    if get_token(token_list, '.'):
        b = get_sum(token_list)
        return Tree('.', b, a)
    else:
        return a


def get_iter(token_list):
    a = get_char(token_list)
    if get_token(token_list, '*'):
        b = get_char(token_list)
        return Tree('*', b, a)
    elif get_token(token_list, '+'):
        b = get_char(token_list)
        return Tree('.', b, Tree('*', b, a))
    else:
        return a


def nullable(node):
    """
    :type node: Tree
    """
    if node.cargo == CHAR_EMPTY:
        return True
    elif node.cargo in available_chars + CHAR_ENDMARK:
        return False
    elif node.cargo == '|':
        return nullable(node.left) or nullable(node.right)
    elif node.cargo == '.':
        return nullable(node.left) and nullable(node.right)
    elif node.cargo == '*':
        return True
    elif node.cargo == '+':
        return False


def firstpos(node):
    """
    :type node: Tree
    """
    if node.cargo == CHAR_EMPTY:
        return set()
    elif node.cargo in available_chars + CHAR_ENDMARK:
        return {node.pos}
    elif node.cargo == '|':
        return firstpos(node.left) | firstpos(node.right)
    elif node.cargo == '.':
        if nullable(node.left):
            return firstpos(node.left) | firstpos(node.right)
        return firstpos(node.left)
    elif node.cargo in '*+':
        return firstpos(node.left)


def lastpos(node):
    """
    :type node: Tree
    """
    if node.cargo == CHAR_EMPTY:
        return set()
    elif node.cargo in available_chars + CHAR_ENDMARK:
        return {node.pos}
    elif node.cargo == '|':
        return lastpos(node.left) | lastpos(node.right)
    elif node.cargo == '.':
        if nullable(node.right):
            return lastpos(node.left) | lastpos(node.right)
        return lastpos(node.right)
    elif node.cargo in '*+':
        return lastpos(node.left)


def followpos(root_tree, result):
    """
    :type root_tree: Tree
    :type result: dict
    """
    if root_tree is None:
        return
    followpos(root_tree.left, result)
    followpos(root_tree.right, result)

    if root_tree.cargo == '.':
        i_set = lastpos(root_tree.left)
        fpos = firstpos(root_tree.right)
        for i in i_set:
            followpos_set = result.get(i)
            if followpos_set is None:
                result.setdefault(i, set())
            result[i] = result[i].union(fpos)

    elif root_tree.cargo == '*':
        i_set = lastpos(root_tree.left)
        fpos = firstpos(root_tree.left)
        for i in i_set:
            followpos_set = result.get(i)
            if followpos_set is None:
                result.setdefault(i, set())
            result[i] = result[i].union(fpos)


def get_followpos(root_tree):
    """
    Подсчет функции followpos для всех позиций
    :type root_tree: Tree
    """
    followpos_result = dict()
    followpos(root_tree, followpos_result)
    keys = followpos_result.keys()
    max_key = max(keys)
    followpos_result.setdefault(max_key+1, set())
    return followpos_result


def build_tree(reg):
    reg_list = convert_regex_to_list(reg)
    return get_sum(reg_list)


def get_char_positions(root, char):
    """
    :param positions: list
    :param char: str
    :type root: Tree
    """
    ret = list()
    if root is None:
        return ret
    if root.cargo == char:
        ret.append(root.pos)
    ret.extend(get_char_positions(root.left, char))
    ret.extend(get_char_positions(root.right, char))
    return ret


def visualize_tree_node(root, fa_graph, level = 0, head_name = None):
    """
    :type root: Tree
    """
    root_str = f'{root}_{level}' if head_name is None else f'({head_name})_{root}_{level}'
    fa_graph.node(name=root_str, label=str(root))
    if root.left is not None:
        left_str = f'{root.left}_{level+1}'
        fa_graph.edge(root_str, left_str)
        visualize_tree_node(root.left, fa_graph, level+1)
    if root.right is not None:
        right_str = f'{root.right}_{level+1}'
        fa_graph.edge(root_str, right_str)
        visualize_tree_node(root.right, fa_graph, level+1)


def visualize_tree(root, filename):
    fa_graph = Digraph('finite_state_machine')
    visualize_tree_node(root, fa_graph)
    fa_graph.view('regexp_tree')
