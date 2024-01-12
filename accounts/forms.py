from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label="confirm Password", 
                                 widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is taken")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password_2 = cleaned_data['password_2']
        if password is not None and password != password_2:
            self.add_error("password_2", "Your password must match")
        return cleaned_data
    

class UserAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        password_2 = cleaned_data["password_2"]
        if password is not None and password != password_2:
            self.add_error("password_2", "Your password must match")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


