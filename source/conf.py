# -*- coding: utf-8 -*-
#
# prjforinfcreditvilfw documentation build configuration file, created by
# sphinx-quickstart on Mon May  8 21:34:49 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
import warnings
import sphinx_bootstrap_theme
import subprocess

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
on_rtd = os.environ.get('READTHEDOCS') == 'True'
if not on_rtd:
    # sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    # https://github.com/sphinx-doc/sphinx/issues/2390
    sys.path.insert(0, 'G:/repos/prjforinfcreditvilfw')

rtd_version = os.environ.get('READTHEDOCS_VERSION', 'local')

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'sphinx.ext.linkcode',
    'sphinx_gallery.gen_gallery',
    'numpydoc',
    'nbsphinx',
    'autoapi.extension'
]

numpydoc_show_class_members = True
numpydoc_class_members_toctree = False

autosummary_generate = True
autosummary_generate_overwrite = False

intersphinx_mapping = {
    'python': ('https://docs.python.org/{.major}'.format(
        sys.version_info), None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference', None),
    'matplotlib': ('https://matplotlib.org/', None),
    'sklearn': ('https://scikit-learn.org/stable', None)
}

from sphinx_gallery.scrapers import matplotlib_scraper

class matplotlib_svg_scraper(object):

    def __repr__(self):
        return self.__class__.__name__

    def __call__(self, *args, **kwargs):
        return matplotlib_scraper(*args, format='svg', **kwargs)

sphinx_gallery_conf = {
    'examples_dirs': ['./examples'],
    'gallery_dirs': ['./auto_examples'],
    'reference_url':  {'prjforinfcreditvilfw': None},
    'default_thumb_file': '_static/img/logo.png',
    'backreferences_dir': 'gen_modules/backreferences',
    'doc_module': ('prjforinfcreditvilfw',),
    'image_scrapers': (matplotlib_svg_scraper(),),
    # 'binder': {
    #     # Required keys
    #     'org': 'rtavenar',
    #     'repo': 'prjforinfcreditvilfw',
    #     'branch': 'master',
    #     'binderhub_url': 'https://mybinder.org',
    #     'dependencies': '../../requirements.txt',
    #     # Optional keys
    #     'use_jupyter_lab': True
    # }
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'prjforinfcreditvilfw'
copyright = u'2020, Fan Wang fanwangecon.github.io'
author = 'Fan Wang'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
import prjforinfcreditvilfw
version = prjforinfcreditvilfw.__version__
# The full version, including alpha/beta/rc tags.
release = prjforinfcreditvilfw.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', '**.ipynb_checkpoints', 'Thumbs.db', '.DS_Store']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = 'sphinx_rtd_theme'
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_theme_options = {
    # Tab name for entire site. (Default: "Site")
    'navbar_site_name': "Site map",

    'navbar_links': [
        ("Quick Start", "quickstart"),
        ("Module Index", "py-modindex"),
        ("Examples", "auto_examples/index"),
    ],

    # Render the next and previous page links in navbar. (Default: true)
    'navbar_sidebarrel': False,

    # Render the current pages TOC in the navbar. (Default: true)
    'navbar_pagenav': False,

    # Tab name for the current pages TOC. (Default: "Page")
    'navbar_pagenav_name': "Current Page",

    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    'globaltoc_depth': -1,
    'globaltoc_includehidden': "false",

    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    'source_link_position': "exclude",

    # Bootswatch (http://bootswatch.com/) theme.
    #
    # Options are nothing (default) or the name of a valid theme
    # such as "cosmo" or "sandstone".
    #
    # The set of valid themes depend on the version of Bootstrap
    # that's used (the next config option).
    #
    # Currently, the supported themes are:
    # - Bootstrap 2: https://bootswatch.com/2
    # - Bootstrap 3: https://bootswatch.com/3
    'bootswatch_theme': "lumen"
}

def setup(app):
    app.add_css_file("custom.css") # also can be a full URL
    # if rtd_version != 'stable':
    #     app.add_javascript("custom.js")

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'prjforinfcreditvilfwdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'prjforinfcreditvilfw.tex', u'prjforinfcreditvilfw Documentation',
   u'Fan Wang', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'prjforinfcreditvilfw', u'prjforinfcreditvilfw Documentation',
     [u'Fan Wang'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'prjforinfcreditvilfw', u'prjforinfcreditvilfw Documentation',
   u'Fan Wang', 'prjforinfcreditvilfw', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False

# The following is used by sphinx.ext.linkcode to provide links to github
REVISION_CMD = 'git rev-parse --short HEAD'


def _get_git_revision():
    try:
        revision = subprocess.check_output(REVISION_CMD.split()).strip()
    except (subprocess.CalledProcessError, OSError):
        print('Failed to execute git to get revision')
        return None
    return revision.decode('utf-8')

def linkcode_resolve(domain, info):
    def find_source():
        # try to find the file and line number, based on code from numpy:
        # https://github.com/numpy/numpy/blob/master/doc/source/conf.py#L286
        obj = sys.modules[info['module']]
        for part in info['fullname'].split('.'):
            obj = getattr(obj, part)
        import inspect
        import os
        fn = inspect.getsourcefile(obj)
        fn = os.path.relpath(fn, start=os.path.dirname(prjforinfcreditvilfw.__file__))
        source, lineno = inspect.getsourcelines(obj)
        return fn, lineno, lineno + len(source) - 1

    if domain != 'py' or not info['module']:
        return None
    try:
        filename = 'prjforinfcreditvilfw/%s#L%d-L%d' % find_source()
    except Exception:
        filename = info['module'].replace('.', '/') + '.py'
    revision = _get_git_revision()
    return "https://github.com/fanwangecon/prjforinfcreditvilfw/blob/%s/%s" % (revision,
                                                                   filename)


warnings.filterwarnings("ignore", category=UserWarning,
                        message='Matplotlib is currently using agg, which is a'
                                ' non-GUI backend, so cannot show the figure.')

# AUTO API
autoapi_type = 'python'
autoapi_dirs = ['../prjforinfcreditvilfw']
