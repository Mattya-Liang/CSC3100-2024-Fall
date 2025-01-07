n, m, P = map(int, input().split())
sequence = list(map(int, input().split()))

positive_count = {}
include_zero = 0
current_sum = sum(sequence)
distinct_values = 0 

for number in sequence:
    abs_number = abs(number)
    if number == 0:
        include_zero += 1
    else:
        if abs_number in positive_count:
            positive_count[abs_number] += 1
        else:
            positive_count[abs_number] = 1

for value, count in positive_count.items():
        if count == 1 and value != 0:
            distinct_values += 1
        elif count >= 2 and value != 0:
            distinct_values += 2

def update(k, x, y, c):
    global current_sum, positive_count, include_zero, distinct_values

    new_value = ((x**2 + k*y + 5*x) % P) * c
    old_value = sequence[k-1]
    sequence[k-1] = new_value
    
    current_sum += new_value - old_value

    old_abs = abs(old_value)
    new_abs = abs(new_value)

    if old_value == 0:
        include_zero -= 1
    else:
        positive_count[old_abs] -= 1
        if positive_count[old_abs] == 0:
            del positive_count[old_abs]
            distinct_values -= 1

    if new_value == 0:
        include_zero += 1
    else:
        if new_abs in positive_count:
            positive_count[new_abs] += 1
            if positive_count[new_abs] == 2:
                distinct_values += 1
        else:
            positive_count[new_abs] = 1
            distinct_values += 1

def query_sum():
    global current_sum
    print(current_sum)

def sum_query_distinct():
    global distinct_values, include_zero
    print(distinct_values + (1 if include_zero > 0 else 0))

for _ in range(m):
    operation = list(map(int, input().split()))
    if operation[0] == 1:
        _, k, x, y, c = operation
        update(k, x, y, c)
    elif operation[0] == 2:
        query_sum()
    elif operation[0] == 3:
        sum_query_distinct()
