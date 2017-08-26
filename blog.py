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

# give datastore a parent
def blog_key(name = 'default'):
	return db.key.from_path('blogs', name)

class Blog(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)	

class MainPage(Handler):
	def render_front(self, title="", art=""):
		arts = db.GqlQuery("SELECT * FROM Blog "
							"ORDER BY created DESC")


		self.render("front.html", title=title, art=art, arts=arts)

	def get(self):
		self.render_front()

	# def post(self):
	# 	title = self.request.get("title")
	# 	art = self.request.get("art")

	# 	if title and art:
	# 		a = Blog(title = title, art = art)
	# 		a.put()

	# 		self.redirect("/")

	# 	else:
	# 		error = "we need both a title and some artwork!"
	# 		self.render_front(title, art, error)

class NewPost(Handler):
	def render_newpost(self, title="", art="", error=""):
		# arts = db.GqlQuery("SELECT * FROM Blog "
		# 					"ORDER BY created DESC")

		self.render("newpost.html", title=title, art=art, error=error)

	def get(self):
		self.render_newpost()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:
			a = Blog(title = title, art = art)
			a.put()

			self.redirect("/(\d+)")

		else:
			error = "we need both parameteres!"
			self.render_newpost(title, art, error)

class Confirm(webapp2.RequestHandler):
#	def render_confirm(self, title="", art=""):
#		arts = db.GqlQuery("SELECT * FROM Blog "
#							"WHERE id == obj.key().id()")

#		self.render("confirm.html", title = title, art = art)

	def get(self)
		arts = Att()
		arts.sent = self.request.get('')
#		self.render_confirm()


app = webapp2.WSGIApplication([('/', MainPage),
								('/newpost', NewPost),
								('/(\d+)', Confirm)], debug=True)