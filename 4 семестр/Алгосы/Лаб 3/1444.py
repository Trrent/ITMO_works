import math

def solve():
    n = int(input().strip())

    coords = [tuple(map(int, input().split())) for _ in range(n)]

    f_x, f_y = coords[0]

    pumpkins = [None] * n

    pumpkins[0] = (0.0, -1.0, 1)

    for i in range(1, n):
        x, y = coords[i]
        length = (x - f_x)**2 + (y - f_y)**2
        degrees = math.degrees(math.atan2(y - f_y, x - f_x))
        if (y - f_y) < 0:
            degrees += 360.0
        pumpkins[i] = (length, degrees, i+1)

    pumpkins.sort(key=lambda p: (p[1], p[0]))

    start_point = 1
    for i in range(1, n - 1):
        if pumpkins[i+1][1] - pumpkins[i][1] > 179.999:
            start_point = i + 1

    print(n)
    print(1)

    for i in range(start_point, n):
        print(pumpkins[i][2])
    for i in range(1, start_point):
        print(pumpkins[i][2])

solve()
