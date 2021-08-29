'''
Created on Aug 17, 2018

@author: fan

This calles functions from local estimate, adds a loop to reduce repetition
'''

import estimation.postprocess.process_main as esticomp
import invoke.local_estimate as invoke_esti
import invoke.local_simulate as invoke_simu


def multistart_esti(paramstr_key_list=None,
                    run_size='x',
                    esti_spec_key_root='esti_test',
                    moment_key=1,
                    momset_key=2,
                    esti_invoke_set=1,
                    simu_invoke_set=2,
                    simu_combo_type_list_ab='a',
                    esti_combo_type_list_ab='c',
                    simu_combo_type_list_date='20180814',
                    esti_combo_type_list_date='20180815',
                    integrated=False,
                    sync_ecs_init=True,
                    simulate_grid=False,
                    combine_results=False,
                    aws_type='batch',
                    job_queue='Spot',
                    simu_save_directory_main='simu',
                    esti_save_directory_main='esti'):
    """Single Parameter Estimation Tool
    
    When estimating a single parameter, first update cloud while simulating over
    grid points of the single estimation parameter from min to max
    
    Then estimate the single parameter using different estimation methods along different
    starting points. 
    
    This is for:
    - testing to make sure things work, because I know true minimum, see if 
        estimation can find true minimum. 
    - before each full joint multi-parameter estimation, run the single parameter
        estimation using the tool here.
        
    Note for all estimation: multiperiod is true by default
    
    Examples
    --------
    import invoke.run_aws_esti_sync.local_estimate_singleparm as svesti_sigle
    svesti_sigle.multistart_esti(
                        paramstr_key_list=None,                           
                        run_size='x',
                        esti_spec_key_root = 'esti_test',
                        moment_key=1,
                        momset_key=2,
                        simu_combo_type_list_ab = 'a',
                        esti_combo_type_list_ab = 'c',
                        simu_combo_type_list_date = '20180814',
                        esti_combo_type_list_date = '20180815',
                        integrated=False,
                        sync_ecs_init=True, 
                        simulate_grid=False,
                        combine_results=True)
    """

    '''
    A. Hard-coded values
        invoke_set = 2: simulation done along detailed vector grid
    '''

    '''
    B. Integrated or not
    '''
    if (integrated):
        ITG = '_ITG'
    else:
        ITG = ''

    '''
    C. Which parameter to simulate and estimate
    '''
    if (paramstr_key_list is None):
        paramstr_key_list = ['beta']

    '''
    D. Estimation Specifications, run through fixed set
    '''
    # _simu important, this will plot out objective

    esti_spec_key_for_simu = esti_spec_key_root + '_11_simu'
    #     aws_type = 'batch'
    #     job_queue = 'Spot'

    '''
    1. Simulate grid over the 4 parameters
    '''
    #     if (simulate_grid):
    combo_type_list_date = simu_combo_type_list_date + run_size + ITG
    sync_ecs = sync_ecs_init
    paramstr_key_list_quick = paramstr_key_list
    if (combine_results == False):
        if ('list_' in str(paramstr_key_list_quick)):
            paramstr_key_list_quick = ['beta']
        invoke_simu.run_here_manage_fargate([simu_invoke_set], sync_ecs,
                                            esti_spec_key_for_simu=esti_spec_key_for_simu,
                                            combo_type_list_ab=simu_combo_type_list_ab,
                                            combo_type_list_date=combo_type_list_date,
                                            paramstr_key_list=paramstr_key_list_quick,
                                            moment_key=moment_key, momset_key=momset_key,
                                            save_directory_main=simu_save_directory_main,
                                            aws_type=aws_type, job_queue=job_queue)

    '''
    2. Estimate 4 parameters using different methods
    '''
    combo_type_list_date = esti_combo_type_list_date + run_size + ITG
    sync_ecs = False
    #     for run in [11,12,21,22,31,32]:
    for run in [11, 21, 31]:
        #     for run in [11]:
        esti_spec_key = esti_spec_key_root + '_' + str(run)
        if (combine_results == False):
            invoke_list_fargate = [esti_invoke_set]
            invoke_esti.estimate_fargate(esti_invoke_set,
                                         sync_ecs=sync_ecs,
                                         esti_spec_key=esti_spec_key,
                                         combo_type_list_ab=esti_combo_type_list_ab,
                                         combo_type_list_date=combo_type_list_date,
                                         paramstr_key_list=paramstr_key_list,
                                         moment_key=moment_key, momset_key=momset_key,
                                         save_directory_main=esti_save_directory_main,
                                         aws_type=aws_type, job_queue=job_queue)
    # do it here to pick up esti_spec_key
    if (combine_results):
        '''
        After AWS run, sync local and aws, now results in different folders 
        based on initial parameters and estimation method. Use method here to 
        pull results together into common panda csv file and also generate 
        single graph with all subfolder estimation iteration results. 
        '''
        if (integrated):
            exo_or_endo = '_exoitg'
            # see lines 109 in steady_loop_integrate.steady_loop_integrate.py
            # see lines 226 in invoke.saverun.local_estimate_save line 226
            exo_or_endo_graph_row_select = exo_or_endo + '_wgtJitg'
        else:
            exo_or_endo = '_exo'
            # see lines 121, 145 in steadyinnerloop.steady_loop_inner.py
            # see lines 226 in invoke.saverun.local_estimate_save line 226
            exo_or_endo_graph_row_select = exo_or_endo + '_wgtJ'

        esticomp.search_combine_indi_esti(paramstr_key_list,
                                          esti_combo_type_list_ab,
                                          combo_type_list_date,
                                          esti_spec_key,
                                          moment_key=moment_key,
                                          momset_key=momset_key,
                                          exo_or_endo_graph_row_select=exo_or_endo_graph_row_select)
