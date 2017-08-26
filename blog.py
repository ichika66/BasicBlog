import os
import webapp2
import jinja2
from string import letters

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
    return db.Key.from_path('blogs', name)

class Blog(db.Model):
	title = db.StringProperty(required = True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)	
	last_modified = db.DateTimeProperty(auto_now = True)

class MainPage(Handler):
	def get(self):
		arts = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
		self.render('front.html', arts = arts)

class NewPost(Handler):
	def get(self):
		self.render("newpost.html")

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:
			a = Blog(parent = blog_key(), title = title, art = art)
			a.put()
			self.redirect('/%s' % str(a.key().id()))

		else:
			error = "we need both parameteres!"
			self.render("newpost.html", title=title, art=art, error=error)

class Confirm(Handler):
	def get(self, post_id):
		key = db.Key.from_path('Blog', int(post_id), parent=blog_key())
		post = db.get(key)
		self.render("confirm.html", post = post)

app = webapp2.WSGIApplication([('/', MainPage),
								('/newpost', NewPost),
								('/([0-9]+)', Confirm)], debug=True)