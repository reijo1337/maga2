from part1.grammar import Grammar


def eps_rules_finder(grammar):
    """
    Алгоритм поиска ε-порождающих нетерминалов
    :type grammar: Grammar
    """
    # Если правило содержит справа терминалы, оно заведомо не будет влиять на ответ, поэтому мы не будем его учитывать.
    rules_without_terminals = [rule for rule in grammar.rules if rule.has_terminals(grammar.terminals)]
    # Для каждого нетерминала будем хранить пометку, является он ε-порождающим или нет.
    # Сначала проставим false в isEpsilon для всех нетерминалов
    isEpsilon = {non_term: False for non_term in grammar.non_terminals}
    # для каждого нетерминала будем хранить список номеров тех правил, в правой части которых он встречается
    concernedRules = {non_term: [] for non_term in grammar.non_terminals}
    # для каждого правила будем хранить счетчик количества
    # нетерминалов в правой части, которые еще не помечены ε-порождающими
    counter = {rule: rule.non_terminals_count(grammar.non_terminals) for rule in rules_without_terminals}

    # Сформируем concernedRules
    for rule in rules_without_terminals:
        for non_term in rule.right_part:
            if non_term != grammar.eps:
                concernedRules[non_term].append(rule)

    # очередь нетерминалов, помеченных ε-порождающими, но еще не обработанных
    Q = list()

    # Те правила, для которых counter сразу же оказался нулевым, добавим в Q
    # и объявим истинным соответствующий isEpsilon, так как это ε-правила
    for rule, count in counter.items():
        if count == 0:
            Q.append(rule.left_part)
            isEpsilon[rule.left_part] = True

    while len(Q) > 0:
        non_term = Q.pop(0)
        for rule in concernedRules[non_term]:
            count = counter[rule]
            counter[rule] = count - 1
            if counter[rule] == 0 and not isEpsilon[rule.left_part]:
                isEpsilon[rule.left_part] = True
                Q.append(rule.left_part)

    return {non_term for non_term, isEps in isEpsilon.items() if isEps}