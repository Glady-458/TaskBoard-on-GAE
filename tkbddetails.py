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
class Detail(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		adu = []
		task=[]
		if user:
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			tkbd = ndb.Key(TaskBoard,int(self.request.get("key"))).get()
			usr = MyUser.query().fetch()
			if len(tkbd.Usersin) != 0:
				for a in tkbd.Usersin:
						if a.get() in usr:
							for u in usr:
								if (tkbd.ProdBy.get().name != u.name):
									if u.key not in tkbd.Usersin:
										if u.key not in adu:
											adu.append(u.key)
			else:
				for u in usr:
					if (tkbd.ProdBy.get().name != u.name):
						if u.key not in tkbd.Usersin:
							if u.key not in adu:
								adu.append(u.key)
			c = 0
			c1 = 0
			c2 = 0

			for tk in tkbd.task:
				tkct= str(tk.complete).strip(" ")
				now = str(datetime.now()).strip(" ")
				if tk.flag != 'Complete':
					c=c+1
				elif tk.flag == 'Complete':
					c1=c1+1
				if tkct[0]==now[0]:
					c2=c2+1

			template_values = {
				'myuser' : myuser,
	            'tkbd' : tkbd,
				'usr' : usr,
				'adu' : adu,
				'c' : c,
				'c1' : c1,
				'c2' : c2,
				}
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
		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = ndb.Key('MyUser', user.user_id()).get()
		tkbd = ndb.Key(TaskBoard,int(self.request.get("tkd_key"))).get()
		if user:
			if tkbd.ProdBy.get().name == myuser.name:
				if self.request.get('button')=='Update':
					tkbd.name=self.request.get('tkd_name')
					#=----------------------------------------
					ids=self.request.POST.getall('ck')
					keys=[]
					for i in ids:
						keys.append(ndb.Key("MyUser",i))
						for i in keys:
							if i not in tkbd.Usersin:
								tkbd.Usersin.append(i)
					#=----------------------------------------
					ids2=self.request.POST.getall('rck')
					keys2=[]
					for i in ids2:
						keys.append(ndb.Key("MyUser",i))
						for i in keys:
							if i in tkbd.Usersin:
								tkbd.Usersin.remove(i)
								for tks in tkbd.task:
									if i == tks.appoint_to:
										tks.flag = 'Un Assign'
										tks.appoint_to=ndb.Key('MyUser',1)
					#=----------------------------------------
					tkbd.update_on=datetime.now()
					tkbd.put()
					self.redirect('/')
				elif self.request.get('button')=='Cancel':
					self.redirect('/')
				elif self.request.get('button')=='Delete':
					if  tkbd.task == [] and tkbd.Usersin==[]:
						myuser.tb.remove(tkbd.key)
						tkbd.key.delete()
						myuser.put()
						self.redirect('/')
					else:
							template = JINJA_ENVIRONMENT.get_template("error.html")
							template_values = {
			                	"error" : "remove all the users and delete all the task to delete this taskboard" ,
			                	"url" : "/"
								}
							self.response.write(template.render(template_values))
