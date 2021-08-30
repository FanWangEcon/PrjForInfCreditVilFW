::::::::::::::::::::::
:: This works for ESR2, ESR4, ESR6 as well as ESR8
::::::::::::::::::::::
cd /d "G:\S3\thaijmp202010\esti_tst\"
mkdir e_20201025_esr_tstN100_aws_list_tKap_mlt_ce1a2
cd /d "G:\S3\thaijmp202010\esti_tst\e_20201025_esr_tstN100_aws_list_tKap_mlt_ce1a2"
aws s3 cp ^
    s3://thaijmp202010/esti_tst/e_20201025_esr_tstN100_aws_list_tKap_mlt_ce1a2/ . ^
    --recursive --exclude "*.png"

cd /d "G:\S3\thaijmp202010\esti_tst\"
mkdir e_20201025_esr_tstN100_aws_list_tKap_mlt_ne1a2
cd /d "G:\S3\thaijmp202010\esti_tst\e_20201025_esr_tstN100_aws_list_tKap_mlt_ne1a2"
aws s3 cp ^
    s3://thaijmp202010/esti_tst/e_20201025_esr_tstN100_aws_list_tKap_mlt_ne1a2/ . ^
    --recursive --exclude "*.png"


cd /d "G:\S3\thaijmp202010\esti_tst\"
mkdir e_20201025_esr_tstN100_aws_list_tKap_mlt_ce1a2
cd /d "G:\S3\thaijmp202010\esti_tst\e_20201025_esr_tstN100_aws_list_tKap_mlt_ce1a2"
aws s3 cp ^
    s3://thaijmp202010/esti_tst/e_20201025_esr_tstN100_aws_list_tKap_mlt_ce1a2/ . ^
    --recursive

cd /d "G:\S3\thaijmp202010\esti_tst\"
mkdir e_20201025_esr_tstN100_aws_list_tKap_mlt_ne1a2
cd /d "G:\S3\thaijmp202010\esti_tst\e_20201025_esr_tstN100_aws_list_tKap_mlt_ne1a2"
aws s3 cp ^
    s3://thaijmp202010/esti_tst/e_20201025_esr_tstN100_aws_list_tKap_mlt_ne1a2/ . ^
    --recursive
