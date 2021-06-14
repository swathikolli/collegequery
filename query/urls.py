from django.urls import path

from . import views
from django.conf.urls.static import  static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("forgot",views.forgot,name="forgot"),
     path("forgot_passwd",views.forgot_passwd,name="forgot_passwd"),
    path("search",views.search,name="search"),
    path("search_outer",views.search_outer,name="search_outer"),
    path("flog",views.flog,name="flog"),
    path("freg",views.freg,name="freg"),
    path("fhome",views.fhome,name="fhome"),
    path("question/<int:name>/<int:qid>",views.question,name="question"),
    path("user_question/<int:name>/<int:qid>",views.user_question,name="user_question"),
    path("user_answer/<int:name>/<int:qid>",views.user_answer,name="user_answer"),
    path("question_outer/<int:qid>",views.question_outer,name="question_outer"),
    path("ask/<int:name>",views.ask,name="ask"),
    path("home/<int:name>",views.home,name="home"),
    path("profile",views.profile,name="profile"),
    path("login",views.login,name="login"),
    path("image",views.image,name="image"),
    path("question_details",views.question_details,name="question_details"),
    path("answer_details",views.answer_details,name="answer_details"),
    path("postedQuestions/<int:name>",views.postedQuestions,name="postedQuestions"),
    path("postedAnswers/<int:name>",views.postedAnswers,name="postedAnswers"),
    path("password_change/<int:name>",views.password_change,name="password_change"),
    path("password_change_back",views.password_change_back,name="password_change_back"),
    path("edit_question",views.edit_question,name="edit_question"),
    path("del_answer",views.del_answer,name="del_answer"),
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)