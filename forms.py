# accounts/forms.py
from django import forms
from .models import User

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'role', 'password']

    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()
        return user
