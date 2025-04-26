"""
Configuración de Sphinx para la documentación del proyecto.
"""

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# Configuración del proyecto
project = 'Sistema de Automatización de Llamadas'
copyright = '2025, Santiago Martinez'
author = 'Santiago Martinez'
release = '1.0.0'

# Extensiones
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinxcontrib.plantuml',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.graphviz',
]

# Configuración de intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'fastapi': ('https://fastapi.tiangolo.com', None),
}

# Configuración de PlantUML
plantuml = 'plantuml'  # Usar plantuml instalado en el sistema
plantuml_output_format = 'svg'
plantuml_latex_output_format = 'pdf'

# Configuración de plantillas
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Configuración de idioma
language = 'es'

# Tema HTML
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# plantuml_path = '/usr/bin/plantuml'

# Configuración de autodoc
autodoc_default_options = {
    'members': True,
    'member_order': 'bysource',
    'special_members': '__init__',
    'undoc_members': True,
    'exclude_members': '__weakref__'
}

# Configuración adicional
html_css_files = [
    'custom.css',
]

html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
    'vcs_pageview_mode': 'blob',
    'style_nav_header_background': '#2980B9',
}

# Configuración de napoleon
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Validación de enlaces
linkcheck_ignore = [
    r'http://localhost:\d+/',
]
