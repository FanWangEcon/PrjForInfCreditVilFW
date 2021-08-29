'''
Created on May 18, 2018

@author: fan

Handles parameter parsing from command line. 
'''

import argparse
import logging
import sys

import invoke.run_main as invoke_run_main
import projectsupport.systemsupport as proj_sys_sup

parser = argparse.ArgumentParser()
parser.add_argument('-A', dest="speckey",
                    help="specification for computational resources and estimation parameters",
                    default='f-ng-s-d')
parser.add_argument('-B', dest="combo_type_p1",
                    help="a or b or other, the file names, first position of combo_type",
                    default='a')
parser.add_argument('-C', dest="combo_type_p2",
                    help="conditional name branch of the file",
                    default='20180529_A')
parser.add_argument('-D', '--list', dest="combo_type_p3",
                    nargs='+',
                    help='parameters been estimated of looped over',
                    required=True)

parser.add_argument('-E', dest="combo_type_p4",
                    help="which element of random init loop to run for estimation",
                    default='None')

parser.add_argument('-F', dest="graph_panda_list_name",
                    help="string list of what to graph and panda output",
                    default='main_graphs')
parser.add_argument('-G', dest="save_directory_main",
                    help="which folder to store json, csv and graph files in",
                    default='simu')

parser.add_argument('--multiprocess', dest='multiprocess',
                    help="turn on multiprocessing so that multiple parameter set values are concurrently solved",
                    action='store_true')
parser.add_argument('--no-multiprocess', dest='multiprocess',
                    help="turn off multiprocessing. Still numba parallel, and vector parallel.",
                    action='store_false')
parser.set_defaults(multiprocess=False)

parser.add_argument('--ge', dest='ge',
                    help="general equilibrium, solve for informal R.",
                    action='store_true')
parser.add_argument('--no-ge', dest='ge',
                    help="Partial equilibrium, given informal R.",
                    action='store_false')
parser.set_defaults(ge=False)

parser.add_argument('--esti', dest='esti',
                    help="This is to estimate using stored values in param_combo as initial estimation values",
                    action='store_true')
parser.add_argument('--no-esti', dest='esti',
                    help="Simulation, not estimation",
                    action='store_false')
parser.set_defaults(esti=False)

args = parser.parse_args()

sys.path.append('c:\\Users\\fan\\PyFan\\ProjectSupport')
sys.path.append('c:\\Users\\fan\\ThaiJMP')

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    #       cd "c:\Users\fan\ThaiJMP\invoke"
    #       python run.py -A l-ng-s-x -B b -C 20180702_Aprd -D data_param.A -E main_graphs --no-ge --no-multiprocess
    #       python run.py -A l-ge-p-x -B b -C 20180702_Aprd -D data_param.A -E main_graphs --ge --no-multiprocess
    #       python run.py -A l-ge-p-x -B b -C 20180702_Aprd -D data_param.A -E all_solu_graphs_tables --ge --multiprocess

    #       python run.py -A l-ng-s-x -B b -C 20180702_alpk -D esti_param.alpha_k -E all_solu_graphs_tables --no-ge --no-multiprocess
    #       python run.py -A l-ge-p-x -B b -C 20180702_alpk -D esti_param.alpha_k -E all_solu_graphs_tables --ge --multiprocess

    #       python run.py -A l-ng-s-x -B b -C 20180702_DAprdMu -D dist_param.data__A.params.mu -E main_graphs --no-ge --no-multiprocess
    #       python run.py -A l-ge-p-x -B b -C 20180702x_DAprdMu -D dist_param.data__A.params.mu -E main_graphs --ge --multiprocess
    #       python run.py -A l-ng-s-x -B b -C 20180702_Aprd -D data_param.A -E main_graphs --no-ge --no-multiprocess
    #       python run.py -A l-ge-p-x -B b -C 20180702_Aprd -D data_param.A -E main_graphs --ge --multiprocess

    proj_sys_sup.log_start(logfile_directory_name='',
                           logging_level=logging.WARNING, log_file='',
                           module_name='')

    combo_type_p3_arg = args.combo_type_p3
    logger.warning('combo_type_p3_arg:%s', combo_type_p3_arg)
    logger.warning('combo_type_p3_arg.__class__.__name__:%s',
                   combo_type_p3_arg.__class__.__name__)

    combo_type_p4_arg = args.combo_type_p4
    logger.warning('combo_type_p4_arg:%s', combo_type_p4_arg)
    logger.warning('combo_type_p4_arg.__class__.__name__:%s',
                   combo_type_p4_arg.__class__.__name__)

    if (combo_type_p3_arg == 'none' or
            combo_type_p3_arg == 'None' or
            combo_type_p3_arg == 'NONE' or
            combo_type_p3_arg == ['NONE'] or
            combo_type_p3_arg == ['None'] or
            combo_type_p3_arg is None):
        combo_type_p3_arg = None

    if (combo_type_p4_arg == 'none' or
            combo_type_p4_arg == 'None' or
            combo_type_p4_arg == 'NONE' or
            combo_type_p4_arg == ['NONE'] or
            combo_type_p4_arg == ['None'] or
            combo_type_p4_arg is None):
        combo_type_p4_arg = None

    '''
    Issue with Batch Accepting List as INPUT
    '''
    if (isinstance(combo_type_p3_arg, list)):
        logger.warning('combo_type_p3_arg is list')
        if (len(combo_type_p3_arg) == 1):
            '''
            With batch when there are multiple parameters, they are put in one string:
                ['esti_param.alpha_k esti_param.beta']
            convert this to actual list
            this is from batch if this has space in between
            '''
            logger.warning('len(combo_type_p3_arg) == 1 is true')
            if (len(combo_type_p3_arg[0].split(" ")) > 1):
                # we are in batch with multiple parameters
                combo_type_p3_arg_list = []
                logger.warning('len(combo_type_p3_arg[0].split(" ")) > 1')
                for param_type_name in combo_type_p3_arg[0].split(" "):
                    combo_type_p3_arg_list.append(param_type_name)
                logger.warning('combo_type_p3_arg_list:%s', combo_type_p3_arg_list)
                logger.warning('Update combo_type_p3_arg')
                combo_type_p3_arg = combo_type_p3_arg_list

    combo_type = [args.combo_type_p1, args.combo_type_p2, combo_type_p3_arg, combo_type_p4_arg]
    invoke_run_main.invoke_main(combo_type=combo_type,
                                speckey=args.speckey,
                                ge=args.ge,
                                multiprocess=args.multiprocess,
                                estimate=args.esti,
                                graph_panda_list_name=args.graph_panda_list_name,
                                save_directory_main=args.save_directory_main)

#     cProfile.run('invoke_soluequi_partial('+combo_type+', r_loop_invoke=False)')
#     p = pstats.Stats('C:/Users/fan/Documents/Dropbox (UH-ECON)/Project Dissertation/model_test/cProfile/main.prof')
#     p.sort_stats('tottime').print_stats(1000)
