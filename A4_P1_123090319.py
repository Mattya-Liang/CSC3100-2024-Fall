class MinHeap:
    def __init__(self):
        self.heap = []
        self.node_pos = {}
    
    def push(self, dist, node):
        self.heap.append((dist, node))
        self.node_pos[node] = len(self.heap) - 1
        self._heapify_up(len(self.heap) - 1)
    
    def pop(self):
        if len(self.heap) == 0:
            return None
        min_node = self.heap[0]
        last_node = self.heap.pop()
        if len(self.heap) > 0:
            self.heap[0] = last_node
            self.node_pos[last_node[1]] = 0
            self._heapify_down(0)
        del self.node_pos[min_node[1]]
        return min_node
    
    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index][0] < self.heap[parent][0]:
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                self.node_pos[self.heap[index][1]] = index
                self.node_pos[self.heap[parent][1]] = parent
                index = parent
            else:
                break
    
    def _heapify_down(self, index):
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        smallest = index
        
        if left_child < len(self.heap) and self.heap[left_child][0] < self.heap[smallest][0]:
            smallest = left_child
        if right_child < len(self.heap) and self.heap[right_child][0] < self.heap[smallest][0]:
            smallest = right_child
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.node_pos[self.heap[index][1]] = index
            self.node_pos[self.heap[smallest][1]] = smallest
            self._heapify_down(smallest)
    
    def update(self, dist, node):
        if node not in self.node_pos:
            self.push(dist, node)
        else:
            index = self.node_pos[node]
            self.heap[index] = (dist, node)
            self._heapify_up(index)

def dijkstra_algorithm(graph, s, n):
    dist = [float('inf')] * (n + 1)
    dist[s] = 0
    visited = [False] * (n + 1)
    
    min_heap = MinHeap()
    min_heap.push(0, s)
    
    while len(min_heap.heap) > 0:
        min_dist, u = min_heap.pop()
        
        if visited[u]:
            continue
        
        visited[u] = True
        
        for v, w in graph[u]:
            if not visited[v]:
                new_dist = dist[u] + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    min_heap.update(dist[v], v)
    
    return dist

def build_edge_info(graph, must_pass_edges, n):
    edge_info = {}
    must_pass_edges_map = {}
    
    for idx, (u, v) in enumerate(must_pass_edges):
        must_pass_edges_map[frozenset((u, v))] = idx
    
    for u in range(1, n + 1):
        for v, w in graph[u]:
            edge_key = frozenset((u, v))
            if edge_key in must_pass_edges_map:
                edge_num = must_pass_edges_map[edge_key]
                edge_info[(u, v)] = (w, edge_num)
                edge_info[(v, u)] = (w, edge_num)
    return edge_info

def find_shortest_path(graph, start, end, must_pass_edges, n):
    dijkstra_cache = {}
    path_cache = set()  
    
    def get_dijkstra_result(source):
        if source not in dijkstra_cache:
            dijkstra_cache[source] = dijkstra_algorithm(graph, source, n)
        return dijkstra_cache[source]

    def create_state(curr, used_edges):
        return (curr, frozenset(used_edges))

    def dfs_path(curr, total_dist, used_edges, edge_info, must_pass_edges, best_dist, recent_min, curr_path):
        if total_dist >= recent_min[0]:
            return float('inf')

        current_state = create_state(curr, used_edges)
        if current_state in path_cache:
            return float('inf')
        path_cache.add(current_state)

        if curr in curr_path and len(used_edges) < len(must_pass_edges):
            path_cache.remove(current_state)
            return float('inf')

        if len(used_edges) == len(must_pass_edges):
            end_dist = get_dijkstra_result(curr)
            if end_dist[end] != float('inf'):
                total_path_dist = total_dist + end_dist[end]
                if total_path_dist < best_dist[0]:
                    best_dist[0] = total_path_dist
                    recent_min[0] = total_path_dist
                path_cache.remove(current_state)
                return total_path_dist
            path_cache.remove(current_state)
            return float('inf')

        remaining_edges = set(range(len(must_pass_edges))) - used_edges
        if remaining_edges:
            min_remaining_dist = float('inf')
            curr_dist = get_dijkstra_result(curr)
            
            for u in range(1, n + 1):
                for v, w in graph[u]:
                    if (u, v) in edge_info and edge_info[(u, v)][1] in remaining_edges:
                        if curr_dist[u] != float('inf'):
                            min_remaining_dist = min(min_remaining_dist, curr_dist[u])

            if total_dist + min_remaining_dist >= recent_min[0]:
                path_cache.remove(current_state)
                return float('inf')

        min_dist = float('inf')
        curr_dist = get_dijkstra_result(curr)
        
        curr_path.add(curr)
        
        for u in range(1, n + 1):
            for v, w in graph[u]:
                if (u, v) in edge_info and edge_info[(u, v)][1] not in used_edges:
                    edge_num = edge_info[(u, v)][1]
                    used_edges.add(edge_num)
                    if curr_dist[u] != float('inf'):
                        new_dist = total_dist + curr_dist[u] + w
                        result = dfs_path(v, new_dist, used_edges, edge_info, 
                                        must_pass_edges, best_dist, recent_min, curr_path)
                        min_dist = min(min_dist, result)
                    used_edges.remove(edge_num)

        curr_path.remove(curr)
        path_cache.remove(current_state)
        return min_dist

    edge_info = build_edge_info(graph, must_pass_edges, n)
    used_edges = set()
    best_dist = [float('inf')]
    recent_min = [float('inf')]
    curr_path = set()
    
    min_dist = dfs_path(start, 0, used_edges, edge_info, must_pass_edges, best_dist, recent_min, curr_path)
    return min_dist if min_dist != float('inf') else -1

n, m, q = map(int, input().split())
edges = []
graph = [[] for _ in range(n + 1)]

for i in range(m):
    u, v, w = map(int, input().split())
    edges.append((u, v, w))
    graph[u].append((v, w))
    graph[v].append((u, w))

must_pass_edges_groups = []
for _ in range(q):
    k = int(input())
    edge_indices = list(map(int, input().split()))
    must_pass_edges = []
    for idx in edge_indices:
        u, v, _ = edges[idx - 1]
        must_pass_edges.append((u, v))
    must_pass_edges_groups.append(must_pass_edges)

for i in range(q):
    start, end = map(int, input().split())
    result = find_shortest_path(graph, start, end, must_pass_edges_groups[i], n)
    print(result)