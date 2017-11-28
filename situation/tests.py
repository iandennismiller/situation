# -*- coding: utf-8 -*-
# situation (c) Ian Dennis Miller

from nose.plugins.attrib import attr
from flask_testing import TestCase
from flask_diamond import db
from .debug_app import create_app
from datetime import datetime
from . import Resource, Event, Person, Excerpt, Place


class BasicTestCase(TestCase):

    def create_app(self):
        return(create_app())

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @attr("single")
    def test_basic(self):
        "ensure the minimum test works"
        person1 = Person.create(name="Rob")
        person2 = Person.create(name="Scott")

        resource1 = Resource.create(
            name="Headline news for November 23",
            publisher="Big Paper Post",
            author="John Doe",
            url="http://example.com/1",
            )

        place1 = Place.create(
            name="Rob's House",
            address="233 Road St",
            lat=43,
            lon=-79,
            )

        excerpt1 = Excerpt.create(
            content="Snippet 1",
            resource=resource1,
            )

        Event.create(name="Incident",
            place=place1,
            timestamp=datetime(2012, 1, 11, 7, 30, 0),
            actors=[person1, person2],
            excerpts=[excerpt1]
        )

    @attr("skip")
    def test_skip(self):
        "this always fails, except when it is skipped"
        self.assertTrue(False)
