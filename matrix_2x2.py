import random
import itertools
import numpy as np

class Matrix_2x2:
    def __init__(self, low_bnd, high_bnd, ev_type, pp_type):
        self._ev_type = ev_type
        self._pp_type = pp_type
        self._matrix = []
        self._mtrx_sample_space = []
        self.init_matrix(low_bnd, high_bnd, ev_type, pp_type)

    def __str__(self):
        return str(self._matrix)

    def init_matrix(self, low_bnd, high_bnd, ev_type, pp_type):
        if ev_type == "rde":
            self.set_matrix_rde(low_bnd, high_bnd, ev_type, pp_type)
        elif ev_type == "re":
            self.set_matrix_re(low_bnd, high_bnd, ev_type, pp_type)
        elif ev_type == "ce":
            self.set_matrix_ce(low_bnd, high_bnd, ev_type, pp_type)
        else:
            print("ERROR:", ev_type, "is not a valid input.")
            quit()

    def get_matrix(self):
        return self._matrix

    def set_matrix(self, mtrx):
        self._matrix = mtrx

    def set_random_matrix(self, low_bnd, high_bnd):
        self.set_matrix(np.random.uniform(low_bnd, high_bnd, (2, 2)))

    def set_matrix_rde(self, low_bnd, high_bnd, ev_type, pp_type):
        self.set_random_matrix(low_bnd, high_bnd)
        mtrx = self.get_matrix()
        tr, det = np.trace(mtrx), np.linalg.det(mtrx)
        ev_1, ev_2 = np.linalg.eigvals(mtrx)
        has_mtrx_been_found = False

        if pp_type not in ["saddle", "source", "sink"]:
            print("ERROR:", pp_type, "is not a valid input.")
            quit()

        while not has_mtrx_been_found:
            if pp_type == "saddle" and (tr ** 2 - 4 * det) > 0 and det < 0 and ev_1 < 0 < ev_2:
                has_mtrx_been_found = True
                self.set_matrix(mtrx)
                break
            elif pp_type == "source" and (tr ** 2 - 4 * det) > 0 and det > 0 and tr > 0 and 0 < ev_1 < ev_2:
                has_mtrx_been_found = True
                self.set_matrix(mtrx)
                break
            elif pp_type == "sink" and (tr ** 2 - 4 * det) > 0 and det > 0 and tr < 0 and ev_1 < ev_2 < 0:
                has_mtrx_been_found = True
                self.set_matrix(mtrx)
                break
            else:
                self.set_random_matrix(low_bnd, high_bnd)
                mtrx = self.get_matrix()
                tr, det = np.trace(mtrx), np.linalg.det(mtrx)
                ev_1, ev_2 = np.linalg.eigvals(mtrx)

    def set_matrix_re(self, low_bnd, high_bnd, ev_type, pp_type):
        if pp_type not in ["sink", "source"]:
            print("ERROR:", pp_type, "is not a valid input.")
            quit()

        sample_space = np.linspace(low_bnd, high_bnd, num=(high_bnd - low_bnd + 1) * 2)
        samples = itertools.product(sample_space, repeat=4)

        for a11, a12, a21, a22 in samples:
            tr = a11 + a22
            det = (a11 * a22) - (a12 * a21)

            if pp_type == "sink" and (tr ** 2 - 4 * det) == 0 and tr < 0:
                temp_mtrx = np.array([[a11, a12], [a21, a22]])
                self.set_mtrx_sample_space(temp_mtrx)

            elif pp_type == "source" and (tr ** 2 - 4 * det) == 0 and tr > 0:
                temp_mtrx = np.array([[a11, a12], [a21, a22]])
                self.set_mtrx_sample_space(temp_mtrx)

        max_index = len(self.get_mtrx_sample_space()) - 1
        random_index = random.randint(0, max_index)
        mtrx = self.get_mtrx_sample_space_elt(random_index)
        self.set_matrix(mtrx)

    def set_matrix_ce(self, low_bnd, high_bnd, ev_type, pp_type):
        self.set_random_matrix(low_bnd, high_bnd)
        mtrx = self.get_matrix()
        tr, det = np.trace(mtrx), np.linalg.det(mtrx)
        ev_1, ev_2 = np.linalg.eigvals(mtrx)
        rule = False

        if pp_type == "center":
            self.set_matrix_ce_center(low_bnd, high_bnd, ev_type, pp_type)
        elif pp_type in ["sp_sink", "sp_source"]:
            while not rule:
                if pp_type == "sp_sink" and (tr ** 2) - 4 * det < 0 and tr < 0:
                    rule = True
                    self.set_matrix(mtrx)
                    break
                elif pp_type == "sp_source" and (tr ** 2) - 4 * det < 0 and tr > 0:
                    rule = True
                    self.set_matrix(mtrx)
                    break
                else:
                    self.set_random_matrix(low_bnd, high_bnd)
                    mtrx = self.get_matrix()
                    tr, det = np.trace(mtrx), np.linalg.det(mtrx)
                    ev_1, ev_2 = np.linalg.eigvals(mtrx)
        else:
            print("ERROR:", pp_type, "is not a valid input.")
            quit()

    def set_matrix_ce_center(self, low_bnd, high_bnd, ev_type, pp_type):
        sample_space = np.linspace(low_bnd, high_bnd, num=(high_bnd - low_bnd + 1) * 2)
        samples = itertools.product(sample_space, repeat=4)

        for a11, a12, a21, a22 in samples:
            tr = a11 + a22
            det = (a11 * a22) - (a12 * a21)
            if (tr ** 2) - 4 * det < 0 and tr == 0:
                temp_mtrx = np.array([[a11, a12], [a21, a22]])
                self.set_mtrx_sample_space(temp_mtrx)

        max_index = len(self.get_mtrx_sample_space()) - 1
        random_index = random.randint(0, max_index)
        mtrx = self.get_mtrx_sample_space_elt(random_index)
        self.set_matrix(mtrx)

    def get_mtrx_sample_space(self):
        return self._mtrx_sample_space

    def get_mtrx_sample_space_elt(self, index):
        return self._mtrx_sample_space[index]
