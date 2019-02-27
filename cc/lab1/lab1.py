from fa_builder import build_for_regexp


def main():
    # regexp = str(input('Введите регулярное выражение: '))
    regexp = '(a|b)*abb'
    print(f'Регулярное выражение: {regexp}')
    print('Строим ДКА по регулярному выражению')
    FA = build_for_regexp(regexp)
    print('Визуализируем ДКА')
    FA.visualize()


if __name__ == '__main__':
    main()
