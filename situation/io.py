# -*- coding: utf-8 -*-
# situation (c) Ian Dennis Miller

import json
from . import Person, Acquaintance, Group, Place, Item, Event, Excerpt, Resource


def dump():
    """
    Build a dictionary containing the entire Situation.

    :returns: a Dict with the situation as nested Dictionaries.
    """
    "save all the people and everything else"
    return({
        "persons": [p.dump() for p in Person.query.order_by(Person.id).all()],
        "acquaintances": [a.dump() for a in Acquaintance.query.order_by(Acquaintance.person_id,
            Acquaintance.acquainted_id).all()],
        "groups": [g.dump() for g in Group.query.order_by(Group.id).all()],
        "places": [p.dump() for p in Place.query.order_by(Place.id).all()],
        "items": [i.dump() for i in Item.query.order_by(Item.id).all()],
        "events": [e.dump() for e in Event.query.order_by(Event.id).all()],
        # "details": [d.dump() for d in Detail.query.order_by(Detail.id).all()],
        "excerpts": [e.dump() for e in Excerpt.query.order_by(Excerpt.id).all()],
        "resources": [r.dump() for r in Resource.query.order_by(Resource.id).all()],
    })


def save(filename):
    """
    Write the Situation to a JSON file.

    :param str filename: the name of the file to output to.
    """
    with open(filename, "w") as f:
        json.dump(dump(), f, indent=True, sort_keys=True)


def build_events_dot():
    """
    Create a DOT graph from the Situation Events.

    :returns: str with a valid DOT representation of actors, events, and locations
    """
    buf = 'digraph G {\nranksep="1.0 equally";\nconcentrate=true;\nlandscape=false;\n'
    for event in Event.query.all():
        for actor in event.actors:
            buf += '"{0}" -> "{1}" [label="{2}"];\n'.format(actor.name, event.name, "")
        if event.place:
            buf += '"{0}" -> "{1}" [label="at"];\n'.format(event.name, event.place.name, "")
    buf += '}'
    return(buf)


def save_events_dot(filename):
    """
    Write the Events as a Dot file.

    :param str filename: the name of the file to output to.
    """
    buf = build_events_dot()
    with open(filename, "w") as f:
        f.write(buf)
