from asyncio import graph
from collections import deque
import heapq


#
# def dfs_recursive(graph, vertex, visited=None):
#     if visited is None:
#         visited = set()
#     visited.add(vertex)
#     print(vertex, end=' ')  # обработка вершины
#     for neighbour in graph[vertex]:
#         if neighbour not in visited:
#             dfs_recursive(graph, neighbour, visited)
#     return visited
#
# graph = {
#     'A': ['B', 'C'],
#     'B': ['A', 'D'],
#     'C': ['A', 'D'],
#     'D': ['B', 'C']
# }
#
# print("DFS рекурсивный:")
# list_n = dfs_recursive(graph, 'A')  # Вывод: A B D C (порядок может отличаться)
# print(f"\n{list_n}")
#
#
# def dfs_iterative(graph, start):
#     visited = set()
#     stack = [start]
#     while stack:
#         vertex = stack.pop()   # берём вершину с вершины стека
#         if vertex not in visited:
#             visited.add(vertex)
#             print(vertex, end=' ')
#             # Добавляем соседей в стек. Чтобы порядок обхода совпадал с рекурсивным,
#             # можно добавить их в обратном порядке, но не обязательно.
#             for neighbour in graph[vertex]:
#                 if neighbour not in visited:
#                     # print(neighbour, end=' ')
#                     stack.append(neighbour)
#     return visited
#
# print("\nDFS итеративный:")
# list_d = dfs_iterative(graph, 'A')
# print(f"\n{list_d}")
#
#
# def bfs(graph, start):
#     visited = set()
#     queue = deque([start])
#     visited.add(start)          # важный момент: помечаем как посещённую при добавлении в очередь, а не при извлечении
#     while queue:
#         vertex = queue.popleft()
#         print(vertex, end=', ')
#         for neighbour in graph[vertex]:
#             if neighbour not in visited:
#                 visited.add(neighbour)
#                 queue.append(neighbour)
#     return visited
#
# print("\nBFS:")
# bfs(graph, 'A')  # Вывод: A B C D (слои: A, потом B и C, потом D)

# def dfs_grid(grid, i, j, visited):
#     rows = len(grid)
#     cols = len(grid[0])
#     # Проверка выхода за границы или посещённой клетки или стены
#     if i < 0 or i >= rows or j < 0 or j >= cols:
#         return
#     if (i, j) in visited or grid[i][j] == '0':
#         return
#     visited.add((i, j))
#     # Рекурсивно идём к соседям
#     dfs_grid(grid, i+1, j, visited)
#     dfs_grid(grid, i-1, j, visited)
#     dfs_grid(grid, i, j+1, visited)
#     dfs_grid(grid, i, j-1, visited)
#

#
# def num_islands(grid):
#     rows = len(grid)
#     cols = len(grid[0])
#     count = 0
#
#     def dfs(i, j):
#         if i < 0 or i >= rows or j < 0 or j >= cols:
#             return
#         if grid[i][j] == '0':
#             return
#         grid[i][j] = '0'
#         dfs(i + 1, j)
#         dfs(i - 1, j)
#         dfs(i, j + 1)
#         dfs(i, j - 1)
#
#     for i in range(rows):
#         for j in range(cols):
#             if grid[i][j] == '1':
#                 dfs(i, j)
#                 count += 1
#
#     return count
#
#
# grid = [
#     ['1', '1', '0', '1', '0'],
#     ['1', '1', '0', '0', '1'],
#     ['0', '0', '1', '0', '0'],
#     ['1', '0', '0', '1', '1']
# ]
#

#
# print(num_islands(grid))

#
# def bfs_shortest_path(graph, start, goal):
#     queue = deque([start])
#     visited = {start}           # множество посещённых вершин
#     parent = {start: None}      # словарь: откуда пришли в эту вершину
#     while queue:
#         vertex = queue.popleft()
#         if vertex == goal:
#             # Восстанавливаем путь
#             path = []
#             while vertex is not None:
#                 path.append(vertex)
#                 vertex = parent[vertex]
#             return path[::-1]   # обратный порядок
#         for neighbour in graph[vertex]:
#             if neighbour not in visited:
#                 visited.add(neighbour)
#                 parent[neighbour] = vertex
#                 queue.append(neighbour)
#     return None  # путь не найден
#
# graph = {
#     'A': ['B', 'C'],
#     'B': ['A', 'D'],
#     'C': ['A', 'D'],
#     'D': ['B', 'C', 'E'],
#     'E': ['D', 'E']
# }
#
# # print(bfs_shortest_path(graph, 'A', 'C'))  # ['A', 'C', 'D', 'E'] или ['A', 'B', 'D', 'E']

#
# def shortest_path_grid(grid, start, goal):
#     rows, cols = len(grid), len(grid[0])
#     sr, sc = start  # координаты старта
#     gr, gc = goal  # координаты цели
#
#     # Матрица visited того же размера, чтобы не ходить кругами.
#     visited = [[False] * cols for _ in range(rows)]
#     visited[sr][sc] = True
#
#     # Очередь хранит кортежи (r, c, distance)
#     queue = deque([(sr, sc, 0)])
#
#     # 4 направления: вверх, вниз, влево, вправо
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#
#     while queue:
#         r, c, dist = queue.popleft()
#
#         # Если достигли цели — возвращаем расстояние
#         if (r, c) == (gr, gc):
#             return dist
#
#         # Проверяем все 4 направления
#         for dr, dc in directions:
#             nr, nc = r + dr, c + dc
#
#             # Проверки:
#             # 1) не вышли ли за границы
#             if 0 <= nr < rows and 0 <= nc < cols:
#                 # 2) не стена ли там
#                 if grid[nr][nc] != '0':
#                     # 3) не посещали ли ранее
#                     if not visited[nr][nc]:
#                         visited[nr][nc] = True
#                         queue.append((nr, nc, dist + 1))
#
#     # Если очередь опустела, а цель не найдена — пути нет
#     return -1
#
#
# grid = [
#     ['1', '1', '1'],
#     ['1', '0', '1'],
#     ['1', '1', '1']
# ]
# start = (0, 0)
# goal = (2, 2)
#
# print(shortest_path_grid(grid, start, goal))

# weighted_graph = {
#     'A': {'B': 4, 'C': 2},
#     'B': {'C': bankapi, 'D': 10},
#     'C': {'D': 3, 'E': 2},
#     'D': {'E': 4},
#     'E': {}
# }
#
# def dijkstra(graph, start):
#     distances = {vertex: float('inf') for vertex in graph}
#     distances[start] = 0
#     priority_queue = [(0, start)]  # (расстояние, вершина)
#     previous = {start: None}       # для восстановления пути (опционально)
#     while priority_queue:
#         current_dist, current_vertex = heapq.heappop(priority_queue)
#         if current_dist > distances[current_vertex]:
#             continue  # устаревший элемент, пропускаем
#         for neighbor, weight in graph[current_vertex].items():
#             distance = current_dist + weight
#             if distance < distances[neighbor]:
#                 distances[neighbor] = distance
#                 previous[neighbor] = current_vertex
#                 heapq.heappush(priority_queue, (distance, neighbor))
#     return distances, previous
#
# dist, prev = dijkstra(weighted_graph, 'A')
# print(dist)  # {'A': 0, 'B': 4, 'C': 2, 'D': bankapi, 'E': 4}
#
#
# def shortest_path_grid(grid):
#     rows, cols = len(grid), len(grid[0])
#     sr, sc = (0, 0)  # координаты старта
#     gr, gc = rows - 1, cols - 1
#     if grid[sr][sc] == 1 or grid[gr][gc] == 1:
#         return -1
#     grid[sr][sc] = 1
#     queue = deque([(sr, sc, 1)])
#     directions = [(-1, -1), (1, 1), (-1, 1), (1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)]
#     while queue:
#         r, c, dist = queue.popleft()
#         if (r, c) == (gr, gc):
#             return dist
#         for dr, dc in directions:
#             nr, nc = r + dr, c + dc
#             if 0 <= nr < rows and 0 <= nc < cols:
#                 if grid[nr][nc] == 0:
#                     grid[nr][nc] = 1
#                     queue.append((nr, nc, dist + 1))
#
#     return -1
#
#
# grid = [
#     [0, 0, 0],
#     [0, 0, 0],
#     [0, 0, 0]
# ]
# print(shortest_path_grid(grid))
# print(grid)

def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    gr, gc = goal

    # Если старт или цель — стена, пути нет
    if grid[sr][sc] == 1 or grid[gr][gc] == 1:
        return None

    # Возможные ходы (8 направлений)
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    # Очередь с приоритетом: элементы вида (f, g, r, c)
    # f = g + h, где h — эвристика
    open_set = []
    start_g = 0
    start_h = max(abs(sr - gr), abs(sc - gc))  # октальная эвристика

    heapq.heappush(open_set, (start_g + start_h, start_g, sr, sc))
    # best_g[r][c] — минимальное известное расстояние от старта до клетки (r,c)
    best_g = [[float('inf')] * cols for _ in range(rows)]
    best_g[sr][sc] = start_g

    # parent[r][c] хранит предыдущую клетку для восстановления пути
    parent = [[None] * cols for _ in range(rows)]

    while open_set:
        print(open_set)
        f, g, r, c = heapq.heappop(open_set)

        # Если мы достигли цели, восстанавливаем путь
        if (r, c) == (gr, gc):
            path = []
            while (r, c) != (sr, sc):
                path.append((r, c))
                r, c = parent[r][c]
            path.append((sr, sc))
            return path[::-1]  # от старта к цели

        # Если извлекли устаревшее состояние (g больше уже найденного), пропускаем
        if g > best_g[r][c]:
            continue

        # Перебираем соседей
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                new_g = g + 1  # каждый шаг стоит 1
                if new_g < best_g[nr][nc]:
                    best_g[nr][nc] = new_g
                    parent[nr][nc] = (r, c)
                    h = max(abs(nr - gr), abs(nc - gc))
                    print(new_g)
                    f = new_g + h
                    heapq.heappush(open_set, (f, new_g, nr, nc))

    return None  # Путь не найден

# Пример использования
grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]
start = (0, 0)
goal = (4, 4)

path = a_star(grid, start, goal)
print("Кратчайший путь:", path)