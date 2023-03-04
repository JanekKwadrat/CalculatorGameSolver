#! /usr/bin/python3

import sys
from collections import deque
from types import NoneType

if len(sys.argv) < 3:
    print('Usage: ./solve.py <goal> <start> [<portals>] <button1> <button2> ...')
    exit()

start = sys.argv[2]
goal = sys.argv[1]

buttons = sys.argv[3:]
if len(buttons[0]) == 6 and all((c in '.v^') for c in buttons[0]):
    portals = buttons[0]
    buttons = buttons[1:]
    portal0, portal1 = 0, 0
    for i in range(6):
        if portals[i] == 'v': portal0 = i
        if portals[i] == '^': portal1 = i
else:
    portals = None

#print(start)
#print(goal)
#print(buttons)

def signed(x: str):
    if x[0] == '-': return '-', x[1:]
    else: return '', x

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

def do_portals(x: str):
    if x == 'error': return 'error'
    if portals == None: return x
    sign, x = signed(x)
    x = '0' * (6 - len(x)) + x
    add = list('000000')
    if x[portal0] == '0': return sign + str(int(x))
    x = list(x)
    add[portal1] = x[portal0]
    x.pop(portal0)
    x = ['0'] + x
    ans = sign + str(int(''.join(x)) + int(''.join(add)))
    ans = do_portals(ans)
    return ans

def apply_np(x_crazy: tuple[str, int, str], rule: str):
    x, crazy, store = x_crazy
    if x == 'error': return x, crazy, store
    elif rule == 'Mirror':
        if x[0] != '-': ans = x + x[::-1]
        else: ans = x + x[:0:-1]
        if len(ans) > 6: ans = 'error'
        return ans, crazy, store
    elif rule == '<<':
        ans = x[:-1]
        if ans == '-' or len(ans) == 0: ans = '0'
        return ans, crazy, store
    elif rule == 'Shift <':
        if x[0] == '-': sign, ans = '-', x[1:]
        else: sign, ans = '', x
        ans = sign + ans[1:] + ans[0]
        ans = str(int(ans))
        if len(ans) > 6: ans = 'error'
        return ans, crazy, store
    elif rule == 'Shift >':
        if x[0] == '-': sign, ans = '-', x[1:]
        else: sign, ans = '', x
        ans = sign + ans[-1] + ans[:-1]
        ans = str(int(ans))
        if len(ans) > 6: ans = 'error'
        return ans, crazy, store
    elif rule == 'SUM':
        if x[0] == '-': sign, ans = '-', x[1:]
        else: sign, ans = '', x
        ans = sign + str(sum(ord(c) - ord('0') for c in ans))
        return ans, crazy, store
    elif rule == 'Reverse':
        if x[0] == '-': sign, ans = '-', x[1:]
        else: sign, ans = '', x
        ans = str(int(sign + ans[::-1]))
        return ans, crazy, store
    elif rule == '+/-':
        if x[0] == '-': sign, ans = '-', x[1:]
        else: sign, ans = '', x
        sign = '' if sign == '-' else '-'
        ans = sign + ans
        return ans, crazy, store
    elif rule[:2] in {'+ ', '- ', '* ', 'x ', '/ '}:
        opr = int(rule[2:]) + crazy
        y = int(x)
        if rule[0] == '+': ans = str(y + opr)
        elif rule[0] == '-': ans = str(y - opr)
        elif rule[0] in {'*', 'x'}: ans = str(y * opr)
        elif rule[0] == '/':
            ans = y // opr
            if y == ans * opr: ans = str(ans)
            else: ans = 'error'
        if len(ans) > 6: ans = 'error'
        return ans, crazy, store
    elif rule.isnumeric():
        opr = str(int(rule) + crazy)
        ans = str(int(x + opr))
        if len(ans) > 6: ans = 'error'
        return ans, crazy, store
    elif rule[:4] == '[+] ':
        opr = int(rule[4:])
        crazy += opr
        return x, crazy, store
    elif rule == 'Store':
        if store != None and store[0] != '-': ans = x + store
        else: ans = x
        return ans, crazy, store
    elif rule == 'StoreStore':
        store = x
        return x, crazy, store
    elif '=>' in rule:
        a, b = rule.split('=>')
        ans = x.replace(a, b)
        return ans, crazy, store
    elif rule == 'Inv10':
        if x[0] == '-': sign, ans = '-', x[1:]
        else: sign, ans = '', x
        ans = sign + ''.join(chr((10 - (ord(c) - ord('0'))) % 10 + ord('0')) for c in ans)
        return ans, crazy, store
    elif rule == 'x^2':
        ans = str(int(x) ** 2)
        if len(ans) > 6: ans = 'error'
        return ans, crazy, store
    elif rule == 'x^3':
        ans = str(int(x) ** 3)
        if len(ans) > 6: ans = 'error'
        return ans, crazy, store

def apply(x_crazy: tuple[str, int, str], rule: str):
    x, crazy, store = apply_np(x_crazy, rule)
    return do_portals(x), crazy, store
    return x, crazy, store

if 'Store' in buttons: buttons.append('StoreStore')

door = dict()
q = deque()

door[(start, 0, None)] = ('OK', None)
q.append((start, 0, None))

#wierzchołki w grafie są postaci krotki (liczba, crazy)
dont_know = None

wanna_break = False
while len(q) > 0:
    u = q.popleft()

    for b in buttons:
        v = apply(u, b)
        if v in door: continue
        door[v] = b, u
        q.append(v)
        if v[0] == goal:
            dont_know = v
            wanna_break = True
            break
    if wanna_break: break

path = []
u = dont_know
#print(u)
while u != (start, 0, None):
    b, u = door[u]
    path.append(b)

path = path[::-1]

print("'" + "' '".join(path) + "'")