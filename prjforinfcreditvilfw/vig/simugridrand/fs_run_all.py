import subprocess

spt_root = 'G:/repos/ThaiJMP/vig/simugridrand/'
# spt_root = 'C:/Users/fan/ThaiJMP/vig/simugridrand/'
ls_spn_paths = [spt_root + 'simugrid/fs_run_main_grid_oneparam_local.py',
                spt_root + 'simugrid/fs_run_main_grid_multiparam_local.py',
                spt_root + 'simugrid/fs_run_main_grid_multiparam_each_local.py',
                spt_root + 'simugrid_momobj/fs_run_main_grid_oneparam_local_mom.py',
                spt_root + 'simurand_momobj/fs_run_main_rand_oneparam_local.py']

for spn_paths in ls_spn_paths:
    cmd_popen = subprocess.Popen(['python', spn_paths],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

    output, err = cmd_popen.communicate()
    print(output.decode('utf-8'))
