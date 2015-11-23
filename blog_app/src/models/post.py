import uuid

import datetime

from src.common.database import Database

__author__ = 'ibininja'


class Post:
    def __init__(self, blog_id, title, content, author, created_date=datetime.datetime.utcnow(), _id=None): #remeber (args, kwargs) always default values are last. *dictionary
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        #Below is condition on line.
        self._id = uuid.uuid4().hex if _id is None else _id #universal unique identifier. modules to generate ID. number4 is random ID. there are other methods for other purposes: look @ documentation


    def save_to_mongo(self):
        Database.insert(collection='posts', data=self.json())


    def json(self):
        return {

            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'title': self.title,
            'content': self.content,
            'created_date': self.created_date
        }


   ##This method returns data or values instead of object
   # @staticmethod
   # def from_mongo(id):
   #     return Database.find_one(collection='posts', query={'id': id})

   #This method converts the returned data to object of the currect class.
   #Instead of we getting values we get an object of this class so we will be able to treat as an object and use the methods existing in this class.
   #By us changing whatever we get to the class type; it makes it easier to make ammendments and store back to mongo.
    @classmethod
    def from_mongo(cls, _id):
        post_data = Database.find_one(collection='posts', query={'_id': _id})
        # return cls(blog_id=post_data['blog_id'],
        #            title=post_data['title'],
        #            content=post_data['content'],
        #            author=post_data['author'],
        #            created_date=post_data['created_date'],
        #            _id=post_data['_id'])
        #The above commented block can be replaces with cls(**post_data) however one key point is that all parameters should be the same eg: author = post_data['author']
        #and not authorname=post_data['author'] namings of variable and dictionary key should be the same.  so:
        return cls(**post_data)

    @staticmethod
    def all_from_mongo():
        return [post for post in Database.find_all(collection='posts')]

    @staticmethod
    def from_blog(_id):
        return [post for post in Database.find(collection='posts', query={'blog_id':_id})] #Database.find(collection='posts', query={'blog_id':id}) returns a cursor