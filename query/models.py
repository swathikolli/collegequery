from django.db import models

# Create your models here.

class Person(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    mailid=models.EmailField(max_length = 254)
    profile_pic=models.ImageField(upload_to='persons_images', null=True, blank=True)
class Question(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=500)
    date=models.CharField(max_length=50)
    time=models.CharField(max_length=50)
    user=models.ForeignKey("query.Person", on_delete=models.CASCADE,related_name="user",blank=True,null=True)
class Answer(models.Model):
    ans=models.CharField(max_length=500)
    date=models.CharField(max_length=50)
    time=models.CharField(max_length=50)
    user=models.ForeignKey("query.Person", on_delete=models.CASCADE,related_name="answer_user",blank=True,null=True)
    question=models.ForeignKey("query.Question", on_delete=models.CASCADE,related_name="answer_question",blank=True,null=True)
