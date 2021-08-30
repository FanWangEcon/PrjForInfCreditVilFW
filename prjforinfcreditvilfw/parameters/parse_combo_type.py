def get_connector():
    st_connector = "="
    return st_connector

def check_combo_type_postmpoly(combo_type):
    """Check if doing postmpoly estimation
    The characteristic if the 5th element exists, this means this is mpoly estimation
    """
    bl_post_mpoly_estisimu = False
    if len(combo_type) == 5:
        bl_post_mpoly_estisimu = True

    return bl_post_mpoly_estisimu


def parse_combo_type_e_check(combo_type_e):
    """
    Check combo_type's fifth element to see if it follows the structure of combo_type_e for esr sequence element
    call, or it is a simulation call's JSON file specification.

    Parameters
    ----------
    combo_type_e : str
        'C1E126M4S3=2' for ESR path call during estimation.
        "M4S3_top_json.json" for simulation call to JSON file.
    """

    st_connector = get_connector()
    ls_combo_type_e_split = combo_type_e.split(st_connector)
    # first check length
    bl_esr_json = True
    if len(ls_combo_type_e_split) == 2:
        [compesti_short_name, esti_top_which] = ls_combo_type_e_split
        # check type
        bl_first_is_str = isinstance(compesti_short_name, str)
        bl_second_is_int = all([st_ele in '1234567890' for st_ele in esti_top_which])
        if bl_first_is_str + bl_second_is_int < 2:
            bl_esr_json = False
    else:
        bl_esr_json = False

    return bl_esr_json


def parse_combo_type_e(combo_type_e=None,
                       compesti_short_name=None,
                       esti_top_which=None):
    """5th element of combo_type join and parse

    cpetshrnam_topwch = compesti_short_name + esti_top_which

    Parameters
    ----------
    combo_type_e : str
        The 5th element of combo_type, for example 'C1E126M4S3=2'
    compesti_short_name :
        i.e.: C1E126M4S3, this is the folder suffix file suffix from mpoly estimation
    esti_top_which : int
        i.e.: 1, meaning to get the top estimate from mpoly round
    """
    st_connector = get_connector()
    if (compesti_short_name is not None) and (esti_top_which is not None):
        st_param_combo_5th = compesti_short_name + st_connector + str(esti_top_which)
        return st_param_combo_5th
    elif combo_type_e is not None:
        # i.e.: 'C1E126M4S3=2'
        [compesti_short_name, esti_top_which] = combo_type_e.split(st_connector)
        return compesti_short_name, esti_top_which
    else:
        raise TypeError(f'{combo_type_e=} is None. '
                        f'Both {compesti_short_name=} and {esti_top_which=} are None as well.')
