#!/usr/bin/env python3

test_int = 'essr'
try:
    test_int = int(test_int)
except ValueError as e:
    print('转换失败')