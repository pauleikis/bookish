from peewee import Model, TextField, PrimaryKeyField, IntegerField

from bookish.app import db


class Pair(Model):
	idx = PrimaryKeyField()
	english = TextField()
	german = TextField()
	attempts = IntegerField(default=2)
	successes = IntegerField(default=0)

	class Meta:
		database = db
		db_table = "translations"

	def __str__(self):
		return str(self.english) + "=" + str(self.german)
