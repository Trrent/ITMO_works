def update_s(bit, i, delta):
    n = len(bit) - 1
    while i <= n:
        bit[i] += delta
        i += i & -i

def find_solder(bit, k):
    n = len(bit) - 1
    pos = 0
    pw = 1 << (n.bit_length() - 1)
    while pw:
        nxt = pos + pw
        if nxt <= n and bit[nxt] < k:
            k -= bit[nxt]
            pos = nxt
        pw >>= 1
    return pos + 1

def main():
    n, k = map(int, input().split())

    bit = [0] * (n + 1)
    for i in range(1, n+1):
        update_s(bit, i, 1)

    result = []
    rem = n
    cur = k

    while rem:
        cur = (cur - 1) % rem + 1 
        idx = find_solder(bit, cur)
        result.append(idx)
        update_s(bit, idx, -1)
        rem -= 1
        cur += k - 1     

    print(*result)

if __name__ == "__main__":
    main()
