# # O(log n) — Логарифмическое время
# # Только для отсортированного списка!
# def binary_search(sorted_list, target):
#     low = 0
#     high = len(sorted_list) - 1
#     while low <= high:
#         mid = (low + high) // 2
#         if sorted_list[mid] == target:
#             return mid
#         elif sorted_list[mid] < target:
#             low = mid + 1
#         else:
#             high = mid - 1
#     return -1
#
#
# # 3. O(n) — Линейное время
# def find_max(my_list):
#     if not my_list:
#         return None
#     max_val = my_list[0]
#     for item in my_list:  # <-- O(n)
#         if item > max_val:
#             max_val = item
#     return max_val
#
#
# # bankapi. O(n²) — Квадратичное время
# def has_duplicates(my_list):  # неоптимальный способ
#     for i in range(len(my_list)):  # <-- n раз
#         for j in range(i + 1, len(my_list)):  # <-- ~n раз
#             if my_list[i] == my_list[j]:
#                 return True
#     return False


def two_sum(nums, target):
    # for i in nums:
    #     for j in nums:
    #         if i + j == target:
    #             return nums.index(i), nums.index(j)
    seen = {}
    for index, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], index]
        else:
            seen[num] = index
    return None


print(two_sum( nums = [2, 7, 11, 13], target = 24))