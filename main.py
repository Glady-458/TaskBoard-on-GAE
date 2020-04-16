#! python2
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from datastore import *
from ctb import *
from edit import Edit

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		url = ''
		url_string = ''
		welcome = 'Welcome back'
		myuser = None
		user = users.get_current_user()
		keys=[]
		tk = []
		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			if myuser == None:
				welcome = 'Welcome to the application'
				myuser = MyUser(id=user.user_id())
				myuser.email_address = user.email()
				myuser.put()
				self.redirect('/edit')
			for i in myuser.tb:
				keys.append(i.get())

			usr = MyUser.query().fetch()
			for u in usr:
				for t in u.tb:
					tk.append(t.get())

			for i in tk:
				for j in i.Usersin:

					p=j.get()
					if p.name == myuser.name:
						keys.append(i)

		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'
		template_values = {
			'url' : url,
			'url_string' : url_string,
			'user' : user,
			'welcome' : welcome,
			'myuser' : myuser,
			'keys' : keys,
			#'tk' : u,
		}
		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
('/', MainPage),
('/edit', Edit),
('/ctb', CTB),
], debug=True)
