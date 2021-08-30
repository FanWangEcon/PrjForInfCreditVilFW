import invoke.run_esr_parser as run_esr_parser

dc_it_execute_type = {'model_assumption': 0, 'compute_size': 0,
                      'esti_size': 0, 'esti_param': 0,
                      'call_type': 1, 'param_date': 0}
for esr_run in [1, 2, 3, 4, 5, 6, 7, 8]:
    dc_st_esr_args_compose, dc_spt_awslocal_esrf_subfolders, \
    dc_combo_type, dc_combo_type_component, \
    dc_st_speckey, dc_st_speckey_mpoly, esrf, \
    it_esti_top_which_max, compute_spec_key, esti_spec_key = \
        run_esr_parser.run_esr_arg_generator(esr_run, dc_it_execute_type=dc_it_execute_type)

# outputs are

# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 1 -s ng_s_t=esti_tinytst_thin_1=3=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ce1a2 -f esti_tst_tKap
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 1 -s ng_s_t=esti_tinytst_thin_1=4=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ne1a2 -f esti_tst_tKap
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 2 -s ng_s_t=esti_tinytst_thin_1=3=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ce1a2 -f esti_tst_tKap
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 2 -s ng_s_t=esti_tinytst_thin_1=4=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ne1a2 -f esti_tst_tKap
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 3 -s mpoly_1=esti_tinytst_mpoly_13=3=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ce1a2 -f esti_tst_tKap
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 3 -s mpoly_1=esti_tinytst_mpoly_13=4=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ne1a2 -f esti_tst_tKap
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 4 -s mpoly_1=esti_tinytst_mpoly_13=3=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ce1a2 -f esti_tst_tKap
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 4 -s mpoly_1=esti_tinytst_mpoly_13=4=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ne1a2 -f esti_tst_tKap
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 5 -s ng_s_t=esti_mplypostsimu_1=3=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ce1a2 -f esti_tst_tKap -cte1 mpoly_1=esti_tinytst_mpoly_13=3=3 -cte2 5
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 5 -s ng_s_t=esti_mplypostsimu_1=4=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ne1a2 -f esti_tst_tKap -cte1 mpoly_1=esti_tinytst_mpoly_13=4=3 -cte2 5
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 6 -s ng_s_t=esti_mplypostsimu_1=3=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ce1a2 -f esti_tst_tKap
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 6 -s ng_s_t=esti_mplypostsimu_1=4=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ne1a2 -f esti_tst_tKap
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 7 -s ng_s_t=esti_mplypostesti_12=3=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ce1a2 -f esti_tst_tKap -cte1 mpoly_1=esti_tinytst_mpoly_13=3=3 -cte2 5
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 7 -s ng_s_t=esti_mplypostesti_12=4=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ne1a2 -f esti_tst_tKap -cte1 mpoly_1=esti_tinytst_mpoly_13=4=3 -cte2 5
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 8 -s ng_s_t=esti_mplypostesti_12=3=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ce1a2 -f esti_tst_tKap
# activate wk_cgefi & cd /d "G:/repos/ThaiJMP/invoke" & python run_esr.py 8 -s ng_s_t=esti_mplypostesti_12=4=3 -cta e -ctb 20201025x_esr_tinytst_cmd -ctc list_tKap_mlt_ne1a2 -f esti_tst_tKap

