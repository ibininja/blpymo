import uuid
import datetime

from src.common.database import Database
from src.models.post import Post

__author__ = 'ibininja'

class Blog:
    #Note here that you would have different blogs so each would have its own attributes
    #That is why it is a normal class with init method
    #_id is the auto generated id in mongoDB. This to avoid having duplicates withing the DB. so we just overwrite the _id.
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.author_id=author_id
        self.title = title
        self.description = description
        self._id=uuid.uuid4().hex if _id is None else _id

    #This is a normal function, without parameters because by default you can't use this without initializing it. So that's is why you just use the self to access the parameters.
    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    created_date=date)
        post.save_to_mongo()


    #Note that this is classmethod. Reasons are we are retrieving posts so all would have the same approach. or the same method of retrieving posts.
    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return{
            'author': self.author,
            'author_id': self.author_id,
            'title': self.title,
            'description': self.description,
            '_id': self._id
        }

    #The classmethod converts the returned values/data to an object of the current class or cls passed.
    #This approach is very usefull to make changes to the values and store to DB or even to use the methods.
    @classmethod
    def from_mongo(cls, _id): #here _id can be just id without _ because it is just a parameter and does not go near the database. the query asigns the value.
        blog_data=Database.find_one(collection='blogs', query={'_id':_id})
        # return cls(author=blog_data['author'],
        #             title=blog_data['title'],
        #             description=blog_data['description'],
        #             _id=blog_data['_id']
        #             )
        #The above commented block can be replaces with cls(**post_data) however one key point is that all parameters should be the same eg: author = post_data['author']
        #and not authorname=post_data['author'] namings of variable and dictionary key should be the same.  so then it can be written as:
        return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs= Database.find(collection='blogs', query={'author_id': author_id})
        return[cls(**blog) for blog in blogs]