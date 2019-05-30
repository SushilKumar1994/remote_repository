from django.contrib import admin
from blogapp.models import Post,Comment
# Register your models here.
#admin.site.register(Post)

class PostAdmin(admin.ModelAdmin):
      list_display=['title','slug','author','body','publish','created','updated','status']
      list_filter=('status','author','publish','created')
      search_fields=('title','body')
      raw_id_fields=('author',)
      prepopulated_fields={'slug':('title',),}
      date_hierarchy="publish"
      ordering=['status','publish']

admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
      list_display=('name','email','post','body','created','updated')
      list_filter=('active','created','updated')
      search_fields=('name','email','body')
admin.site.register(Comment,CommentAdmin)
