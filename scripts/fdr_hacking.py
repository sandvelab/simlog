import sys
sys.path.append("..")


import dataclasses
import numpy as np

from scripts.config import logger
from simlog.simlog import get_methylation_vectors_for_group_of_patients, get_pvalues_per_index, get_lowest_fdr

def main():
    num_full_experiments = 3
    experiment_settings = [{'n_patients':5, 'n_sites':10},
                           {'n_patients':50, 'n_sites':100}]

    for setting in logger.loopContext(["experiment_"]).iter(experiment_settings):
        lowest_fdrs = np.zeros(num_full_experiments)
        for experiment_iter in logger.loopContext(["iter_"]).range(num_full_experiments):
            logger.log_dict(setting, ["settings"])

            healthy_group = get_methylation_vectors_for_group_of_patients(setting['n_patients'], setting['n_sites'])
            logger.log_raw_numbers(healthy_group, ["arrayValues", "healthy"], level=logger.LOW)
            diseased_group = get_methylation_vectors_for_group_of_patients(setting['n_patients'], setting['n_sites'])
            logger.log_raw_numbers(diseased_group, ["arrayValues", "diseased"], level=logger.LOW)

            pvalues = get_pvalues_per_index(healthy_group, diseased_group)
            logger.log_histogram(pvalues, ["pvalues"])

            lowest_fdrs[experiment_iter] = get_lowest_fdr(pvalues)

        print("Result")
        print(lowest_fdrs)
        ALPHA = 0.05
        num_significant_fdrs = np.sum(lowest_fdrs < ALPHA)
        print(num_significant_fdrs)
        logger.log_raw_text(str(num_significant_fdrs), ["numSignificantFdrs"], level=logger.HIGH) #could have stored in list and logged outside loop..

if __name__ == "__main__":
    main()

