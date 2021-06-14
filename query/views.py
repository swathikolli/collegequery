from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
import json
import smtplib
from datetime import date
from .models import *
from datetime import date
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')
 

#home page
def index(request):
    ob1=Question.objects.raw('select * from query_question')
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    return  render(request, "query/home.html", {
                "questions":ob1,
                "uname":user_name


            })
def forgot(request):
    return render(request, "query/for.html")
# forget password rest
def forgot_passwd(request):
    if request.method == "POST" :
        username = request.POST["username"]
        emailid= request.POST["emailid"]
    ob=Person.objects.raw('select * from query_person where  query_person.mailid=%s',[emailid]) 
    for i in ob:
        pw=i.password
    u_password="your password is:" + pw
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login("collegequery2021@gmail.com","Query@2021")
    server.sendmail("collegequery2021@gmail.com",emailid,pw)
    server.quit()    
    return render(request, "query/login.html")
def flog(request):
    return render(request, "query/login.html")
def fhome(request):
    return render(request, "query/home.html")
def freg(request):
    return render(request, "query/register.html")
# question and previous answers will display and can post answer
def question(request,name,qid):
    id=name
    q_id=qid
    ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[id]) 
    ob1=Question.objects.raw('select * from query_question where  query_question.id=%s',[q_id]) 
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    answers=Answer.objects.raw('select * from query_answer a where  a.question_id=%s',[q_id])
    user_name_answer=Person.objects.raw('select p.username,a.id from query_person p,query_answer a where  a.user_id==p.id')
    return render(request, "query/question_inner.html", {
                "details":ob,
                "question":ob1,
                "uname":user_name,
                "answers":answers,
                "user_name_answer": user_name_answer
            }) 
#Ask page to post question
def ask(request,name):
    id=name
    ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[id])  
    return  render(request, "query/askpage_inner.html", {
                "details":ob
            })
#home page after login
def home(request,name):
    id=name
    ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[id])  
    ob1=Question.objects.raw('select * from query_question')
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    return  render(request, "query/profile.html", {
                "details":ob,
                "questions":ob1,
                "uname":user_name

            })
#After submitting register form redirect to the profile page
def profile(request):
    m=0
    if request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        emailid= request.POST["email"]
        data=Person()
        data.username=username
        data.password=password
        data.mailid=emailid
        email=Person.objects.raw('select * from query_person')  
        for e in email:
            if e.mailid == emailid:
                 m=1
                 return render(request, "query/register.html",{
             "message":"This mail is already registered.."
             })
        DOMAINS_ALLOWED = ['rguktsklm.ac.in']
        email_domain = emailid.split('@')[-1]

        if email_domain not in DOMAINS_ALLOWED:
                 m=1
                 return render(request, "query/register.html",{
             "message":"This mail id not accepted"
             })
        try:
            data.profile_pic = request.FILES['profile_pic']
        except:
            print("No image selected")
    
        if m==0:
               data.save()

    ob=Person.objects.raw('select * from query_person where  query_person.username=%s',[username])  
    id=""
    for m in ob:
        id=m.id
    ob1=Person.objects.raw('select * from query_person where  query_person.id=%s',[id]) 
    ob2=Question.objects.raw('select * from query_question')
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    return  render(request, "query/profile.html", {
                "details":ob1,
                "questions":ob2,
                "uname":user_name            })
#After submitting question
def question_details(request):
    if request.method == "POST" :
        q_title = request.POST["q_title"]
        description = request.POST["description"]
        userid=request.POST["userid"]
        data=Question()
        data.title=q_title
        data.description=description
        today=date.today()
        d=today.strftime("%B %d, %Y")
        data.date=d
        now=datetime.now()
        data.time=now.strftime("%H:%M:%S")
        data.user_id=userid 
        data.save()
    ob1=Person.objects.raw('select * from query_person where  query_person.id=%s',[userid])  
    
    return  render(request, "query/askpage_inner.html",{
        "details":ob1
        })
#Afeter submitting the answer
def answer_details(request):
    if request.method == "POST" :
        description = request.POST["description"]
        userid=request.POST["userid"]
        qid=request.POST["qid"]
        data=Answer()
        data.ans=description
        today=date.today()
        d=today.strftime("%B %d, %Y")
        data.date=d
        now=datetime.now()
        data.time=now.strftime("%H:%M:%S")
        data.user_id=userid 
        data.question_id=qid
        data.save()
    ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[userid])  
    ob1=Question.objects.raw('select * from query_question where  query_question.id=%s',[qid]) 
    ob2=Person.objects.raw('select a.mailid,q.id from query_person a,query_question q where  a.id==q.user_id and  q.id=%s',[qid])
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    answers=Answer.objects.raw('select * from query_answer a where  a.question_id=%s',[qid])
    user_name_answer=Person.objects.raw('select p.username,a.id from query_person p,query_answer a where  a.user_id==p.id')
    for qn in ob1:
        questions_title=qn.title
    for q in ob2:
        questioner_mailid=q.mailid
    mail_data= "Some one Answered your question:" +questions_title
    server = smtplib.SMTP_SSL("smtp.gmail.com",465)
    server.login("collegequery2021@gmail.com","Query@2021")
    server.sendmail("collegequery2021@gmail.com",questioner_mailid,"Some one anwered to your question")
    server.quit()    

    return  render(request, "query/question_inner.html",{
        "details":ob,
        "question":ob1,
        "uname":user_name,
        "answers":answers,
        "user_name_answer": user_name_answer,
        "questioner_mailid":questioner_mailid
        })
def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["lusername"]
        password = request.POST["lpassword"]
    ob=Person.objects.raw('select * from query_person where  query_person.username=%s',[username])  
    pword=""
    for m in ob:
        pword=m.password
    ob1=Question.objects.raw('select * from query_question')
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id') 
    if(pword==password):
        # Check if authentication successful
            return  render(request, "query/profile.html", {
                "details":ob,
                "questions":ob1,
                "uname":user_name
            })
    else:
            return render(request, "query/login.html", {
                "message": "Invalid username and/or password."
            })

    return render(request, "query/home.html")
def image(request):
     if request.method == "POST":
        profile_img = request.POST["img"]
        username=request.POST["t"]
     ob1=Person.objects.raw('select * from query_person where  query_person.username=%s',[username]) 
     for m in ob1:
        m.photo=profile_img
        m.save()
     return render(request, "query/index.html", {
                "img": profile_img,
                "details":ob1

            })

def search(request):
    m=0
    if request.method == "POST" :
        uid = request.POST["userid"]
        search_data= request.POST["question"]
    ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[uid])  
    id=""
    for m in ob:
        id=m.id
    ob1=Person.objects.raw('select * from query_person where  query_person.id=%s',[id]) 
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    word_tokens = nltk.word_tokenize(search_data)
    stop_words = set(stopwords.words('english'))
    key_words = []
 
    for w in word_tokens:
        if w not in stop_words:
            key_words.append(w)
    
    l=len(key_words)
    if(l==0):
         return  render(request, "query/search.html", {
                "details":ob1,
                "uname":user_name            })
    try:
        for key in key_words:
             questions=Question.objects.filter(title__contains=key) 
    except:
        questions=[{'title':'No matching Found'}]
    
    if not questions:
         return  render(request, "query/search.html", {
                "details":ob1,
                "uname":user_name            })

    return  render(request, "query/profile.html", {
                "details":ob1,
                "questions":questions,
                "uname":user_name            })
def search_outer(request):
    m=0
    if request.method == "POST" :
        search_data= request.POST["question"]
    word_tokens = nltk.word_tokenize(search_data)
    stop_words = set(stopwords.words('english'))
    key_words = []
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    for w in word_tokens:
        if w not in stop_words:
            key_words.append(w)
    
    l=len(key_words)
    if(l==0):
         return  render(request, "query/search.html", {
                         })
    try:
        for key in key_words:
             questions=Question.objects.filter(title__contains=key) 
    except:
        questions=[{'title':'No matching Found'}]
    
    if not questions:
         return  render(request, "query/search.html", {
                    })

    return  render(request, "query/home.html", {
                "questions":questions,
                 "uname":user_name            })

def question_outer(request,qid):
    q_id=qid
    ob1=Question.objects.raw('select * from query_question where  query_question.id=%s',[q_id]) 
    answers=Answer.objects.raw('select * from query_answer a where  a.question_id=%s',[q_id])
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    user_name_answer=Person.objects.raw('select p.username,a.id from query_person p,query_answer a where  a.user_id==p.id')
    return render(request, "query/question_outer.html", {
                "questions":ob1,
                "answers":answers,
                "uname":user_name,
                "user_name_answer": user_name_answer
            }) 
def postedQuestions(request,name):
    id=name
    ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[id])  
    ob1=Question.objects.raw('select * from query_question where query_question.user_id=%s',[id])
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    return  render(request, "query/user_profile_page.html", {
                "details":ob,
                "questions":ob1,
                "uname":user_name

            })
#inorder to give edit option
def user_question(request,name,qid):
    id=name
    q_id=qid
    ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[id]) 
    ob1=Question.objects.raw('select * from query_question where  query_question.id=%s',[q_id]) 
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    answers=Answer.objects.raw('select * from query_answer a where  a.question_id=%s',[q_id])
    user_name_answer=Person.objects.raw('select p.username,a.id from query_person p,query_answer a where  a.user_id==p.id')
    return render(request, "query/user_question_inner.html", {
                "details":ob,
                "question":ob1,
                "uname":user_name,
                "answers":answers,
                "user_name_answer": user_name_answer
            }) 
def postedAnswers(request,name):
    id=name
    ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[id])  
    ob1=Answer.objects.raw('select qq.* from query_question qq,query_answer qa where qa.question_id == qq.id and qa.user_id=%s',[id])
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    return  render(request, "query/user_answer_profile.html", {
                "details":ob,
                "questions":ob1,
                "uname":user_name

            })
def user_answer(request,name,qid):
    id=name
    q_id=qid
    ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[id]) 
    ob1=Question.objects.raw('select * from query_question where  query_question.id=%s',[q_id]) 
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    answers=Answer.objects.raw('select * from query_answer a where  a.question_id=%s',[q_id])
    user_name_answer=Person.objects.raw('select p.username,a.id from query_person p,query_answer a where  a.user_id==p.id')
    return render(request, "query/user_answer_inner.html", {
                "details":ob,
                "question":ob1,
                "uname":user_name,
                "answers":answers,
                "user_name_answer": user_name_answer
            }) 
def password_change(request,name):
    id=name
    ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[id])  
    ob1=Answer.objects.raw('select qq.* from query_question qq,query_answer qa where qa.question_id == qq.id and qa.user_id=%s',[id])
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
    return  render(request, "query/password_change.html", {
                "details":ob,
                "questions":ob1,
                "uname":user_name

            })

def password_change_back(request):
    if request.method == "POST" :
        id = request.POST["username"]
        new_pass=request.POST["n_pass"]
        current_pass=request.POST["c_pass"]
        new_passa=request.POST["n_passa"]
    ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[id]) 
    message="" 
    s=False
    for b in ob:
        current_password=b.password
    if new_pass == new_passa:
        if current_password == current_pass:
            Person.objects.filter(id=id).update(password=new_pass)
            s=True 
        else:
            message="enter correct password"
    else:
        message="new password should equal to confirm password"
    if s==True:
        message="password changed successfully"
    
    ob1=Answer.objects.raw('select qq.* from query_question qq,query_answer qa where qa.question_id == qq.id and qa.user_id=%s',[id])
    user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')

    return  render(request, "query/password_change.html", {
                "details":ob,
                "questions":ob1,
                "uname":user_name,
                "message":message

            })

#delete question
def edit_question(request):
   if request.method == 'POST':
        id = request.POST["qid"]
        uid=request.POST["userid"]
       ## access you data by playing around with the request.POST object
   Question.objects.filter(id=id).delete()
   ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[uid])  
   ob1=Question.objects.raw('select * from query_question')
   user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
   return  render(request, "query/user_profile_page.html", {
                "details":ob,
                "questions":ob1,
                "uname":user_name

            })
def del_answer(request):
   if request.method == 'POST':
        id = request.POST["aid"]
        uid=request.POST["userid"]
       ## access you data by playing around with the request.POST object
   Answer.objects.filter(id=id).delete()
   ob=Person.objects.raw('select * from query_person where  query_person.id=%s',[uid])  
   ob1=Question.objects.raw('select * from query_question')
   user_name=Person.objects.raw('select a.username,q.id from query_person a,query_question q where  a.id==q.user_id')
   return  render(request, "query/user_answer_profile.html", {
                "details":ob,
                "questions":ob1,
                "uname":user_name

            })



      