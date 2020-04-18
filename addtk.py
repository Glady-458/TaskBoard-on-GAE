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
class ATask(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        task=[]
        if user:
            myuser=ndb.Key('Myuser',user.user_id()).get()
            tkbd = ndb.Key(TaskBoard,int(self.request.get("key"))).get()
            for i in tkbd.task:
                task.append(i)
            template = JINJA_ENVIRONMENT.get_template("addtask.html")
            template_values = {
                'tkbd' : tkbd,
                'tk' : task,
            }
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

        if self.request.get('button') == 'Add':
            name=[]
            for i in tkbd.task:
                name.append(i.name)
            n=self.request.get('tk_name')
            if n not in name:
                tkbd.task.append(Task(name=self.request.get('tk_name'),
                start=datetime.now(),
                createed_by=myuser.key,
                appoint_to=ndb.Key('MyUser',self.request.get('assign')),
                end = datetime.strptime(self.request.get('dl'),'%Y-%m-%d')
                ))
                tkbd.update_on = datetime.now()
                tkbd.put()


        elif self.request.get('button') == 'Cancel':
            self.redirect('/ctb')
