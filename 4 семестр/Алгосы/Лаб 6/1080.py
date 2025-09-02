from collections import deque

def main(adj):
    color = [-1] * (len(adj))
    color[1] = 0
    q = deque([1])

    while q:
        u = q.popleft()
        for v in adj[u]:
            if color[v] == -1:
                color[v] = 1 - color[u]
                q.append(v)
            elif color[v] == color[u]:
                print(-1)
                return
    print(''.join(str(color[i]) for i in range(1, len(adj))))


if __name__ == "__main__":
    n = int(input())
    nodes = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        towns = [int(t) for t in input().split()]
        while True:
            x = towns.pop(0)
            if x == 0:
                break
            nodes[i].append(x)
            nodes[x].append(i)
    main(nodes)