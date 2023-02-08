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
    username = CharField(unique=True)
    email = CharField()
    password = CharField()
    profile_image_url = CharField()

class Authentication(BaseModel):
    user = ForeignKeyField(User, backref="authentications")
    token = CharField()

class Category(peewee.Model):
    category_name = peewee.CharField()

    class Meta:
        database = db

class Article(peewee.Model):
    # user_info = peewee.ForeignKeyField(User, to_field='username')
    category_name = peewee.ForeignKeyField(Category, to_field='category_name')
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
# Article.create(category_name='Software Development', title='Testing2', thumbnail='dummy', text='wrkecguc rwkg crekj ekckrjwccekt cecekjbt e tkce wtmnrw kctwcc,msdkxsrlkbckt cej cce t', short_description='xwxoirh ekjt ekjt')
# Article.create(category_name='Software Development', title='Testing3', thumbnail='dummy', text='xkejgrd ectkgr  wxsr ct dct e chqrw crher htcytc rgvb5cryd tsbexe j gfkt eckdj cjkc rkc c dtc ec t cek', short_description='kekjvf ejhe ck ejhvew crjwhvcrw cnmr')
# Article.create(category_name='Leadership', title='Testing4', thumbnail='dummy', text='xkjsfkebrjx reerr cethk crygjcbdfhcs erfsdfbdhrycd gfgdhvytegcfd ghvtcrf ewhk tew ec hktc t', short_description='ckjtvg etecbtewtwtewctweccc rheceytchgretrc ')
# Article.create(category_name='Management', title='Testing5', thumbnail='dummy', text='xskjgfsevrkegwuitcd fsdtegfdhrterdffbd gsewffbgd fdff gdfce ewkjt ce tcehwktcewr ct ewkj', short_description='xcjkhtv cejkdtvce bjhketcew tjh ct met c')
# Article.create(category_name='Leadership', title='Testing6', thumbnail='dummy', text='cs cd vrhv v v fsdtegfdhrterdffbd gsewffbgd fdff gdfce ewkjt ce tcehwktcewr ct ewkj', short_description='xcjcdtev yrd vdvtveyv rkhtv cejkdtvce bjhketcew tjh ct met c')

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
    return [{"id": article.id, "title": article.title ,"description": article.short_description, "category": article.category} for  article in articles]
    # return [model_to_dict(article) for article in articles]

#Display Article By Id

@app.get("/article/{id}")
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
async def login(username, password):
    
    try:
        user = User.get(User.username == username)

        bytes = password.encode('utf-8')
        
        salt = bcrypt.gensalt()
        
        hash = bcrypt.hashpw(bytes, salt)

        if User.password == hash:
            token = str(uuid.uuid4())
            Authentication.create(user=user, token=token)
            return {"message": "Login successful", "token": token}
        else:
            raise HTTPException(status_code=400, detail="Incorrect password")
    except User.DoesNotExist:
        raise HTTPException(status_code=400, detail="Username not found")


#Sign Up API

@app.post("/sign-up")
# async def register(username, email, password):
async def register(request: Request):

    request_data = await request.json()
    
    password = request_data.get("password")
    username = request_data.get("username")
    email = request_data.get("email")
    
    bytes = password.encode('utf-8')
        
    salt = bcrypt.gensalt()
    
    hash = bcrypt.hashpw(bytes, salt)

    try:
        new_user = User.create(username = username, email = email, password = hash)
    except peewee.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Username already registered")

    token = str(uuid.uuid4())
    Authentication.create(user=new_user, token=token)
    return {"message": "User registered", "token": token}


