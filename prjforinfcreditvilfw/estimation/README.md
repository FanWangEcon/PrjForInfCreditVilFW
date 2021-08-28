# Multiple Period Estimation Structure

Start at a random set of parameter values, including random/different parameters
for time/region specific variables. Estimation routine considers joint objective
function of multiple time/region. Results are stored in N region/time json
files, each region/period gets own json file. The json file also stores
aggregate objective. Each json file has key for region/period

When reviewing results, can sort by overall objective, then conditional on each
group, presents results for all parameter values, as with single estimation
results.

# Invoking Estimation

combo_type: is the initial parameters and fixed non-estimated parameters
combo_list: a one element list containing updated dictionaries in param_combo
reflecting current estimation iteration.

# Estimation Structure

In [estimation.estimate.py](/estimation/estimate.py):
- Specify which parameters are to be Estimated
- Set estimation routine tolerance levels
- Pick estimation routines
- Initialize all model parameters param_combo
- Initialize estimation parameter vector based on initial param_combo
- Invoke estimationroutine

[estimation.estimate_objective.py](/estimation/estimate_objective.py)
- Update parameters
- Solve model and generate outputs
- Channel towards moment or likelihood based estimation

[estimation.moments.py](/estimation/moments.py)

## Updating Keys for Estimation

In [estimation.estimate.py](/estimation/estimate.py), estimation parameters are
initialized. This is done in a little funky way.

Invocations are based on param_combo. Model is solved based on param_combo, not on
param_inst. param_inst is generated within solu.solve_model based on param_combo.

So I need to grab out in order to initialize estimation initial parameters that are
definied for param_combo. Which happens in [estimation.estimate.py](/estimation/estimate.py)
line 44 (param_inst_preset.get_param_inst_preset_combo).

Then inside [estimation.estimate_objective.py](/estimation/estimate_objective.py), I
update param_combo based on what parameters are getting estimated. In the initial round, the
updates are the same as what are in the param_combo, because we grab out the base/default
parameter first. But in later rounds, the parameters get updated in estimation process,
and in every iteration, the param_inst to be used in solution is changed by modifying the
param_combo.

What happens to nested parameter (from dist_param)?

## Loading in Keys and Parameters.

from run_estimate:
  - specify the param_type name, and specify esti_specs
  - get: param_list(param_type, esti_specs)
    + the idea here is the list has same esti_specs, but different random initial values
    potentially.
    + for different types of esti_specs, that should be specified at the esti_type level.
    + param_type = ['a','20180723test_2312',['esti_param.alpha_k,esti_param.beta'],'kap_m0_nld_m']
  - esti_specs could be from a library of pre-specified esti_specs, or override with Parameters defined in run_estimates
  - loop over param_combo in param_list
+ looping for fargate means

## Folder Structure

- root folder in terms of which parameters are estimated:
  + i.e.: *\Project Dissertation\esti\c_20180801_rhoo_beta*
- subfolder in terms of which estimation method is used, and which one of the random starting point use
  + i.e.: *\Project Dissertation\esti\c_20180801_rhoo_beta\C1E1_c0*
+ subsubfolder contains results from each estimation run
  - each estimation run contains log and json for each iteration, and an aggregate graph
  + i.e.: *\Project Dissertation\esti\c_20180801_rhoo_beta\C1E1_c0\AGG_EXO_20180801_rhoo_beta_bJ2.png*

Folder Structure Improvements to incorporate four sets of information:
+ estimation folder name captures:
- param_type[2]: set of parameters estimated
- moments_type: data for estimation
- momsets_type: which set of moments to match
- esti_option_type, esti_func_type: estimation method, initial values, tolerance etc

## Estimating with multiple Periods Together

- moment keys are nested, so simulation file moment matcher should fail, producing empty esti_obj
- generate objective in multiperiod function
  + grab sub-dict based on period key in data nested dict
  + match to model models
  + now they have same key
  + aggregate up objective with simple sum across periods
- at multiperiod estimation stage, have period specific: param_dict_moments
  + based on period specific parameters' simulation
    + estimating all parameters, stored with period specific suffix
    + during multi-estate replace generic key values by period specific key values.
  + matched to period specific data
    - stored in nested dictionary with common key under period root key

# Log in estimation

- an estimation logger, independent of the solution logger:
  + estimate.py:l72, log_file = False if off, True if on
  + logs results in estimate.objective.multiperiod for example.
