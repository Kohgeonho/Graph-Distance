import sys
from itertools import chain
from collections import defaultdict

monitor = True

def input_single(dtype=int):
    return dtype(sys.stdin.readline().strip())

def input_list(dtype=int):
    return [dtype(i) for i in sys.stdin.readline().strip().split()]

def BellmanFord(G, V, src, DMAX=10000001):
    '''
    While updating distances, if there is no updates, it means there is no negative cycles 
    containing node src. If some point, distances from src to src is smaller than 0, 
    it means that we found negative cycle.
    '''
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

        if D[src] < 0:
            return True 
    
    return False

for tc in range(input_single()):
    N, M, W = input_list()
    WMAX = 5000001
    G = defaultdict(list)
    A = False

    for _ in range(M):
        s, d, w = input_list()
        G[s].append((w, d))
        G[d].append((w, s))

    for _ in range(W):
        s, d, w = input_list()
        G[s].append((-w, d))

    '''It should be done for every node.'''
    for v in range(1, N+1):
        if BellmanFord(G, N, v, DMAX=WMAX):
            A = True
            break

    print("YES" if A else "NO")