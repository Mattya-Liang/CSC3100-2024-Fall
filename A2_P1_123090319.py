n = int(input())
sequence = list(map(int, input().split()))

count = {i: 0 for i in range(0, n + 1)}
positions = {i: [] for i in range(0, n + 1)}

for idx, num in enumerate(sequence):
    if num in count:
        count[num] += 1
        positions[num].append(idx)

def minimum_number_of_elements(n, sequence):

    deletions = 0
    processed_numbers = set()
    count_zero_numbers = [i for i in range(1, n + 1) 
                           if count[i] == 0]
   

    for deleted_numbers in count_zero_numbers:
        deleted_number = sequence[deleted_numbers - 1]
        processed_numbers.add(deleted_numbers)
        count[deleted_number] -= 1
        sequence[deleted_numbers - 1] = 0
        deletions += 1
        if count[deleted_number] == 0:
            count_zero_numbers.append(deleted_number)

    if not count_zero_numbers:
        return deletions

    return deletions    

print((minimum_number_of_elements(n, sequence)))