from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Follower)
admin.site.register(Post)
admin.site.register(User)