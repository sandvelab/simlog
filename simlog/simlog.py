"""Main module."""
import numpy as np
from scipy.stats import ttest_ind
import numpy as np


def get_arrays():
    arrays = []
    for i in range(100):
        arrays.append(np.random.uniform(0, 1, 1000))
    return arrays


def get_pvalues_per_index(list1, list2):
    pvalues = np.zeros(1000)
    for j in range(1000):
        group1 = [list1[i][j] for i in range(100)]
        group2 = [list2[i][j] for i in range(100)]
        _, pvalue = ttest_ind(group1, group2)
        pvalues[j] = pvalue
    return pvalues


def get_fdr(pvalues, alpha=0.05):
    n = len(pvalues)
    indices = np.argsort(pvalues)
    sorted_pvalues = pvalues[indices]
    fdr = np.zeros(n)
    for i in range(n):
        fdr[i] = sorted_pvalues[i] * n / (i + 1)
    min_fdr = np.minimum.accumulate(fdr[::-1])[::-1]
    fdr = np.minimum(min_fdr, 1)
    return fdr


def get_lowest_fdr(pvalues):
    fdr = get_fdr(pvalues)
    lowest_fdr = np.min(fdr)
    return lowest_fdr


