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
                    right_part = r.right_part.extends(rule.right_part[1:])
                    grammar.add_rule(rule.left_part, ' '.join(right_part))
        # TODO Устранить непосредственную рекурсию среди Ai продукций

