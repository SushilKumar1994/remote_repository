from django.shortcuts import render,get_object_or_404
from blogapp.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.mail import send_mail
from blogapp.forms import EmailSendForm,CommentForm
from taggit.models import Tag
# Create your views here.

def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,3)

    page_number=request.GET.get('page')

    try:
         post_list=paginator.page(page_number)
    except PageNotAnInteger:
         post_list=paginator.page(1)
    except EmptyPage:
          post_list=paginator.page(paginator.num_pages)  #http://127.0.0.1:8000/?page=200 then if not available then display last page

    return render(request,"post_list.html",context={'post_list':post_list,'tag':tag})


#from django.views.generic import ListView
'''
class PostListView(ListView):
       model=Post
       template_name="post_list.html"
       context_object_name="post"
       paginate_by=2
'''

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published') #publish__year=year,publish__month=month,publish__day=day
    comments=post.comments.filter(active=True)  #one post related comments will be filtered
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post                        #current post is being assigned
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()

    return render(request,"post_detail.html",context={'post':post,'form':form,'csubmit':csubmit,'comments':comments})
def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status="published")
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
              cd=form.cleaned_data
              subject=f"{cd['name']}({cd['email']}) recommands you to read '{post.title}'"
              post_url=request.build_absolute_uri(post.get_absolute_url())
              message=f"Read Post At:\n {post_url}\n\n{cd['name']} \'s Comments:\n{cd['comments']}"

              send_mail(subject,message,'sushil@blog.com',[cd['to']])
              sent=True
    else:
       form=EmailSendForm()
    return render(request,"sharebymail.html",{'form':form,'post':post,'sent':sent})
