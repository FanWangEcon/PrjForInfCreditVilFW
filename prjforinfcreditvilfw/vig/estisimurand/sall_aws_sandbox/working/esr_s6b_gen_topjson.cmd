:::::::::::::::::::::::::
echo STEP 6
:::::::::::::::::::::::::
:: -----------
echo central:
:: ~~~~~~~~~~
python run_esr.py                        ^
    6                                    ^
    -s    b_ng_p_d=esti_mplypostsimu_1=3=3 ^
    -cta  e                              ^
    -ctb  20201025_esr_tstN100_aws        ^
    -ctc  list_tKap_mlt_ce1a2            ^
    -f    esti_tst                           ^
    --awslocal                           ^
    -top  5
echo northeast:
:: ~~~~~~~~~~~~
:: python run_esr.py 6 -s    b_ng_p_d=esti_mplypostsimu_1=3=4 -cta  e -ctb  20201025_esr_tstN100_aws -ctc  list_tKap_mlt_ne1a2 -f    esti --awslocal -top  5
python run_esr.py                        ^
    6                                    ^
    -s    b_ng_p_d=esti_mplypostsimu_1=4=3 ^
    -cta  e                              ^
    -ctb  20201025_esr_tstN100_aws        ^
    -ctc  list_tKap_mlt_ne1a2            ^
    -f    esti_tst                           ^
    --awslocal                           ^
    -top  5
