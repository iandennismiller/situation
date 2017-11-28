# -*- coding: utf-8 -*-
# situation (c) Ian Dennis Miller

from nose.plugins.attrib import attr
from .debug_app import create_app
from flask_testing import TestCase


class BasicTestCase(TestCase):

    def create_app(self):
        return(create_app())

    def setUp(self):
        from flask_diamond import db
        db.create_all()

    @attr("single")
    def test_basic(self):
        "ensure the minimum test works"
        assert self.app

        from . import Resource

        Resource.create(
            name="Headline news for November 23",
            publisher="Big Paper Post",
            author="John Doe",
            url="http://example.com",
            )

    @attr("skip")
    def test_skip(self):
        "this always fails, except when it is skipped"
        self.assertTrue(False)
