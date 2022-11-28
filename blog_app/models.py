from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



# CATEGORY TABLE
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


# BLOG TABLE
class BlogPost(models.Model):
    
    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')
    
    
    options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    excerpt = models.TextField(null=True)
    slug = models.SlugField(max_length=200, unique_for_date='publish_date')
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    blog_content = models.TextField()
    status = models.CharField(max_length=10, choices=options, default='draft')
    objects = models.Manager() # default manager
    newmanager = NewManager() # custom manager
    
    
    def get_single_post(self):
        return reverse('blog:single_post', args=[self.slug])
    
    class Meta:
        ordering = ('publish_date',)
    
    def __str__(self):
        return self.title
    
    
# COMMENT TABLE
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    
    class META:
        ordering = ('publish',)
        

    def __str__(self):
        return f'Commented by {self.name}'
