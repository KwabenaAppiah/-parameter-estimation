import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Importing 3D plotting tools
import shutil
import math
import os
import plotly.graph_objects as go # This package must be installed

class GraphicDisplay:
    def __init__(self, error_type, matrix_case_type):
        pass
        # self._plot_points()
        self._matrix_case_type = matrix_case_type
        self._error_type = error_type
        self._threshold_vals = [1e-14, 1e-12, 1e-10, 1e-8]
        self._point_colors = ["blue", "#800080", "red"]
        self._alpha_vals = [1, 0.3]
        self._marker_type = '.' #or 'o'

    def show_plot(self):
        plt.show()

    def plot_2D_line_graph(self, t, lists, matrix_id_number, labels, sub_directory, plot_type_unformatted, line_color = "N/A"):
        # Assuming all lists have the same length
        axis_label = plot_type_unformatted
        directory_type = self.format_case_type_directory(plot_type_unformatted )
        # output_directory = os.path.join("output/" + directory_type + "/")
        output_directory = os.path.join("output/" + sub_directory + "/" + directory_type + "/")

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        plt.figure(figsize = (16, 8), dpi = 300)  # Set figure size and DPI

        for i in range(len(lists)):
            if line_color != "N/A":
                plt.plot(t, lists[i], label = labels[i], color = line_color)
            else:
                plt.plot(t, lists[i], label = labels[i])

        plt.xlabel('Time')
        plt.ylabel(axis_label)
        plt.title("Matrix " + str(matrix_id_number) + " - " + axis_label)
        plt.xscale('log')
        plt.yscale('log')
        plt.legend()

        # Save the plot in the specified directory with a unique filename
        #filename = f"parameter_error_matrix _{matrix_id_number}.jpg"
        filename = directory_type + "_matrix_" + str(matrix_id_number)  + ".jpg"
        plt.savefig(os.path.join(output_directory, filename), format = 'jpeg')
        plt.close()  # Close the plot to free up resources


    def format_case_type_title(self, input_string):
        # Replace underscores with spaces
        result_string = input_string.replace('_', ' ')

        # Capitalize the first letter after a hyphen
        result_string = '-'.join([word.capitalize() if '-' in word else word for word in result_string.split('-')])

        # Capitalize the first letter of the entire string
        return result_string.title()

    def format_case_type_filename(self, input_string):
        result_string = input_string.replace('_', '-')
        return result_string.lower()

    def format_case_type_directory(self, input_string):
        # Make the string lowercase
        lowercase_string = input_string.lower()

        # Replace spaces with underscores
        modified_string = lowercase_string.replace(" ", "_")

        return modified_string


    def plot_ev_graph_html(self, point_lists, nth_avg_param_err):
        # Create 'html_output' directory if it doesn't exist
        # output_directory = 'html_output'+ '/' + self._error_type.lower()
        # output_directory = 'output/ev_graphs/' + self._error_type.lower()
        output_directory = 'output/' + self._error_type.lower() + "_error"


        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        fig = go.Figure()
        case_type_title = self.format_case_type_title(self._matrix_case_type)
        case_type_filename = self.format_case_type_filename(self._matrix_case_type)
        title_of_plot = "Eigenvalue Plot | " + case_type_title + " | " + self._error_type + " Error"
        filename = "eigenvalue-plot" + case_type_filename + "-" + self._error_type.lower() + "-error"

        # Continue looping until all point_lists are processed
        for i in range(len(point_lists)):
            # Extracting x, y, z coordinates from the current list
            x = point_lists[i][0]
            y = point_lists[i][1]
            z = point_lists[i][2]

            # Calculate a single value from the list
            nth_avg_param_err_elt = nth_avg_param_err[i]

            # Set color and alpha based on nth_avg_param_err value
            if self._threshold_vals[3] < nth_avg_param_err_elt and nth_avg_param_err_elt < math.inf:
                point_color, alpha_value = self._point_colors[2], self._alpha_vals[0]

            elif self._threshold_vals[2] < nth_avg_param_err_elt and nth_avg_param_err_elt <= self._threshold_vals[3]:
                point_color, alpha_value = self._point_colors[2], self._alpha_vals[1]

            elif self._threshold_vals[1] < nth_avg_param_err_elt and nth_avg_param_err_elt <= self._threshold_vals[2]:
                point_color, alpha_value = self._point_colors[1], self._alpha_vals[1]

            elif self._threshold_vals[0] < nth_avg_param_err_elt and nth_avg_param_err_elt <= self._threshold_vals[1]:
                point_color, alpha_value = self._point_colors[0], self._alpha_vals[1]

            elif 0 <= nth_avg_param_err_elt and nth_avg_param_err_elt <= self._threshold_vals[0]:
                point_color, alpha_value = self._point_colors[0], self._alpha_vals[0]

            # Add scatter trace to the figure
            fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[z], mode='markers', marker=dict(size=3, color=point_color, opacity=alpha_value), name=f'Point {i + 1}'))

        # Update layout with axis labels
        fig.update_layout(scene = dict(xaxis_title='λ₁', yaxis_title='λ₂', zaxis_title='λ₃'), title=title_of_plot, title_font=dict(size=20, family='Arial', color='black'), title_x=0.5)

        # Export interactive HTML applet
        output_file_path = os.path.join(output_directory, f'{filename}.html')
        fig.write_html(output_file_path)


    def plot_ev_graph(self, point_lists, nth_avg_param_err):
        case_type_title = self.format_case_type_title(self._matrix_case_type)
        title_of_plot = "Eigenvalue Plot | " + case_type_title + " | " + self._error_type + " Error"
        fig = plt.figure(title_of_plot)
        ax = fig.add_subplot(111, projection = '3d')

        for i in range(len(point_lists)):
            # Extracting x, y, z coordinates from the current list
            x = point_lists[i][0]
            y = point_lists[i][1]
            z = point_lists[i][2]

            # Plotting the point with red color
            if self._threshold_vals[3] < nth_avg_param_err[i] and nth_avg_param_err[i] < math.inf:
                point_color, alpha_value = self._point_colors[2], self._alpha_vals[0]

            # elif 1e-4 < ... <= 1e-1:
            elif self._threshold_vals[2] < nth_avg_param_err[i] and nth_avg_param_err[i] <= self._threshold_vals[3]:
                point_color, alpha_value = self._point_colors[2], self._alpha_vals[1]

            # elif 1e-8 < ... <= 1e-4:
            elif self._threshold_vals[1] < nth_avg_param_err[i] and nth_avg_param_err[i] <= self._threshold_vals[2]:
                point_color, alpha_value = self._point_colors[1], self._alpha_vals[1]

            #elif 1e-12 < ...  <= 1e-8:
            elif self._threshold_vals[0] < nth_avg_param_err[i] and nth_avg_param_err[i] <= self._threshold_vals[1]:
                point_color, alpha_value = self._point_colors[0], self._alpha_vals[1]

            #elif 0 <= ...  <= 1e-12:
            elif 0 <= nth_avg_param_err[i] and nth_avg_param_err[i] <= self._threshold_vals[0]:
                point_color, alpha_value = self._point_colors[0], self._alpha_vals[0]

            ax.scatter(x, y, z, c = point_color, marker = self._marker_type, alpha = alpha_value)


        ax.set_xlabel('$λ_{1}$')
        ax.set_ylabel('$λ_{2}$')
        ax.set_zlabel('$λ_{3}$')


    # def plot_2D_line_graph(self, t, lists, labels, matrix_id_number):
    #     # Assuming all lists have the same length
    #     output_directory = os.path.join("output/parameter_error/")
    #
    #     # Create the output directory if it doesn't exist
    #     if not os.path.exists(output_directory):
    #         os.makedirs(output_directory)
    #
    #     plt.figure(figsize=(16, 8), dpi=300)  # Set figure size and DPI
    #
    #     for i in range(len(lists)):
    #         plt.plot(t, lists[i], label=labels[i])
    #
    #     plt.xlabel('Time')
    #     plt.ylabel('Parameter Error')
    #     plt.title("Matrix " + str(matrix_id_number) + " - Parameter Error")
    #     plt.xscale('log')
    #     plt.yscale('log')
    #     plt.legend()
    #
    #     # Save the plot in the specified directory with a unique filename
    #     filename = f"parameter_error_matrix_{matrix_id_number}.jpg"
    #     plt.savefig(os.path.join(output_directory, filename), format='jpeg')
    #     plt.close()  # Close the plot to free up resources
