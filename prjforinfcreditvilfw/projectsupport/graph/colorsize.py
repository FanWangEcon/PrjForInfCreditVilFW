'''
Created on May 13, 2018

@author: fan

import projectsupport.graph.color as support_colors
'''


def choice_cts_colors():
    """
    import projectsupport.graph.color as support_colors
    cts_colors = support_colors.choice_cts_colors()
    """
    #     np.random.seed(1394)
    #
    #     colorBn = np.random.rand(3,)
    #     colorKn = np.random.rand(3,)
    #     colorCc = np.random.rand(3,)
    #     colorPr = np.random.rand(3,)

    color_dict = {'colorBn': 'b',
                  'colorKn': 'r',
                  'colorCc': 'k',
                  'colorPr': 'g',
                  'colorYy': 'y'}

    return color_dict


def seven_cate_colors():
    """
    import projectsupport.graph.color as support_colors
    discrete_colors = support_colors.seven_cate_colors()
    
    """
    """Unified Location for Coloring"""
    colorSet = {0: 'b',
                1: 'g',
                2: 'r',
                102: 'r',
                3: 'c',
                4: 'm',
                104: 'm',
                5: 'y',
                105: 'y',
                6: 'k'}

    return colorSet


def scatter_size(x_vec_len):
    """
    Aggregation graphs, plot larger dot if the vecotr has less points
    
    Parameters
    ----------
    x_vec_len: int
        x_vec_len = 1 if combo_list single element, combo_type[2] == None, not looping over, need larger sizes
        x_vec_len = 5 if combo_list has multiple (5) elements.
        
    Examples
    --------
    import projectsupport.graph.color as support_colors
    x_vec_len = 1
    line_specs = support_colors.scatter_size(x_vec_len)
    scatter_size = line_specs['scatter_size']
    scatter_alpha = line_specs['scatter_alpha']
    scatter_marker = line_specs['scatter_marker']
    line_width = line_specs['line_width']
    line_alpha = line_specs['line_alpha']
    """

    if (x_vec_len == 1):
        line_specs = {
            'scatter_size': 15 ** 2,
            'scatter_alpha': 0.70,
            'scatter_marker': 'X',
            'line_width': 1,
            'line_alpha': 0.70,
        }
    elif (x_vec_len >= 2 and x_vec_len <= 4):
        line_specs = {
            'scatter_size': 8 ** 2,
            'scatter_alpha': 1,
            'scatter_marker': 'X',
            'line_width': 1,
            'line_alpha': 1,
        }
    elif (x_vec_len >= 5 and x_vec_len <= 8):
        line_specs = {
            'scatter_size': 4 ** 2,
            'scatter_alpha': 1,
            'scatter_marker': 'X',
            'line_width': 1,
            'line_alpha': 0.4,
        }
    else:
        line_specs = {
            'scatter_size': 2 ** 2,
            'scatter_alpha': 1,
            'scatter_marker': 'X',
            'line_width': 1,
            'line_alpha': 0.2,
        }

    return line_specs
