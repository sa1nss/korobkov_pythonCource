def find_negative_row_sums(matrix):

    negative_row_sums = []
    for row in matrix:
        if any(x < 0 for x in row):  # Check if the row contains a negative element
            negative_row_sums.append(sum(row))  # Add the sum of the row to the list
    return negative_row_sums


def find_saddle_points(matrix):
   
    saddle_points = []
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    # Find the minimum element in each row
    min_in_rows = [min(row) for row in matrix]

    # Find the maximum element in each column
    max_in_cols = [
        max(matrix[row][col] for row in range(num_rows)) 
        for col in range(num_cols)
    ]

    # Check each cell for being a saddle point
    for i in range(num_rows):
        for j in range(num_cols):
            if matrix[i][j] == min_in_rows[i] and matrix[i][j] == max_in_cols[j]:
                saddle_points.append((i, j))  # Add the coordinates of the saddle point

    return saddle_points


# Main execution block
if __name__ == "__main__":
    # Example input matrix
    matrix = [
        [3, -2, 5],
        [1, 4, 6],
        [-1, 8, 9]
    ]

    # Display the matrix
    print("Matrix:")
    for row in matrix:
        print(row)

    # Part 1: Sum of elements in rows containing at least one negative element
    negative_row_sums = find_negative_row_sums(matrix)
    print("\nSums of elements in rows containing at least one negative element:")
    print(negative_row_sums, end="\n\n")

    # Part 2: Finding saddle points
    saddle_points = find_saddle_points(matrix)
    print("Coordinates of saddle points (row and column indices):")
    if saddle_points:
        for point in saddle_points:
            print(f"Saddle point found at row {point[0]}, column {point[1]}", end="\n")
    else:
        print("No saddle points found.", end="\n")
        