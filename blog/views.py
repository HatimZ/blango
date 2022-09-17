from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils import timezone
from blog.models import Post

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