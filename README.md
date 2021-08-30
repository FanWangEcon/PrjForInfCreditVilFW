# PrjForInfCreditVilFW

This is a repository for [An Empirical Equilibrium Model of Formal and Informal Credit Markets in Developing Countries](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3316939). This repository contains the latest version of code in support of this research paper.

The repository is available at [pypi](https://pypi.org/project/prjforinfcreditvilfw/) as well as on [github](https://github.com/FanWangEcon/PrjForInfCreditVilFW).

## Software and Operating System

### Summary

This is a python package (python [3.8](https://www.python.org/downloads/release/python-380/) built with [poetry](https://python-poetry.org/)). The package can be installed from [pypi](https://pypi.org/project/prjforinfcreditvilfw/#history) where the latest version would be available at.

For convenience, the [Anaconda suite for python 3](https://www.anaconda.com/products/individual) can be installed so that python is available on the local computer. All dependencies for running the programs are listed in the *pyproject.toml* file under the root directory. Dependencies associated with [ReadTheDocs](https://readthedocs.org/) are shown at *source/requirements_rtd.txt*. The support package [pyfan](https://pyfan.readthedocs.io/en/latest/) contains some common functions, extracted to be used in other projects, and is one of the dependencies.

Core functions from various modules in the package generally, although not always, have associated [unittests](https://docs.python.org/3/library/unittest.html) in each module's test sub-folder. Some unittests generate log outputs and other generate csv files or images. To generate and store outputs from tests, change to desired output directories in: *projectsupport.systemsupport.main_directory*. An example unittest can be found here *prjforinfcreditvilfw/soluvalue/test_soluvalue/test_optimax.py*.

As described in the paper, significant components of the package interfaces with various services at [AWS](https://aws.amazon.com/) and relies on [elastic containers](https://aws.amazon.com/ecr/). An AWS account is required along with associated keys and passwords. The tutorial website [Py4Econ](https://fanwangecon.github.io/Py4Econ/) was built partly in support of this project to provide examples on setting up containers as well as interacting with [EC2](https://aws.amazon.com/ec2/?nc2=h_ql_prod_cp_ec2), [ECR](https://aws.amazon.com/ecr/), [S3](https://aws.amazon.com/s3/), [batch](https://aws.amazon.com/batch/), and [fargate](https://aws.amazon.com/fargate/) services. Py4Econ has a section on *Amazon Web Services* and another section on *Docker Container*.

### Requirements

While there are various testers that could be called locally to test individual aspects of the programming structure, the overall solution and estimation structure is meant to be used with AWS Batch and on EC2 instances. Programs are designed to work with EC2 [Compute Optimized](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/compute-optimized-instances.html) and/or [Memory Optimized](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/memory-optimized-instances.html) instances that have larger than 32 GB of memory and more than 16 vcpus. Generally, during batch runs, [r5.16xlarge](https://aws.amazon.com/ec2/instance-types/r5/) could be selected as the primary instances to be started.

In terms of software, the package generates a docker container, with the docker files in the boto3aws.aws_ecr.container module. All required packages are contained in the container. [Amazon Linux 2](https://aws.amazon.com/amazon-linux-2/) can be chosen as the EC2 operating system. Testers can be run locally under other operating systems as well.

### Dependencies

Below, is a copy of the list of dependencies from the *pyproject.toml* file under the root directory. These would be installed or updated automatically when the PrjForInfCreditVilFW package is installed.

```{toml}
[tool.poetry]
name = "PrjForInfCreditVilFW"
version = "0.1.1"
description = ""
authors = ["Fan Wang <wangfanbsg75@live.com>"]

[tool.poetry.dependencies]
python = "^3.8"
python-frontmatter = "^0.5.0"
pyyaml = "^5.3.1"
numpy = "^1.18.5"
scipy = "^1.4.1"
matplotlib = "^3.2.1"
cython = "^0.29.20"
seaborn = "^0.10.1"
statsmodels = "^0.11.1"
numba = "^0.50.1"
sklearn = "^0.0"
boto3 = "^1.15.18"
urllib3 = "^1.25.10"
cryptography = "^3.0.0"
interpolation = "^2.0.0"
pyfan = "^0.1.0"

[tool.poetry.dev-dependencies]
pytest = "^5.2"

[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"
```

### Expected Computation Time

The vig module contains various testing files. There are also unittests in a number of other modules. A subset of these vignettes and unittests can be tested instantaneously. Main simulation functions generally take seconds, with graphing etc often taking more time. Main simulation function in the vignettes and unittests are generally called with small simulation size with imprecise approximations for the purpose of testing. The core functions are meant to be called on AWS as stated previously.

## Package module summary

### Call Programs

#### module invoke

While there are various testers that could be called locally to test individual aspects of the programming structure, the overall solution and estimation structure is meant to be used with AWS Batch and on EC2 instances. Programs are meant to be invoked via calls to docker containers via command line, with requisite command line instructions auto-generated based on solution and estimation requirements.

- command line parameter parser and caller:
    + run.py: generic gateway function for simulating the model via command line with command line parameter parserr.
    + run_esr.py: gateway function with command line argument parsing to invoke estimation, simulation call.
    + run_esr_parser.py: parse command line arguments for *run_esr*.
    + run_esr_parser_calls.py: call the parse to generate parameter inputs for batch calls.
    + run_sg.py: gateway function that parses command line simulation calls (at random initial parameters).
    + run_sg_parser.py: generate input arguments for *run_sg* command line calls.
- simulation related functions:
    + run_simulate.py: call model solution file, solve for value and policy functions and endogenous asset distributions.
    + local_simulate.py: local simulation non-command line invoker, generate input requirements and call distributional function
- estimation related functions
    + run_estimate.py: generate necessary arguments for docker container command line calls for estimation and call the estimate module.
    + local_estimate.py:
    + run_estimate_aws_multi.py: manage multi-start estimation calls to AWS batch.
    + run_estimate_aws_globsumm.py: gateway estimation caller to manage multi-start with AWS batch, to sync locally with AWS s3, to estimation locally, and to summarize estimation results.

#### module vig.estisimurand

Various modules and command line files that communicates between local and AWS in an 8 step estimation procedure.

- estisimurand.sall_aws: module containing command line and function instructions for aws calls.
- estisimurand.sall_aws_sandbox: sandbox with more examples and functionalized and hard-coded instructions.
- estisimurand.sall_local: module containing command line and function instructions for local calls.
- estisimurand.sall_local_sandbox: sandbox with more examples and functionalized and hard-coded instructions.

### Dynamic Programming, Asset Distributions and Equilibrium

#### module modelhh

Contains functions for current and future utility (approximation given the state-space). Also includes two groups of submodules:

- modelhh.functions: Core functions of the paper for each model component. Contains unittests for all functions.
- modelhh.future: Functions related to future values. Contains unittests for all functions.
G:\repos\PrjForInfCreditVilFW\

*Note: Includes several unittests.*

#### module soluvalue

Given model components specified in *modelhh*, various functions that discrete and continuous optimization problem given current expected value function. Functions that iterate and solve for the value function and policy function. Several functions related to CEV calculations given non-standard utility representation in the paper.

*Note: Includes several unittests.*

#### module solusteady

Given the dynamic programming solutions from *soluvalue*, solve for endogenous asset distributions. Also includes submodule:

- solusteady.distribution: Several conditional and marginal distribution functions.

*Note: Includes several unittests.*

#### module soluequi

Given the distributional results from *solusteady*, solve for equilibrium interest rate, given solutions from one or more productivity types.

### Various Support Programs and Functions

#### module dataandgrid

This module is responsible for generating asset choice grid given model parameters across joint asset space. Optimal choices are discretized over these grids. Includes two submodules:

- dataandgrid.dynamic: includes functions that dynamically fills up asset space with feasible savings, borrowing and risky capital investment choices, based on model parameters, consumption bounds today, natural borrowing bounds, as well as collateral based borrowing bounds. These grids are household specific.
- dataandgrid.fixed: includes functions that uses fixed choice grid regardless of household's cash position and parameter situation.

*Note: Includes several unittests.*

#### module analyze

This module is responsible for provide some visualizations and tabular outputs based on the results from the *soluvalue*, *solusteady*, and *soluequi* modules, with one function for each. There is additionally a hard-coded function for checking simulation outputs.

#### module projectsupport

To support other functions, this module provides a number of services that complements what is provided by the separately installed support package [pyfan](https://pyfan.readthedocs.io/en/latest/).

The module includes various key functions related to file communication with AWS, local file storage and retrieval, etc. Functions there call upon some of the functions in the submodules includes. Submodules are:

- projectsupport.datamanage: supports JSON management
- projectsupport.graph: [matplotlib](https://matplotlib.org/) based individual graphing services
- projectsupport.hardcode: all hard-coded strings are stored in functions in this package, to facilitate easy renaming of output results etc

### Testing and Invoking Model for Solution and Estimation on AWS

#### module boto3aws

This module interfaces with various AWS services. The submodules include:

- boto3aws.aws_ec2: for initiating, creating and shutting down EC2 instances
- boto3aws.aws_ecr: for storing to and retrieving from elasticity containers
- boto3aws.aws_batch: for managing and submitting batch tasks
- boto3aws.aws_fargate: for managing and submitting fargate tasks (do not allow for spot instances)
- boto3aws.aws_s3: for storing files to s3 that are outputted during compute runs inside EC2
- boto3aws.manageaws: generic management functions
- boto3aws.tools: tools for command line, sample commands etc.

These modules can only work with proper security and password settings, which have been deleted from these files.

#### module estimation

The module contains estimation functions that combine objectives based on model predictions and data from different data-segments. Various estimation options are available as options.

The postprocess module combines utilities that combine various initial simulation results, combines results and generates polynomial surface for intermediate estimation in order to generate starting seeds for estimation.

The submodules include:
- postprocess.jsoncsv: process estimation results and fit
- postprocess.texdo: convert results to latex and do formats for visualizations

#### module parameters

Modules preset with benchmark and other specifications:

- parameters.paramset: module with pre-set parameter groupings and settings for simulation
- parameters.runspecs: module with estimation and simulation specficiations for EC2 instances for Batch and Fargate settings

A number of modules generate combination of parameters:

- parameters.loop_combo_type_list: module with short-cut strings to generate parameter lists
- parameters.loop_param_combo_list: module to generate list of parameter value combinations over parameters
- parameters.minmax: module with bound values for parameters

A number of modules service different groups of parameters:

- parameters.data: module for parameters related to data
- parameters.dist: module for parameters related to distribution
- parameters.esti: module for parameters related to estimation
- parameters.grid: module for parameters related to grid
- parameters.model: module for parameters related to model specifications
- parameters.interpolant: module for settings related to interpolation

*Note: Includes several unittests.*

#### the vig module

Modules containing vignettes for testing several functions. These are not unittests.

- vig.parameters: module for testing parameters
- vig.simupoint: module for testing simulations, over single parameter set
- vig.simugridrand: module for testing simulations, over meshed grid of parameters
- vig.simucounter: module for testing several counterfactuals
