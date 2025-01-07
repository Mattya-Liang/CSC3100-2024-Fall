class MaxHeap:
    def __init__(self):
        self.heap = []
        self.pos = {}
        
    def size(self):
        return len(self.heap)
    
    def swap(self, i, j):
        self.pos[self.heap[i][1]] = j
        self.pos[self.heap[j][1]] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def push(self, item):
        self.heap.append(item)
        self.pos[item[1]] = len(self.heap) - 1
        self._sift_up(len(self.heap) - 1)
    
    def pop(self):
        if not self.heap:
            return None
        
        self.swap(0, len(self.heap) - 1)
        item = self.heap.pop()
        del self.pos[item[1]]
        
        if self.heap:
            self._sift_down(0)
        
        return item
    
    def update(self, node, new_value):
        if node not in self.pos:
            self.push((new_value, node))
            return
        
        idx = self.pos[node]
        old_value = self.heap[idx][0]
        self.heap[idx] = (new_value, node)
        
        if new_value > old_value:
            self._sift_up(idx)
        else:
            self._sift_down(idx)
    
    def _sift_up(self, idx):
        parent = (idx - 1) // 2
        while idx > 0 and self.heap[parent][0] < self.heap[idx][0]:
            self.swap(parent, idx)
            idx = parent
            parent = (idx - 1) // 2
    
    def _sift_down(self, idx):
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            
            if left < len(self.heap) and self.heap[left][0] > self.heap[largest][0]:
                largest = left
            if right < len(self.heap) and self.heap[right][0] > self.heap[largest][0]:
                largest = right
                
            if largest == idx:
                break
                
            self.swap(idx, largest)
            idx = largest

def dijkstra_with_heap(graph, start, end):
    max_heap = MaxHeap()
    max_min_values = {node: float('-inf') for node in graph}
    max_min_values[start] = float('inf')
    
    max_heap.push((float('inf'), start))
    
    while max_heap.size() > 0:
        curr_min_value, curr_node = max_heap.pop()
        
        if curr_node == end:
            return curr_min_value
        
        if curr_min_value < max_min_values[curr_node]:
            continue
        
        for next_node, weight in graph[curr_node].items():
            path_min = min(curr_min_value, weight)
            
            if path_min > max_min_values[next_node]:
                max_min_values[next_node] = path_min
                max_heap.update(next_node, path_min)
    
    return max_min_values[end]

n, m = map(int, input().split())
graph = {}
initial_edges = set()

for i in range(m):
    u, v, w = map(int, input().split())
    if u not in graph:
        graph[u] = {}
    if v not in graph:
        graph[v] = {}
    graph[u][v] = w
    graph[v][u] = w
    initial_edges.add(frozenset([u, v]))

q = int(input())

updates = []
for _ in range(q):
    ki = int(input())
    day_changes = []
    for _ in range(ki):
        a, b, c = map(int, input().split())
        day_changes.append((a, b, c))
    updates.append(day_changes)

queries = []
for _ in range(q + 1):
    si, ti = map(int, input().split())
    queries.append((si, ti))

for day in range(q + 1):
    if day > 0:
        for (a, b, c) in updates[day - 1]:
            if frozenset([a, b]) in initial_edges:
                if a not in graph:
                    graph[a] = {}
                if b not in graph:
                    graph[b] = {}
                graph[a][b] = c
                graph[b][a] = c

    si, ti = queries[day]

    if si not in graph or ti not in graph:
        print(-1)
        continue
        
    result = dijkstra_with_heap(graph, si, ti)
    print(result)