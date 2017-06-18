from peewee import Model, TextField, PrimaryKeyField, IntegerField

from bookish.app import db


class Translation(Model):

    class Meta:
        database = db

    idx = PrimaryKeyField()
    lithuanian = TextField()
    tier = IntegerField(default=1)
    comment = TextField(null=True)
    attempts = IntegerField(default=2)
    successes = IntegerField(default=1)

    def __str__(self):
        return str(self.lithuanian)


class NounTranslation(Translation):
    word_type = "noun"

    class Meta:
        db_table = "nouns"

    singular = TextField()
    plural = TextField(null=True)


class VerbTranslation(Translation):
    word_type = "verb"

    class Meta:
        db_table = "verbs"

    infinitive = TextField()
    present = TextField()
    past = TextField()
    perfect = TextField()


class SimpleTranslation(Translation):
    word_type = "word"

    class Meta:
        db_table = "words"

    word = TextField()
