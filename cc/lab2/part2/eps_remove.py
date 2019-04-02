from part1.grammar import Grammar


def eps_rules_finder(grammar):
    """
    Алгоритм поиска ε-порождающих нетерминалов
    :type grammar: Grammar
    """
    eps_non_terminals = set()
    # Найти все ε-правила. Составить множество, состоящее из нетерминалов, входящих в левые части таких правил.
    for rule in grammar.rules:
        if rule.right_part[0] == grammar.eps:
            eps_non_terminals.add(rule.left_part)

    # Перебираем правила грамматики Γ.
    is_changed = True
    while is_changed:
        is_changed = False
        for rule in grammar.rules:
            #  Если найдено правило A→C1C2...Ck, для которого верно, что каждый Ci принадлежит множеству
            if eps_non_terminals.issuperset(rule.right_part):
                # то добавить A в множество.
                eps_non_terminals.add(rule.left_part)
                is_changed = True
    return eps_non_terminals
