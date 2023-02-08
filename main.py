from fastapi import FastAPI, Request, Response, HTTPException, UploadFile, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
from hashlib import sha256
from jinja2 import Template
from fastapi.responses import RedirectResponse
from playhouse.shortcuts import model_to_dict
import datetime
import pytz
import peewee
import uuid
import os
from peewee import*
import bcrypt
import json
from fastapi.middleware.cors import CORSMiddleware

time_zone = pytz.timezone('Asia/Kolkata')

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

db = peewee.SqliteDatabase("final_data.db")

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(primary_key=True)
    email = CharField()
    password = CharField()
    profile_pic = CharField()

class Authentication(BaseModel):
    user = ForeignKeyField(User, backref="authentications")
    token = CharField()

class Category(peewee.Model):
    category_name = peewee.CharField(unique=True)

    class Meta:
        database = db

class Article(peewee.Model):
    # user_info = peewee.ForeignKeyField(User, to_field='username')
    category_name = peewee.ForeignKeyField(Category, to_field='category_name')
    username = ForeignKeyField(User, to_field='username', backref='author_name')
    title = peewee.CharField()
    thumbnail = peewee.CharField()
    created_at = peewee.DateTimeField(default = datetime.datetime.now(time_zone).strftime("%Y-%m-%d %H: %M:%S"))
    updated_at = peewee.DateTimeField(default = datetime.datetime.now(time_zone).strftime("%Y-%m-%d %H: %M:%S"))
    text = peewee.CharField()
    short_description = peewee.CharField()

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Article , Category, User, Authentication])

# allow running from the command line

create_tables()

# Category.create(category_name = 'View All')
# Category.create(category_name ='Design')
# Category.create(category_name = 'Product')
# Category.create(category_name  ='Software Engineering')
# Category.create(category_name  ='Customer Service')
# Article.create(username = 'vaibhav', category_name ='Software Engineering', title='Testing2', thumbnail='dummy', text='wrkecguc rwkg crekj ekckrjwccekt cecekjbt e tkce wtmnrw kctwcc,msdkxsrlkbckt cej cce t', short_description='xwxoirh ekjt ekjt')
# Article.create(username = 'ajay', category_name ='Software Engineering', title='Testing3', thumbnail='dummy', text='xkejgrd ectkgr  wxsr ct dct e chqrw crher htcytc rgvb5cryd tsbexe j gfkt eckdj cjkc rkc c dtc ec t cek', short_description='kekjvf ejhe ck ejhvew crjwhvcrw cnmr')
# Article.create(username = 'sanjuli', category_name ='Design', title='Testing4', thumbnail='dummy', text='xkjsfkebrjx reerr cethk crygjcbdfhcs erfsdfbdhrycd gfgdhvytegcfd ghvtcrf ewhk tew ec hktc t', short_description='ckjtvg etecbtewtwtewctweccc rheceytchgretrc ')
# Article.create(username = 'vaibhav', category_name ='Product', title='Testing5', thumbnail='dummy', text='xskjgfsevrkegwuitcd fsdtegfdhrterdffbd gsewffbgd fdff gdfce ewkjt ce tcehwktcewr ct ewkj', short_description='xcjkhtv cejkdtvce bjhketcew tjh ct met c')
# Article.create(username = 'aman', category_name ='Customer Service', title='Testing6', thumbnail='dummy', text='cs cd vrhv v v fsdtegfdhrterdffbd gsewffbgd fdff gdfce ewkjt ce tcehwktcewr ct ewkj', short_description='xcjcdtev yrd vdvtveyv rkhtv cejkdtvce bjhketcew tjh ct met c')
# Article.create(username = 'aman', category_name ='Product', title='Product Launch', thumbnail='dummy', text='Creating and distributing a press release for your upcoming launch is essential because it can help you: Spread the word about your new product. Create a buzz around your brand and increase brand awareness Drive more sales. Let’s look at these benefits in detail and discover more reasons why you should get a well-structured pitch in place. So, here’s how a product launch press release can help your business: Efficiently share key product details with consumers and stakeholders. A press release is an easy way to communicate effectively with the business environment you operate in. Pitching to publishers focused on your niche will facilitate an easy way to convey essential product information to customers, industry experts, and stakeholders. Author’s Tip: Choose your publisher, blogger, or influencer wisely! According to Fractl, 80% of publishers say that relevancy in their beat is an important criterion for accepting or declining a pitch. If you don’t know how to pick the right publisher for your company’s news release, you can always search for a press release distribution service provider.', short_description='Having a Product Launch Press Release')
# Article.create(username = 'aman', category_name ='Design', title='Testing6', thumbnail='dummy', text='cs cd vrhv v v fsdtegfdhrterdffbd gsewffbgd fdff gdfce ewkjt ce tcehwktcewr ct ewkj', short_description='xcjcdtev yrd vdvtveyv rkhtv cejkdtvce bjhketcew tjh ct met c')
# Article.create(username = 'aman', category_name ='Design', title='Testing6', thumbnail='dummy', text='cs cd vrhv v v fsdtegfdhrterdffbd gsewffbgd fdff gdfce ewkjt ce tcehwktcewr ct ewkj', short_description='xcjcdtev yrd vdvtveyv rkhtv cejkdtvce bjhketcew tjh ct met c')

# Display category by Category Name

@app.get("/category/{category_name}")
async def get_user_posts(category_name : str):
    try:
        category = Category.get(Category.category_name == category_name)
    except Category.DoesNotExist:
        raise HTTPException(status_code=400, detail="Category not found")
    
    articles = Article.select().where(Article.category_name == category)
    category_articles = [{"category_name": article.title, "description": article.text} for article in articles]
    
    
    return [model_to_dict(article) for article in articles]

#Display All Articles

@app.get("/articles/")
def get_articles():
    articles = Article.select()
    return [{"user_info": article.username,"id": article.id, "title": article.title ,"description": article.short_description, "time":article.created_at, "thumbnail":article.thumbnail} for  article in articles]
    # return [model_to_dict(article) for article in articles]

#Display Article By Id

@app.get("/articles/{id}")
def get_single_article(id : int):
    article = Article.select().where(Article.id == id).first()
    # single_article = Article.get(Article.id == id)
    return {
        "title": article.title,
        "text": article.text
    }
    
#Create New Article

@app.post("/create_article")
async def create_post(request: Request):
    request_data = await request.json()
    # token = request.headers.get("Authorization")
    username = request_data.get("username")
    title = request_data.get("title")
    text = request_data.get("text")
    category_name = request_data.get("category_name")
    short_description = request_data.get("short_description")
    thumbnail = request_data.get("thumbnail")
    # print(image_url)
    

    # try:
    #     authentication = Authentication.get(Authentication.token == token)
    #     user = authentication.user
    # except Authentication.DoesNotExist:
    #     raise HTTPException(status_code=400, detail="Invalid Token")

    try:
        new_article = Article.create(
            title=title,
            username = username,
            text=text,
            category_name=category_name,
            short_description = short_description,
            thumbnail = thumbnail       
        )
    except peewee.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Error creating post")

    return {"message": "Post created successfully"}

#Edit Article using Article Id

@app.put("/edit_articles/{article_id}")
async def update_article(request : Request, article_id: int):
    try:
        request_data = await request.json()
    # token = request.headers.get("Authorization")
        article = Article.get(Article.id == article_id)
        article.title = request_data.get("title")
        article.text = request_data.get("text")
        article.category_name = request_data.get("category_name")
        article.updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        article.thumbnail = request_data.get("thumbnail")
        article.short_description = request_data.get("short_description")
        article.save()
        return {"message": "Article updated successfully", 'article': article}
    except Article.DoesNotExist:
        raise HTTPException(status_code=404, detail="Article not found")

#Delete Article

@app.delete("/delete_article/{id}")
async def deleteArticle(id): 
    try:
        query = Article.delete().where(Article.id == int(id))
        print(query)
        query.execute()
        return {'status': status.HTTP_200_OK}
    except Article.DoesNotExist:
        return {'message': 'Article Does Not Exist'}


#Sign in API

@app.post("/login")
async def login(request: Request):
    req = await request.json()
    username = req.get('username')
    password = req.get('password')
    
    try:
        user = User.get(User.username == username)
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt() 
        hash = bcrypt.hashpw(bytes, salt)

        if User.password == hash:
            token = str(uuid.uuid4())
            auth = Authentication.get(Authentication.user_id == user.username)
            auth.token = token
            auth.save()
            return {"message": "Login successful", "token": token}
        else:
            return {'message': 'Invalid Credentials'}
    except User.DoesNotExist:
        return {'message': 'Username not found'}


#Sign Up API

@app.post("/register")
async def register(request: Request):
    req = await request.json()
    username = req.get('username')
    password = req.get('password')
    email = req.get('email')
    profile_pic = req.get('profile_pic')

    
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    
    hash = bcrypt.hashpw(bytes, salt)

    try:
        new_user = User.create(username=username, email=email, password=hash, profile_pic=profile_pic)
        new_user.save()
    except peewee.IntegrityError:
        return {'message': 'Username already exists'}
    token = str(uuid.uuid4())
    Authentication.create(user_id=new_user.username, token=token)
    return {"message": "User registered", "token": token}


# @app.get("/search/{username}")

# async def search_by_author(request : Request):
#     request_data = request.json()

#     username = request_data.get("username")

#     try:
#         user = User.get(User.username == username)
#     except User.DoesNotExist:
#         raise HTTPException(status_code=400, detail="Author not found")
    
#     author = User.select().where(User.username == username)
#     category_articles = [{"category_name": article.title, "description": article.text} for article in articles]
    
    
#     return [model_to_dict(article) for article in articles]

