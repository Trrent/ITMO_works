from collections import deque

def solve(n, edges, s, f):
    graph = [[] for _ in range(n+1)]
    indeg = [0]*(n+1)
    for u, v, c in edges:
        graph[u].append((v, c))
        indeg[v] += 1

    q = deque(i for i in range(1, n+1) if indeg[i] == 0)
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, _ in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    NEG = -10**18
    profit = [NEG]*(n+1)
    profit[s] = 0

    for u in topo:
        pu = profit[u]
        if pu == NEG:
            continue
        for v, cost in graph[u]:
            if pu + cost > profit[v]:
                profit[v] = pu + cost

    if profit[f] == NEG:
        print("No solution")
    else:
        print(profit[f])


if __name__ == "__main__":
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    s, f = map(int, input().split())
    solve(n, edges, s, f)
