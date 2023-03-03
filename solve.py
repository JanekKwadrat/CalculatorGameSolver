#! /usr/bin/python3

import sys

if len(sys.argv) < 3:
    print('Usage: ./solve.py <goal> <start> <button1> <button2> ...')
    #exit()

numberA = sys.argv[2]
numberB = sys.argv[1]

buttons = sys.argv[3:]

print(numberA)
print(numberB)
print(buttons)

def good(x: str):
    if len(x) == 0: return 'error'
    elif len(x) > 6: return 'error'
    elif x == '-': return 'error'
    else:
        ok = False
        if x[0] != '-' and x.isnumeric(): ok = True
        if x[0] == '-' and x[1:].isnumeric(): ok = True
        if not ok: return 'error'
    return x

def apply(x: str, rule: str):
    if x == 'error': return x
    elif rule == 'Mirror':
        if x[0] != '-': ans = x + x[::-1]
        else: ans = x + x[:0:-1]
        if len(ans) > 6: ans = 'error'
        return ans
    elif rule == '<<':
        ans = x[:-1]
        if ans == '-' or len(ans) == 0: ans = '0'
        return ans
    elif rule[:2] in {'+ ', '- ', '* ', '/ '}:
        opr = int(rule[2:])
        y = int(x)
        if rule[0] == '+': ans = str(y + opr)
        elif rule[0] == '-': ans = str(y - opr)
        elif rule[0] == '*': ans = str(y * opr)
        elif rule[0] == '/':
            ans = y // opr
            if y == ans * opr: ans = str(ans)
            else: ans = 'error'
        if len(ans) > 6: ans = 'error'
        return ans


