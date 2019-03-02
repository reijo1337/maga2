from fa_builder import build_for_regexp
from fa_minimization import minimize


def main():
    # regexp = str(input('Введите регулярное выражение: '))
    regexp = '(a|b)*abb'
    print(f'Регулярное выражение: {regexp}')
    print('Строим ДКА по регулярному выражению')
    FA = build_for_regexp(regexp)
    states = FA.states()
    for state in states:
        print(state)
    print('Визуализируем ДКА')
    FA.visualize('original_fa.gv')
    print('Минимизация ДКА и визуализация')
    min_fa = minimize(FA)
    min_fa.visualize('min_fa.gv')


if __name__ == '__main__':
    main()
