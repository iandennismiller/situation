API
===

This is the **situation** Application Programming Interface (API).
This document provides a reference for using **situation** to write your own code.

situation
---------

.. automodule:: situation

.. autofunction:: dump

.. autofunction:: save

.. autofunction:: id_generator

Resource
^^^^^^^^

.. autoclass:: Resource(name, url, publisher, author, [description])
   :members:

Excerpt
^^^^^^^

.. autoclass:: Excerpt(content, resource, [xpath])
   :members:

Person
^^^^^^

.. autoclass:: Person(name, alias, [excerpts, events, places, possessions, properties, groups, acquaintances])
   :members:

Acquaintance
^^^^^^^^^^^^

.. autoclass:: Acquaintance(isa, person, acquainted, [excerpts])
   :members:

Place
^^^^^

.. autoclass:: Place(name, description, address, lat, lon, [owners, excerpts])
   :members:

Item
^^^^

.. autoclass:: Item(name, [excerpts, owners, description])
   :members:

Group
^^^^^

.. autoclass:: Group(name, [members, excerpts])
   :members:

Event
^^^^^

.. autoclass:: Event(name, [description, place, phone, timestamp, actors, excerpts, items])
   :members:
