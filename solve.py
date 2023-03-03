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
    elif rule == 'Shift <':
        if x[0] == '-': sign, ans = '-', x[1:]
        else: sign, ans = '', x
        ans = sign + ans[1:] + ans[0]
        ans = str(int(ans))
        if len(ans) > 6: ans = 'error'
        return ans
    elif rule == 'SUM':
        if x[0] == '-': sign, ans = '-', x[1:]
        else: sign, ans = '', x
        ans = sign + str(sum(ord(c) - ord('0') for c in ans))
        return ans
    elif rule[:2] in {'+ ', '- ', '* ', 'x ', '/ '}:
        opr = int(rule[2:])
        y = int(x)
        if rule[0] == '+': ans = str(y + opr)
        elif rule[0] == '-': ans = str(y - opr)
        elif rule[0] in {'*', 'x'}: ans = str(y * opr)
        elif rule[0] == '/':
            ans = y // opr
            if y == ans * opr: ans = str(ans)
            else: ans = 'error'
        if len(ans) > 6: ans = 'error'
        return ans
    elif rule[:3] == '[+] ':
        # do zaimplementowania
        pass

door = dict()
q = deque()

door[(start, 0)] = ('OK', None)
q.append((start, 0))

while len(q) > 0:
    x, crazy = q.popleft()
    if x == goal: break

    for b in buttons:
        y, crazy2 = apply((x, crazy), b)
        #if type(y) == NoneType:
        #    print(x, b)
        if y in door: continue
        door[y] = b, x
        q.append(y)

path = []
x = goal
while x != start:
    b, x = door[x]
    path.append(b)

path = path[::-1]

print("'" + "' '".join(path) + "'")