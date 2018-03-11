"""

Tests for the *BaggingTree* class.

"""

import sys
import pytest
import numpy as np
from numpy.testing.utils import assert_array_almost_equal, assert_raises
from src.model_code.baggingtree import BaggingTree

@pytest.fixture
def setup():
    np.random.seed(1)
    X_train = np.random.normal(size=(10,2))
    y_train = X_train[:,0] + X_train[:,1] + np.random.normal(size=(10))
    y_test = np.ones((10,2))
    return X_train, y_train, y_test
  

def test_baggingtree_if_same_if_new_instance(setup):
    X_train, y_train, y_test = setup
    bagged_tree = BaggingTree(random_seed=1, b_iterations=5)
    first_prediction = bagged_tree.fit(X_train, y_train).predict(y_test)
    bagged_tree = BaggingTree(random_seed=1, b_iterations=5)
    second_prediction = bagged_tree.fit(X_train, y_train).predict(y_test)
    assert_array_almost_equal(first_prediction, second_prediction)

def test_baggingtree_if_different_if_same_instance(setup):
    X_train, y_train, y_test = setup
    bagged_tree = BaggingTree(random_seed=1, b_iterations=5)
    first_prediction = bagged_tree.fit(X_train, y_train).predict(y_test)
    second_prediction = bagged_tree.fit(X_train, y_train).predict(y_test)
    # We check if they are not equal.
    # The probability that they are equal is so low that we should be worried elsewise.
    assert_raises(AssertionError, assert_array_almost_equal, first_prediction, second_prediction)

def test_baggingtree_two_predicts_the_same(setup):
    X_train, y_train, y_test = setup
    bagged_tree = BaggingTree(random_seed=1, b_iterations=5)
    fitted_tree = bagged_tree.fit(X_train, y_train)
    first_predict = fitted_tree.predict(y_test)
    second_predict = fitted_tree.predict(y_test)
    assert_array_almost_equal(first_predict, second_predict)
    

def test_baggingtree_with_zeros_and_ones():
    bagged_tree = BaggingTree(random_seed=1, b_iterations=5)
    fitted_tree = bagged_tree.fit(np.zeros((10,2)), np.zeros(10))
    prediction = fitted_tree.predict(np.ones((10,2)))
    assert_array_almost_equal(prediction,np.zeros(10))

def test_test():
    pass


if __name__ == '__main__':
    status = pytest.main([sys.argv[1]])
    sys.exit(0)
