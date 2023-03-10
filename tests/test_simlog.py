#!/usr/bin/env python
"""Tests for `simlog` package."""
import pytest
import numpy as np

from simlog.logger import HLogger
from simlog.simlog import get_arrays, get_pvalues_per_index, get_lowest_fdr

def test():
    print("hello")
    assert 1 == 1

@pytest.fixture
def list1():
    return get_arrays()

@pytest.fixture
def p_values():
    return np.array([0.02, 0.05, 0.10])

@pytest.fixture
def list2():
    return get_arrays()


def test_get_arrays():
    arrays = get_arrays()
    assert np.array(arrays).shape == (100, 1000)


def test_get_lowest_fdr(p_values):
    fdrs = get_lowest_fdr()
    assert np.array(fdrs).shape == (3,)

def test_get_pvalues_per_index(list1, list2):
    values = get_pvalues_per_index(list1, list2)
    assert np.array(values).shape == (1000,)

def test_create_logger():
    logger = HLogger(["mock"])

def test_create_sublogger():
    logger = HLogger(["mock"])
    sublogger = logger.create_sublogger(["submock"])
    sublogger.store_result("Hello filecontent")
    logger.archive_to_file("mylog.yaml")

    gatherer = ResultsGatherer(".", "mylog.yaml")
    assert gatherer.get_individual_result(["mock","submock"]) == "Hello filecontent"

# this is me Iva

#
# this is how we
