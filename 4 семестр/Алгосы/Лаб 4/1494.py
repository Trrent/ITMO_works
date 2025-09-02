def main():
    n = int(input())
    seq = [int(input()) for i in range(n)]

    stack = []
    next_ball = 1
    cheater = False

    for ball in seq:
        if cheater:
            break

        if ball >= next_ball:
            for b in range(next_ball, ball):
                stack.append(b)
            next_ball = ball + 1
        else:
            if stack and stack[-1] == ball:
                stack.pop()
            else:
                cheater = True

    print("Cheater" if cheater else "Not a proof")


if __name__ == "__main__":
    main()
