import numpy as np

from heapq import heappush, heappop
from itertools import chain
from collections import deque, defaultdict
from tqdm import tqdm

def GraphGenerator(V, E, DMAX=200, signed=False, weighted=True):
    weights = np.random.choice(DMAX, E)
    nodes = np.random.choice(V-1, 3*E)
    nodes = [(u, v) for u, v in zip(nodes[::2], nodes[1::2]) if u != v]
    if signed:
        weights = map(lambda x: x - (DMAX >> 4), weights)
    
    if weighted:
        return [
            (u, v, w)
            for (u, v), w in tqdm(zip(nodes, weights))
        ]
    else:
        return [
            (*nodes[i], 1)
            for i in range(V)
        ]

def GraphConverter(T, V, E, returnType="dict", inType="tuple", weighted=True, INF=10000001):
    
    if inType == "tuple":
        if returnType == "dict":
            G = defaultdict(list)
            for src, dst, dist in T:
                G[src].append((dist, dst))

            return G
        
        elif returnType == "matrix":
            G = [[INF] * V for _ in range(V)]
            for src, dst, dist in T:
                G[src-1][dst-1] = min(dist, G[src-1][dst-1])

            return G

    elif inType == "matrix":
        if returnType == "dict":
            G = defaultdict(list)
            for src in range(V):
                for dst in range(V):
                    G[src].append((T[src][dst], dst))

            return G

def Dijkstra(G, V, src, Gtype="dict", DMAX=10000001):
    D = [DMAX] * (V + 1)
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

def BFS(G, V, src, Gtype="dict"):
    D = [-1] * (V + 1)
    D[src] = 0
    Q = deque([(src, 0)])

    while Q:
        src, d = Q.popleft()
        for _, dst in G[src]:
            if D[dst] < 0:
                D[dst] = d + 1
                Q.append((dst, d+1))

    return D

def Floyd(G, V, Gtype="matrix", display=False):
    N = V
    for n in range(N):
        for i in range(N):
            for j in range(N):
                if i != n and j != n:
                    G[i][j] = min(G[i][j], G[i][n] + G[n][j])

    return G