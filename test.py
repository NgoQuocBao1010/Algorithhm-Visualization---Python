from collections import deque

a = deque()

for i in range(10):
    a.append(i)

a.popleft()
for e in a:
    print(e)