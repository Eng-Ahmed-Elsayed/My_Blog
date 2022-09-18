from django import forms

from .models import User, Contact


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password','avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file mb-3'}),
        }
        
class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control mb-3'})
        }
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['your_name', 'your_email', 'reason_for_contact', 'your_message']
        widgets = {
            'your_name': forms.TextInput(attrs={'class': 'form-control '}),
            'your_email': forms.EmailInput(attrs={'class': 'form-control '}),
            'reason_for_contact': forms.TextInput(attrs={'class': 'form-control '}),
            'your_message': forms.Textarea(attrs={'class': 'form-control '}),

        }