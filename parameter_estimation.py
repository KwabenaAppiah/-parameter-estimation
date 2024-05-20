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
    ev_type, pp_type = None, None
    print(len(param_list))

    if len(param_list) == 2:
        while ev_type == None:
            ev_type = input("Please enter your eigenvalue type: ")
            if ev_type != None:
                print("You entered:", ev_type)

        while pp_type == None:
            pp_type = input("Please enter your phase portrait type: ")
            if pp_type != None:
                print("You entered:", pp_type)
                
        print("")
        lin_nudge_alg = LinearNudgingAlg(len(param_list), bound_value, total_matricies, ev_type, pp_type, param_list)

    elif len(param_list) > 2:
        lin_nudge_alg = LinearNudgingAlg(len(param_list), bound_value, total_matricies, ev_type, pp_type, param_list)


    else:
        print('ERROR: Please check your input.', '\n')
        sys.exit()



def parse_param_list(args):
    # Combine the string values separated by commas into a single list
    string_values = ' '.join(args[3:])
    string_values = [value.strip(',') for value in string_values.split()]
    return string_values

if __name__ == "__main__":
    main()
