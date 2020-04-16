#! python2
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import time
from datastore import *
from edit import Edit
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class CTB(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = myuser_key.get()
		usr = MyUser.query().fetch()
		myu=myuser
		# if user:		167176955777861719774
		# 	myu_key=ndb.Key('MyUser', user.user_id())
		# 	myu=myu_key.get()
		template_values = {
            'tk' : myu,
            'myuser' : myuser,
			'usr' : usr,
			'user' : user,
			'MyUser' : MyUser,
		}
		template = JINJA_ENVIRONMENT.get_template('ctb.html')
		self.response.write(template.render(template_values))

    def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		# myuser_key = ndb.Key('MyUser', user.user_id())
		# myuser = myuser_key.get()
		#keyno = int(time.time()*1000)+int(user.user_id())-117015319568420173343-8789446238771050223-60000000000001021146
		if self.request.get('button') == 'Add':
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			#tkbd_key = ndb.Key('TaskBoard', user.user_id())
			#tkbd=tkbd_key.get()
			#myuser.tb.append([ndb.Key(TaskBoard,keyno)])
			ids=self.request.POST.getall('ck')
			keys=[]
			for i in ids:
				keys.append(ndb.Key("MyUser",i))
			tkbd_key=ndb.Key('TaskBoard',user.user_id())
			tkbd=tkbd_key.get()
			tkbd=TaskBoard(name = self.request.get('tk_name'),
							ProdBy = self.request.get('tk_pro'),
							Usersin= keys)

			tkbd.put()
			myuser.tb.append(tkbd.key)
			myuser.put()
			self.redirect('/')
			# myuser.tb.name=append(self.request.get('tk_name'))

		elif self.request.get('button') == 'Cancel':
			self.redirect('/')
