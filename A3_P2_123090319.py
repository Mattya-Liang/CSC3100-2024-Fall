n, k, bag_size = map(int, input().split())
items = []
for _ in range(n):
    id_i, value_i = input().split()
    id_i = int(id_i)
    value_i = float(value_i)
    shelf_num = id_i % k
    items.append((shelf_num, id_i, value_i))

def assign_to_shelves(items, k):
    shelves = {}

    for i in range(k):
        shelves[i] = []
    
    for shelf_num, item_id, value in items:
        shelves[shelf_num].append((shelf_num, item_id, value))
    
    shelves_list = []
    for i in range(k):
        if shelves[i]:
            sorted_shelf_items = sorted(shelves[i], key=lambda x: -x[1])
            shelves_list.extend(sorted_shelf_items)
        else:
            shelves_list.append((i, 0, 0.0))
            
    while shelves_list and shelves_list[0][1] == 0:
        shelves_list.pop(0)
    while shelves_list and shelves_list[-1][1] == 0:
        shelves_list.pop()
    print(shelves_list)
    return shelves_list

def max_value_from_shelves(shelves_list, bag_size, n):
    if not shelves_list:
        return 0.0
        
    max_value = 0.0
    
    for current_size in range(min(bag_size, n), 0, -1):
        left_side = 0
        right_side = current_size - 1
        
        current_value = 0.0
        shelf_counts = {}
        empty_count = 0
        
        for i in range(current_size):
            idx = (left_side + i) % n
            shelf = shelves_list[idx]
            if shelf[1] == 0:
                empty_count += 1
            else:
                current_value += shelf[2]
                shelf_id = shelf[0]
                shelf_counts[shelf_id] = shelf_counts.get(shelf_id, 0) + 1
        
        if empty_count <= 1 and is_valid_combination(shelf_counts):
            max_value = max(max_value, current_value)
        
        for _ in range(n):
            left_idx = left_side % n
            left_shelf = shelves_list[left_idx]
            if left_shelf[1] != 0:
                current_value -= left_shelf[2]
                shelf_id = left_shelf[0]
                shelf_counts[shelf_id] -= 1
                if shelf_counts[shelf_id] == 0:
                    del shelf_counts[shelf_id]
            elif empty_count > 0:
                empty_count -= 1
                
            right_idx = (right_side + 1) % n
            right_shelf = shelves_list[right_idx]
            if right_shelf[1] != 0:
                current_value += right_shelf[2]
                shelf_id = right_shelf[0]
                shelf_counts[shelf_id] = shelf_counts.get(shelf_id, 0) + 1
            else:
                empty_count += 1
            
            left_side = (left_side + 1) % n
            right_side = (right_side + 1) % n
            
            if empty_count <= 1 and is_valid_combination(shelf_counts):
                max_value = max(max_value, current_value)
    
    return max_value

def is_valid_combination(shelf_counts):
    if not shelf_counts:
        return True
    values = list(shelf_counts.values())
    return len(values) == len(set(values))

shelves_list = assign_to_shelves(items, k)
result = round(max_value_from_shelves(shelves_list, bag_size, n), 1)
print(result)