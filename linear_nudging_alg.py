from graphic_display import GraphicDisplay
# from matrix_nxn import Matrix_NxN # Not in use
import matplotlib.pyplot as plt
import numpy as np
import datetime
import math
import time
import sys
import os

# 3D Stuff
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class LinearNudgingAlg:
    def __init__(self, *args):
        self._eigenvalue_magnitudes = []
        self._nth_avg_abs_param_errors = []
        self._nth_avg_rel_param_errors = []
        self._param_list = args[3]

        self._matrix_case_type = ''
        self._abs_graph_display = GraphicDisplay("Absolute", self._matrix_case_type)
        self._rel_graph_display = GraphicDisplay("Relative", self._matrix_case_type)
        self.prepare_sim(args)

        # The code within this conditional should only work with 3 x 3 matricies.
        if args[0] == len(args[3]) == 3:
            ########### EV Magnitudes
            self._abs_graph_display.plot_ev_graph_html(self._eigenvalue_magnitudes, self._nth_avg_abs_param_errors)
            self._abs_graph_display.show_plot()
            self._rel_graph_display.plot_ev_graph_html(self._eigenvalue_magnitudes, self._nth_avg_rel_param_errors)
            self._rel_graph_display.show_plot()

    def create_n_x_m_matrix_list(self, n, m):
        matrix = [[[] for j in range(m)] for i in range(n)]
        return matrix

    def get_eigenvalue_magnitude(self, A):
        src_eigenvals = np.linalg.eigvals(A)
        ev_magnitudes = []

        for i in range(len(src_eigenvals)):
            if isinstance(src_eigenvals[i], complex):
                ev_magnitudes.append(math.sqrt((src_eigenvals[i].real) ** 2 + (src_eigenvals[i].imag) ** 2))
            else:
                ev_magnitudes.append(src_eigenvals[i])
        return ev_magnitudes



    def get_param_error(self, est_param, true_param):
        return est_param - true_param

    def get_abs_param_error(self, est_param, true_param):
        return abs(self.get_param_error(est_param, true_param))

    def get_rel_param_error(self, est_param, true_param):
        return abs(self.get_param_error(est_param, true_param) / true_param)

    def prepare_sim(self, args):
        if len(args) == 4:
            n, bound_value, total_matricies, matrix_case_type = args[0], args[1], args[2], args[3]
            self.init_sim(n, bound_value, total_matricies, matrix_case_type)

    def print_mtrx_stats(self, A):
        A.print_by_row()
        print("Eigenvalues:", A.get_eigenvalues(), "\n")
        print("Trace:", A.get_trace(), "\n")
        print("Determinant:", A.get_determinant(), "\n")

    def generate_matrix(self, n, bounds):   # Generates a random n x n matrix
      A = np.random.uniform(-bounds, bounds, [n, n])
      # A = np.array([[1, 2, 3], [4, 5, 6],  [7, 8, 9]] )   # Manual option
      return A

    def init_sim(self, n, bound_value, total_matricies, matrix_case_type):
        sim_time = 10 # Stop time
        dt = 0.001    # Time step
        t_span = (0, sim_time)  # For solve_ivp (not used)
        t = np.arange(0, sim_time, dt) # Evaluation times
        T_R = 0.5        # Relaxation period
        init_param_err = bound_value * 2
        nudging_param_value = 1000
        Mu = np.eye(n) * nudging_param_value

        for i in range(total_matricies):
            print("--------- MATRIX " + str(i) + " -------------------------------------------------------------", "\n")
            A = self.generate_matrix(n, bound_value)
            print(f"A = {A} \n")
            print(f"Eigenvalues = {np.linalg.eigvals(A)} \n")

            update_times_mtrx = np.empty((n, n), dtype = object)
            At = np.zeros((n, n), dtype = object)
            A_est = np.zeros((n, n), dtype = object)
            # Mu = np.eye(n) * nudging_param_value

            for j in range(n):
                for k in range(n):
                    update_times_mtrx[j, k] = np.array([0])

            # Add each element to the list
            for j in range(n):
                for k in range(n):
                    At[j, k] = A[j, k]
                    A_est[j, k] = np.array([At[j, k]])

            #Update the list based on the inputs
            for h in range(n):
                row, col = self.parse_matrix_parameter(self._param_list[h])
                for j in range(n):
                    for k in range(n):
                        if j == row and k == col:
                            At[j, k] = A[j, k] + init_param_err
                            A_est[j, k] = np.array([At[j, k]])

            S = np.zeros((1, n * 2))  # Each new solution point makes a new row
            U = np.zeros((1, n)) # Error terms: U = [u, v, w] = [xt - x, yt - y, zt - z] E.g. for 3 x 3 case
            U_rel = np.zeros((1, n))
            U_abs = np.zeros((1, n))
            for j in range(n * 2):
                if j < n:
                    S[0, j] = 1
                else:
                    S[0, j] = 3

            # Initialize system
            for j in range(n):
                U[0, j] = S[0, n + j] - S[0, j]
                U_abs[0, j] = abs(U[0, j])
                U_rel[0, j] = abs(U[0, j] / S[0, j])

            self._eigenvalue_magnitudes.append(self.get_eigenvalue_magnitude(A))
            self.nudge_alg(A, dt, t, T_R, update_times_mtrx, At, A_est, Mu, S, U, U_abs, U_rel, i, matrix_case_type)
            print("\n")


    def parse_matrix_parameter(self, matrix_param):
        # Extracting the row and column indices from the input string
        row = int(matrix_param[1]) - 1
        col = int(matrix_param[2:]) - 1
        return row, col


    def F(self, t, A, S, At, Mu, U):
        """
        INPUT        t : time
        RETURNS  S_dot : right hand side of coupled reference + auxiliary system
        """
        n = A.shape[0] # Returns the number of rows of A
        X_dot = np.matmul(A, S[t, 0:n])
        Xt_dot = np.matmul(At, S[t, n:]) - np.matmul(Mu, U[t])
        S_dot = np.append(X_dot, Xt_dot)
        return S_dot

    def get_row_and_col_indicies(self, list, n):
        rows_indicies, cols_indicies = [], []
        for i in range(n):
            r, c = self.parse_matrix_parameter(self._param_list[i])
            rows_indicies.append(r)
            cols_indicies.append(c)
        return rows_indicies, cols_indicies


    def is_same_index(self, list):
        return all(i == list[0] for i in list)

    def nudge_alg(self, A, dt, t, T_R, update_times_mtrx, At, A_est, Mu, S, U, U_rel, U_abs, matrix_id_number, matrix_case_type):
        n = A.shape[0]
        abs_param_err = [[] for _ in range(n)]
        rel_param_err = [[] for _ in range(n)]

        for i in range(n):
            j, k = self.parse_matrix_parameter(self._param_list[i])
            abs_param_err[i].append(self.get_abs_param_error(A_est[j, k][0], A[j, k]))
            rel_param_err[i].append(self.get_rel_param_error(A_est[j, k][0], A[j, k]))
        new_err_list = np.empty(n)
        new_err_list_abs = np.empty(n)
        new_err_list_rel = np.empty(n)


        for i in range(len(t) - 1):
            for h in range(n):
                j, k = self.parse_matrix_parameter(self._param_list[h])
                param_name = f'a{j + 1}{k + 1}'  # Construct the parameter name based on indices

                if param_name in self._param_list:
                    # print('index, j, k:', h,':' ,j, k)
                    if abs(U[i, j]) >= 0 and S[i, n + k] != 0 and t[i] - update_times_mtrx[j, k][-1] >= T_R:
                        At[j, k] = At[j, k] - Mu[k, k] * U[i, j] / S[i, n + k]
                        A_est[j, k] = np.append(A_est[j, k], At[j, k])
                        update_times_mtrx[j, k] = np.append(update_times_mtrx[j, k], t[i])
                    abs_param_err[h].append(self.get_abs_param_error(A_est[j, k][-1], A[j, k]))
                    rel_param_err[h].append(self.get_rel_param_error(A_est[j, k][-1], A[j, k]))

            # Integrate coupled reference and auxiliary system (forward Euler method)
            new_row = S[i] + self.F(i, A, S, At, Mu, U) * dt
            S = np.vstack((S, new_row))

            # Record new state error
            # print('ID,', 'g,',  'i,', 'elt:')
            for g in range(n):
                new_err_list[g] = S[i + 1, n + g] - S[i + 1, g]
                new_err_list_abs[g] = abs(new_err_list[g] )
                new_err_list_rel[g] = abs(new_err_list[g] / S[i + 1, g])
                # print( matrix_id_number,  g, i, new_err_list[g]) # For testing
                #self._state_error_matrix[matrix_id_number][g].append(new_err_list[g])
            # print("") - For printing

            # Record new state error
            U = np.vstack((U, new_err_list))
            U_abs = np.vstack((U_abs, new_err_list_abs))
            U_rel = np.vstack((U_rel, new_err_list_rel))

        self._nth_avg_abs_param_errors.append(self.get_avg_of_list(abs_param_err))
        self._nth_avg_rel_param_errors.append(self.get_avg_of_list(rel_param_err))
        self.result_output(update_times_mtrx, A, A_est, t, S, U, U_abs, U_rel, abs_param_err, rel_param_err, matrix_id_number)


    def get_avg_of_list(self, my_list):
        sum = 0
        for i in range(len(my_list)):
            sum = my_list[i][-1] + sum
        return sum / len(my_list)

    # def get_rms(self, U_list, n):
    #
    #     return abs_diff_list



    def get_root_mean_square(self, double_list):
        output_list = []
        squared_list = []

        # 1 Raise each element to the second power
        squared_list = [[x**2 for x in sublist] for sublist in double_list]

        # 2 Sum elements in each column and take the square root
        for col in range(len(squared_list[0])):
            column_sum = sum(row[col] for row in squared_list)
            output_list.append(math.sqrt(column_sum))

        return output_list


    def result_output(self, update_times_mtrx, A, A_est, t, S, U, U_abs, U_rel, abs_param_err, rel_param_err, matrix_id_number ):
        n = A.shape[0]
        print(f"X = \n {S[:, 0:n]}\n")
        print(f"Xt = \n {S[:, n:]}\n")
        print(f"U_abs[-1] = {U_abs[-1]}\n") #Absolute Error
        print(f"U_rel[-1] = {U_rel[-1]}\n") #Relative Error

        U_list = [[] for _ in range(n)]
        U_list_abs = [[] for _ in range(n)]
        U_list_rel = [[] for _ in range(n)]

        for i in range(len(U)):
            for j in range(n):
                U_list[j].append(U[i][j])
                U_list_abs[j].append(U_abs[i][j])
                U_list_rel[j].append(U_rel[i][j])

        abs_state_err_rms = self.get_root_mean_square(U_list_abs)
        abs_param_err_rms = self.get_root_mean_square(abs_param_err)


        rel_state_err_rms = self.get_root_mean_square(U_list_rel)
        rel_param_err_rms = self.get_root_mean_square(rel_param_err)
        # print('adla', abs_state_err_rms)


        # self._abs_graph_display.plot_2D_line_graph(t, U_list, matrix_id_number, "State Error")
        state_error_labels = [f'u{i + 1}' for i in range(len(U_list))]

        # ABSOLUTE ERROR
        self._abs_graph_display.plot_2D_line_graph(t, U_list_abs, matrix_id_number, state_error_labels, "Absolute State Error")
        self._abs_graph_display.plot_2D_line_graph(t, abs_param_err, matrix_id_number, self._param_list, "Absolute Parameter Error")
        self._abs_graph_display.plot_2D_line_graph(t, [abs_state_err_rms], matrix_id_number, ['Abs. State Err. (RMS)'], "Absolute State Error RMS", "dodgerblue")
        self._abs_graph_display.plot_2D_line_graph(t, [abs_param_err_rms], matrix_id_number, ['Abs. Param Err. (RMS)'], "Absolute Parameter Error RMS", "cornflowerblue")

        # RELATIVE ERROR
        self._rel_graph_display.plot_2D_line_graph(t, U_list_rel, matrix_id_number, state_error_labels, "Relative State Error")
        self._rel_graph_display.plot_2D_line_graph(t, rel_param_err, matrix_id_number, self._param_list, "Relative Parameter Error")
        self._rel_graph_display.plot_2D_line_graph(t, [rel_state_err_rms], matrix_id_number, ['Rel. State Err. (RMS)'], "Relative State Error RMS", "darkorange")
        self._abs_graph_display.plot_2D_line_graph(t, [rel_param_err_rms], matrix_id_number, ['Rel. Param Err. (RMS)'], "Relative Parameter Error RMS", "coral")

        for i in range(n):
            j, k = self.parse_matrix_parameter(self._param_list[i])
            print(f"{self._param_list[i]} = {A[j, k]}")
            print(f"{self._param_list[i].title()}[-1] = {A_est[j, k][-1]}")
            print(self._param_list[i], "Absolute Error:", abs_param_err[i][-1])
            print(self._param_list[i], "Relative Error:", rel_param_err[i][-1])
            print(f"{self._param_list[i].title()} = {A_est[j , k]}")
            print("")
