"""
Created on Mar 25, 2018

@author: fan

Nearest Neighbor Algorithm. 
Given that one point in the two dimensional tics set is optimal, what are the
surrounding points?
"""

import logging
import numpy as np

import dataandgrid.choices.dynamic.minmaxfillquad as minmaxfillquad
import dataandgrid.choices.fixed.tics as tics

logger = logging.getLogger(__name__)


def get_tics_grid(len_choices=2000, func_type='a', tiltratio=0.0, intertiltratio=0.0):
    """    
    1. cur max linear index (Array, for each state)
    2. cur max coordinate index
    3. higher lower left right coodinates
    4. four corners linear index
    5. choice value at four corner linear index (4 array, for each state)
    
    from gentics, K is group, B is index within group, so B1, B2, BN, then B1, B2, BN, etc
    K1, K1, K1, K2, K2, K2, etc.
    
    dimension currently is K is col, B is row, this corresponds to the shape 
    higher col count is higher K, higher row count is higher B 
    """

    '''
    A. Generate Choice Grids, utility at choice grids
    '''
    len_states = 2
    choicegrid_tics_mat, B_choice_discretePoints, K_choice_discretePoints = \
        tics.gentics(len_states=len_states,
                     len_shocks=1,
                     len_choices=len_choices)

    choicegrid_tics_mat[:, 1] = choicegrid_tics_mat[:, 1] + choicegrid_tics_mat[:, 0] * tiltratio + \
                                - choicegrid_tics_mat[:, 1] * choicegrid_tics_mat[:, 0] * intertiltratio

    K_tics = choicegrid_tics_mat[:, 0]
    B_tics = choicegrid_tics_mat[:, 1]

    K_tics_reshape = np.reshape(K_tics, (len_states, len_choices))
    B_tics_reshape = np.reshape(B_tics, (len_states, len_choices))

    value = test_func(K_tics, B_tics, func_type)
    value_reshape = np.reshape(value, (len_states, len_choices))
    K_reshape = np.reshape(K_tics, (len_states, len_choices))
    B_reshape = np.reshape(B_tics, (len_states, len_choices))

    logger.debug('value_reshape:\n%s', value_reshape)
    logger.debug('np.transpose(B_reshape):\n%s', np.transpose(B_reshape))
    logger.debug('np.transpose(K_reshape):\n%s', np.transpose(K_reshape))

    '''
    B. Iteration
    loop controls how many times to zoom in.
    0 means 1 inner
    0,1 means 2 inner loops 
    '''
    cdim_row = K_choice_discretePoints
    cdim_col = B_choice_discretePoints
    B_choice_mat = B_reshape
    K_choice_mat = K_reshape

    value_list = [value]
    choicegrid_list = [choicegrid_tics_mat]

    for inner_inter in [0, 1, 2]:
        value_inner, max_val, max_idx, choicegrid_tics_mat_inner, bound_box_index = \
            max_tics_iter(value_reshape, func_type,
                          cdim_row, cdim_col,
                          K_choice_mat, B_choice_mat,
                          K_tics_reshape, B_tics_reshape)

        '''Update Vectors'''
        K_new_grid = choicegrid_tics_mat_inner[:, 0]
        B_new_grid = choicegrid_tics_mat_inner[:, 1]
        logger.debug('K_new_grid.shape:\n%s', K_new_grid.shape)
        logger.debug('B_new_grid.shape:\n%s', B_new_grid.shape)

        value_reshape = value_inner
        K_choice_mat = np.reshape(K_new_grid, (len_states, len_choices))
        B_choice_mat = np.reshape(B_new_grid, (len_states, len_choices))

        '''Append to List'''
        value_list.append(value_inner)
        choicegrid_list.append(choicegrid_tics_mat_inner)

    return value_list, choicegrid_list, max_val, max_idx, bound_box_index


def max_tics_iter(value_mat, func_type,
                  cdim_row, cdim_col,
                  K_choice_mat, B_choice_mat,
                  K_tics, B_tics):
    """
    Parameters
    ----------
    value_mat: 2d array
        each row a state, each column a choice
    cdim_row: integer
        number of rows, rows are K (K is Y)
    cdim_col: integer
        number of columns, cols are B (B is X)        
    B_choice_mat: 2d array
        each row a state, each column a potential state specific B choice
    K_choice_mat: 2d array
        each row a state, each column a potential state specific K choice
    K_tics: 1d array
        0 0 0 0.5 0.5 0.5 1 1 1 
    B_tics: 1d array
        0 0.5 1 0 0.5 1 0 0.5 1
    """

    '''
    A. Maximization Problem
    '''
    max_idx = np.nanargmax(value_mat, axis=1)
    max_val = np.nanmax(value_mat, axis=1)
    logger.debug('max_idx:\n%s', max_idx)

    '''
    B. Transform 1, max index to coordinates
    '''
    K_choice_mat_new, B_choice_mat_new, bound_box_index = \
        get_max_tics_box(max_idx, cdim_row, cdim_col,
                         K_choice_mat, B_choice_mat,
                         K_tics, B_tics, choice_vec=False)
    choicegrid_tics_mat_inner = np.column_stack((np.ravel(K_choice_mat_new), np.ravel(B_choice_mat_new)))
    logger.debug('K_choice_mat_new, B_choice_mat_new:\n%s', choicegrid_tics_mat_inner)

    '''
    C. Returns
    '''
    value_inner = test_func(K_choice_mat_new, B_choice_mat_new, func_type)
    logger.debug('value_inner:\n%s', value_inner)

    return value_inner, max_val, max_idx, choicegrid_tics_mat_inner, bound_box_index


def get_max_tics_box(max_idx, cdim_row, cdim_col,
                     K_choice_mat, B_choice_mat,
                     K_tics, B_tics, choice_vec=False):
    """    
    cdmin to be clear that we are thinking about row-major for python
    python is row major, so if data is like [X1 X2 X1 X2] and [Y1 Y1 Y2 Y2]
    Then each X1 X2 in each row, X1 X1 each col, each col different X
    Y1 Y1 in first row, each row different Y
     
    Parameters
    ----------
    max_idx: 1d array 
        an array of maximum index, each value is for a particular state
    cdim_row: integer
        number of rows, rows are K (K is Y)
    cdim_col: integer
        number of columns, cols are B (B is X)
    B_choice: 2d array
        choices for B' for all states
        row major, rows are states, cols are choices
    K_choice: 2d array
        choices for K' for all states
        row major, rows are states, cols are choices        
    choice_vec: dict of arrays 
        two arrays K and B, in dictionary, just from 1 state
    """

    '''
    C. Transform 1, max index to coordinates
    '''
    [max_idx_row, max_idx_col] = \
        np.unravel_index(max_idx, (cdim_row, cdim_col), order='C')
    logger.debug('max_idx_row:\n%s', max_idx_row)
    logger.debug('max_idx_col:\n%s', max_idx_col)

    '''
    D. Transform 2, max index to coordinates: this step is for me to visual index location, not needed. 
    '''
    if (choice_vec):
        K_mesh, B_mesh = np.meshgrid(np.arange(cdim_row), np.arange(cdim_col))
        K_reshape_mat = np.reshape(choice_vec['K'], (cdim_row, cdim_col), order='C')
        B_reshape_mat = np.reshape(choice_vec['B'], (cdim_row, cdim_col), order='C')
        logger.debug('B_reshape_mat:\n%s', B_reshape_mat)
        logger.debug('K_reshape_mat:\n%s', K_reshape_mat)

    '''
    E. Bound Box Index and Points 
    '''
    bound_box_index = find_index_box(cdim_row, cdim_col, max_idx_row, max_idx_col)
    bound_box_point_K, bound_box_point_B = find_boxidex_value(
        bound_box_index,
        cdim_row, cdim_col,
        B_choice_mat, K_choice_mat)
    '''
    F. New Grid
    '''
    top_left_K, top_right_K, bottom_left_K, bottom_right_K = \
        bound_box_point_K[0], bound_box_point_K[1], bound_box_point_K[2], bound_box_point_K[3]
    top_left_B, top_right_B, bottom_left_B, bottom_right_B = \
        bound_box_point_B[0], bound_box_point_B[1], bound_box_point_B[2], bound_box_point_B[3]

    top_left_K, top_right_K, bottom_left_K, bottom_right_K = \
        np.reshape(top_left_K, (-1, 1)), \
        np.reshape(top_right_K, (-1, 1)), \
        np.reshape(bottom_left_K, (-1, 1)), \
        np.reshape(bottom_right_K, (-1, 1))
    top_left_B, top_right_B, bottom_left_B, bottom_right_B = \
        np.reshape(top_left_B, (-1, 1)), \
        np.reshape(top_right_B, (-1, 1)), \
        np.reshape(bottom_left_B, (-1, 1)), \
        np.reshape(bottom_right_B, (-1, 1))

    '''
    G. Sub Grid
    '''
    #     K_tics = np.reshape(K_tics, (1, -1))
    #     B_tics = np.reshape(B_tics, (1, -1))
    K_choice_mat_new, B_choice_mat_new = minmaxfillquad.minmax_fill_quad(
        top_left_K, top_right_K, bottom_left_K, bottom_right_K,
        top_left_B, top_right_B, bottom_left_B, bottom_right_B,
        K_tics, B_tics)

    return K_choice_mat_new, B_choice_mat_new, bound_box_index


def test_func(K_tics, B_tics, func_type='b'):
    if (func_type == 'a'):
        value = 0.5 + K_tics - K_tics ** 2 + \
                0.2 + 0.1 * B_tics - 0.40 * B_tics ** 2 + \
                -0.02 * K_tics * B_tics
    else:
        value = 0.5 + K_tics - K_tics ** 2 + \
                0.2 + 0.5 * B_tics - 0.40 * B_tics ** 2 + \
                -0.02 * K_tics * B_tics

    return value


def find_index_box(bigbox_row_count, bigbox_col_count,
                   max_idx_row, max_idx_col):
    """Given coordinate, find containing index box
    
    Parameters
    ----------
    bigbox_row_count: int
        starts at 1
    point_row_idx: int
        starts at 0
        
    B is row, K is column
    """

    bound_box_upper = np.minimum(max_idx_row + 1, bigbox_row_count - 1)
    bound_box_lower = np.maximum(max_idx_row - 1, 0)

    bound_box_right = np.minimum(max_idx_col + 1, bigbox_col_count - 1)
    bound_box_left = np.maximum(max_idx_col - 1, 0)

    logger.debug('\n bound_box_upper, bound_box_lower, bound_box_left, bound_box_right:\n%s',
                 np.column_stack((bound_box_upper, bound_box_lower, bound_box_left, bound_box_right)))

    return [bound_box_upper, bound_box_lower, bound_box_left, bound_box_right]


def find_boxidex_value(bound_box_index, bigbox_row_count, bigbox_col_count,
                       B_choice_mat, K_choice_mat):
    """
    Given box index, find the associated current b' and k' choice points, associated
    with top left, top right, bottom left, and bottom right.
    
    B is row, K is column 
    """

    top_left_linear_idx = np.ravel_multi_index(np.row_stack((bound_box_index[0], bound_box_index[2])),
                                               (bigbox_row_count, bigbox_col_count), order='C')
    top_right_linear_idx = np.ravel_multi_index(np.row_stack((bound_box_index[0], bound_box_index[3])),
                                                (bigbox_row_count, bigbox_col_count), order='C')
    bottom_left_linear_idx = np.ravel_multi_index(np.row_stack((bound_box_index[1], bound_box_index[2])),
                                                  (bigbox_row_count, bigbox_col_count), order='C')
    bottom_right_linear_idx = np.ravel_multi_index(np.row_stack((bound_box_index[1], bound_box_index[3])),
                                                   (bigbox_row_count, bigbox_col_count), order='C')

    bound_box_linear_idx = np.row_stack((top_left_linear_idx,
                                         top_right_linear_idx,
                                         bottom_left_linear_idx,
                                         bottom_right_linear_idx))

    len_states = B_choice_mat.shape[0]
    B_points = B_choice_mat[np.arange(len_states), bound_box_linear_idx]
    K_points = K_choice_mat[np.arange(len_states), bound_box_linear_idx]

    return K_points, B_points
