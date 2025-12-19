from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Hagtag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Saved_Post)
admin.site.register(Seen_Post)