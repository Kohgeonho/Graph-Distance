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
  
  - Time Complexity: O(VE)
  
  - Python code

```python
from itertools import chain

def BellmanFord(G, src, Gtype="dict", DMAX=10000001):
    D = [DMAX] * (len(G) + 1)
    D[src] = 0
    update = True

    while update > 0:
        update = False
        for s, dist, d in chain((s, dist, d) for s in G for dist, d in G[s]):
            if D[s] + dist < D[d]:
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

