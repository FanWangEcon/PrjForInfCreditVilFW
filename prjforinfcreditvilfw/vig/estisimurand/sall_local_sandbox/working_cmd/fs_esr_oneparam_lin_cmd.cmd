:: "G:/repos/ThaiJMP/vig/estisimurand/sall_local/fs_esr_oneparam_lin_cmd.cmd"
conda activate wk_cgefi
cd /d "G:/repos/ThaiJMP/invoke"

:::::::::::::::::::::::::::::::::::::::
:: Define some parameters
:::::::::::::::::::::::::::::::::::::::
:: A1. folder name
set esrf=esti_tst

:: A2. subfolder name
set esrbstfilesuffix=_esr_tstN5_cmd

:: B. ITG or x, normal, or detailed
set esrbxrditg=x_ITG
REM set esrbxrditg=x

:: C1. compute spec key
set esrscomputespeckey=b_ng_p_d
REM set esrscomputespeckey=ng_s_t

:: C2. test scale (esti spec key)
set esrssttestscale=_tinytst_


:::::::::::::::::::::::::::::::::::::::
:: Operations
:::::::::::::::::::::::::::::::::::::::
echo STEP 1
:: -----------
echo central:
:: ~~~~~~~~~~
python run_esr.py                        ^
    1                                    ^
    -s    %esrscomputespeckey%=esti%esrssttestscale%thin_1=3=3 ^
    -cta  e                              ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%    ^
    -ctc  list_tKap_mlt_ce1a2            ^
    -f    %esrf%
echo northeast:
:: ~~~~~~~~~~~~
python run_esr.py                        ^
    1                                    ^
    -s    %esrscomputespeckey%=esti%esrssttestscale%thin_1=4=3 ^
    -cta  e                              ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%        ^
    -ctc  list_tKap_mlt_ne1a2            ^
    -f    %esrf%

echo STEP 2
:: -----------
echo central:
:: ~~~~~~~~~~
python run_esr.py                        ^
    2                                    ^
    -s    %esrscomputespeckey%=esti%esrssttestscale%thin_1=3=3 ^
    -cta  e                              ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%        ^
    -ctc  list_tKap_mlt_ce1a2            ^
    -f    %esrf%                           ^
    -top  5
echo northeast:
:: ~~~~~~~~~~~~
python run_esr.py                        ^
    2                                    ^
    -s    %esrscomputespeckey%=esti%esrssttestscale%thin_1=4=3 ^
    -cta  e                              ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%        ^
    -ctc  list_tKap_mlt_ne1a2            ^
    -f    %esrf%                           ^
    -top  5


echo STEP 3
:: -----------
echo central:
:: ~~~~~~~~~~
python run_esr.py                           ^
    3                                       ^
    -s    mpoly_1=esti%esrssttestscale%mpoly_13=3=3 ^
    -cta  e                                 ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ce1a2               ^
    -f    %esrf%
echo northeast:
:: ~~~~~~~~~~~~
python run_esr.py                           ^
    3                                       ^
    -s    mpoly_1=esti%esrssttestscale%mpoly_13=4=3 ^
    -cta  e                                 ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ne1a2               ^
    -f    %esrf%

echo STEP 4
:: -----------
echo central:
:: ~~~~~~~~~~
python run_esr.py                           ^
    4                                       ^
    -s    mpoly_1=esti%esrssttestscale%mpoly_13=3=3 ^
    -cta  e                                 ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ce1a2               ^
    -f    %esrf%                              ^
    -top  5
echo northeast:
:: ~~~~~~~~~~~~
python run_esr.py                           ^
    4                                       ^
    -s    mpoly_1=esti%esrssttestscale%mpoly_13=4=3 ^
    -cta  e                                 ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ne1a2               ^
    -f    %esrf%                              ^
    -top  5


echo echo STEP 5
:: :: -------------
echo central
python run_esr.py                            ^
    5                                        ^
    -s    %esrscomputespeckey%=esti_mplypostsimu_1=3=3     ^
    -cta  e                                  ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ce1a2                ^
    -cte1 mpoly_1=esti%esrssttestscale%mpoly_13=3=3  ^
    -cte2 5                                  ^
    -f    %esrf%
:: northeast
python run_esr.py                            ^
    5                                        ^
    -s    %esrscomputespeckey%=esti_mplypostsimu_1=4=3     ^
    -cta  e                                  ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ne1a2                ^
    -cte1 mpoly_1=esti%esrssttestscale%mpoly_13=4=3  ^
    -cte2 5                                  ^
    -f    %esrf%

echo STEP 6
:: --------
echo central
python run_esr.py                            ^
    6                                        ^
    -s    %esrscomputespeckey%=esti_mplypostsimu_1=3=3     ^
    -cta  e                                  ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ce1a2                ^
    -f    %esrf%                               ^
    -top  5
:: northeast
python run_esr.py                            ^
    6                                        ^
    -s    %esrscomputespeckey%=esti_mplypostsimu_1=4=3     ^
    -cta  e                                  ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ne1a2                ^
    -f    %esrf%                               ^
    -top  5

echo echo STEP 7
:: :: -------------
echo central
python run_esr.py                            ^
    7                                        ^
    -s    %esrscomputespeckey%=esti_mplypostesti_12=3=3    ^
    -cta  e                                  ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ce1a2                ^
    -cte1 mpoly_1=esti%esrssttestscale%mpoly_13=3=3  ^
    -cte2 5                                  ^
    -f    %esrf%
:: northeast
python run_esr.py                            ^
    7                                        ^
    -s    %esrscomputespeckey%=esti_mplypostesti_12=4=3    ^
    -cta  e                                  ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ne1a2                ^
    -cte1 mpoly_1=esti%esrssttestscale%mpoly_13=4=3  ^
    -cte2 5                                  ^
    -f    %esrf%

echo STEP 8
:: --------
echo central
python run_esr.py                            ^
    8                                        ^
    -s    %esrscomputespeckey%=esti_mplypostesti_12=3=3     ^
    -cta  e                                  ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ce1a2                ^
    -f    %esrf%                               ^
    -top  5
:: northeast
python run_esr.py                            ^
    8                                        ^
    -s    %esrscomputespeckey%=esti_mplypostesti_12=4=3     ^
    -cta  e                                  ^
    -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
    -ctc  list_tKap_mlt_ne1a2                ^
    -f    %esrf%                               ^
    -top  5
