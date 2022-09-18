from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    username = models.CharField(_('username'), max_length=15, unique=True, null=False, blank=False)
    first_name = models.CharField(_('first_name'), max_length=50, null=False, blank=False)
    last_name = models.CharField(_('last_name'), max_length=50, null=False, blank=False)
    email = models.EmailField(_('email'), unique=True, null=False, blank=False)
    phone = models.CharField(_('phone'), max_length=30, unique=False, null=True, blank=True)
    author = models.BooleanField(_('author'), blank=True, null=False, default=False)
    avatar = models.ImageField(_('avatar'), null=True, default='avatar.svg', blank=True, upload_to='users_images')
    bio = models.TextField(_('bio'), null=False, blank=True, default='Still No Bio Sadge')
    job = models.CharField(_('job'), max_length=30, null=False, blank=True, default='My Job')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    @property
    def fullname(self):
        return self.first_name + ' ' + self.last_name


class Category(models.Model):
    name = models.CharField(_('name'), max_length=50, null=True, blank=True, unique=True)
    # avatar = models.ImageField(null=True, default='bg-banner.jpg', blank=True, upload_to='categories_images')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def category_trend(self):
        posts = Post.objects.filter(Q(categories__name=self.name))
        return posts.count()
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name_plural = ("Categories")

class Post(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(_('title'), max_length=50, null=False, blank=False, unique=True)
    categories = models.ManyToManyField(
        Category, related_name=_('Categories'), blank=False
    )
    image = models.ImageField(_('image'), null=False, blank=False, upload_to='posts_images')
    min_to_read = models.IntegerField(_('min_to_read'), null=False, blank=True, default=10)
    body = RichTextUploadingField(_('body'), blank=True)
    tags = TaggableManager(_('tags'), )
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def post_trend(self):
        comments = Comment.objects.filter(Q(post__id=self.id))
        return comments.count()

    @property
    def tags_to_str(self):
        tags =  self.tags.all()
        tags_to_str = ''
        for tag in tags:
            tags_to_str += str(tag) + ', '
        return tags_to_str
    

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-updated', '-created']
    


class Comment(models.Model):
    post = models.ForeignKey( Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_field = models.CharField(_('comment_field'), max_length=200, blank=False, null=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.post) + '_' + str(self.user) + '_comment'

    class Meta:
        ordering = ['-updated', '-created']


class Contact(models.Model):
    your_name = models.CharField(_('your_name'), max_length=50, blank=False, null=False)
    your_email = models.EmailField(_('your_email'), blank=False, null=False)
    reason_for_contact = models.CharField(_('reason_for_contact'), max_length=50, blank=False, null=False)
    your_message = models.TextField(_('your_message'), null=False, blank=False)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return str(self.your_name)  + '_' + str(self.your_email)

    class Meta:
        ordering = ['-updated', '-created']