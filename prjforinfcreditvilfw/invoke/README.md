Command line parameters provided by: [invoke.run.py](/invoke/run.py). This is invoked
when calling the program from command line on local computers. This is also invoked
when calling the program from cloud where programs are packaged in containers.

[invoke.local_run.py](/invoke/run.py)


## local_simulate:

- param_type_list (*fargate* level)
  + on fargate for example, currently do many counterfactuals, looping over vector of parameter values for many parameters at the same time
- param_type
  + a name for a particular param_combo_list, param_type name would be different for each parameter name, while
  param_combo_list is for each of these parameters, looping over a vector of values for that one parameter
- param_combo_list
  + Looping over whatever combinations of parameter sets
  + But mainly about looping over individual parameter at a range of values
  + See how aggregates change as parameters change
  + See how likelihood or Moment differences change as parameters change
- param_combo
  + generates one set of aggregate results
  + a particular set of parameter values to be solved and to get aggregate orand equilibrium
  data for. Can also generate likelihood moment info for the current parameter set with some
  additional parameters for what moments to use etc.

## local_estimate:

- param_type_list (*fargate* level, no loop for each, each invoke separate)
  + can invoke multiple sets of param_combo_list (param_type) on fargate if needed with say different estimation routines.
  + Need to specifiy param_type, and compute_specs and esti_specs
- param_type
  + a name for a particular param_combo_list, param_type name would be different for each parameter name, while
  + param_type + esti_specs determine param_combo_list's param_combo estimation specifciations.
- param_combo_list (*fargate* level, equivalent to param_type_list)
  + Looping over potentially a random set of initial starting points.
  + This is the fargate level
  + Each result when done, should go into a file with final estimation results. Also maybe intermediate.
  + Could even show graph a set of different starting values, converging all to the same point.
- param_combo (equivalent to param_combo_list from run.py due to sequence of results generated)
  + generate a sequence of aggregate results based on estimation routine, starting from initial values explicitly specified in param_combo, and following estimation routine specified in param_combo.
  + with respect to the run.py codes, each param_combo in the iteration of sequence of parameters in estimation process is a different [param_combo] = param_list for invokation the same coding structure as run.py
  + no aggregate graphings from inside each [param_combo] needed
  + aggregate graphs outside, for the sequence of [aggregates1, ..., aggregateN] = estimation(init=param_combo)
