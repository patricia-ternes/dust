# Imports
from generate_data.ensemble_kalman_filter_data import *
from utils import *

import numpy as np
import pytest
import sys
sys.path.append('../stationsim/')

from ensemble_kalman_filter import EnsembleKalmanFilter, ActiveAgentNormaliser

# Test data
round_destination_data = get_round_destination_data()

pair_coords_data = get_pair_coords_data()

pair_coords_error_data = get_pair_coords_error_data()

separate_coords_data = get_separate_coords_data()

separate_coords_error_data = get_separate_coords_error_data()

random_destination_data = get_random_destination_data()

n_active_agents_base_data = get_n_active_agents_base_data()

n_active_agents_mean_data = get_n_active_agents_mean_data()

n_active_agents_max_data = get_n_active_agents_max_data()

n_active_agents_min_data = get_n_active_agents_min_data()

population_mean_base_data = get_population_mean_base_data()

population_mean_mean_data = get_population_mean_mean_data()

population_mean_min_data = get_population_mean_min_data()

population_mean_max_data = get_population_mean_max_data()

mean_data = get_mean_data()

error_normalisation_type_data = get_error_normalisation_type_data()

distance_error_default_data = get_distance_error_default_data()

distance_error_base_data = get_distance_error_base_data()

calculate_rmse_default_data = get_calculate_rmse_default_data()

make_obs_error_data = get_make_obs_error_data()

make_gain_matrix_data = get_make_gain_matrix_data()

separate_coords_exits_data = get_separate_coords_exits_data()

update_status_data = get_update_status_data()

make_noise_data = get_make_noise_data()

update_state_mean_data = get_update_state_mean_data()

np_cov_data = get_np_cov_data()

destination_vector_data = get_destination_vector_data()

origin_vector_data = get_origin_vector_data()

# Tests
@pytest.mark.parametrize('dest, n_dest, expected', round_destination_data)
def test_round_destination(dest, n_dest, expected):
    """
    Test EnsembleKalmanFilter.round_destination()

    Test that the round_destination method rounds the destination exit number
    to the nearest integer value modulo the number of gates.

    Parameters
    ----------
    dest : float
        Floating point value of the estimated destination number
    n_dest : int
        The integer number of possible destination gates
    expected : int
        Expected result of round_destination
    """
    assert EnsembleKalmanFilter.round_destination(dest, n_dest) == expected


@pytest.mark.parametrize('arr1, arr2, expected', pair_coords_data)
def test_pair_coords(arr1, arr2, expected):
    """
    Test EnsembleKalmanFilter.pair_coords()

    Test that the pair_coords method returns an appropriate list when provided
    with two list-like input arrays, i.e. given
        arr1 = [x0, x1, ..., xN]
        arr2 = [y0, y1, ..., yN]

    the method returns a list of
        [x0, y0, x1, y1, ..., xN, yN]

    Parameters
    ----------
    arr1 : list-like
        First list of elements
    arr2 : list-like
        Second list of elements
    expected : list
        Expected resulting list of pair_coords() as outlined above
    """
    assert EnsembleKalmanFilter.pair_coords(arr1, arr2) == expected


@pytest.mark.parametrize('arr1, arr2, expected', pair_coords_error_data)
def test_pair_coords_error(arr1, arr2, expected):
    """
    Test that EnsembleKalmanFilter.pair_coords() throws an appropriate error

    Test that, when provided with arrays of incompatible length, pair_coords()
    throws an appropriate error.

    Parameters
    ----------
    arr1 : list-like
        First list of elements
    arr2 : list-like
        Second list of elements
    expected : Exception
        Expected ValueError exception
    """
    with expected:
        assert EnsembleKalmanFilter.pair_coords(arr1, arr2)


@pytest.mark.parametrize('arr, expected1, expected2', separate_coords_data)
def test_separate_coords(arr, expected1, expected2):
    """
    Test that EnsembleKalmanFilter.separate_coords() splits coordinate array
    into two arrays

    Test that separate_coords() splits an array like
        [x0, y0, x1, y1, ..., xN, yN]

    into two arrays like
        [x0, x1, ..., xN]
        [y0, y1, ..., yN]

    Parameters
    ----------
    arr : list-like
        Input array of alternating x-y's
    expected1 : list-like
        Array of x-coordinates
    expected2 : list-like
        Array of y-coordinates
    """
    assert EnsembleKalmanFilter.separate_coords(arr) == (expected1, expected2)


@pytest.mark.parametrize('arr, expected', separate_coords_error_data)
def test_separate_coords_error(arr, expected):
    """
    Test that EnsembleKalmanFilter.separate_coords() throws an appropriate
    error

    Test that, when provided with an array of odd length, separate_coords()
    throws an appropriate error

    Parameters
    ----------
    arr : list-like
        Input list
    expected : Exception
        Expected ValueError exception
    """
    with expected:
        assert EnsembleKalmanFilter.separate_coords(arr)


@pytest.mark.parametrize('gates_in, gates_out, gate_in',
                         random_destination_data)
def test_make_random_destination(gates_in, gates_out, gate_in):
    enkf = set_up_enkf()
    gate_out = enkf.make_random_destination(gates_in, gates_out, gate_in)
    assert gate_out != gate_in
    assert 0 <= gate_out < enkf.n_exits


def test_error_normalisation_default_init():
    # Set up enkf
    enkf = set_up_enkf()
    assert enkf.error_normalisation is None


@pytest.mark.parametrize('n_active, expected', n_active_agents_base_data)
def test_get_n_active_agents_base(n_active, expected):
    enkf = set_up_enkf()
    enkf.error_normalisation = ActiveAgentNormaliser.BASE
    enkf.base_model.pop_active = n_active
    assert enkf.get_n_active_agents() == expected


@pytest.mark.parametrize('ensemble_active, expected',
                         n_active_agents_mean_data)
def test_get_n_active_agents_mean_en(ensemble_active, expected):
    enkf = set_up_enkf()
    enkf.error_normalisation = ActiveAgentNormaliser.MEAN_EN
    for i, model in enumerate(enkf.models):
        model.pop_active = ensemble_active[i]
    assert enkf.get_n_active_agents() == expected


@pytest.mark.parametrize('ensemble_active, expected',
                         n_active_agents_max_data)
def test_get_n_active_agents_max_en(ensemble_active, expected):
    enkf = set_up_enkf()
    enkf.error_normalisation = ActiveAgentNormaliser.MAX_EN
    for i, model in enumerate(enkf.models):
        model.pop_active = ensemble_active[i]
    assert enkf.get_n_active_agents() == expected


@pytest.mark.parametrize('ensemble_active, expected',
                         n_active_agents_min_data)
def test_get_n_active_agents_min_en(ensemble_active, expected):
    enkf = set_up_enkf()
    enkf.error_normalisation = ActiveAgentNormaliser.MIN_EN
    for i, model in enumerate(enkf.models):
        model.pop_active = ensemble_active[i]
    assert enkf.get_n_active_agents() == expected


@pytest.mark.parametrize('diffs, n_active, expected',
                         population_mean_base_data)
def test_get_population_mean_base(diffs, n_active, expected):
    enkf = set_up_enkf()
    enkf.error_normalisation = ActiveAgentNormaliser.BASE
    enkf.base_model.pop_active = n_active
    diffs = np.array(diffs)

    assert enkf.get_population_mean(diffs) == expected


@pytest.mark.parametrize('diffs, ensemble_active, expected',
                         population_mean_mean_data)
def test_get_population_mean_mean_en(diffs, ensemble_active, expected):
    # Set up enkf
    enkf = set_up_enkf()
    enkf.error_normalisation = ActiveAgentNormaliser.MEAN_EN

    # Define number of active agents for each ensemble member
    for i, model in enumerate(enkf.models):
        model.pop_active = ensemble_active[i]

    # Define results and truth values
    diffs = np.array(diffs)

    assert enkf.get_population_mean(diffs) == expected


@pytest.mark.parametrize('diffs, ensemble_active, expected',
                         population_mean_min_data)
def test_get_population_mean_min_en(diffs, ensemble_active, expected):
    # Set up enkf
    enkf = set_up_enkf()
    enkf.error_normalisation = ActiveAgentNormaliser.MIN_EN

    # Define number of active agents for each ensemble member
    for i, model in enumerate(enkf.models):
        model.pop_active = ensemble_active[i]

    # Define results and truth values
    diffs = np.array(diffs)

    assert enkf.get_population_mean(diffs) == expected


@pytest.mark.parametrize('diffs, ensemble_active, expected',
                         population_mean_max_data)
def test_get_population_mean_max_en(diffs, ensemble_active, expected):
    # Set up enkf
    enkf = set_up_enkf()
    enkf.error_normalisation = ActiveAgentNormaliser.MAX_EN

    # Define number of active agents for each ensemble member
    for i, model in enumerate(enkf.models):
        model.pop_active = ensemble_active[i]

    # Define results and truth values
    diffs = np.array(diffs)

    assert enkf.get_population_mean(diffs) == expected


@pytest.mark.parametrize('results, truth, expected', mean_data)
def test_get_mean(results, truth, expected):
    enkf = set_up_enkf()

    results = np.array(results)
    truth = np.array(truth)

    assert enkf.get_mean_error(results, truth) == expected


x = '''error_normalisation, results, truth, active_pop, ensemble_active,
       expected'''


@pytest.mark.parametrize(x, error_normalisation_type_data)
def test_error_normalisation_type(error_normalisation, results, truth,
                                  active_pop, ensemble_active, expected):
    enkf = set_up_enkf(error_normalisation)

    results = np.array(results)
    truth = np.array(truth)

    for i, model in enumerate(enkf.models):
        model.pop_active = ensemble_active[i]

    enkf.base_model.pop_active = active_pop

    assert enkf.get_mean_error(results, truth) == expected


@pytest.mark.parametrize('x_error, y_error, expected',
                         distance_error_default_data)
def test_make_distance_error_default(x_error, y_error, expected):
    enkf = set_up_enkf()

    x_error = np.array(x_error)
    y_error = np.array(y_error)

    assert pytest.approx(expected) == enkf.make_distance_error(x_error,
                                                               y_error)


@pytest.mark.parametrize('x_error, y_error, n_active, expected',
                         distance_error_base_data)
def test_make_distance_error_base(x_error, y_error, n_active, expected):
    enkf = set_up_enkf(ActiveAgentNormaliser.BASE)
    enkf.base_model.pop_active = n_active

    assert pytest.approx(expected) == enkf.make_distance_error(x_error,
                                                               y_error)


@pytest.mark.parametrize('x_truth, y_truth, x_result, y_result, expected',
                         calculate_rmse_default_data)
def test_calculate_rmse_default(x_truth, y_truth,
                                x_result, y_result, expected):
    # Setup
    enkf = set_up_enkf()

    # Convert all inputs to arrays
    x_truth = np.array(x_truth)
    x_result = np.array(x_result)
    y_truth = np.array(y_truth)
    y_result = np.array(y_result)

    results = enkf.calculate_rmse(x_truth, y_truth, x_result, y_result)
    assert results[0] == expected


x = 'truth, result, active_pop, ensemble_active, normaliser, expected'

@pytest.mark.parametrize(x, make_obs_error_data)
def test_make_obs_error(truth, result,
                        active_pop, ensemble_active,
                        normaliser, expected):
    """
    Test that enkf.make_obs_error() correctly calculates observation errors,
    ignoring changes to how many agents are active in the base model and the
    ensemble-member models.
    """
    # Setup
    enkf = set_up_enkf(normaliser)

    # Set active agents
    enkf.base_model.pop_active = active_pop
    for i, model in enumerate(enkf.models):
        model.pop_active = ensemble_active[i]

    # Convert to arrays where necessary
    truth = np.array(truth)
    result = np.array(result)

    # Assertion
    assert enkf.make_obs_error(truth, result) == expected


@pytest.mark.parametrize('state_ensemble, data_covariance, H, expected',
                         make_gain_matrix_data)
def test_make_gain_matrix(state_ensemble, data_covariance, H, expected):
    enkf = set_up_enkf()
    H_transpose = H.T
    result = enkf.make_gain_matrix(state_ensemble,
                                   data_covariance,
                                   H, H_transpose)
    np.testing.assert_allclose(result, expected)


@pytest.mark.parametrize('state_vector, pop_size, expected',
                         separate_coords_exits_data)
def test_separate_coords_exits(state_vector, pop_size, expected):
    enkf = set_up_enkf()
    enkf.population_size = pop_size
    np.testing.assert_array_equal

    result = enkf.separate_coords_exits(state_vector)

    for i in range(len(result)):
        np.testing.assert_array_equal(result[i], expected[i])


@pytest.mark.parametrize('m_statuses, filter_status, expected',
                         update_status_data)
def test_update_status(m_statuses, filter_status, expected):
    enkf = set_up_enkf()

    enkf.active = filter_status

    for i, s in enumerate(m_statuses):
        enkf.models[i].status = s

    enkf.update_status()

    assert enkf.active == expected


@pytest.mark.parametrize('array, expected', np_cov_data)
def test_np_cov(array, expected):
    result = np.cov(array)
    assert result.shape == expected.shape
    np.testing.assert_array_almost_equal(result, expected)


@pytest.mark.parametrize('shape, R_vector', make_noise_data)
def test_make_noise(shape, R_vector):
    enkf = set_up_enkf()

    if isinstance(shape, int):
        assert len(R_vector) == shape
    elif isinstance(shape, tuple):
        assert (len(R_vector) == shape[0]) or (len(R_vector) == shape[1])

    all_samples = list()

    for i in range(1000):
        # Pass seed for test reproducibility
        noise = enkf.make_noise(shape, R_vector, seed=i)
        all_samples.append(noise)

    all_samples = np.array(all_samples)

    for i in range(shape):
        m = np.mean(all_samples[:, i])
        s = np.std(all_samples[:, i])
        assert m == pytest.approx(0, abs=0.1)
        assert s == pytest.approx(R_vector[i], 0.2)


@pytest.mark.parametrize('state_ensemble, expected', update_state_mean_data)
def test_update_state_mean(state_ensemble, expected):
    enkf = set_up_enkf()

    result = enkf.update_state_mean(state_ensemble)

    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize('agent_destinations, expected',
                         destination_vector_data)
def test_make_base_destination_vector(agent_destinations, expected):
    enkf = set_up_enkf()

    for i, agent in enumerate(enkf.base_model.agents):
        agent.loc_desire = np.array(agent_destinations[i])

    result = enkf.make_base_destinations_vector()
    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize('origins, statuses, expected', origin_vector_data)
def test_make_base_origin_vector(origins, statuses, expected):
    enkf = set_up_enkf()

    for i, agent in enumerate(enkf.base_model.agents):
        agent.status = statuses[i]
        agent.loc_start = origins[i]

    result = enkf.make_base_origins_vector()
    np.testing.assert_array_equal(result, expected)
