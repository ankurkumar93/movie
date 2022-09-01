from django.contrib import admin

from .models import *

admin.site.register(Movie)

class UserAdmin(admin.ModelAdmin):
    fields = ('username',)

admin.site.register(User, UserAdmin)

class MovieCollectionAdmin(admin.ModelAdmin):
    fields = ('title', 'movies', 'description', 'user')

admin.site.register(MovieCollection, MovieCollectionAdmin)


