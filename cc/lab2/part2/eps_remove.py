import itertools

from part1.grammar import Grammar
from part1.rule import Rule


def eps_rules_finder(grammar):
    """
    Алгоритм поиска ε-порождающих нетерминалов
    :type grammar: Grammar
    """
    # Если правило содержит справа терминалы, оно заведомо не будет влиять на ответ, поэтому мы не будем его учитывать.
    rules_without_terminals = [rule for rule in grammar.rules if not rule.has_terminals(grammar.non_terminals)]
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


def eps_remove(grammar):
    """
    Алгоритм удаления ε-правил из грамматики
    :type grammar: Grammar
    """
    ret = Grammar()

    # Добавить все правила из P в P′
    ret.terminals = grammar.terminals.copy()
    ret.non_terminals = grammar.non_terminals.copy()
    ret.rules = grammar.rules.copy()
    ret.start = grammar.start

    # Найти все ε-порождаюшие нетерминалы.
    eps_non_terms = eps_rules_finder(grammar)
    # Для каждого правила вида A→α0B1α1B2α2...Bkαk
    for rule in grammar.rules:
        rule_eps = eps_non_terms.intersection(rule.right_part)
        # добавить в P′ все возможные варианты правил,
        # в которых либо присутствует, либо удалён каждый из нетерминалов Bj(1⩽j⩽k)
        for i in range(len(rule_eps)):
            for combo in itertools.combinations(rule_eps, i+1):
                new_rule = Rule(rule.left_part, ' '.join(rule.right_part))
                for ch in combo:
                    new_rule.right_part.remove(ch)
                if len(new_rule.right_part) > 0:
                    ret.rules.append(new_rule)

    # Удалить все ε-правила из P′
    eps_rules = []
    for rule in ret.rules:
        if rule.right_part[0] == ret.eps:
            eps_rules.append(rule)
    for rule in eps_rules:
        ret.rules.remove(rule)

    return ret
