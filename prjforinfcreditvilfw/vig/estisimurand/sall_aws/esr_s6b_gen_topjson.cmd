:::::::::::::::::::::::::
echo STEP 6
:::::::::::::::::::::::::
:: for x tinytst tstN5
:::::::::::::::::::::::::
:: -----------
echo central:
:: ~~~~~~~~~~
python run_esr.py                        ^
    6                                    ^
    -s    ng_s_t=esti_mplypostsimu_1=3=3 ^
    -cta  e                              ^
    -ctb  20201025x_esr_tstN5_aws        ^
    -ctc  list_tKap_mlt_ce1a2            ^
    -f    esti_tst                       ^
    --awslocal                           ^
    -top  5
echo northeast:
:: ~~~~~~~~~~~~
:: python run_esr.py 6 -s    ng_s_t=esti_mplypostsimu_1=3=4 -cta  e -ctb  20201025x_esr_tstN5_aws -ctc  list_tKap_mlt_ne1a2 -f    esti --awslocal -top  5
python run_esr.py                        ^
    6                                    ^
    -s    ng_s_t=esti_mplypostsimu_1=4=3 ^
    -cta  e                              ^
    -ctb  20201025x_esr_tstN5_aws        ^
    -ctc  list_tKap_mlt_ne1a2            ^
    -f    esti_tst                       ^
    --awslocal                           ^
    -top  5
