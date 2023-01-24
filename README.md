# Graph distance
## Problems
<img src="https://d2gd6pc034wcta.cloudfront.net/tier/13.svg" width="13pt"> [BaekJoon 1865 Wormhole](https://www.acmicpc.net/problem/1865)

(related problems)

<img src="https://d2gd6pc034wcta.cloudfront.net/tier/12.svg" width="13pt"> [BaekJoon 11404 Floyd](https://www.acmicpc.net/problem/11404)

<img src="https://d2gd6pc034wcta.cloudfront.net/tier/12.svg" width="13pt"> [BaekJoon 1753 Shortest Path](https://www.acmicpc.net/problem/1753)

## Algorithm
Several algorithms for calculating shortest distances on graph were the candidates.

### [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)

  This algorithm is used to find the shortest paths **from a single source vertex to all other vertices** in a weighted graph. It uses a priority queue to determine which vertex to visit next and updates the shortest distance for each vertex as it is visited.
  
  It is unable to be used in **negative-distance** graph.
  
  - Time Complexity: O(E + VlogV)
    
  - Python code

``` python
from heapq import heappush, heappop

def Dijkstra(G, src, Gtype="dict", DMAX=10000001):
    D = [DMAX] * (len(G) + 1)
    D[src] = 0
    H = [(0, src)]

    while H:
        d, src = heappop(H)
        for dist, dst in G[src]:
            if 0 <= D[dst] <= d + dist:
                continue 

            D[dst] = dist + d
            heappush(H, (d + dist, dst))

    return D
```

### [Bellman-Ford algorithm](https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm)
  
This algorithm is similar to Dijstra's algorithm but it **can also handle negative edge weights.** It uses a relaxation technique to update the shortest distance for each vertex.

It is unable to used in graph that has **negative cycle**.
  
  - Time Complexity: O(VE)
  
  - Python code

```python
from itertools import chain

def BellmanFord(G, V, src, Gtype="dict", DMAX=10000001):
    D = [DMAX] * (V + 1)
    D[src] = 0
    update = True

    for i in range(V):
        if not update:
            break
        update = False
        for s, dist, d in chain((s, dist, d) for s in G for dist, d in G[s]):
            if D[s] < DMAX and D[s] + dist < D[d]:
                update = True 
                D[d] = D[s] + dist

    return D
```
  
### [A* algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)

This algorithm is an extension of Dijkstra's algorithm and it is used to find the shortest path in a graph with a heuristic function. This heuristic function is used to guide the search towards the goal node, which leads to a faster search.

  - Time Complexity: O(E + VlogV)

### [BFS](https://en.wikipedia.org/wiki/Breadth-first_search)

This algorithm is used to find the shortest path froma  single source vertex to all other vertices in an **unweighted graph**. It visits all the vertices of the graph by expanding the search in a breadth-first manner.

  - Time Complexity: O(V + E)
  
  - Python code
  
```python
from collections import deque

def BFS(G, src, Gtype="dict"):
    D = [-1] * (len(G) + 1)
    D[src] = 0
    Q = deque([(src, 0)])

    while Q:
        src, d = Q.popleft()
        for dst in G[src]:
            if D[dst] < 0:
                D[dst] = d + 1
                Q.append((dst, d+1))

    return D
```

### [Floyd-Warshall algorithm](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm)

This algorithm is used to find the shortest path between **all pairs of vertices** in a weighted graph. It uses dynamic programming to calculate the shortest path between each pair of vertices.

  - Time Complexity: O(V^3)
  
  - Python code
  
```python
def Floyd(G, Gtype="matrix", display=False):
    N = len(G)
    for n in range(N):
        for i in range(N):
            for j in range(N):
                if i != n and j != n:
                    G[i][j] = min(G[i][j], G[i][n] + G[n][j])

    return G
```

Since the problem(1865) is weighted, signed graph, we cannot use Dijkstra and BFS algorithm. A* algorithm is also inefficient because it is for single-single distance while we should calculate many-many vertices. Bellman-Ford or Floyd-Warshall algorithm seems appropriate. 
  
## Experiments

### Unweighted Graph

```python
V, E = 100000, 6000000
T = GraphGenerator(V, E)
G = GraphConverter(T, V, E, returnType="dict", weighted=False)

Dijkstra(G, V, 1)
BFS(G, V, 1)
```

|Algorithm|Time Complexity|Time(s)|
|------|---|---|
|Dijkstra|$O(V+ElogE)$|17.22|
|BFS|$O(V+E)$|2.26|

### Weighted Graph

```python
V, E = 20000, 300000
T = GraphGenerator(V, E)
G = GraphConverter(T, V, E, returnType="dict")

Dijkstra(G, V, 1)
BellmanFord(G, V, 1)
```

|Algorithm|Time Compelxity|Time(s)|
|------|---|---|
|Dijkstra|$O(V+ElogE)$|0.35|
|Bellman-Ford|$O(VE)$|1.63|

### Many-to-many

```python
V, E = 500, 2500
T = GraphGenerator(V, E)
G = GraphConverter(T, V, E, returnType="dict")
M = GraphConverter(T, V, E, returnType="matrix")

for v in range(1, V+1): 
    Dijkstra(G, V, v)
for v in range(1, V+1):
    BellmanFord(G, V, v)
Floyd(M, V)
```

|Algorithm|Time Complexity|Time(s)|
|------|---|---|
|Dijkstra|$O(V^2 + VElogE)$|0.74|
|Bellman-Ford|$O(V^2E)$|2.70|
|Floyd-Warshall|$O(V^3)$|42.17|
|Bellman-Ford w/o early-stopping|$O(V^2E)$|236.96|

- Early stopping (when there is no more update) in Bellman-Ford algorithm makes it faster than Floyd-Warshall, yet Bellman-Ford algorithm's time complexity for worst case is bigger than Floyd's.

### E > V^2

```python
V, E = 100, 100000
T = GraphGenerator(V, E)
G = GraphConverter(T, V, E, returnType="dict")
M = GraphConverter(T, V, E, returnType="matrix")

for v in range(1, V+1): 
    Dijkstra(G, V, v)
for v in range(1, V+1):
    BellmanFord(G, V, v)
Floyd(M, V)
```

|Algorithm|Time Complexity|Time(s)|
|------|---|---|
|Dijkstra|$O(V^2 + VElogE)$|24.18|
|Bellman-Ford|$O(V^2E)$|15.26|
|Floyd-Warshall|$O(V^3)$|0.32|
|Dijkstra w/ matrix|$O(V^4)$|0.97|
|Bellman-Ford w/ matrix|$O(V^4)$|0.77|

* w/ matrix: limit the number of edges to $V^2$ by only choosing the minimum distance between two nodes.

### Algorithm Comparison

|Weighted|Signed|$E>V^2$|Best Algorithm|
|------|---|---|---|
|X|X|X|BFS|
|O|X|X|Dijkstra|
|O|O|X|Bellman-Ford|
|O|O|O|Floyd-Warshall|

## Memo

- 위 실험의 결과에 따라 각 문제들은 다음 알고리즘으로 해결하는 것이 가장 효율적이다.

|Problem|V|E|Weighted|Signed|Best Algorithm|
|-------|-|-|--------|------|--------------|
|[BaekJoon 1753 Shortest Path](https://www.acmicpc.net/problem/1753)|20000|300000|O|X|Dijkstra|
|[BaekJoon 1865 Wormhole](https://www.acmicpc.net/problem/1865)|500|5200|O|O|Bellman-Ford|
|[BaekJoon 11404 Floyd](https://www.acmicpc.net/problem/11404)|100|100000|O|X|Floyd-Warshall|

- [1865번 웜홀](https://www.acmicpc.net/problem/1865) 은 정석적인 Bellman-Ford 방식으로 풀면 Python3으로는 통과하지 못함 (94% TOE)
  
  Pypy3으로는 AC ([Code](https://github.com/Kohgeonho/Wormhole/blob/main/sol2.py))
  
  Bellman-Ford의 한계(negative cycle이 있으면 안된다)를 이용하면 $O(VE)$로 해결가능 ([Code](https://github.com/Kohgeonho/Wormhole/blob/main/sol.py))
  
  애초에 이 문제는 shortest distance가 아닌 negative cycle의 유무에 집중하기 때문 ([link](https://www.acmicpc.net/board/view/72995) 참고)
  
- Class4에서 가장 어려웠고 배울점이 많았던 문제

  ![image](https://user-images.githubusercontent.com/62281102/214366849-74780068-6d20-403a-a0d5-21eab59c72aa.png)

  
