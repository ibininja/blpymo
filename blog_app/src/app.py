from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

__author__ = 'ibininja'

from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)  # __main__
app.secret_key = 'mokdad'  # use complex if going public


@app.route('/')
def home_template():
    return render_template('home.html')


# http://mysite.com/api/login
@app.route('/login')
def hello_method():
    return render_template('login.html')


# http://mysite.com/api/register
@app.route('/register')
def register_method():
    return render_template('register.html')


@app.before_first_request  # means run this before the first requrest.
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None
        return render_template('login.html',
                               failed_login=True)  # check if variable check_login is passed, other wise do not display error message

    return render_template("profile.html", email=session['email'])


@app.route('/test')
def test_method():
    return "Hello World"


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)
    return render_template("profile.html", email=session['email'])

@app.route('/blogs/<string:user_id>')
@app.route('/blogs') #this to access own blog
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email)

@app.route('/posts/<string:blog_id>') #posts would not exist without blogs. having blog_id is a must so no app.rout without blog_id like above in user_blogs
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()
    return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog._id)

#we do not need user ID. cause he has to be logged in to make new posts
@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    #user came in directly from a url; so show them the create new from
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title= request.form['title']
        description= request.form['description']
        user = User.get_by_email(session['email'])

        new_blog=Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()
        #the below returns or calls user_blogs
        return make_response(user_blogs(user._id))

@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    #user came in directly from a url; so show them the create new from
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title= request.form['title']
        content= request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()
        print(blog_id)
        #the below returns or calls user_blogs
        return make_response(blog_posts(blog_id))

if __name__ == '__main__':
    app.run(port=4555, debug=True)  # to choose port to run on use app.run(port=4555) or whatever port number you like
