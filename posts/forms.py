from django import forms


from base.models import Post, Comment

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'categories', 'tags', 'min_to_read', 'image', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control text-center"}),
            'categories': forms.SelectMultiple(attrs={'class': "form-control text-center "}),
            # 'tags': forms.TextInput(attrs={'class': "form-control text-center "}),
            'min_to_read': forms.NumberInput(attrs={'class': "form-control text-center "}),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_field']
        widgets = {
            'comment_field': forms.Textarea(attrs={'class': 'form-control shadow-none', 'rows': '7'})
        }