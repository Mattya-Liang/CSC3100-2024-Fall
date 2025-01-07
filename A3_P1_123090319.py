n, m, t = map(int, input().split())
edges = []

for _ in range(m):
    u, v, w = map(int, input().split())
    edges.append((u, v, w))

def minimum_health_point(n, m, t, edges):

    tree = {}
    for u, v, w in edges:
        if u not in tree:
            tree[u] = []
        if v not in tree:
            tree[v] = []
        tree[u].append((v, w))
        tree[v].append((u, w))

    def bfs(start):
        remained_node = [(start, 0, 0)]
        visited_node = {start}
        min_hp = []

        while remained_node:
            node, mp, hp = remained_node.pop(0)
            is_leaf = True 

            for neighbor, w in tree[node]:
                if neighbor not in visited_node:
                    visited_node.add(neighbor)
                    is_leaf = False
                    new_mp = mp + 1
                    new_hp = hp + max(0, w - new_mp)
                    remained_node.append((neighbor, new_mp, new_hp))

            if is_leaf and (node != start or len(tree[node]) == 1):
                min_hp.append(hp)

        return max(min_hp) if min_hp else 0

    return bfs(t)

print(minimum_health_point(n, m, t, edges))