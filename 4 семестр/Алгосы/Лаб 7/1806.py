import heapq

def main():
    n = int(input())
    times = list(map(int, input().split()))
    ids = [input().strip() for _ in range(n)]
    index = {ids[i]: i for i in range(n)}

    INF = 10**18
    dist = [INF]*n
    prev = [-1]*n
    dist[0] = 0

    pq = [(0, 0)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == n-1:
            break

        s = ids[u]
        for i in range(10):
            cost = times[i]
            orig = s[i]
            for c in '0123456789':
                if c == orig: 
                    continue
                t = s[:i] + c + s[i+1:]
                v = index.get(t)
                if v is not None:
                    nd = d + cost
                    if nd < dist[v]:
                        dist[v] = nd
                        prev[v] = u
                        heapq.heappush(pq, (nd, v))
            for j in range(i+1, 10):
                if s[j] == orig:
                    continue
                lst = list(s)
                lst[i], lst[j] = lst[j], lst[i]
                t = ''.join(lst)
                v = index.get(t)
                if v is not None:
                    nd = d + cost
                    if nd < dist[v]:
                        dist[v] = nd
                        prev[v] = u
                        heapq.heappush(pq, (nd, v))

    if dist[n-1] == INF:
        print(-1)
    else:
        path = []
        cur = n-1
        while cur != -1:
            path.append(cur+1)
            cur = prev[cur]
        path.reverse()
        print(dist[n-1])
        print(len(path))
        print(*path)

if __name__ == "__main__":
    main()
