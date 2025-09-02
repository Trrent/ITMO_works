import heapq
from collections import defaultdict

def main():
    n = int(input())
    person_city = {}
    person_money = {}
    all_cities = set()

    for _ in range(n):
        name, city, w_s = input().split()
        w = int(w_s)
        person_city[name] = city
        person_money[name] = w
        all_cities.add(city)

    m, k = map(int, input().split())
    events = []
    for _ in range(k):
        d_s, pname, dest = input().split()
        d = int(d_s)
        events.append((d, pname, dest))
        all_cities.add(dest)
    events.sort(key=lambda x: x[0])

    city_sum = {city: 0 for city in all_cities}
    for name, city in person_city.items():
        city_sum[city] += person_money[name]

    sum_count = defaultdict(int)
    sum_cities = defaultdict(set)
    maxheap = []

    for city, s in city_sum.items():
        sum_count[s] += 1
        sum_cities[s].add(city)
    for s in sum_count:
        heapq.heappush(maxheap, -s)

    def get_top_sum():
        while maxheap:
            s = -maxheap[0]
            if sum_count[s] > 0:
                return s
            heapq.heappop(maxheap)
        return 0

    city_days = defaultdict(int)
    prev_day = 1
    idx = 0
    L = len(events)

    while idx < L:
        d, _, _ = events[idx]
        span = d - prev_day + 1
        if span > 0:
            top = get_top_sum()
            if sum_count[top] == 1:
                leader = next(iter(sum_cities[top]))
                city_days[leader] += span

        while idx < L and events[idx][0] == d:
            _, pname, dest = events[idx]
            w = person_money[pname]
            old = person_city[pname]

            old_s = city_sum[old]
            sum_count[old_s] -= 1
            sum_cities[old_s].remove(old)
            city_sum[old] = old_s - w
            new_old_s = old_s - w
            sum_count[new_old_s] += 1
            sum_cities[new_old_s].add(old)
            heapq.heappush(maxheap, -new_old_s)

            prev_s2 = city_sum.get(dest, 0)
            sum_count[prev_s2] -= 1
            sum_cities[prev_s2].discard(dest)
            city_sum[dest] = prev_s2 + w
            new_s2 = prev_s2 + w
            sum_count[new_s2] += 1
            sum_cities[new_s2].add(dest)
            heapq.heappush(maxheap, -new_s2)

            person_city[pname] = dest
            idx += 1

        prev_day = d + 1

    if prev_day <= m:
        span = m - prev_day + 1
        if span > 0:
            top = get_top_sum()
            if sum_count[top] == 1:
                leader = next(iter(sum_cities[top]))
                city_days[leader] += span

    for city in sorted(city_days):
        days = city_days[city]
        if days > 0:
            print(city, days)

if __name__ == "__main__":
    main()
