def count_non_zero_columns(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    count = 0

    for col in range(cols):
        has_zero = False
        for row in range(rows):
            if matrix[row][col] == 0:
                has_zero = True
                break
        if not has_zero:
            count += 1

    return count


def sort_rows_by_characteristic(matrix):
    def characteristic(row):
        return sum(x for x in row if x > 0 and x % 2 == 0)

    sorted_matrix = sorted(matrix, key=characteristic)
    return sorted_matrix


if __name__ == "__main__":
    matrix = [
        [2, 4, 0],
        [6, 0, 8],
        [1, 2, 3],
        [0, 5, 7]
    ]

    non_zero_columns_count = count_non_zero_columns(matrix)
    print("Number of columns without null elements:", non_zero_columns_count)

    sorted_matrix = sort_rows_by_characteristic(matrix)
    print("Matrix after sorting rows:")
    for row in sorted_matrix:
        print(row)