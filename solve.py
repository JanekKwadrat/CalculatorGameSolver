#! /usr/bin/python3

import sys
from collections import deque
from types import NoneType

if len(sys.argv) < 3:
    print('Usage: ./solve.py <goal> <start> <button1> <button2> ...')
    exit()

start = sys.argv[2]
goal = sys.argv[1]

buttons = sys.argv[3:]

#print(start)
#print(goal)
#print(buttons)

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

def apply(x_crazy: tuple[str, int], rule: str):
    x, crazy = x_crazy
    if x == 'error': return x, crazy
    elif rule == 'Mirror':
        if x[0] != '-': ans = x + x[::-1]
        else: ans = x + x[:0:-1]
        if len(ans) > 6: ans = 'error'
        return ans, crazy
    elif rule == '<<':
        ans = x[:-1]
        if ans == '-' or len(ans) == 0: ans = '0'
        return ans, crazy
    elif rule == 'Shift <':
        if x[0] == '-': sign, ans = '-', x[1:]
        else: sign, ans = '', x
        ans = sign + ans[1:] + ans[0]
        ans = str(int(ans))
        if len(ans) > 6: ans = 'error'
        return ans, crazy
    elif rule == 'SUM':
        if x[0] == '-': sign, ans = '-', x[1:]
        else: sign, ans = '', x
        ans = sign + str(sum(ord(c) - ord('0') for c in ans))
        return ans, crazy
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
        return ans, crazy
    elif rule.isnumeric():
        opr = str(int(rule) + crazy)
        ans = str(int(x + opr))
        if len(ans) > 6: ans = 'error'
        return ans, crazy
    elif rule[:4] == '[+] ':
        opr = int(rule[4:])
        crazy += opr
        return x, crazy

door = dict()
q = deque()

door[(start, 0)] = ('OK', None)
q.append((start, 0))

#wierzchołki w grafie są postaci krotki (liczba, crazy)

wanna_break = False
while len(q) > 0:
    u = q.popleft()
    if u[0] == goal: break

    for b in buttons:
        v = apply(u, b)
        if v in door: continue
        door[v] = b, u
        q.append(v)
        if v[0] == goal:
            wanna_break = True
            break
    if wanna_break: break

path = []
x = goal
crz = 0
while (x, crz) not in door: crz += 1
u = (x, crz)
#print(u)
while u != (start, 0):
    b, u = door[u]
    path.append(b)

path = path[::-1]

print("'" + "' '".join(path) + "'")