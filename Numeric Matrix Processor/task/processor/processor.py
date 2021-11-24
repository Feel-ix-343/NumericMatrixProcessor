import math
from typing import List


class Matrix:
    def __init__(self, rows: int, columns: int, matrix):
        self.rows = rows
        self.columns = columns
        self.matrix = matrix


class MatrixFunctions:
    ERROR = "The operation cannot be performed"

    def __init__(self, working_matrix: Matrix):
        self.working_matrix = working_matrix

    def add(self, operation_matrix: Matrix):
        is_same_rows: bool = self.working_matrix.rows == operation_matrix.rows
        is_same_columns: bool = self.working_matrix.columns == operation_matrix.columns

        if is_same_rows and is_same_columns:
            for i in range(self.working_matrix.rows):
                for x in range(self.working_matrix.columns):
                    self.working_matrix.matrix[i][x] += operation_matrix.matrix[i][x]
        else:
            self.error()

    def multiply_by_constant(self, constant):
        for i in range(self.working_matrix.rows):
            self.working_matrix.matrix[i] = map(lambda x: x * constant, self.working_matrix.matrix[i])

    def multiply_by_matrix(self, operation_matrix: Matrix):
        if self.working_matrix.columns == operation_matrix.rows:
            place_holder = [[] for _ in range(self.working_matrix.rows)]
            for i in range(self.working_matrix.rows):
                for x in range(operation_matrix.columns):
                    sum_ = 0
                    for y in range(self.working_matrix.columns):
                        sum_ += self.working_matrix.matrix[i][y] * operation_matrix.matrix[y][x]
                    place_holder[i].append(sum_)
            self.working_matrix.matrix = place_holder
        else:
            self.error()

    def transpose(self, operation_num):
        place_holder = []
        if operation_num == 1:
            for x in range(self.working_matrix.columns):
                place_holder.append([])
                for y in range(self.working_matrix.rows):
                    place_holder[x].append(self.working_matrix.matrix[y][x])
            self.working_matrix.matrix = place_holder
        elif operation_num == 2:
            for x in range(self.working_matrix.columns)[::-1]:
                place_holder.append([])
                for y in range(self.working_matrix.rows)[::-1]:
                    place_holder[self.working_matrix.columns - x - 1].append(self.working_matrix.matrix[y][x])
            self.working_matrix.matrix = place_holder
        elif operation_num == 3:
            for i in range(self.working_matrix.rows):
                self.working_matrix.matrix[i] = self.working_matrix.matrix[i][::-1]
        elif operation_num == 4:
            self.working_matrix.matrix = self.working_matrix.matrix[::-1]

    def calc_determinant(self, rec_mat=None):
        rec_mat = self.working_matrix.matrix if rec_mat is None else rec_mat
        rows = len(rec_mat[0])
        total = 0
        if rows > 2:
            for i in range(rows):               # I know
                    total += math.pow(-1, 1 + (i + 1)) * rec_mat[0][i] * self.calc_determinant(list(map(lambda row: row[:i] + row[i + 1:], rec_mat[1:])))
            return total
        elif rows == 1:
            return rec_mat[0][0]
        else:
            return rec_mat[0][0] * rec_mat[1][1] - rec_mat[0][1] * rec_mat[1][0]

    def calc_inverse(self):
        matrix = self.working_matrix.matrix
        determinant = self.calc_determinant(matrix)
        if determinant == 0:
            print("This matrix doesn't have an inverse.")
            run()
        cofactors = []
        for i in range(self.working_matrix.rows):
            cofactors.append([])
            for x in range(self.working_matrix.columns):
               cofactors[i].append(math.pow(-1, x + i + 2) * self.calc_determinant(list(map(lambda row: row[:x] + row[x + 1:],
                                                                matrix[:i] + matrix[i + 1:]))))

        o = MatrixFunctions(Matrix(len(cofactors), len(cofactors[0]), cofactors))
        o.transpose(1)
        o.multiply_by_constant(1 / determinant)

        self.working_matrix = o.working_matrix

    def print_matrix(self):
        for row in self.working_matrix.matrix:
            print(' '.join(map(str, row)))

    def error(self):
        print(self.ERROR, "\n")
        run()


class GetInputs:
    def __init__(self, type_):
        self.values = []
        self.RESULT = "The result is:"
        self.type_ = type_
        if type_ == 1 or type_ == 3:
            self.n_of_matrices = 2
            self.MESSAGE = ["Enter size of first matrix: ", "Enter size of second matrix: "]
            self.MESSAGE2 = ["Enter first matrix:", "Enter second matrix:"]
        elif type_ == 2 or type_ == 5 or type_ == 6:
            self.n_of_matrices = 1
            self.MESSAGE = ["Enter size of matrix: "]
            self.MESSAGE2 = ["Enter matrix:"]
            self.MESSAGE3 = "Enter constant: "
        elif type_ == 4:
            self.n_of_matrices = 1
            self.MESSAGE = ["Enter size of matrix: "]
            self.MESSAGE2 = ["Enter matrix:"]
            self.MESSAGE3 = '\n'.join(["1. Main diagonal",
                                       "2. Side diagonal",
                                       "3. Vertical line",
                                       "4. Horizontal line",
                                       "Your choice: "])

    def get_input(self):
        if self.type_ == 4:
            self.values.append(int(input(self.MESSAGE3)))
        for i in range(self.n_of_matrices):
            rows, columns = map(int, input(self.MESSAGE[i]).split())
            print(self.MESSAGE2[i])
            matrix = [list(map(lambda x: float(x) if '.' in x else int(x), input().split())) for _ in range(rows)]
            self.values.append(Matrix(rows, columns, matrix))

        if self.type_ == 2:
            self.values.append((lambda x: float(x) if '.' in x else int(x))(input(self.MESSAGE3)))


def run():
    print("1. Add matrices\n"
          "2. Multiple matrix by a constant\n"
          "3. Multiply matrices\n"
          "4. Transpose matrix\n"
          "5. Calculate a determinant\n"
          "6. Inverse matrix\n"
          "0. Exit")
    input_ = int(input("Your choice: "))

    if input_ == 1:
        input_ = GetInputs(input_)
        input_.get_input()
        o = MatrixFunctions(input_.values[0])
        o.add(input_.values[1])
        print(input_.RESULT)
        o.print_matrix()
        run()
    elif input_ == 2:
        input_ = GetInputs(input_)
        input_.get_input()
        o = MatrixFunctions(input_.values[0])
        o.multiply_by_constant(input_.values[1])
        print(input_.RESULT)
        o.print_matrix()
        run()
    elif input_ == 3:
        input_ = GetInputs(input_)
        input_.get_input()
        o = MatrixFunctions(input_.values[0])
        o.multiply_by_matrix(input_.values[1])
        print(input_.RESULT)
        o.print_matrix()
        run()
    elif input_ == 4:
        input_ = GetInputs(input_)
        input_.get_input()
        o = MatrixFunctions(input_.values[1])
        o.transpose(input_.values[0])
        print(input_.RESULT)
        o.print_matrix()
        run()
    elif input_ == 5:
        input_ = GetInputs(input_)
        input_.get_input()
        o = MatrixFunctions(input_.values[0])
        print(input_.RESULT)
        print(o.calc_determinant())
    elif input_ == 6:
        input_ = GetInputs(input_)
        input_.get_input()
        o = MatrixFunctions(input_.values[0])
        print(input_.RESULT)
        o.calc_inverse()
        o.print_matrix()
    elif input_ == 0:
        quit()


if __name__ == '__main__':
    run()
