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

    Any time an Excerpt is used, that Excerpt must be directly quotable from a Resource.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the resource is called
    :param str url: the canonical URL for the resource
    :param str publisher: the name of the institution reputationally backing this resource
    :param str author: the name of the author(s)
    :param str description: a short summary of this resource
    """

    __schema__ = ResourceSchema
    id = db.Column(db.Integer, primary_key=True)
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    name = db.Column(db.String(4096))
    url = db.Column(db.String(4096))
    publisher = db.Column(db.String(4096))
    author = db.Column(db.String(4096))
    description = db.Column(db.String(8**7))

    def __str__(self):
        return(self.url)


class Excerpt(db.Model, CRUDMixin, MarshmallowMixin):
    """
    Description.

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
    Description.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the person is called
    :param str alias: that *other* thing the person is called
    :param str slug: a URL-friendly identifier
    :param [Excerpt] excerpts: null
    :param [Event] events: null
    :param [Place] places: null
    :param [Item] possessions: null
    :param [Place] properties: null
    :param [Group] groups: null
    :param [Acquaintance] acquaintances: null
    """

    __schema__ = PersonSchema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
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
    Description.

    :param str isa: null
    :param Person person: null
    :param Person acquainted: null
    :param [Excerpt] excerpts: null
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
    Description.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the place is called
    :param str description: null
    :param str address: null
    :param float lat: null
    :param float lon: null
    :param [Person] owners: null
    :param [Excerpt] excerpts: null
    """

    __schema__ = PlaceSchema
    id = db.Column(db.Integer, primary_key=True)
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    name = db.Column(db.String(255))
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
    Description.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the item is called
    :param str description: null
    :param [Person] owners: null
    :param [Excerpt] excerpts: null
    """

    __schema__ = ItemSchema
    id = db.Column(db.Integer, primary_key=True)
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    name = db.Column(db.String(255))
    description = db.Column(db.String(8**7))
    owners = db.relationship('Person', secondary="items_owners", lazy='dynamic', backref="items")
    excerpts = db.relationship('Excerpt', secondary="items_excerpts", lazy='dynamic')

    def __str__(self):
        return(self.name)


class Group(db.Model, CRUDMixin, MarshmallowMixin):
    """
    Description.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the group is called
    :param [Person] members: null
    :param [Excerpt] excerpts: null
    """

    __schema__ = GroupSchema
    id = db.Column(db.Integer, primary_key=True)
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    name = db.Column(db.String(255))
    members = db.relationship('Person', secondary="groups_members", lazy='dynamic',
        backref="groups")
    excerpts = db.relationship('Excerpt', secondary="groups_excerpts", lazy='dynamic')

    def __str__(self):
        return self.name


class Event(db.Model, CRUDMixin, MarshmallowMixin):
    """
    Description.

    :param int id: the database object identifier
    :param str unique: alpha-numeric code for shorthand identifier
    :param str name: what the event is called
    :param str description: null
    :param Place place: null
    :param bool phone: *true* if this event is a phone call
    :param DateTime timestamp: null
    :param [Person] actors: null
    :param [Excerpt] excerpts: null
    :param [Item] items: null
    """

    __schema__ = EventSchema
    id = db.Column(db.Integer, primary_key=True)
    unique = db.Column(db.String(255), unique=True, default=id_generator)
    name = db.Column(db.String(255))
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
