from django.contrib import admin
from .models import Post, Comment

# Personalización de Post
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'fecha_publicacion', 'imagen', 'video']
    search_fields = ['title', 'content']

# Personalización de Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    search_fields = ['author', 'content']

# Registramos los modelos con sus respectivas personalizaciones
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
