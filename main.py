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

# User.create(username = "Vaibhav", password="1234", email = "vaibhav@gmail.com", profile_pic= "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkfvQFaMNLPNbjDrlUTv-F3w-S_EC_fjnlxIEJDks&s")
# User.create(username = "Sanjuli", password="1234", email = "sanjuli@gmail.com", profile_pic= "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkfvQFaMNLPNbjDrlUTv-F3w-S_EC_fjnlxIEJDks&s")
# User.create(username = "Anand", password="1234", email = "Anand@gmail.com", profile_pic= "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkfvQFaMNLPNbjDrlUTv-F3w-S_EC_fjnlxIEJDks&s")

# Article.create(username = 'Vaibhav', category_name ='Design', title='The Future of UI/UX Design: Trends and Best Practices for 2023', thumbnail='https://example.com/images/uiuxdesign.jpg', text="UI/UX design has been evolving rapidly over the past few years and with new technologies emerging, it's important for designers to stay updated on the latest trends and best practices. Here's what we can expect to see in 2023 and beyond: Artificial Intelligence (AI) and Machine Learning (ML) - With advancements in AI and ML, we can expect to see more personalized and intuitive design experiences. This can range from personalized product recommendations to chatbots that can handle customer service inquiries. Motion design - Motion design has been gaining popularity in recent years and this trend is expected to continue. The use of animations and micro-interactions will make user interfaces more engaging and user-friendly. Dark mode - The popularity of dark mode is expected to continue, as it not only looks sleek and modern but also helps reduce eye strain and improve battery life on mobile devices. Voice interfaces - Voice interfaces are becoming more common and are expected to be a key part of the future of UI/UX design. This includes voice-activated devices like Amazon Alexa and Google Home, as well as voice-controlled interfaces for mobile and desktop applications. Virtual and Augmented Reality (VR/AR) - VR and AR are becoming more accessible, and we can expect to see an increase in their use for design and product demonstrations, as well as for training and education purposes. When it comes to best practices, designers should focus on creating user-centered designs that prioritize accessibility and user experience. This includes using clear and concise language, providing clear and accessible navigation, and conducting user testing to validate design decisions. In conclusion, the future of UI/UX design is all about creating personalized, intuitive, and engaging experiences through the use of technology and design best practices. As the field continues to evolve, designers need to stay updated on the latest trends and best practices to remain competitive and deliver the best possible user experiences.UI/UX design has been evolving rapidly over the past few years and with new technologies emerging, it's important for designers to stay updated on the latest trends and best practices. Here's what we can expect to see in 2023 and beyond: Artificial Intelligence (AI) and Machine Learning (ML) - With advancements in AI and ML, we can expect to see more personalized and intuitive design experiences. This can range from personalized product recommendations to chatbots that can handle customer service inquiries. Motion design - Motion design has been gaining popularity in recent years and this trend is expected to continue. The use of animations and micro-interactions will make user interfaces more engaging and user-friendly. Dark mode - The popularity of dark mode is expected to continue, as it not only looks sleek and modern but also helps reduce eye strain and improve battery life on mobile devices. Voice interfaces - Voice interfaces are becoming more common and are expected to be a key part of the future of UI/UX design. This includes voice-activated devices like Amazon Alexa and Google Home, as well as voice-controlled interfaces for mobile and desktop applications. Virtual and Augmented Reality (VR/AR) - VR and AR are becoming more accessible, and we can expect to see an increase in their use for design and product demonstrations, as well as for training and education purposes. When it comes to best practices, designers should focus on creating user-centered designs that prioritize accessibility and user experience. This includes using clear and concise language, providing clear and accessible navigation, and conducting user testing to validate design decisions. In conclusion, the future of UI/UX design is all about creating personalized, intuitive, and engaging experiences through the use of technology and design best practices. As the field continues to evolve, designers need to stay updated on the latest trends and best practices to remain competitive and deliver the best possible user experiences.", short_description='A comprehensive guide to the future of UI/UX design, including the latest trends and best practices for the upcoming year.')

# Article.create(username = 'Sanjuli', category_name ='Software Engineering', title='Agile Software Development: What it is and why it matters', thumbnail=' https://example.com/images/agilesoftwaredevelopment.jpg', text='Agile software development is a method of software development that emphasizes collaboration, flexibility, and speed. It is a way of working that values delivering working software quickly and regularly, over following a strict plan or timeline. At its core, Agile development is based on the Agile Manifesto, a set of values and principles for software development that prioritize: Customer collaboration over contract negotiation. Working software over comprehensive documentation Responding to change over following a plan There are several reasons why Agile software development is becoming increasingly popular. Firstly, it allows teams to respond to changing requirements and feedback more quickly and effectively. This is because the process emphasizes frequent, short-term goals and regular feedback, rather than relying on a long-term plan that may become outdated. Another benefit of Agile development is improved collaboration and communication between team members. The process encourages regular meetings and close collaboration between developers, designers, and stakeholders, leading to better results and', short_description='A comprehensive guide to Agile software development, including an explanation of what it is, why it matters, and best practices for implementation.')

# Article.create(
#     username = 'Vaibhav', 
#     category_name ='Software Engineering', 
#     title='The Perks of Being Resourceful', 
#     thumbnail=' https://www.talentlms.com/library/wp-content/uploads/being-resourceful-online-training-course-thumb.jpg', 
#     text="Mark Watney is hands down one of my favourite characters from a movie (and/or a book). Matt Damon played it brilliantly in The Martian for which he got an Oscar nomination.Apart from his one-liners and uplifting sense of humour (even in the direst of situations), what makes Mark Watney standout from the rest of us is his limitless resourcefulness. You can put him in an impoverished habitat on a barren planet and he would manage to grow potatoes using his own poop. Who wouldn’t want to be more like him! The opposite of being resourceful is being hapless. Paul Graham writes:Hapless implies passivity. To be hapless is to be battered by circumstances—to let the world have its way with you, instead of having your way with the world.” Resourcefulness is about finding a way to get what you want, without waiting for conditions to be perfect or otherwise blaming the circumstances. Resourceful people either push through in the face of adverse conditions or manage to reverse the adverse conditions to achieve goals. After coming to terms with his new reality (being alone on mars with limited food) Watney’s attitude was, I’m going to have to science the shit out of this, instead of, I’m gonna die or My teammates are effing stupid or It’s NASA’s fault. It’s their responsibility to save me now. Of course NASA would do their part, but Watney didn’t just put it all on them. He took the shared responsibility of solving the problem, without worrying about whose ‘mistake’ it was or thinking about whose ‘responsibility’ it was. That’s resourcefulness! Resourcefulness isn’t creativity. People often confuse between the two. Yes, we have to be creative to be resourceful, but that’s not all. You need creativity to paint or write well, but you need to be resourceful to find a way to be seen or get published. Being creative doesn’t make you resourceful by default. Resourcefulness implies that the difficulties are novel. You can’t just look up and follow a set of prescribed steps. You can’t simply apply a tried and tested solution because you don’t know the nature of the problem. You have to keep trying new things. This is the essence of being resourceful. Resourcefulness isn’t an attitude. You cannot wake up one day and decide to be resourceful henceforth. It needs to be cultivated over time. Unless you have the required tools, compounded by creativity, along with a curious and positive attitude, it’s impossible to be resourceful. Mark Watney wasn’t a nobody. He was a NASA astronaut, a botanist, and an engineer. He had enough knowhow to burn hydrazine to generate water, grow potatoes from his poop, modify a rover for a long journey by adding solar cells and additional battery, using Morse code to communicate after he accidentally shorting out the electronics of Pathfinder, and whatnot! You cannot be resourceful unless you have ‘resources’. The most successful people are Watneyesque. They have all the necessary knowhow compounded by a positive attitude. They are neither hapless nor helpless. They don’t have to be babysitted. In other words, they can “take care of themselves.” But we don’t have to be a NASA astronaut left for dead on Mars to be resourceful. There are ample opportunities on Earth. When the Airbnb guys rented air mattresses to pay rent, they displayed resourcefulness. When they targeted the Democratic National Convention (2008) attendees, they displayed resourcefulness. When they sold cereal boxes to pay their credit card bills, they displayed resourcefulness. Can this quality be learnt? Yes, of course! The first step is to learn the fundamentals of as many things as we can. This will help us build a latticework of mental models that we can apply in numerous situations. The second step is to shift our thinking from reactive (victim) to proactive (victor). For example, going from “There’s nothing I can do” to “What are my alternatives?” This simple step, this shift in mindset reframes our mind to look at problems from a different perspective. Where there were shut doors, suddenly there are windows of possibilities that can be leveraged. We are no longer paralysed by our circumstances.",
#      short_description='The opposite of being resourceful is being hapless. Paul Graham writes:“Hapless implies passivity. To be hapless is to be battered by circumstances—to let the world have its way with you, instead of having your way with the world.')




# Article.create(username = 'vaibhav', category_name ='Software Engineering', title='Testing2', thumbnail='dummy', text='wrkecguc rwkg crekj ekckrjwccekt cecekjbt e tkce wtmnrw kctwcc,msdkxsrlkbckt cej cce t', short_description='xwxoirh ekjt ekjt')
# Article.create(username = 'ajay', category_name ='Software Engineering', title='Testing3', thumbnail='dummy', text='xkejgrd ectkgr  wxsr ct dct e chqrw crher htcytc rgvb5cryd tsbexe j gfkt eckdj cjkc rkc c dtc ec t cek', short_description='kekjvf ejhe ck ejhvew crjwhvcrw cnmr')
# Article.create(username = 'sanjuli', category_name ='Design', title='Testing4', thumbnail='dummy', text='xkjsfkebrjx reerr cethk crygjcbdfhcs erfsdfbdhrycd gfgdhvytegcfd ghvtcrf ewhk tew ec hktc t', short_description='ckjtvg etecbtewtwtewctweccc rheceytchgretrc ')
# Article.create(username = 'vaibhav', category_name ='Product', title='Testing5', thumbnail='dummy', text='UI/UX design has been evolving rapidly over the past few years and with new technologies emerging, it's important for designers to stay updated on the latest trends and best practices. Here's what we can expect to see in 2023 and beyond: Artificial Intelligence (AI) and Machine Learning (ML) - With advancements in AI and ML, we can expect to see more personalized and intuitive design experiences. This can range from personalized product recommendations to chatbots that can handle customer service inquiries. Motion design - Motion design has been gaining popularity in recent years and this trend is expected to continue. The use of animations and micro-interactions will make user interfaces more engaging and user-friendly.', short_description='xcjkhtv cejkdtvce bjhketcew tjh ct met c')
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
    return [{"user_info": article.username,"id": article.id, "title": article.title ,"description": article.short_description, "time":article.created_at, "thumbnail":article.thumbnail, "category":article.category_name} for  article in articles]
    # return [model_to_dict(article) for article in articles]

#Display Article By Id

@app.get("/articles/{id}")
def get_single_article(id : int):
    article = Article.select().where(Article.id == id).first()
    # single_article = Article.get(Article.id == id)
    return {
        "title": article.title,
        "short_description": article.short_description,
        "category" : article.category_name,
        "user_info": article.username,
        "thumbnail" : article.thumbnail,
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

