import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class BlogPost(db.Model):
	title = db.StringProperty(required = True)
	post = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)	

class MainPage(Handler):
	def render_front(self, title="", post=""):
		self.render("front.html", title= title, post=post)

	def get(self):
		self.render_front()

class NewPost(Handler):
	def render_newpost(self, title="", post="", error=""):
		self.render("newpost.html", title=title, post=post, error=error)

	def get(self):
		self.render_newpost()

	def post(self):
		title = self.request.get("title")
		post = self.request.get("post")

		if title and post:
			a = BlogPost(title = title, post = post)
			a.put()

			self.redirect("/newpost")

		else:
			error = "we need both a title and some posts!"
			self.render_newpost(title, post, error)


app = webapp2.WSGIApplication([('/', MainPage),
								('/newpost', NewPost)], debug=True)
