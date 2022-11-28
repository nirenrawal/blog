from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .forms import NewCommentForm
from .models import BlogPost, Category
from django.views.generic import ListView


def home(request):
    all_post = BlogPost.newmanager.all()
    return render(request, 'blog_app/index.html', {'posts': all_post})



def single_post(request, post):
    post = get_object_or_404(BlogPost, slug=post, status='published')
    comments = post.comments.filter(status=True)
    user_comment = None
    
    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post.slug)
    else:
        comment_form = NewCommentForm()
    return render(
        request, 
        'blog_app/single_post.html', 
        {
            'post': post, 
            'comments': user_comment, 
            'comments': comments, 
            'comment_form': comment_form, 
        }
    )


class CatListView(ListView):
    template_name = 'blog_app/category.html'
    context_object_name = 'catlist'
    
    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': BlogPost.objects.filter(category__name=self.kwargs['category']).filter(status='published')
        }
        return content
    
    
def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        'category_list': category_list
    }
    return context




