"""Main module."""
import numpy as np
from scipy.stats import ttest_ind
import numpy as np

from scripts.config import logger


def get_methylation_vectors_for_group_of_patients(num_patients, num_methylation_sites):
    arrays = []
    for i in range(num_patients):
        array = np.random.uniform(0, 1, num_methylation_sites)
        arrays.append(array)
    return arrays


def get_pvalues_per_index(list1, list2):
    n_sites = len(list1[0]) #ugly..
    pvalues = np.zeros(n_sites)
    for j in range(n_sites):
        group1 = [list1[i][j] for i in range(len(list1))]
        group2 = [list2[i][j] for i in range(len(list2))]
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
    logger.log_histogram(fdr, ["fdrs"])
    lowest_fdr = np.min(fdr)
    logger.log_raw_text(str(lowest_fdr), ["lowestFdr"], level=logger.HIGH)
    return lowest_fdr


