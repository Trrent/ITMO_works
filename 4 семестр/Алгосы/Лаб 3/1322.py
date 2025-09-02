def decode_bwt(k, last_column):
    n = len(last_column)

    temp = sorted([(char, i) for i, char in enumerate(last_column)])

    result = []
    k -= 1
    for _ in range(n):
        result.append(temp[k][0])
        k = temp[k][1]

    return ''.join(result)


k = int(input().strip())
last_column = input().strip()

print(decode_bwt(k, last_column))
