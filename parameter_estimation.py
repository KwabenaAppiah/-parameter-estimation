from linear_nudging_alg import LinearNudgingAlg
import numpy as np
import shutil
import sys
import os
import re


def main():
    bound_value = int(sys.argv[1])
    total_matricies = int(sys.argv[2])
    param_list = parse_param_list(sys.argv)

    if 2 <= len(param_list):
        lin_nudge_alg = LinearNudgingAlg(len(param_list), bound_value, total_matricies, param_list)

    elif len(param_list) == 1 and param_list[0] == 'main_diagonal' or param_list[0] == 'anti-diagonal' or check_if_column(param_list[0]):
        print("Please provide 'n' for your matrix.")
        sys.exit()
    else:
        print('ERROR: Please check your input.', '\n')
        sys.exit()


def check_if_column(input_string):
    # Define the pattern using regular expression
    str_pattern = r'column_(\d+)$'
    is_column = False

    # Match the pattern against the input string
    if re.match(str_pattern, input_string):
        is_column = True

    return is_column


def parse_param_list(args):
    # Combine the string values separated by commas into a single list
    string_values = ' '.join(args[3:])
    string_values = [value.strip(',') for value in string_values.split()]
    return string_values

if __name__ == "__main__":
    main()
