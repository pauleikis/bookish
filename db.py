from bookish.app import app, db
from bookish.model import Pair


if __name__ == "__main__":
	with app.app_context():
		db.drop_table(Pair, fail_silently=True)
		db.create_tables([Pair])
		Pair.create(english="black", german="schwarz")
		db.commit()
