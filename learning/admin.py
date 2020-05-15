from django.contrib import admin
from .models import *

admin.site.register(Domain)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(PublicComment)