#! python2
from google.appengine.ext import ndb

class Task(ndb.Model):
	name = ndb.StringProperty()
	createed_by = ndb.KeyProperty(kind="MyUser",repeated=False)
	appoint_to = ndb.KeyProperty(kind="MyUser",repeated=False)
	start = ndb.DateTimeProperty()
	end = ndb.DateTimeProperty()

class MyUser(ndb.Model):
	email_address = ndb.StringProperty()
	name = ndb.StringProperty()
	age = ndb.IntegerProperty()
	tb = ndb.KeyProperty(kind="TaskBoard",repeated=True)


class TaskBoard(ndb.Model):
	name = ndb.StringProperty()
	ProdBy = ndb.StringProperty()
	Usersin = ndb.KeyProperty(kind="MyUser", repeated=True)
	create_on = ndb.DateTimeProperty()
	update_on = ndb.DateTimeProperty()
	task = ndb.StructuredProperty(Task, repeated=True)
