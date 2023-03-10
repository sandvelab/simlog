import dataclasses
import numpy as np
from simlog.simlog import get_arrays, get_pvalues_per_index, get_lowest_fdr


@dataclasses.dataclass
class SimulationParams:
    pass





class PostProcessor:
    def __init__(self, logger):
        #logger provides the config
        pass

    def get_result(self, keys):
        pass


def main():
    logger = HLogger("fdrHackingResults")
    n = 100
    for i in range(n):
        list1 = get_arrays(logger.get_sublogger([str(i),"arrayValues","diseased"]))
        list2 = get_arrays(logger.get_sublogger([str(i),"arrayValues","healthy"]))
        pvalues = get_pvalues_per_index(list1, list2, logger)
        lowest_fdrs = np.zeros(n)
        lowest_fdrs[i] = get_lowest_fdr(pvalues)
    print("Result")
    print(lowest_fdrs)
    print(np.sum(lowest_fdrs < 0.5))


if __name__ == "__main__":
    main()

