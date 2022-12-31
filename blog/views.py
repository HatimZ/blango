from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils import timezone
from blog.models import Post
from django.shortcuts import render, get_object_or_404, redirect
from blog.forms import CommentForm

# Create your views here.
user_model = get_user_model()



def index(request):
    posts = Post.objects.filter(published_at__lte = timezone.now())

    return render(request , "blog/index.html" , {'posts' : posts} )


def author_details(author):
    if not isinstance(author, user_model):
      
        return ""

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    return name


def post_details(request, slug):
    post = get_object_or_404(Post , slug = slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(request , "blog/post-detail.html", {"post": post , "comment_form": comment_form } )


