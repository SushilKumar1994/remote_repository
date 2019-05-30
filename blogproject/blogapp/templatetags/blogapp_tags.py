
from blogapp.models import Post
from django.db.models import Count

from django import template
register=template.Library()

@register.simple_tag(name='my_tag')
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('latest_posts1234.html')
def show_latest_posts(count):
    latest_posts=Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

'''
@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
'''
