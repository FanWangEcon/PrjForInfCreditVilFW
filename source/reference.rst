.. sectnum::

This page provides the API reference for `package <https://prjforinfcreditvilfw.readthedocs.io/en/latest/>`__. Modules and functions are listed below in different sections.

Data Structures
---------------

Various data structures.

Array
~~~~~

Functions to manipulate numpy arrays and other structures.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.amto.array.geomspace
   prjforinfcreditvilfw.amto.array.gridminmax
   prjforinfcreditvilfw.amto.array.mesh
   prjforinfcreditvilfw.amto.array.scalararray

JSON
~~~~~

Function to manipulate JSON Structures

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
  :toctree: gen_modules
  :template: module.rst

  prjforinfcreditvilfw.amto.json.json


List and Dict
~~~~~~~~~~~~~~

List and dictionary

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
  :toctree: gen_modules
  :template: module.rst

  prjforinfcreditvilfw.amto.lsdc.lsdcconvert


Numeric
~~~~~~~~

Numeric manipulations

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
  :toctree: gen_modules
  :template: module.rst

  prjforinfcreditvilfw.amto.numeric.round


Amazon Web Services
-------------------

Functions to support AWS service usages.

General
~~~~~~~~

AWS general functions.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.aws.general.credentials
   prjforinfcreditvilfw.aws.general.path

S3
~~~~~

Functions for S3 storage.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.aws.s3.pushsync



Development
-----------

Package and function development support functions.

Log Support
~~~~~~~~~~~~~~~

Log support functions.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.devel.flog.logsupport

Object
~~~~~~

Object support functions.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.devel.obj.classobjsupport




Generate
-----------

Generate specific data-structures.


Random
~~~~~~

Data structures based on random seed draws.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.gen.rand.randgrid




Graph
-----------

Graphing support tools.

Example
~~~~~~~

Graphing example functions.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.graph.exa.scatterline3

Generic
~~~~~~~

All purpose graph support functions

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.graph.generic.allpurpose

Tools
~~~~~

Some graphing tools.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.graph.tools.subplot




Pandas
-----------

Pandas related functions.

Categorical
~~~~~~~~~~~

Functions to handle categorical variables.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.panda.categorical.catevars
   prjforinfcreditvilfw.panda.categorical.strsvarskeys

In and Out
~~~~~~~~~~

Functions for combine, export, etc dataframes.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.panda.inout.combine
   prjforinfcreditvilfw.panda.inout.readexport

Stats
~~~~~

Stats operations on dataframes.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.panda.stats.cutting
   prjforinfcreditvilfw.panda.stats.mean_varcov
   prjforinfcreditvilfw.panda.stats.polynomial_regression




Statistics
-----------

Statistical functions.

Interpolate
~~~~~~~~~~~

Interpolation functions.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.stats.interpolate.interpolate2d

Markov
~~~~~~

Markov related functions.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.stats.markov.transprobcheck

Multinomial
~~~~~~~~~~~

Discrete choice multinomial functions.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.stats.multinomial.multilogit




Utilities
-----------

General support functions.

In and Out
~~~~~~~~~~

Export, import etc.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.util.inout.exportpanda
   prjforinfcreditvilfw.util.inout.iosupport

Path
~~~~~

Path and location related functions.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.util.path.getfiles
   prjforinfcreditvilfw.util.path.movefiles

PDF
~~~~~

PDF generation support functions

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.util.pdf.pdfgen

RMD
~~~~~

RMD and bookdown related functions.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
   :toctree: gen_modules
   :template: module.rst

   prjforinfcreditvilfw.util.rmd.bookdownparse
   prjforinfcreditvilfw.util.rmd.mattexmd
   prjforinfcreditvilfw.util.rmd.rmdparse

Timer
~~~~~

Timer functions.

.. currentmodule:: prjforinfcreditvilfw

.. autosummary::
  :toctree: gen_modules
  :template: module.rst

  prjforinfcreditvilfw.util.timer.timer
