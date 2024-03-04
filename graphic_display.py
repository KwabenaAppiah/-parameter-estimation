import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Importing 3D plotting tools
import shutil
import math
import os
import plotly.graph_objects as go # This package must be installed

class GraphicDisplay:
    def __init__(self, n, error_type, ev_type, pp_type):
        self._n = n
        self._error_type = error_type
        self._ev_type = ev_type
        self._pp_type = pp_type
        self._threshold_vals = [1e-14, 1e-12, 1e-10, 1e-8]
        self._point_colors = ["blue", "#800080", "red"]
        self._alpha_vals = [1, 0.3]
        self._marker_type = '.' #or 'o'


    def show_plot(self):
        plt.show()

    def plot_2D_line_graph(self, t, lists, matrix_id_number, labels, sub_directory, plot_type_unformatted, line_color = "N/A", x_scale_type = "log", y_scale_type = "log"):
        # Assuming all lists have the same length
        axis_label = plot_type_unformatted
        directory_type = self.format_case_type_directory(plot_type_unformatted )
        # output_directory = os.path.join("output/" + directory_type + "/")
        n_x_n = str(self._n) + 'x' + str(self._n)

        if(self._n == 2):
            ev_type = self._ev_type
            pp_type = self._pp_type
            output_directory = os.path.join("output/" + ev_type + "_" + pp_type  + "_" + n_x_n + "/" + sub_directory + "/" + directory_type + "/")
        else:
            output_directory = os.path.join("output/" +  n_x_n + "/" + sub_directory + "/" + directory_type + "/")

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

        plt.xscale(x_scale_type)
        plt.yscale(y_scale_type)
        plt.legend()

        if(self._n == 2):
            plt.title("MATRIX " + str(matrix_id_number) + ' | ' + ev_type.upper() + ' | ' + pp_type.upper() + " - " + axis_label)
            filename = directory_type + "_" + ev_type + "_" + pp_type + "_matrix_" + str(matrix_id_number)  + ".jpg"
        else:
            plt.title("MATRIX " + str(matrix_id_number) + " - " + axis_label)
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



    def set_ev_subplots(self, ev_type, pp_type, case_type, bounds, loop_limit, param_err_type):
        self._ev_fig, self._ev_ax = plt.subplots()
        param_label_1, param_label_2 = self.get_static_vars_dict_elt("param_label_1"), self.get_static_vars_dict_elt("param_label_2")
        graph_description = "Avg. " + param_err_type.capitalize() + " Error of " + param_label_1 + " and " + param_label_2
        title = ev_type.upper() + " | " + pp_type.upper() + " | " + case_type.upper() + " | BNDS " + bounds + " | " + loop_limit + " CC | " + graph_description
        self._ev_ax.set_title(label = title, pad = 30, fontsize = 15)
        self._ev_ax.set_xlabel("$\u03BB_{1}$", loc = "right", fontsize = 14)
        self._ev_ax.set_ylabel("$\u03BB_{2}$", loc = "top", fontsize = 14)
        self._ev_fig.set_size_inches(16, 8)
        self._ev_ax = plt.gca()

        # Hide two spines
        self._ev_ax.spines["right"].set_color("none")
        self._ev_ax.spines["top"].set_color("none")

        # Move bottom and left spine to 0, 0
        self._ev_ax.spines["bottom"].set_position(("data", 0))
        self._ev_ax.spines["left"].set_position(("data", 0))

        # Move ticks positions
        self._ev_ax.xaxis.set_ticks_position("bottom")
        self._ev_ax.yaxis.set_ticks_position("left")

        self._ev_ax.plot(1, 0, ">k", transform = self._ev_ax.get_yaxis_transform(), clip_on = False)
        self._ev_ax.plot(0, 1, "^k", transform = self._ev_ax.get_xaxis_transform(), clip_on = False)



    def plot_3D_ev_graph(self, point_lists, nth_avg_param_err):
        # Create 'html_output' directory if it doesn't exist
        ev_type = self._ev_type
        pp_type = self._pp_type
        n_x_n = str(self._n) + 'x' + str(self._n)
        output_directory = 'output/' + n_x_n + '/'+ self._error_type.lower() + "_error"

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        fig = go.Figure()

        title_of_plot = "Eigenvalue Plot | " +  self._error_type + " Error"
        filename = "eigenvalue-plot" + "-" + self._error_type.lower() + "-error"

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
            fig.add_trace(go.Scatter3d(x = [x], y = [y], z = [z], mode = 'markers', marker = dict(size = 3, color = point_color, opacity = alpha_value), name = f'Point {i + 1}'))

        # Update layout with axis labels
        fig.update_layout(scene = dict(xaxis_title = 'λ₁', yaxis_title = 'λ₂', zaxis_title = 'λ₃'), title = title_of_plot, title_font = dict(size = 20, family = 'Arial', color = 'black'), title_x = 0.5)

        # Export interactive HTML applet
        output_file_path = os.path.join(output_directory, f'{filename}.html')
        fig.write_html(output_file_path)
