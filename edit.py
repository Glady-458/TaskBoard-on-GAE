#! python2
import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from datastore import MyUser
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class Edit(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		if user:
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			template_values = {
				'myuser' : myuser,
	            'user' : user}
			template = JINJA_ENVIRONMENT.get_template('edit.html')
		else:
			template = JINJA_ENVIRONMENT.get_template("error.html")
			template_values = {
			"error" : "Please login first!" ,
			"url" : "/"
			}

		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		if self.request.get('button') == 'Update':
			user = users.get_current_user()
			if user:
				myuser_key = ndb.Key('MyUser', user.user_id())
				myuser = myuser_key.get()
				myuser.name = self.request.get('users_name')
				myuser.age = int(self.request.get('users_age'))

				myuser.put()
				self.redirect('/')


		elif self.request.get('button') == 'Cancel':
			self.redirect('/')
