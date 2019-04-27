from nfa.fa_state import State
from nfa.fa import Automata


def e_closure(R: set):
    """
    Множество состояний НКА, достижимых из состояний, входящих в R, посредством только переходов по e
    """
    ret = set()
    for state in R:
        ret.update(state.epsilonTransitions)
        ret.update(e_closure(state.epsilonTransitions))
    return frozenset(ret)


def move(R, a):
    """
    Ммножество состояний НКА, в которые есть переход на входе a для состояний из R
    """
    ret = set()
    for state in R:
        for dest in state.getTransitionsForChar(a):
            ret.add(dest)
    return ret


def nfa_to_dfa(nfa: Automata):
    """
    Построение ДКА по НКА
    :param nfa: НКА
    :return: ДКА
    """
    Qs = {
        'marked': [],
        'unmarked': [],
    }
    q0s = e_closure({nfa.startState})
    Qs['unmarked'].append(q0s)
    start = state_from_states(q0s)
    states_to_state = {q0s: start}
    while len(Qs['unmarked']) > 0:
        R = Qs['unmarked'].pop(0)
        Qs['marked'].append(R)
        for a in nfa.alphabet():
            S = e_closure(move(R, a))
            S = S.union(move(R, a))
            if len(S) > 0:
                if S not in Qs['marked'] and S not in Qs['unmarked']:
                    Qs['unmarked'].append(S)
                    new_state = state_from_states(S)
                    states_to_state[S] = new_state
                states_to_state[R].moveOnChar(a, states_to_state[S])
    return Automata(start)

def state_from_states(states):
    ret = State({s.positions for s in states})
    for s in states:
        if s.isFinalState:
            ret.isFinalState = True
    return ret