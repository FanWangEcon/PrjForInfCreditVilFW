'''
Created on Aug 30, 2018

@author: fan
'''

import estimation.postprocess.texdo.texdo_DATASIMUPROBJ as texdo_DATASIMUPROBJ
import estimation.postprocess.texdo.texdo_ALLPARAMS as texdo_ALLPARAMS

def out2tex(top_esti_df, save_directory, esti_obj_rank = 0, compesti_short_name=None):
    """tex newcommands

    Parameters
    ----------
    compesti_short_name : str
        string of comp esti name, like *C1E126M4S3*, add these to suffix if this is not None


    Examples
    --------
    import estimation.postprocess.gen_tex as gen_tex
    gen_tex.out2tex(top_esti_df, save_directory, save_tex)    
    """

    st_suffix = ''
    if compesti_short_name is not None:
        st_suffix = '_' + compesti_short_name

    '''
    1. Process top_esti_df, to eliminate extra rows (not necessary
    '''        
    
    
    '''
    2. Table that shows 7 category Participation Shares in Data
        top_esti_df might not have all vars, if not, DO NOT USE DEFAULT VALUES 
        Actually only fill up th
    '''
    save_name = 'DATASIMUPROBJ' + st_suffix
    texdo_DATASIMUPROBJ.fill_template(top_esti_df,
                                      save_name = save_name,
                                      save_directory = save_directory,
                                      save_tex = True,
                                      esti_obj_rank = esti_obj_rank)
        
    save_name = 'PARAMS' + st_suffix
    texdo_ALLPARAMS.fill_template(top_esti_df,
                                  save_name = save_name,
                                  save_directory = save_directory,
                                  save_tex = True,
                                  esti_obj_rank = esti_obj_rank)