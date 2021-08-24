'''
Created on Jul 12, 2018

@author: fan
 '''

import numpy as np


def integrate_singlevar(p_of_X_c_A,
                        p_of_A=None,
                        X_vec=None,
                        A_vec=None,
                        ravel=True,
                        return_list=['p_of_X']):
    '''
    Dealing with one single variable 
        
    Let size(A) = M, size(X) = N
        Parameters
        ----------
        p_of_X_c_A: 2d numpy array
            N by M
            P(X|A), discritized probability of X=x conditional on A=a
            from solving the model elsewhere.  
            probabilities for some variable X, one single variable

        X_vec: 1d numpy array
            N elements
            
        p_of_A: 1d numpy array
            M elements
            P(A), discretized exogenous probability of A=a
                    
            
    Returns
    -------
    p_of_X: numpy 1d array 
        marginal distribution of X
    p_of_X_and_A: numpy 2d array
        joint distribution of X and A
    E_of_X_c_A: numpy array
        for each point along A, Asset distribution integrated
    E_of_X: scalar
    
    
    Example
    -------    
    import solusteady.integrate as soluintegrate
    p_of_X = integrate_singlevar(p_of_X_c_A, p_of_A=None, return_list=['p_of_X'])['p_of_X']
        
    '''

    return_dict = {}

    '''
    p(X) = sum_{A} ( p(X|A)*p(A) )
    '''
    if (p_of_A is not None):

        if ('p_of_X' in return_list):
            # Marginal Distribution of X
            # (N by M) x (M by 1) = N by 1
            p_of_X = np.matmul(p_of_X_c_A, np.reshape(p_of_A, (-1, 1)))
            if (ravel):
                p_of_X = np.ravel(p_of_X)
            return_dict['p_of_X'] = p_of_X

        if ('p_of_X_and_A' in return_list):
            # Joint Distribution of X and A
            p_of_X_and_A = p_of_X_c_A * np.reshape(p_of_A, (-1, 1))
            if (p_of_X_and_A):
                p_of_X = np.ravel(p_of_X_and_A)
            return_dict['p_of_X_and_A'] = p_of_X_and_A

    '''
    E(X|A) = sum_{X} ( p(X|A)*X )
    '''
    if (X_vec is not None):

        if any(ret in return_list for ret in ('E_of_X', 'E_of_X_c_A')):
            # Expected value of X conditional on A
            # (1 by N) x (N by M) = 1 by M
            E_of_X_c_A = np.matmul(np.reshape(X_vec, (1, -1)), p_of_X_c_A)

            if ('E_of_X' in return_list):
                # (1 by N) x (M by 1) = N by 1
                if (p_of_A is not None):
                    E_of_X = np.matmul(E_of_X_c_A, np.reshape(p_of_A, (-1, 1)))
                    if (ravel):
                        E_of_X = np.ravel(E_of_X)
                    return_dict['E_of_X'] = E_of_X

                    # Happens here after E_of_X, do not ravel E_of_X_c_A before E_of_X calculated
            if ('E_of_X_c_A' in return_list):
                if (ravel):
                    E_of_X_c_A = np.ravel(E_of_X_c_A)
                return_dict['E_of_X_c_A'] = np.ravel(E_of_X_c_A)

    return return_dict


def integrate_multivar(E_of_Xv_c_A, p_of_A):
    '''
    Dealing with multiple X variables 
    Already integrated averages from model without type for example
        
    Let size(A) = M, size(Xv) = Q
        
    Parameters
    ----------
    E_of_Xv_c_A: 2d numpy array
        E(X|A), E, each row a different X
        each column a different A
        Q by M matrix  
    p_of_A: 1d numpy array 
        P(A), discretized exogenous probability of A=a
        M len        
    '''

    # Expected of X integrated over A
    # (Q by M) x (M by 1)  
    E_of_Xv = np.matmul(E_of_Xv_c_A, np.reshape(p_of_A, (-1, 1)))

    return_dict = {}
    return_dict['E_of_Xv'] = np.ravel(E_of_Xv)

    return E_of_Xv
