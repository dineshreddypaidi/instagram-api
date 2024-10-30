from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.CustomUser)
admin.site.register(models.Follows)
admin.site.register(models.Post)
admin.site.register(models.Postlikes)
admin.site.register(models.Postcomment)
admin.site.register(models.stories)