Regarding Situation
===================

The **Situation** ontology is based upon research with several problem domains.
To put it simply, the **Situation** library provides a way to *precisely describe* some situations.

What is a situation?
--------------------

A situation - specifically, a social situation - is a configuration of people and circumstances, all of which are subject to description.
The situation should answer the question: *what is* - specifically with respect to Heidegger's notion of Thrownness (Geworfenheit).
What is one thrown into?
They are thrown into what there is - *da sein* or *Dasein*.
In this sense, situation is an impoverished shadow of Dasein.

Domain Specific Language
------------------------

**Situation** can be thought of as a Domain Specific Language (DSL) that provides an ontology for social situations.
To put it simply, this is a way to *precisely describe* some situations.

The constructs that typically underly a situation include people and relationships, events, places, and items.
These commonly-used entities are formalized by the *Situation* library.
Advantages to using a DSL include specificity and conciseness.

Networked nature of Situations
------------------------------

Situations may be expressed as a multi-partite graph - that is, a graph with many kinds of nodes and many kinds of edges.
There is often an underlying social graph connecting the people in the situation.
In addition, there may be other graphs overlaid upon the social graph.

Specifying a Situation
----------------------

Despite the graphical nature of situations, it is frustrating to construct a situation using a graphical approach.
I have found that imperative statements are much simpler to construct and accumulate.
In practice, it is simpler to rely upon the computer to extract the network from these statements.
The same situational network is implied by these statements.

I speculate that an impediment to situation construction with a computer display is the difficulty of working with layers of networks.

Flask-Diamond
-------------

A Situation must be hosted upon a custom Flask-Diamond application.
This provides a broad platform for developing deep integrations with your data pipeline.
Flask-Diamond provides helpful support, including database back-end, web-based data browser, and REST API building.

Situation size is bound by disk size, not memory size, because the situation is stored using a database engine like Postgresql or embedded sqlite3.
Anything described using *Situation* can be subsequently queried in a variety of ways, including directly with SQL.
Consequently, situation size is practically unlimited and situations can be queried effectively - even at scale.
