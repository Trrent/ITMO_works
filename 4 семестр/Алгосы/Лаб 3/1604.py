import heapq

k = int(input())
if k == 1:
    count = int(input().strip())
    print("1 " * count)
    exit()

temp = list(map(int, input().split()))
heap = [(-temp[i], i + 1) for i in range(k)]
heapq.heapify(heap)

while heap[0][0] != 0:
    first = heapq.heappop(heap)
    second = heapq.heappop(heap)

    print(first[1], end=" ")
    first = (first[0] + 1, first[1])

    if second[0] != 0:
        print(second[1], end=" ")
        second = (second[0] + 1, second[1])

    heapq.heappush(heap, first)
    heapq.heappush(heap, second)            