#!usr/bin/python3
# -*- coding: utf-8 -*-

from collections import namedtuple

Patterns = namedtuple('Patterns', ['digit_figure', 'possible_digits'])

DIGIT_MAP = \
    {
        0: Patterns(' _ '
                    '| |'
                    '|_|', {'8'}),
        1: Patterns('   '
                    '  |'
                    '  |', {'7'}),
        2: Patterns(' _ '
                    ' _|'
                    '|_ ', {}),
        3: Patterns(' _ '
                    ' _|'
                    ' _|', {'9'}),
        4: Patterns('   '
                    '|_|'
                    '  |', {}),
        5: Patterns(' _ '
                    '|_ '
                    ' _|', {'6', '9'}),
        6: Patterns(' _ '
                    '|_ '
                    '|_|', {'5', '8'}),
        7: Patterns(' _ '
                    '  |'
                    '  |', {'1'}),
        8: Patterns(' _ '
                    '|_|'
                    '|_|', {'0', '6', '9'}),
        9: Patterns(' _ '
                    '|_|'
                    ' _|', {'3', '5', '8'}),
    }


def __extract_figure(figure_account, i):
    figure = ''
    for line in range(0, 3):
        for p in range(0, 3):
            figure += figure_account[line * 27 + i * 3 + p]
    return figure


def __parse_digit(figure):
    for k in DIGIT_MAP:
        if DIGIT_MAP[k].digit_figure == figure:
            return str(k)
    return '?'


def __parse(figure_account):
    account_number = ''
    for i in range(0, 9):
        account_number += __parse_digit(__extract_figure(figure_account, i))
    return account_number


def __validate(account_number):
    if len(account_number) != 9:
        return False
    num_sum = 0
    for i, digit in enumerate(account_number):
        num_sum += (9-i) * int(digit)
    return num_sum % 11 == 0


def ocr(figure_account):
    account_number = __parse(figure_account)
    if account_number.count('?'):
        return '{} ILL'.format(account_number)
    if not __validate(account_number):
        return '{} ERR'.format(account_number)
    return '{}'.format(account_number)


def replace_str(target_s, i, target_c):
    if i == len(target_s)-1:
        return target_s[:i] + target_c
    return target_s[:i] + target_c + target_s[i+1:]


def guess_digit(figure):
    possible_digit = set()
    for i in range(0, 9):
        if figure[i] != ' ':
            possible_digit.add(__parse_digit(replace_str(figure, i, ' ')))
        if i in [1, 4, 7]:
            possible_digit.add(__parse_digit(replace_str(figure, i, '_')))
        if i in [3, 5, 6, 8]:
            possible_digit.add(__parse_digit(replace_str(figure, i, '|')))
    return possible_digit - {__parse_digit(figure), '?'}


def __guess_ill_account(figure_account, account_number):
    ill_digit_index = account_number.find('?')
    guess_digits = guess_digit(__extract_figure(figure_account, ill_digit_index))
    for d in guess_digits:
        replaced_account = replace_str(account_number, ill_digit_index, d)
        if __validate(replaced_account):
            return '{}'.format(replaced_account)


def __guess_normal_account(account_number):
    guess_accounts = []
    for i in range(0, 9):
        for digit_s in DIGIT_MAP[int(account_number[i])].possible_digits:
            replaced_account = replace_str(account_number, i, digit_s)
            if __validate(replaced_account):
                guess_accounts.append(replaced_account)
    if len(guess_accounts) == 0:
        return '{} ERR'.format(account_number)
    elif len(guess_accounts) == 1:
        return '{}'.format(guess_accounts.pop())
    else:
        return '{} AMB {}'.format(account_number, guess_accounts)


def guess(figure_account):
    """
    figure_account, like '    _  _     _  _  _  _  _ '
                         '  | _| _||_||_ |_   ||_||_|'
                         '  ||_  _|  | _||_|  ||_| _|'

    account_number, like '123456789'

    figure, like ' _ '
                 '|_|'
                 '|_|'

    digit, like '8'

    """
    account_number = __parse(figure_account)
    if account_number.count('?') > 1:
        return '{} ILL'.format(account_number)

    if account_number.count('?') == 1:
        return __guess_ill_account(figure_account, account_number)

    if __validate(account_number):
        return '{}'.format(account_number)
    else:
        return __guess_normal_account(account_number)


def guess_multi_accounts(file_path):
    out_put = ''
    with open(file_path, 'r') as file:
        figure_account = ''
        for n, line in enumerate(file, start=1):
            if n % 4 != 0:
                figure_account += line.rstrip('\n')
            else:
                out_put += guess(figure_account) + '\n'
                figure_account = ''
    return out_put
