def main():
    m, n, k = map(int, input().split())

    rows = [[] for _ in range(m+1)]
    cols = [[] for _ in range(n+1)]
    for _ in range(k):
        x, y = map(int, input().split())
        rows[x].append(y)
        cols[y].append(x)

    for i in range(1, m+1):
        rows[i].sort()
    for j in range(1, n+1):
        cols[j].sort()

    countH = 0
    singleH = []
    for i in range(1, m+1):
        last = 0
        for y in rows[i]:
            gap = y - last - 1
            if gap >= 2:
                countH += 1
            elif gap == 1:
                singleH.append((i, last+1))
            last = y
        gap = n - last
        if gap >= 2:
            countH += 1
        elif gap == 1:
            singleH.append((i, last+1))

    countV = 0
    singleV = []
    for j in range(1, n+1):
        last = 0
        for x in cols[j]:
            gap = x - last - 1
            if gap >= 2:
                countV += 1
            elif gap == 1:
                singleV.append((last+1, j))
            last = x
        gap = m - last
        if gap >= 2:
            countV += 1
        elif gap == 1:
            singleV.append((last+1, j))

    setH1 = set(singleH)
    isolated = 0
    for coord in singleV:
        if coord in setH1:
            isolated += 1

    print(countH + countV + isolated)

if __name__ == "__main__":
    main()
