from functools import lru_cache


def climb_stairs_naive(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    return climb_stairs_naive(n - 1) + climb_stairs_naive(n - 2)


def climb_stairs_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n == 1:
        return 1
    if n == 2:
        return 2
    memo[n] = climb_stairs_memo(n - 1, memo) + climb_stairs_memo(n - 2, memo)
    return memo[n]


@lru_cache(maxsize=None)
def climb_stairs_lru(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    return climb_stairs_lru(n - 1) + climb_stairs_lru(n - 2)


print(climb_stairs_lru(100))