from part1.grammar import Grammar


def remove_left_recursion(grammar):
    """
    Удаление левой рекусрии из грамматики
    :type grammar: Grammar
    """
    # Расположить нетерминалы в некотором порядке A1, A2, ..., An
    A = grammar.non_terminals
    # for i:=1 to n do begin
    for i in range(len(A)):
        # for j:=1 to i-1 do begin
        for j in range(i):
            # Получим все продукции вида Ai->Ajy
            aij_rules = []
            for rule in grammar.rules:
                if rule.left_part == A[i] and A[j] == rule.right_part[0]:
                    aij_rules.append(rule)
            # Заменим продукции
            for rule in aij_rules:
                # Продукции Aj
                aj = rule.right_part[0]
                aj_rules = []
                for r in grammar.rules:
                    if r.left_part == aj:
                        aj_rules.append(r)
                # Замена продукции
                grammar.rules.remove(rule)
                for r in aj_rules:
                    right_part = r.right_part.copy()
                    right_part.extend(rule.right_part[1:])
                    grammar.add_rule(rule.left_part, ' '.join(right_part))
        # Устранить непосредственную рекурсию среди Ai продукций
        # Запишем все правила вывода из A в виде: A→Aα1∣…∣Aαn∣β1∣…∣βm
        recursive_rules = {
            'rec': [],
            'nonrec': [],
        }
        for rule in grammar.rules:
            if rule.left_part == A[i]:
                if rule.right_part[0] == A[i]:
                    recursive_rules['rec'].append(rule)
                else:
                    recursive_rules['nonrec'].append(rule)

        if len(recursive_rules['rec']) > 0:
            new_non_literal = f'{A[i]}1'
            grammar.add_non_terminal(new_non_literal)
            # Заменим правила вывода из A на A→β1A′∣… ∣βmA′∣β1∣…∣βm.
            for rule in recursive_rules['nonrec']:
                grammar.rules.remove(rule)
                if rule.right_part[0] != grammar.eps:
                    grammar.add_rule(A[i],
                                     ' '.join(rule.right_part) + ' ' + new_non_literal)
                else:
                    grammar.add_rule(A[i], new_non_literal)
                    grammar.add_rule(new_non_literal, 'eps')

            # Создадим новый нетерминал A′→α1A′∣…∣αnA′∣α1∣…∣αn.
            for rule in recursive_rules['rec']:
                grammar.rules.remove(rule)
                grammar.add_rule(new_non_literal,
                                 ' '.join(rule.right_part[1:]) + ' ' + new_non_literal)
