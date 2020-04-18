#! python2
import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from datastore import *
from datetime import datetime
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class ETask(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		if user:
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			tkbd = ndb.Key(TaskBoard,int(self.request.get("key"))).get()
			for task in tkbd.task:
				if self.request.get("tknm") == task.name:
					tk=task
			template_values = {
				'myuser' : myuser,
	            'tkbd' : tkbd,
				'tk':tk
				}
			template = JINJA_ENVIRONMENT.get_template('tkinfo.html')
		else:
			template = JINJA_ENVIRONMENT.get_template("error.html")
			template_values = {
			"error" : "Please login first!" ,
			"url" : "/"
			}

		self.response.write(template.render(template_values))

	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = ndb.Key('MyUser', user.user_id()).get()
		tkbd = ndb.Key(TaskBoard,int(self.request.get("tk_key"))).get()
		if self.request.get('button')=='Edit':
			for task in tkbd.task:
				if task.name == self.request.get("utk_name"):
					tk=task
			if user:
				if myuser.name in tkbd.Usersin or myuser.key == tkbd.ProdBy:
					tk.name=self.request.get('tk_name')
					tk.end= datetime.strptime(self.request.get('dl'),'%Y-%m-%d')
					tk.appoint_to= ndb.Key('MyUser',self.request.get('appt'))
					tk.flag='Pending'
					tkbd.put()
					self.redirect('/')
		elif self.request.get('button')=='Cancel':
				self.redirect('/')
		elif self.request.get('button')=='Complete':
				for task in tkbd.task:
					if task.name == self.request.get("utk_name"):
						tk=task
				if user:
					tk.flag='Complete'
					tk.complete=datetime.now()
					tkbd.put()
					self.redirect('/')
		elif self.request.get('button')=='Delete':
			tasks = []
			for task in tkbd.task:
				if task.name != self.request.get("utk_name"):
					tasks.append(task)
				if user:
						tkbd.task=tasks
						tkbd.put()
				self.redirect('/')

# #! python2
# import webapp2
# import jinja2
# from google.appengine.api import users
# from google.appengine.ext import ndb
# import os
# import time
# from datastore import *
# from edit import Edit
# from datetime import datetime
# JINJA_ENVIRONMENT = jinja2.Environment(
# 	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
# 	extensions=['jinja2.ext.autoescape'],
# 	autoescape=True)
# class ETask(webapp2.RequestHandler):
#     def get(self):
#         self.response.headers['Content-Type'] = 'text/html'
#         tkbd = ndb.Key(TaskBoard,int(self.request.get("key"))).get()
#         for task in tkbd.task:
#             if task.name == self.request.get('tknm'):
#                 tk=task
#
#         template_values = {
#         'tkbd' : tkbd,
#         'tk' : tk
#         }
#         template = JINJA_ENVIRONMENT.get_template("tkinfo.html")
#         self.response.write(template.render(template_values))
#     def post(self):
# 		self.response.headers['Content-Type'] = 'text/html'
#
# 		tkbd = ndb.Key(TaskBoard,int(self.request.get("key"))).get()
# 		if user:
# 			if self.request.get('button') == 'Edit':
# 				for task in tkbd.task:
# 					if task.name == self.request.get('tknm'):
# 						tk=task
# 				tk.name=self.request.get('tk_name')
# 				tk.put()
# 				self.redirect('/')
# 		# elif self.request.get('button') == 'Cancel':
# 		# 	self.redirect('/')
# 		# elif self.request.get('button') == 'Complete':
# 		# 	tk="rr"
# 		# elif self.request.get('button') == 'Delete':
# 		# 	tf="dsf"
# 		# else:
# 		# 	self.redirect('/')
