def main():
    n = int(input())
    x_coords = []
    y_coords = []
    for _ in range(n):
        x, y = map(int, input().split())
        x_coords.append(x)
        y_coords.append(y)

    x_coords.sort()
    y_coords.sort()

    total = 0

    for i in range(1, n):
        dx = x_coords[i] - x_coords[i - 1]
        dy = y_coords[i] - y_coords[i - 1]
        total += (dx + dy) * i * (n - i) * 2

    average_distance = total // (n * (n - 1))
    print(average_distance)

if __name__ == "__main__":
    main()
