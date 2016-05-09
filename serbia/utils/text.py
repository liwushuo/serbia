# -*- coding: utf-8 -*-

import string
from random import choice


def gen_random_string(length):
    return ''.join(choice(string.ascii_lowercase + string.digits) for _ in range(length))


def gen_random_number(length):
    return ''.join(choice(string.digits) for _ in range(length))


def reverse_order(order):
    if not order:
        order = 'desc'

    return 'asc' if order == 'desc' else 'desc'
