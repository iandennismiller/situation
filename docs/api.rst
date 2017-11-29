API
===

situation
---------

.. automodule:: situation

.. autofunction:: dump

.. autofunction:: save

.. autofunction:: id_generator

Resource
^^^^^^^^

.. autoclass:: Resource(id, unique, name, url, publisher, author, description)
   :members:

Excerpt
^^^^^^^

.. autoclass:: Excerpt(id, unique, content, resource_id, [xpath])
   :members:

Person
^^^^^^

.. autoclass:: Person
   :members:

Acquaintance
^^^^^^^^^^^^

.. autoclass:: Acquaintance
   :members:

Place
^^^^^

.. autoclass:: Place
   :members:

Item
^^^^

.. autoclass:: Item
   :members:

Group
^^^^^

.. autoclass:: Group
   :members:

Event
^^^^^

.. autoclass:: Event
   :members:
