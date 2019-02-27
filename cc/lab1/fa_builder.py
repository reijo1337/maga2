import syntax_tree as st

def build_for_regexp(regexp):
    """
    Построение ДКА из регуляьрного выражения
    :type regexp: str
    """
    Q = {
        'marked': list(),
        'unmarked': list(),
    }
    tree = st.build_tree(regexp)
    followpos_dict = st.get_followpos(tree)
    q0 = st.firstpos(tree)
    Q['unmarked'].append(q0)
    while len(Q) != 0:
        R = Q['unmarked'].pop(0)
        Q['marked'].append(R)
