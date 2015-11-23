import uuid

import datetime
from flask import session

from src.common.database import Database
from src.models.blog import Blog

__author__ = 'ibininja'

class User(object):

    #should containt the information the user would need.
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    # The below 2 methods are like get from_mongo but are with specific attributes.
    # The classmethod is because when we get info from DB they are just data not object. so we turn it to class.
    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email":email})
        if data is not None:
            return cls(**data)
    @classmethod
    def get_by_id(cls, _id):
        data= Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)
        #Default is return None here is would else return None

    @staticmethod
    # User.login_valid("email@email.com", "1234")
    def login_valid(email, password):
        #   check if user email match password sent
        user = User.get_by_email(email)
        if user is not None:
            #check password
            return user.password == password
        return False
        pass

    # The below is the original
    # @staticmethod
    # def register(email, password):
    #     user = User.get_by_email(email)
    #     if user is None:
    #         new_user = User(email, password)
    #         new_user.save_to_mongo()
    #     else:
    #         # user exists
    #         return False
    # The above can be replaced with this:
    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['session'] = email
            # as information to user all is good.
            return True
        else:
            # user exists You can return any info to user.
            return False

    @staticmethod
    def login(user_email):
        # login_valid has already been called so user has been validated
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        # Verify the structure of documents in DB for ease of retrieval.
        # Retrieval is best using an author ID because author name can be duplicated. unless is username. So Blog model is updated now to suit the change. prior only author name existed.
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        #author, title, description, author_id; the author details can be obtained from session
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)
        blog.save_to_mongo()

    @staticmethod #cause we are not using any variables in the current class.
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()): #blog_id to know which blog to save to. This is automated no need to input from user.
        # title, content, date=datetime.utcnow()
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date) #This has save to mongodb so we do not need to add save here.


    def json(self):
        return{
            "email": self.email,
            "_id": self._id,
            "password": self.password
            # Note that this method is not safe to send to browser/client or over network.
            # use it only for internal operations. else create another method without password parameter.

        }

    def save_to_mongo(self):
        Database.insert("users", self.json())