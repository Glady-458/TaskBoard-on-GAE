#! python2
import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from datastore import *
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class Detail(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		if user:
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			tkbd = ndb.Key(TaskBoard,int(self.request.get("key"))).get()
			template_values = {
				'myuser' : myuser,
	            'tkbd' : tkbd}
			template = JINJA_ENVIRONMENT.get_template('details.html')
		else:
			template = JINJA_ENVIRONMENT.get_template("error.html")
			template_values = {
			"error" : "Please login first!" ,
			"url" : "/"
			}

		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
