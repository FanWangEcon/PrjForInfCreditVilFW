:: "G:/repos/ThaiJMP/vig/estisimurand/sall_local/fs_esr_oneparam_lin_cmd.cmd"
conda activate wk_cgefi
cd /d "G:/repos/ThaiJMP/invoke"

echo STEP 1
:: -----------
echo central:
:: ~~~~~~~~~~
python run_esr.py                        ^
    1                                    ^
    -s    ng_s_t=esti_tinytst_thin_1=3=3 ^
    -cta  e                              ^
    -ctb  20201025x_ITG_esr_tstN5_cmd        ^
    -ctc  list_tKap_mlt_ce1a2            ^
    -f    esti_tst
echo northeast:
:: ~~~~~~~~~~~~
python run_esr.py                        ^
    1                                    ^
    -s    ng_s_t=esti_tinytst_thin_1=4=3 ^
    -cta  e                              ^
    -ctb  20201025x_ITG_esr_tstN5_cmd        ^
    -ctc  list_tKap_mlt_ne1a2            ^
    -f    esti_tst

echo STEP 2
:: -----------
echo central:
:: ~~~~~~~~~~
python run_esr.py                        ^
    2                                    ^
    -s    ng_s_t=esti_tinytst_thin_1=3=3 ^
    -cta  e                              ^
    -ctb  20201025x_ITG_esr_tstN5_cmd        ^
    -ctc  list_tKap_mlt_ce1a2            ^
    -f    esti_tst                           ^
    -top  5
echo northeast:
:: ~~~~~~~~~~~~
python run_esr.py                        ^
    2                                    ^
    -s    ng_s_t=esti_tinytst_thin_1=4=3 ^
    -cta  e                              ^
    -ctb  20201025x_ITG_esr_tstN5_cmd        ^
    -ctc  list_tKap_mlt_ne1a2            ^
    -f    esti_tst                           ^
    -top  5


echo STEP 3
:: -----------
echo central:
:: ~~~~~~~~~~
python run_esr.py                           ^
    3                                       ^
    -s    mpoly_1=esti_tinytst_mpoly_13=3=3 ^
    -cta  e                                 ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ce1a2               ^
    -f    esti_tst
echo northeast:
:: ~~~~~~~~~~~~
python run_esr.py                           ^
    3                                       ^
    -s    mpoly_1=esti_tinytst_mpoly_13=4=3 ^
    -cta  e                                 ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ne1a2               ^
    -f    esti_tst

echo STEP 4
:: -----------
echo central:
:: ~~~~~~~~~~
python run_esr.py                           ^
    4                                       ^
    -s    mpoly_1=esti_tinytst_mpoly_13=3=3 ^
    -cta  e                                 ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ce1a2               ^
    -f    esti_tst                              ^
    -top  5
echo northeast:
:: ~~~~~~~~~~~~
python run_esr.py                           ^
    4                                       ^
    -s    mpoly_1=esti_tinytst_mpoly_13=4=3 ^
    -cta  e                                 ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ne1a2               ^
    -f    esti_tst                              ^
    -top  5


echo echo STEP 5
:: :: -------------
echo central
python run_esr.py                            ^
    5                                        ^
    -s    ng_s_t=esti_mplypostsimu_1=3=3     ^
    -cta  e                                  ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ce1a2                ^
    -cte1 mpoly_1=esti_tinytst_mpoly_13=3=3  ^
    -cte2 5                                  ^
    -f    esti_tst
:: northeast
python run_esr.py                            ^
    5                                        ^
    -s    ng_s_t=esti_mplypostsimu_1=4=3     ^
    -cta  e                                  ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ne1a2                ^
    -cte1 mpoly_1=esti_tinytst_mpoly_13=4=3  ^
    -cte2 5                                  ^
    -f    esti_tst

echo STEP 6
:: --------
echo central
python run_esr.py                            ^
    6                                        ^
    -s    ng_s_t=esti_mplypostsimu_1=3=3     ^
    -cta  e                                  ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ce1a2                ^
    -f    esti_tst                               ^
    -top  5
:: northeast
python run_esr.py                            ^
    6                                        ^
    -s    ng_s_t=esti_mplypostsimu_1=4=3     ^
    -cta  e                                  ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ne1a2                ^
    -f    esti_tst                               ^
    -top  5

echo echo STEP 7
:: :: -------------
echo central
python run_esr.py                            ^
    7                                        ^
    -s    ng_s_t=esti_mplypostesti_12=3=3    ^
    -cta  e                                  ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ce1a2                ^
    -cte1 mpoly_1=esti_tinytst_mpoly_13=3=3  ^
    -cte2 5                                  ^
    -f    esti_tst
:: northeast
python run_esr.py                            ^
    7                                        ^
    -s    ng_s_t=esti_mplypostesti_12=4=3    ^
    -cta  e                                  ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ne1a2                ^
    -cte1 mpoly_1=esti_tinytst_mpoly_13=4=3  ^
    -cte2 5                                  ^
    -f    esti_tst

echo STEP 8
:: --------
echo central
python run_esr.py                            ^
    8                                        ^
    -s    ng_s_t=esti_mplypostesti_12=3=3     ^
    -cta  e                                  ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ce1a2                ^
    -f    esti_tst                               ^
    -top  5
:: northeast
python run_esr.py                            ^
    8                                        ^
    -s    ng_s_t=esti_mplypostesti_12=4=3     ^
    -cta  e                                  ^
    -ctb  20201025x_ITG_esr_tstN5_cmd            ^
    -ctc  list_tKap_mlt_ne1a2                ^
    -f    esti_tst                               ^
    -top  5
