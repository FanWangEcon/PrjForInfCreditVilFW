:::::::::::::::::::::::::::::::::::::::
:: Define some parameters
:::::::::::::::::::::::::::::::::::::::
:: ESR STEP
SET /A esrstep = 8

:: A1. folder name
set esrf=esti_tst_onefile_ITGN5

:: A2. subfolder name
set esrbstfilesuffix=_esr_tstN5_aws

:: B. ITG or x, normal, or detailed
set esrbxrditg=_ITG

:: C1. compute spec key
set esrscomputespeckey=b_ng_p_d

:: C2. test scale (esti spec key)
set esrssttestscale=_tinytst_

:::::::::::::::::::::::::::::::::::::::
:: Operations
:::::::::::::::::::::::::::::::::::::::

IF /I "%esrstep%" EQU "0" (
    echo RUN THIS INSIDE WK_AWS
    echo STEP 0
    cd /d G:\S3\thaijmp202010\%esrf%\
    mkdir e_20201025_ITG_esr_tstN5_aws_list_tKap_mlt_ce1a2
    cd /d G:\S3\thaijmp202010\%esrf%\e_20201025_ITG_esr_tstN5_aws_list_tKap_mlt_ce1a2
    echo STEP cded
    aws s3 cp ^
        s3://thaijmp202010/%esrf%/e_20201025_ITG_esr_tstN5_aws_list_tKap_mlt_ce1a2/ . ^
        --recursive
    echo STEP synced

    cd /d G:\S3\thaijmp202010\%esrf%\
    mkdir e_20201025_ITG_esr_tstN5_aws_list_tKap_mlt_ne1a2
    cd /d G:\S3\thaijmp202010\%esrf%\e_20201025_ITG_esr_tstN5_aws_list_tKap_mlt_ne1a2
    aws s3 cp ^
        s3://thaijmp202010/%esrf%/e_20201025_ITG_esr_tstN5_aws_list_tKap_mlt_ne1a2/ . ^
        --recursive
)

:: "G:/repos/ThaiJMP/vig/estisimurand/sall_local/fs_esr_oneparam_lin_cmd.cmd"
:: conda activate wk_cgefi
cd /d "G:/repos/ThaiJMP/invoke"
echo RUN BELOW INSIDE WK_CGEFI

IF /I "%esrstep%" EQU "2" (
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
        --awslocal                           ^
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
        --awslocal                           ^
        -top  5
)

IF /I "%esrstep%" EQU "4" (
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
        --awslocal                           ^
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
        --awslocal                           ^
        -top  5
)

IF /I "%esrstep%" EQU "6" (
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
        --awslocal                           ^
        -top  5
    :: northeast
    python run_esr.py                            ^
        6                                        ^
        -s    %esrscomputespeckey%=esti_mplypostsimu_1=4=3     ^
        -cta  e                                  ^
        -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
        -ctc  list_tKap_mlt_ne1a2                ^
        -f    %esrf%                               ^
        --awslocal                           ^
        -top  5
)

IF /I "%esrstep%" EQU "8" (
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
        --awslocal                           ^
        -top  5
    :: northeast
    python run_esr.py                            ^
        8                                        ^
        -s    %esrscomputespeckey%=esti_mplypostesti_12=4=3     ^
        -cta  e                                  ^
        -ctb  20201025%esrbxrditg%%esrbstfilesuffix%            ^
        -ctc  list_tKap_mlt_ne1a2                ^
        -f    %esrf%                               ^
        --awslocal                           ^
        -top  5
)

:: cd /d G:\repos\ThaiJMP\vig\estisimurand\sall_aws_sandbox\template_onefile
:: CALL esr_s2468_sync_gather.CMD
:: cd /d G:\repos\ThaiJMP\vig\estisimurand\sall_aws_sandbox\template_onefile && CALL esr_s2468_sync_gather.CMD
