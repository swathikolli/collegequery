from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Person,Question,Answer
# Register your models here.
admin.site.register(Person)
admin.site.register(Question)
admin.site.register(Answer)


# Register your models here.
