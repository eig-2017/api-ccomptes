# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import unicodecsv

from flask import url_for
from datetime import datetime

from cada.models import Advice


HEADER = [
    'Numéro de dossier',
    'Administration',
    'Type',
    'Année',
    'Séance',
    'Objet',
    'Thème et sous thème',
    'Mots clés',
    'Avis'
]


ANON_HEADER = ('id', 'url', 'replace', 'with')


def reader(f):
    '''CSV Reader factory for CADA format'''
    return unicodecsv.reader(f, encoding='utf-8', delimiter=b',', quotechar=b'"')


def writer(f):
    '''CSV writer factory for CADA format'''
    return unicodecsv.writer(f, encoding='utf-8', delimiter=b',', quotechar=b'"')


def cleanup(text):
    '''Sanitize text field from HTML encoded caracters'''
    return text.replace('&quot;', '"').replace('&amp;', '&')


def from_row(row):
    '''Create an advice from a CSV row'''
    subject = (row[5][0].upper() + row[5][1:]) if row[5] else row[5]
    return Advice.objects.create(
        id=row[0],
        administration=cleanup(row[1]),
        type=row[2],
        publication=datetime.strptime(row[4], '%d/%m/%Y'),
        subject=cleanup(subject),
        topics=[t.title() for t in cleanup(row[6]).split(', ')],
        tags=[tag.strip() for tag in row[7].split(',') if tag.strip()],
        content=cleanup(row[8]),
    )


def to_row(advice):
    '''Serialize an advice into a CSV row'''
    return [
        advice.id,
        advice.administration,
        advice.type,
        advice.publication.year,
        advice.publication.strftime('%d/%m/%Y'),
        advice.subject,
        ', '.join(advice.topics),
        ', '.join(advice.tags),
        advice.content,
    ]


def to_anon_row(advice):
    return (advice.id, url_for('front.display', id=advice.id, _external=True), '', '')
