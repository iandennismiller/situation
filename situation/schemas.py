# -*- coding: utf-8 -*-
# situation (c) Ian Dennis Miller

from flask_diamond import ma
from flask_marshmallow.fields import fields
from slugify import slugify


class ResourceSchema(ma.Schema):
    "Description"

    class Meta:
        additional = ("id", "unique", "name", "url", "publisher", "author", "description")


class ExcerptSchema(ma.Schema):
    "Description"

    class Meta:
        additional = ("id", "unique", "content", "resource_id", "xpath")


class PersonSchema(ma.Schema):
    "Description"

    slug = fields.Method("get_slugify")
    excerpts = fields.Nested('ExcerptSchema', allow_none=True, many=True, only=["id"])
    events = fields.Nested('EventSchema', allow_none=True, many=True, only=["id"])
    places = fields.Nested('PlaceSchema', allow_none=True, many=True, only=["id"])
    possessions = fields.Nested('ItemSchema', allow_none=True, many=True, only=["id"])
    properties = fields.Nested('PlaceSchema', allow_none=True, many=True, only=["id"])
    groups = fields.Nested('GroupSchema', allow_none=True, many=True, only=["id"])
    acquaintances = fields.Nested('PersonSchema', allow_none=True, many=True,
        only=["person_id", "acquainted_id"])

    # TODO: this is a nested query
    # "encounters": [i.id for e in self.events for i in e.items],

    def get_slugify(self, obj):
        return(slugify(obj.name))

    class Meta:
        additional = ("id", "name", "alias", "unique")


class AcquaintanceSchema(ma.Schema):
    "Description"

    excerpts = fields.Nested('ExcerptSchema', allow_none=True, many=True, only=["id"])

    class Meta:
        additional = ("isa", "person", "acquainted")


class PlaceSchema(ma.Schema):
    "Description"

    slug = fields.Method("get_slugify")
    excerpts = fields.Nested('ExcerptSchema', allow_none=True, many=True, only=["id"])
    events = fields.Nested('EventSchema', allow_none=True, many=True, only=["id"])
    owners = fields.Nested('PersonSchema', allow_none=True, many=True, only=["id"])

    def get_slugify(self, obj):
        return(slugify(obj.name))

    class Meta:
        additional = ("id", "unique", "name", "description", "address", "lat", "lon")


class ItemSchema(ma.Schema):
    "Description"

    slug = fields.Method("get_slugify")
    excerpts = fields.Nested('ExcerptSchema', allow_none=True, many=True, only=["id"])
    owners = fields.Nested('PersonSchema', allow_none=True, many=True, only=["id"])

    def get_slugify(self, obj):
        return(slugify(obj.name))

    class Meta:
        additional = ("id", "unique", "name", "description")


class GroupSchema(ma.Schema):
    slug = fields.Method("get_slugify")
    excerpts = fields.Nested('ExcerptSchema', allow_none=True, many=True, only=["id"])
    members = fields.Nested('PersonSchema', allow_none=True, many=True, only=["id"])

    def get_slugify(self, obj):
        return(slugify(obj.name))

    class Meta:
        additional = ("id", "unique", "name")


class EventSchema(ma.Schema):
    slug = fields.Method("get_slugify")
    timestamp = fields.Method("get_timestamp")
    excerpts = fields.Nested('ExcerptSchema', allow_none=True, many=True, only=["id"])
    items = fields.Nested('ItemSchema', allow_none=True, many=True, only=["id"])
    actors = fields.Nested('PersonSchema', allow_none=True, many=True, only=["id"])

    def get_slugify(self, obj):
        return(slugify(obj.name))

    def get_timestamp(self, obj):
        return(obj.timestamp.strftime('%Y-%m-%dT%H:%M:%S'))

    class Meta:
        additional = ("id", "unique", "name", "phone", "description", "place_id")
