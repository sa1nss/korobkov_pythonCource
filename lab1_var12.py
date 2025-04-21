def compact_matrix(matrix):
    filtered_rows = [row for row in matrix if any(row)]
    
    num_cols = len(filtered_rows[0]) if filtered_rows else 0
    non_zero_columns = [i for i in range(num_cols) if any(row[i] != 0 for row in filtered_rows)]
    
    compacted_matrix = [[row[i] for i in non_zero_columns] for row in filtered_rows]
    
    return compacted_matrix


def find_first_positive_row(matrix):
    for idx, row in enumerate(matrix):
        if any(x > 0 for x in row):
            return idx + 1 
    return None  


matrix = [
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 0],
    [0, -2, 3, 0],
    [0, 0, 0, 0]
]

compacted_matrix = compact_matrix(matrix)

first_positive_row = find_first_positive_row(compacted_matrix)

print("Compacted matrix:")
for row in compacted_matrix:
    print(row)

print("\nNumber of the first line with a positive element:", first_positive_row)