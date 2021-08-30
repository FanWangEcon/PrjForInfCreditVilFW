:::::::::::::::::::::::::
echo STEP 4
:::::::::::::::::::::::::
:: for x tinytst tstN5
:::::::::::::::::::::::::
:: -----------
:: Note operation below auto uploads generated *mpoly_reg_coef* to corresponding S3 folder.
echo central:
:: ~~~~~~~~~~
python run_esr.py                        ^
    4                                    ^
    -s    mpoly_1=esti_tinytst_mpoly_13=3=3 ^
    -cta  e                              ^
    -ctb  20201025x_esr_tstN5_aws           ^
    -ctc  list_tKap_mlt_ce1a2            ^
    -f    esti_tst                       ^
    --awslocal                           ^
    -top  5
:: python run_esr.py 2 -s ng_s_t=esti_medtst_thin_1=3=3 -cta e -ctb 20201025x_esr_medtst -ctc  list_tKap_mlt_ce1a2 -f esti --awslocal -top 5
echo northeast:
:: ~~~~~~~~~~~~
python run_esr.py                        ^
    4                                    ^
    -s    mpoly_1=esti_tinytst_mpoly_13=4=3 ^
    -cta  e                              ^
    -ctb  20201025x_esr_tstN5_aws           ^
    -ctc  list_tKap_mlt_ne1a2            ^
    -f    esti_tst                       ^
    --awslocal                           ^
    -top  5
