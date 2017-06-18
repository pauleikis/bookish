#!/usr/bin/env python
from argparse import ArgumentParser

from bookish.app import app, db
from bookish.model import NounTranslation, VerbTranslation, SimpleTranslation

parser = ArgumentParser()
parser.add_argument('--drop', action="store_true")
parser.add_argument('type', choices=['nouns', 'verbs', 'words'])
parser.add_argument('file')


def import_data(file, type):
    with app.app_context():
        if type == "nouns":
            for line in open(file):
                try:
                    lithuanian, singular, plural, comment = tuple(map(str.strip, line.split(",", maxsplit=3)))
                except ValueError:
                    print(tuple(map(str.strip, line.split(",", maxsplit=3))))
                    raise
                trans, _ = NounTranslation.get_or_create(lithuanian=lithuanian, defaults={
                    "singular": singular,
                    "plural": plural or None,
                    "comment": comment or None,
                })
                trans.singular = singular
                trans.plural = plural or None
                trans.comment = comment or None
                trans.save()
        if type == "verbs":
            for line in open(file):
                lithuanian, infinitive, present, past, perfect = tuple(map(str.strip, line.split(",", maxsplit=4)))
                trans, _ = VerbTranslation.get_or_create(lithuanian=lithuanian, defaults={
                    "infinitive": infinitive,
                    "present": present,
                    "past": past,
                    "perfect": perfect,
                })
                trans.infinitive = infinitive or None
                trans.present = present or None
                trans.past = past or None
                trans.perfect = perfect or None
                trans.save()
        if type == "words":
            for line in open(file):
                lithuanian, word, comment = tuple(map(str.strip, line.split(",", maxsplit=2)))
                trans, _ = SimpleTranslation.get_or_create(lithuanian=lithuanian, defaults={
                    "word": word,
                    "comment": comment or None,
                })
                trans.word = word or None
                trans.comment = comment or None
                trans.save()
        db.commit()


if __name__ == "__main__":
    args = parser.parse_args()
    with app.app_context():
        if args.drop:
            db.drop_table(NounTranslation, fail_silently=True)
            db.drop_table(VerbTranslation, fail_silently=True)
            db.drop_table(SimpleTranslation, fail_silently=True)
        db.create_tables([NounTranslation, VerbTranslation, SimpleTranslation], safe=True)
        db.commit()
    if args.file and args.type:
        import_data(args.file, args.type)
