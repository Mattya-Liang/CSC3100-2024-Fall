def calculate_time_complexity():
    t = int(input().strip())
    total_complexities = []

    for _ in range(t):
        invalid = None
        used_variables = set()
        stack = []
        rencent_complexity = program_complexity = 0

        l = int(input().strip())

        for _ in range(l):
            line = input().strip().split()
            form = line[0]

            if form == 'F':
                variable, x, y = line[1], line[2], line[3]

                if variable in used_variables:
                    continue

                used_variables.add(variable)
                x_num = -1 if x == 'n' else int(x)
                y_num = -1 if y == 'n' else int(y)

                stack.append((variable, x_num, y_num))

                if ((x_num == -1 and y_num != -1) or 
                    (x_num != -1 and y_num != -1 and x_num > y_num)) and invalid is None:
                    invalid = variable

                if invalid is not None:
                    continue

                if y_num == -1 and x_num != -1:
                    rencent_complexity += 1

            elif form == 'E':
                if not stack:
                    continue

                variable, x_num, y_num = stack.pop()
                used_variables.remove(variable)

                if variable == invalid:
                    invalid = None

                if invalid is not None:
                    continue

                program_complexity = max(program_complexity, rencent_complexity)

                if y_num == -1 and x_num != -1:
                    rencent_complexity -= 1

        total_complexities.append(f"O(n^{program_complexity})" if program_complexity > 0 else "O(1)")

    for complexity in total_complexities:
        print(complexity)

calculate_time_complexity()