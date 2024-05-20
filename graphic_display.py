from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Importing 3D plotting tools
import numpy as np
import shutil
import datetime
import math
import time
import os
import plotly.graph_objects as go # This package must be installed


class GraphicDisplay:
    def __init__(self, n, total_matricies, error_type, ev_type, pp_type):
        self._n = n
        self._total_matricies = total_matricies
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
        # output_directory = os.path.join("../output/" + directory_type + "/")
        n_x_n = str(self._n) + 'x' + str(self._n)

        if(self._n == 2):
            ev_type = self._ev_type
            pp_type = self._pp_type
            output_directory = os.path.join("../output/" + ev_type + "_" + pp_type  + "_" + n_x_n + "/" + sub_directory + "/" + directory_type + "/")
        else:
            output_directory = os.path.join("../output/" +  n_x_n + "/" + sub_directory + "/" + directory_type + "/")

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




    def plot_3D_ev_graph(self, point_lists, nth_avg_param_err):
        # Create 'html_output' directory if it doesn't exist
        ev_type = self._ev_type
        pp_type = self._pp_type
        n_x_n = str(self._n) + 'x' + str(self._n)
        output_directory = '../output/' + n_x_n + '/'+ self._error_type.lower() + "_error"
        total_matricies = str(self._total_matricies)

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        fig = go.Figure()

        title_of_plot = "Eigenvalue Plot | " +  self._error_type + " ERROR" + " | " + total_matricies  + " CC "
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


    def get_date_str(self):
        raw_date = datetime.datetime.now()
        t = time.localtime()
        date_str = str(raw_date.year) + "." + str(time.strftime("%m")) + "." + str(time.strftime("%d"))
        return date_str


    def find_largest_list_value(self, lst):
        if not lst:  # Check if the list is empty
            return None

        # Find the absolute largest value in the list
        abs_largest_value = max(lst, key = abs)

        return abs_largest_value


    def plot_trace_det_graph(self, traces, determinants, nth_avg_param_err):
        fig, ax = plt.subplots()
        ev_type = self._ev_type
        pp_type = self._pp_type
        error_type = self._error_type
        n = str(self._n)
        total_matricies = str(self._total_matricies)

        n_x_n = str(self._n) + 'x' + str(self._n)
        max_trace = self.find_largest_list_value(traces)
        output_directory = "../output/" + ev_type + "_" + pp_type  + "_" + n_x_n + "/" + self._error_type.lower() + "_error"

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        filename = "trace-det-plot" + "-" + self._error_type.lower() + "-error"
        title_of_plot = ev_type.upper() + " | " + pp_type.upper() + " | " + error_type.upper() + " ERROR" + " | " + total_matricies  + " CC "

        ax.set_title(label = title_of_plot, pad = 30, fontsize = 15)
        ax.set_xlabel("Tr", loc = "right", fontsize = 14)
        ax.set_ylabel("Det", loc = "top", fontsize = 14)


        fig.set_size_inches(16, 8)
        ax = plt.gca()

        # Hide two spines
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")

        # Move bottom and left spine to 0, 0
        ax.spines["bottom"].set_position(("data", 0))
        ax.spines["left"].set_position(("data", 0))

        # Move ticks positions
        ax.xaxis.set_ticks_position("bottom")
        ax.yaxis.set_ticks_position("left")

        ax.plot(1, 0, ">k", transform = ax.get_yaxis_transform(), clip_on = False)
        ax.plot(0, 1, "^k", transform = ax.get_xaxis_transform(), clip_on = False)

        for i in range(len(traces)):
            x = traces[i]
            y = determinants[i]

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

            # Plot points
            ax.scatter(x, y, color = point_color, alpha = alpha_value)



        # Graph Parabola
        if abs(max_trace) == 0:
            max_trace = 10
        x = np.linspace(-(max_trace), max_trace, 100)
        y = x**2 / 4
        ax.plot(x, y, linewidth = 1.5, c = "orange")

        label_1 = "0 <= $x̄_{Err}$ <="  + str(self._threshold_vals[0])
        label_2 = str(self._threshold_vals[0]) + " < $x̄_{Err}$ <= " + str(self._threshold_vals[1])
        label_3 = str(self._threshold_vals[1]) + " < $x̄_{Err}$ <= " + str(self._threshold_vals[2])
        label_4 = str(self._threshold_vals[2]) + " < $x̄_{Err}$ <=" + str(self._threshold_vals[3])
        label_5 = str(self._threshold_vals[3]) + " < $x̄_{Err}$ < ∞"

        custom_handles = [
            Line2D([0], [0], marker = "o", markerfacecolor = "r", color = "w", alpha = 1, markersize = 7, label = label_5),
            Line2D([0], [0], marker = "o", markerfacecolor = "r", color = "w", alpha = 0.3, markersize = 7, label = label_4),
            Line2D([0], [0], marker = "o", markerfacecolor = "#800080", color = "w", alpha = 0.3, markersize = 7, label = label_3),
            Line2D([0], [0], marker = "o", markerfacecolor = "b", color = "w", alpha = 0.3, markersize = 7, label = label_2),
            Line2D([0], [0], marker = "o", markerfacecolor = "b", color = "w", markersize = 7, label = label_1),
            Line2D([0], [0], color = "orange", alpha = 1, lw = 3, label = "T\N{SUPERSCRIPT TWO} - 4D = 0")]


        if(pp_type == "saddle"):
            ax.legend(handles = custom_handles, loc = "upper left", bbox_to_anchor = (-.15, 1.15), borderpad = 1)

        # #mid-left
        elif(pp_type == "source" or pp_type == "sp_source" ):
            ax.legend(handles = custom_handles, loc = "center left", bbox_to_anchor = (-.13, .4), borderpad = 1)

        #mid-right
        elif(pp_type == "sink" or pp_type == "sp_sink" or pp_type == "center"):
            ax.legend(handles = custom_handles, loc = "center right", bbox_to_anchor = (1.1, .4), borderpad = 1)

        # Export plot as JPEG file
        output_file_path = os.path.join(output_directory, f'{filename}.jpg')
        fig.savefig(output_file_path, format = 'jpeg', dpi = 300)
        plt.close()



    def plot_2D_ev_graph(self, point_lists, nth_avg_param_err):

        fig, ax = plt.subplots()
        ev_type = self._ev_type
        pp_type = self._pp_type
        error_type = self._error_type
        n = str(self._n)
        total_matricies = str(self._total_matricies)

        n_x_n = str(self._n) + 'x' + str(self._n)
        # output_directory = 'output/' + n_x_n + '/' + self._error_type.lower() + "_error"
        output_directory = "../output/" + ev_type + "_" + pp_type  + "_" + n_x_n + "/" + self._error_type.lower() + "_error"

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        filename = "eigenvalue-plot" + "-" + self._error_type.lower() + "-error"
        title_of_plot = ev_type.upper() + " | " + pp_type.upper() + " | " + error_type.upper() + " ERROR" + " | " + total_matricies  + " CC "

        ax.set_title(label = title_of_plot, pad = 30, fontsize = 15)
        ax.set_xlabel("$\u03BB_{1}$", loc = "right", fontsize = 14)
        ax.set_ylabel("$\u03BB_{2}$", loc = "top", fontsize = 14)
        fig.set_size_inches(16, 8)
        ax = plt.gca()

        # Hide two spines
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")

        # Move bottom and left spine to 0, 0
        ax.spines["bottom"].set_position(("data", 0))
        ax.spines["left"].set_position(("data", 0))

        # Move ticks positions
        ax.xaxis.set_ticks_position("bottom")
        ax.yaxis.set_ticks_position("left")

        ax.plot(1, 0, ">k", transform = ax.get_yaxis_transform(), clip_on = False)
        ax.plot(0, 1, "^k", transform = ax.get_xaxis_transform(), clip_on = False)

        for i in range(len(point_lists)):
            x = point_lists[i][0]
            y = point_lists[i][1]

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

            # Plot points
            ax.scatter(x, y, color = point_color, alpha = alpha_value)
        # ax.set_xlabel('λ₁')
        # ax.set_ylabel('λ₂')

        # Init legend
        bbox_x = bbox_y = 0
        legend_loc = "center left"

        label_1 = "0 <= $x̄_{Err}$ <="  + str(self._threshold_vals[0])
        label_2 = str(self._threshold_vals[0]) + " < $x̄_{Err}$ <= " + str(self._threshold_vals[1])
        label_3 = str(self._threshold_vals[1]) + " < $x̄_{Err}$ <= " + str(self._threshold_vals[2])
        label_4 = str(self._threshold_vals[2]) + " < $x̄_{Err}$ <=" + str(self._threshold_vals[3])
        label_5 = str(self._threshold_vals[3]) + " < $x̄_{Err}$ < ∞"

        custom_handles = [
            Line2D([0], [0], marker = "o", markerfacecolor = "r", color = "w", alpha = 1, markersize = 7, label = label_5),
            Line2D([0], [0], marker = "o", markerfacecolor = "r", color = "w", alpha = 0.3, markersize = 7, label = label_4),
            Line2D([0], [0], marker = "o", markerfacecolor = "#800080", color = "w", alpha = 0.3, markersize = 7, label = label_3),
            Line2D([0], [0], marker = "o", markerfacecolor = "b", color = "w", alpha = 0.3, markersize = 7, label = label_2),
            Line2D([0], [0], marker = "o", markerfacecolor = "b", color = "w", markersize = 7, label = label_1)]


        if(ev_type == "rde" and pp_type == "saddle"):
            legend_loc, bbox_x, bbox_y = "upper left", -0.15, 1

        elif(ev_type == "rde" and pp_type == "sink"):
            legend_loc, bbox_x, bbox_y = "upper left", -0.16, .9

        elif(ev_type == "rde" and pp_type == "source"):
            legend_loc, bbox_x, bbox_y = "upper left", -0.16, .9

        elif(ev_type == "re" and pp_type == "sink" ):
            legend_loc, bbox_x, bbox_y = "lower right", .91, -.06

        elif(ev_type == "re" and pp_type == "source" ):
            legend_loc, bbox_x, bbox_y = "lower right", 1, .1

        elif(ev_type == "ce"):
            legend_loc, bbox_x, bbox_y = "lower right", 1, .1


        ax.legend(handles = custom_handles, loc = legend_loc, bbox_to_anchor = (bbox_x, bbox_y), borderpad = 1.1)
        # Init legend

        # Export plot as JPEG file
        output_file_path = os.path.join(output_directory, f'{filename}.jpg')
        fig.savefig(output_file_path, format = 'jpeg', dpi = 300)
        plt.close()
