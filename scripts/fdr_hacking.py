import numpy as np
from simlog.simlog import get_arrays, get_pvalues_per_index, get_lowest_fdr


def main():
    n = 10000
    list1 = get_arrays()
    list2 = get_arrays()
    pvalues = get_pvalues_per_index(list1, list2)
    lowest_fdrs = np.zeros(n)
    for i in range(n):
        lowest_fdrs[i] = get_lowest_fdr(pvalues)
    print("Result")
    print(lowest_fdrs)
    print(np.sum(lowest_fdrs < 0.5))


main()
