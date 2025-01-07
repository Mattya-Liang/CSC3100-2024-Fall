n, q = map(int, input().split())
permutation = list(map(int, input().split()))
l_values = list(map(int, input().split()))
r_values = list(map(int, input().split()))

def valid_permutation(n, q, permutation, l_values, r_values):
    array_values_position = {}
    for idx, value in enumerate(permutation):
        if value not in array_values_position:
            array_values_position[value] = []
        array_values_position[value].append(idx)

    if (l_values[0] not in array_values_position or 
        r_values[0] not in array_values_position or 
        array_values_position[l_values[0]][0] != 0 or 
        array_values_position[r_values[0]][-1] != n - 1):
        return 0

    for i in range(0, q):
        if l_values[i] not in array_values_position or r_values[i] not in array_values_position:
            return 0
        
        l_values_min_position = min(array_values_position[l_values[i]]) 
        r_values_max_position = max(array_values_position[r_values[i]])
        
        if r_values_max_position - l_values_min_position > 0:
            continue
        else:
            return 0

    return 1

print(valid_permutation(n, q, permutation, l_values, r_values))
