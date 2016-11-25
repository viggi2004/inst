from mongoengine import *
class User(Document):
	id = StringField(primary_key=True)
	username = StringField()
	def dict(self):
		return {
			'id': self.id,
			'username': self.username
		}