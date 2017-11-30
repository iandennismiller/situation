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

.. autoclass:: Resource(unique, name, url, publisher, author, [description])
   :members:

Excerpt
^^^^^^^

.. autoclass:: Excerpt(unique, content, resource_id, [xpath])
   :members:

Person
^^^^^^

.. autoclass:: Person(name, unique, alias, slug, [excerpts, events, places, possessions, properties, groups, acquaintances])
   :members:

Acquaintance
^^^^^^^^^^^^

.. autoclass:: Acquaintance(isa, excerpts, person, acquainted)
   :members:

Place
^^^^^

.. autoclass:: Place
   :members:

Item
^^^^

.. autoclass:: Item(unique, name, slug, excerpts, owners, [description])
   :members:

Group
^^^^^

.. autoclass:: Group
   :members:

Event
^^^^^

.. autoclass:: Event
   :members:
