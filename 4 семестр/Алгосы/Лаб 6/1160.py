from collections import deque


def solve(n, edges):
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb: return False
        parent[rb] = ra
        return True
    
    parent = list(range(n + 1))
    parent = list(range(n+1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def unite(a, b):
        ra, rb = find(a), find(b)
        if ra == rb: 
            return False
        parent[rb] = ra
        return True

    plan = []
    max_len = 0
    for w, u, v in edges:
        if unite(u, v):
            plan.append((u, v))
            if w > max_len:
                max_len = w
            if len(plan) == n-1:
                break

    out = [str(max_len), str(len(plan))]
    for u, v in plan:
        out.append(f"{u} {v}")
    print("\n".join(out))

if __name__ == "__main__":
    n, m = map(int, input().split())
    nodes = []
    for _ in range(m):
        a, b, c = map(int, input().split())
        nodes.append((c, b, a))
    nodes.sort(key=lambda x: x[0])    
    solve(n, nodes)
