import sys
from itertools import chain
from collections import defaultdict

monitor = True

def input_single(dtype=int):
    return dtype(sys.stdin.readline().strip())

def input_list(dtype=int):
    return [dtype(i) for i in sys.stdin.readline().strip().split()]

def BellmanFord(G, V, src, DMAX=10000001):
    D = [DMAX] * (V + 1)
    D[src] = 0

    update = True

    for _ in range(V+1):
        if not update:
            break
        update = False
        for s, dist, d in chain((s, dist, d) for s in G for dist, d in G[s]):
            if D[s] < DMAX and D[s] + dist < D[d]:
                update = True 
                D[d] = D[s] + dist
    
    return update

for tc in range(input_single()):
    N, M, W = input_list()
    WMAX = 5000001
    G = defaultdict(list)
    A = False

    G[0] = [(0, s) for s in range(1, N+1)]

    for _ in range(M):
        s, d, w = input_list()
        G[s].append((w, d))
        G[d].append((w, s))

    for _ in range(W):
        s, d, w = input_list()
        G[s].append((-w, d))

    A = BellmanFord(G, N, 0, DMAX=WMAX)

    print("YES" if A else "NO")