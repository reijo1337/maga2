from fa_builder import build_for_regexp
from fa_minimization import minimize, minimization


def main():
    # regexp = str(input('Введите регулярное выражение: '))
    regexp = 'ccc(ab|ab)+c*'
    print(f'Регулярное выражение: {regexp}')
    print('Строим ДКА по регулярному выражению')
    FA = build_for_regexp(regexp)
    states = FA.states()
    for state in states:
        print(state)
    print('Визуализируем ДКА')
    FA.visualize('original_fa')
    print('Минимизация ДКА и визуализация')
    min_fa = minimization(FA)
    min_fa.visualize('min_fa')
    check1 = 'ababaabb'
    print(f'Проверка строки {check1}')
    min_fa.check(check1)


if __name__ == '__main__':
    main()
