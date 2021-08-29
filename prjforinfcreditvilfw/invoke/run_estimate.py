'''
Created on July 29, 2018

@author: fan

Invoke
'''

import logging
import time

import estimation.estimate as esti
import parameters.combo as paramcombo
import parameters.parse_combo_type as parsecombotype
import parameters.runspecs.compute_specs as computespec
import parameters.runspecs.estimate_specs as estispec
import projectsupport.hardcode.file_name as proj_hardcode_filename
import projectsupport.hardcode.string_shared as hardstring
import projectsupport.systemsupport as proj_sys_sup

logger = logging.getLogger(__name__)


def invoke_estimate(combo_type,
                    compute_spec_key='l-ng-s-x', esti_spec_key='',
                    moment_key=0, momset_key=1,
                    ge=False, multiprocess=False,
                    graph_list=None, save_directory_main='esti',
                    logging_level=logging.WARNING,
                    log_file=True,
                    log_file_suffix=''):
    """
    For Fargate or Batch, by this point, a task or job has already been
    added or submitted. This is running the submitted task and job.     
    """

    '''
    3. Obtaining compute specifications
        - compute_specs are the same for all param_combo in combo_list
    '''
    cur_compute_spec = computespec.compute_set(compute_spec_key)
    print('cur_compute_spec:', cur_compute_spec)
    aws_fargate = cur_compute_spec['aws_fargate']
    ge = cur_compute_spec['ge']
    multiprocess = cur_compute_spec['multiprocess']

    '''
    2a. Generate Path, Download TOP JSON and MPOlY Surface from S3 
    '''
    # Do not have to specify in compute_set fargate true or false, at this point
    # already on cloud or local, the fargate true of false is just for task/job
    # submissions
    compesti_short_name = hardstring.gen_compesti_short_name(compute_spec_key, esti_spec_key, moment_key,
                                                             momset_key)
    cur_esti_spec = estispec.estimate_set(esti_spec_key, moment_key=moment_key, momset_key=momset_key)
    compesti_specs = cur_compute_spec.copy()
    compesti_specs.update(cur_esti_spec)
    compesti_specs['compesti_short_name'] = compesti_short_name

    # Also add save_directory_main to compesti, this way can get the parameter name when json is called
    compesti_specs['save_directory_main'] = save_directory_main

    '''
    ESTIMATION FOLDER LEVEL 1
    '''
    sub_folder_name = proj_sys_sup.gen_path(combo_type, st_type='simuesti_subfolder')
    save_directory = proj_sys_sup.get_paths(save_directory_main, sub_folder_name=sub_folder_name)

    '''
    If dealing with ESR3 AWS, MPOLY file like *e_20201025x_esr_medtst_list_tKap_mlt_ce1a2_mpoly_reg_coef.csv* is
    on S3, in structure like: thaijmp202010/esti/e_20201025x_esr_medtst_list_tKap_mlt_ce1a2/. Need to download
    the file to /data/esti/e_20201025x_esr_medtst_list_tKap_mlt_ce1a2/ in the docker container, for estimation
    function to call to generate estimation approximation surface
    '''
    logger.warning(f'{compesti_specs["bl_mpoly_approx"]=} and {proj_sys_sup.check_is_on_aws_docker()=}')
    if compesti_specs['bl_mpoly_approx'] and proj_sys_sup.check_is_on_aws_docker():
        spn_docker_path_mpoly_reg_coef = proj_hardcode_filename.get_path_to_mpoly_reg_coef(
            combo_type, main_folder_name=save_directory_main)
        logger.warning(f'{spn_docker_path_mpoly_reg_coef=}')
        spn_s3_path_mpoly_reg_coef = proj_sys_sup.s3_download_to_docker_mpoly(spn_docker_path_mpoly_reg_coef)
        logger.warning(f'{spn_s3_path_mpoly_reg_coef=}')

    '''
    ERS5 and ERS7 estimation, need to load the jsontop file which is generated in local aws from ESR4, and uploaded 
    to S3, and then now needs to be downloaded to the docker container.  
    '''
    logger.warning(f'{parsecombotype.check_combo_type_postmpoly(combo_type)=}')
    if parsecombotype.check_combo_type_postmpoly(combo_type) and proj_sys_sup.check_is_on_aws_docker():
        spn_docker_path_top_json = proj_hardcode_filename.get_path_to_top_json(
            combo_type, main_folder_name=save_directory_main)
        logger.warning(f'{spn_docker_path_top_json=}')
        spn_s3_path_top_json = proj_sys_sup.s3_download_to_docker_mpoly(spn_docker_path_top_json)
        logger.warning(f'{spn_s3_path_top_json=}')

    '''
    2b. Combo_list
    This REQUIRES for ERS5 and ERS7 that TOP JSon is already loaded from the code just above 
    '''
    combo_list = paramcombo.get_combo(combo_type, compesti_specs)
    logger.critical('combo_list:\n%s', combo_list)

    '''Start Timer'''
    startTime = time.time()

    '''
    4. Looping over combo_list
    '''
    for param_combo in combo_list:
        '''
        4a. obtain current specifications for estimation
            + esti_specs could be the same for all param_combo if the specs come frm cur_esti_spec Line 73
            + esti_specs would be different if esti_spec_key = 'nonespec', and parameters insidecombo_list_c_esti.py
                override
            + Example:
                - combo_type_list:
                    + a list of or just 1 different initial parameters
                - esti_method
                    + 'MomentsSimuStates'
                - param_esti_list_key
                    + 'list_policy_Kap'
                - moment_type
                    + ['a','20180724_test']
                - esti_option_type
                    + 2
                - esti_func_type:
                    + nldmd
        '''

        esti_method = param_combo['esti_method']
        moments_type = param_combo['moments_type']
        esti_option_type = param_combo['esti_option_type']
        esti_func_type = param_combo['esti_func_type']

        esti.estimate(combo_type, param_combo,
                      esti_method=esti_method,
                      moments_type=moments_type,
                      esti_option_type=esti_option_type,
                      esti_func_type=esti_func_type,
                      compesti_specs=compesti_specs,
                      ge=ge, multiprocess=multiprocess,
                      graph_list=graph_list, save_directory=save_directory)

    t = time.time() - startTime
    logger.warning('Time Used: %s', t)
    print('Time Used:', str(t))
