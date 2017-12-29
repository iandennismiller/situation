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

Language Primitives
^^^^^^^^^^^^^^^^^^^

The language is described in detail in :doc:`API` documentation

- Resource
- Excerpt
- Person
- Acquaintance
- Place
- Item
- Group
- Event

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

Data Science Application
------------------------

A Situation must be hosted upon a custom `Flask-Diamond <http://flask-diamond.org>`_ application.
This provides a broad platform for developing deep integrations with your data science pipeline.
Flask-Diamond provides helpful support, including database back-end, web-based data browser, and REST API building.

Situation size is bound by disk size, not memory size, because the situation is stored using a database engine like Postgresql or embedded sqlite3.
Anything described using *Situation* can be subsequently queried in a variety of ways, including directly with SQL.
Consequently, situation size is practically unlimited and situations can be queried effectively - even at scale.

What can a Situation do?
------------------------

A situation supports analysis; ask it questions.
The pattern I've used is to specify a situation, then dump it as a JSON object to visualize.

Diamonds
--------

.. Rauthmann, J. F., Gallardo-Pujol, D., Guillaume, E. M., Todd, E., Nave, C. S., Sherman, R. A., … Funder, D. C. (2014). The Situational Eight DIAMONDS: A taxonomy of major dimensions of situation characteristics. Journal of Personality and Social Psychology, 107(4), 677.
.. Duty, Intellect, Adversity, Mating, pOsitivity, Negativity, Deception, and Sociality

Predicate Logic
---------------

There already exist formal notations for specifying entities, their memberships, and their interrelationships.

Semantic Web
^^^^^^^^^^^^

Resource Description Framework (RDF), a component of the so-called "Semantic Web," permits expressions that could be applied to social situation description.
The general form, "Subject is Adjective with/about Object," may be expressed with prefix notation - a predicate - as Adjective(Subject, Object).
Thus, the representation of "Alice is Friends with Bob" yields Friends(Alice, Bob).
This "Friends" predicate provides a language primitive for constructing a social network.

The Ontological Web Language (OWL) is a framework for specifying categories and groups.

RDF already provides the necessary grammar for supporting expressions of this form, so many aspects of a Situation ought to be expressible using RDF.

Situations ought to be representable with RDF and OWL.

There are several drawbacks to using the Semantic Web as a platform for situation modeling.

The languages are quite "heavy" in the sense that they seek to provide solutions for many problem domains.
This is a poor fit for the current problem which has a very narrow domain and therefore doesn't strictly require language support for other capabilities.

We do not control the languages.

XML and Semantic Web tools are inconsistent.
I've found it's unpleasant to work directly with XML.
It's inconvenient to build custom GUI components to simplify XML data entry.
GUI data entry necessarily constrains the range if input, so most of the expressive capability of XML is not available during the data entry process, anyway.
Analysis upon raw XML is virtually impossible; it must be transformed to another format (e.g. CSV) in order to interchange with an analysis pipeline.

Other representations for RDF, particularly triples notation, are concise and look surprisingly similar to Situation.

Graph Interchange
-----------------

Dot/GraphViz
^^^^^^^^^^^^

Gephi
^^^^^

NetworkX
^^^^^^^^

Neo4J
^^^^^

