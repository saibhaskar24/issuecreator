from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Comment, IField, Issue
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2',
                  )

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class IssueForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    location = forms.CharField(max_length=128)
    description = forms.Textarea()

    class Meta:
        model = Issue
        fields = ('title', 'description', 'location')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = IField
        fields = ('image', )