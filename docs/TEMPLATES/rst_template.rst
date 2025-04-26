.. _module-name:

Module Name
==========

.. module:: app.module_name

Overview
--------

Brief description of the module and its purpose.

Detailed description with more information about what this module does,
its purpose, and any important implementation details.

Classes
-------

.. autoclass:: ClassName
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

Functions
---------

.. autofunction:: function_name

Usage Examples
-------------

Basic Usage
~~~~~~~~~~

.. code-block:: python

   from app.module_name import ClassName
   
   instance = ClassName("param1", param2=42)
   result = instance.method_name()

Advanced Usage
~~~~~~~~~~~~~

.. code-block:: python

   from app.module_name import function_name
   
   result = function_name("param1", [1, 2, 3])

API Reference
------------

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - ``ClassName``
     - Brief description of ClassName
   * - ``function_name``
     - Brief description of function_name

See Also
--------

* :ref:`related-module` - Description of related module
* :ref:`another-related-module` - Description of another related module

Diagrams
--------

.. uml::

   @startuml
   class ClassName {
     +attribute1: str
     +attribute2: int
     +method_name(param1: str, param2: int): dict
   }
   @enduml
