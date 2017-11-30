# -*- coding: utf-8 -*-
# situation (c) Ian Dennis Miller

import json
import string
import random
from flask_diamond import db
from flask_diamond.mixins.crud import CRUDMixin
from flask_diamond.mixins.marshmallow import MarshmallowMixin
from .schemas import ResourceSchema, ExcerptSchema, PersonSchema, AcquaintanceSchema, \
    PlaceSchema, ItemSchema, GroupSchema, EventSchema
from .secondary import AcquaintanceExcerpt


# https://stackoverflow.com/questions/2257441/python-random-string-generation-with-upper-case-letters-and-digits
def id_generator(size=8, chars=None):
    """
    Create a random sequence of letters and numbers.

    :param int size: the desired length of the sequence
    :param str chars: the eligible character set to draw from when picking random characters
    :returns: a string with the random sequence
    """
    if chars is None:
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))


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


class Resource(db.Model, CRUDMixin, MarshmallowMixin):
    """
    A Resource is an authoritative information source from which evidence is drawn.

    Usually, a Resource is an artifact like a newspaper article, a report, or another
    document.  These documents usually have an associated URL.

    There may be many Resource from a single publisher or organization.  Currently,
    the publisher is not a special component of the situation ontology.  If it is
    necessary to include a publisher in a model, represent it as a Group.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the resource is called (usually the title or headline)
    :param str url: the canonical URL for the resource
    :param str publisher: the name of the institution whose reputation backs this resource
    :param str author: the name of the author(s)
    :param str description: a short summary of this resource
    """

    __schema__ = ResourceSchema
    id = db.Column(db.Integer, primary_key=True)
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    name = db.Column(db.String(4096), nullable=False)
    url = db.Column(db.String(4096))
    publisher = db.Column(db.String(4096))
    author = db.Column(db.String(4096))
    description = db.Column(db.String(8**7))

    def __str__(self):
        return(self.url)


class Excerpt(db.Model, CRUDMixin, MarshmallowMixin):
    """
    An Excerpt is a direct quote that comes from any Resource.

    Any time an Excerpt is used, that Excerpt must be directly quotable from a Resource.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str content: the actual quoted material of the excerpt
    :param Resource resource: the Resource from which this excerpt comes
    :param str xpath: the xpath leading to this excerpt within the Resource
    """

    __schema__ = ExcerptSchema
    id = db.Column(db.Integer, primary_key=True)
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    content = db.Column(db.String(8**7))
    resource = db.relationship('Resource', backref='excerpts')
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)
    xpath = db.Column(db.String(4096))

    def __str__(self):
        return(self.content)


class Person(db.Model, CRUDMixin, MarshmallowMixin):
    """
    A Person is an actor in a Situation.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the person is called
    :param str alias: that *other* thing the person is called
    :param str slug: a URL-friendly identifier
    :param [Excerpt] excerpts: excerpts related to this Person
    :param [Event] events: events related to this Person
    :param [Place] places: places related to this Person
    :param [Item] possessions: items related to this Person
    :param [Place] properties: places owned by this Person
    :param [Group] groups: groups this Person is a member of
    :param [Acquaintance] acquaintances: people this Person knows
    """

    __schema__ = PersonSchema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(255))
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    excerpts = db.relationship('Excerpt', secondary="persons_excerpts", lazy='dynamic')

    def isa(self, isa_type, of=None):
        e = Acquaintance(person=self, isa=isa_type, acquainted=of)
        result = e.save()
        return result

    def __str__(self):
        return(self.name)


class Acquaintance(db.Model, CRUDMixin, MarshmallowMixin):
    """
    An Acquaintance is a relationship between Persons.

    This represents a directed edge, so a separate Acquaintance must be created
    to establish reciprocity.

    :param str isa: a description of the type of relationship
    :param Person person: the "source" of the acquaintance
    :param Person acquainted: the "target" of the acquaintance
    :param [Excerpt] excerpts: excerpts related to this Acquaintance
    """

    __schema__ = AcquaintanceSchema
    isa = db.Column(db.String(64))
    excerpts = db.relationship('Excerpt', secondary="acquaintance_excerpts", lazy='dynamic')
    person_id = db.Column(db.Integer(), db.ForeignKey('person.id'), primary_key=True)
    person = db.relationship(Person, primaryjoin=person_id == Person.id, backref='acquaintances')
    acquainted_id = db.Column(db.Integer(), db.ForeignKey('person.id'), primary_key=True)
    acquainted = db.relationship(Person, primaryjoin=acquainted_id == Person.id)

    def add_excerpt(self, excerpt):
        annotation = AcquaintanceExcerpt.create(
            excerpt_id=excerpt.id,
            person_id=self.person_id,
            acquainted_id=self.acquainted_id
            )
        return annotation

    def __str__(self):
        return("%s isa %s of %s)" % (self.person, self.isa, self.acquainted))


class Place(db.Model, CRUDMixin, MarshmallowMixin):
    """
    A Place is a location.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the place is called
    :param str description: a short summary of this place
    :param str address: a human-readable postal address
    :param float lat: latitude
    :param float lon: longitudel
    :param [Person] owners: the property owner(s)
    :param [Excerpt] excerpts: excerpts related to this Place
    """

    __schema__ = PlaceSchema
    id = db.Column(db.Integer, primary_key=True)
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(8**7))
    address = db.Column(db.String(4096))
    lat = db.Column(db.Float())
    lon = db.Column(db.Float())
    owners = db.relationship('Person', secondary="places_owners", lazy='dynamic',
        backref="properties")
    excerpts = db.relationship('Excerpt', secondary="places_excerpts", lazy='dynamic')

    def __str__(self):
        return(self.name)


class Item(db.Model, CRUDMixin, MarshmallowMixin):
    """
    An item is any "thing" that is work describing.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the item is called
    :param str description: a short summary of this item
    :param [Person] owners: the property owner(s)
    :param [Excerpt] excerpts: excerpts related to this Item
    """

    __schema__ = ItemSchema
    id = db.Column(db.Integer, primary_key=True)
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(8**7))
    owners = db.relationship('Person', secondary="items_owners", lazy='dynamic', backref="items")
    excerpts = db.relationship('Excerpt', secondary="items_excerpts", lazy='dynamic')

    def __str__(self):
        return(self.name)


class Group(db.Model, CRUDMixin, MarshmallowMixin):
    """
    A Group is a collection of Persons who are associated with one another.

    Membership in a group implies a many-to-many relationship between the members.
    A group is different from an Acquaintance; it is bi-directional, not uni-directional.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the group is called
    :param [Person] members: people who are members of this Group
    :param [Excerpt] excerpts: excerpts related to this Group
    """

    __schema__ = GroupSchema
    id = db.Column(db.Integer, primary_key=True)
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    name = db.Column(db.String(255), nullable=False)
    members = db.relationship('Person', secondary="groups_members", lazy='dynamic',
        backref="groups")
    excerpts = db.relationship('Excerpt', secondary="groups_excerpts", lazy='dynamic')

    def __str__(self):
        return self.name


class Event(db.Model, CRUDMixin, MarshmallowMixin):
    """
    An Event is an occurrence that somehow alters the Situation.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the event is called
    :param str description: a short summary of this item
    :param Place place: null
    :param bool phone: *true* if this event is a phone call
    :param DateTime timestamp: null
    :param [Person] actors: null
    :param [Excerpt] excerpts: excerpts related to this Event
    :param [Item] items: null
    """

    __schema__ = EventSchema
    id = db.Column(db.Integer, primary_key=True)
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(8**7))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    place = db.relationship("Place", backref="events")
    phone = db.Column(db.Boolean(), default=False)
    timestamp = db.Column(db.DateTime())
    actors = db.relationship('Person', secondary="events_actors", lazy='dynamic', backref="events")
    excerpts = db.relationship('Excerpt', secondary="events_excerpts", lazy='dynamic')
    items = db.relationship('Item', secondary="events_items", lazy='dynamic')

    def __str__(self):
        return self.name
