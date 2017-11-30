# -*- coding: utf-8 -*-
# situation (c) Ian Dennis Miller

from flask_diamond import db
from flask_diamond.mixins.crud import CRUDMixin


class AcquaintanceExcerpt(db.Model, CRUDMixin):
    """
    Excerpts describing or relating to an Acquaintance.

    An acquaintance is defined by a compound primary key.  In order to implement a
    many-to-many mapping, it must be possible for each acquaintanceship to have
    multiple excerpts for it.

    This table is able to implement these join conditions.
    """

    __tablename__ = 'acquaintance_excerpts'
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['person_id', 'acquainted_id'],
            ['acquaintance.person_id', 'acquaintance.acquainted_id']
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    excerpt_id = db.Column(db.Integer, db.ForeignKey('excerpt.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    acquainted_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)

"Excerpts."
persons_excerpts = db.Table('persons_excerpts',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('excerpt_id', db.Integer, db.ForeignKey('excerpt.id'))
)

"Excerpts."
places_excerpts = db.Table('places_excerpts',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('place_id', db.Integer, db.ForeignKey('place.id')),
    db.Column('excerpt_id', db.Integer, db.ForeignKey('excerpt.id'))
)

"Excerpts."
items_excerpts = db.Table('items_excerpts',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('excerpt_id', db.Integer, db.ForeignKey('excerpt.id'))
)

"Excerpts."
events_excerpts = db.Table('events_excerpts',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('excerpt_id', db.Integer, db.ForeignKey('excerpt.id'))
)

"Excerpts."
groups_excerpts = db.Table('groups_excerpts',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('excerpt_id', db.Integer, db.ForeignKey('excerpt.id'))
)

places_owners = db.Table('places_owners',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('place_id', db.Integer, db.ForeignKey('place.id')),
    db.Column('owner_id', db.Integer, db.ForeignKey('person.id'))
)


items_owners = db.Table('items_owners',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id')),
    db.Column('owner_id', db.Integer, db.ForeignKey('person.id'))
)


groups_members = db.Table('groups_members',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('member_id', db.Integer, db.ForeignKey('person.id'))
)


events_actors = db.Table('events_actors',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('person.id'))
)

events_items = db.Table('events_items',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
)
