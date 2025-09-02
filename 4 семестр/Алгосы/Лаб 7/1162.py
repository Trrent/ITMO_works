def solve():
    n, m, s, v = input().split()
    n, m, s = int(n), int(m), int(s)
    v = float(v)

    edges = []
    for _ in range(m):
        a, b, rab, cab, rba, cba = input().split()
        a, b = int(a), int(b)
        rab, cab = float(rab), float(cab)
        rba, cba = float(rba), float(cba)
        edges.append((a, b, rab, cab))
        edges.append((b, a, rba, cba))

    value = [0.0] * (n + 1)
    value[s] = v

    for _ in range(n - 1):
        updated = False
        for u, w, rate, comm in edges:
            if value[u] >= comm:
                new_amount = (value[u] - comm) * rate
                if new_amount > value[w]:
                    value[w] = new_amount
                    updated = True
        if not updated:
            break

    for u, w, rate, comm in edges:
        if value[u] >= comm and (value[u] - comm) * rate > value[w]:
            print("YES")
            return

    print("NO")


if __name__ == "__main__":
    solve()
