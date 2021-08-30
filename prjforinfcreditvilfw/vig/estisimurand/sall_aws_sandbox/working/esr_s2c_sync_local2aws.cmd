:: These are actually not needed manually, auto upload mpoly files during esr_s2b
:: Upload to remote mpoly estimation approximation file.

cd /d "G:\S3\thaijmp202010\esti\e_20201025x_esr_medtst_list_tKap_mlt_ce1a2"
aws s3 cp ^
    .
    s3://thaijmp202010/esti/e_20201025x_esr_medtst_list_tKap_mlt_ce1a2/ ^
    --include "*mpoly_reg_coef.csv"

cd /d "G:\S3\thaijmp202010\esti\e_20201025x_esr_medtst_list_tKap_mlt_ne1a2"
aws s3 cp ^
    .
    s3://thaijmp202010/esti/e_20201025x_esr_medtst_list_tKap_mlt_ne1a2/ ^
    --include "*mpoly_reg_coef.csv"

