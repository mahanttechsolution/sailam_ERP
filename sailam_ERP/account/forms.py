from django import forms

class loginForm(forms.Form):
    username=forms.CharField(help_text="Enter UserName",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'UserName'}),label="Enetr User Name",error_messages={'error':"Username Can not be empty"},max_length=50)
    password=forms.CharField(help_text="Enter Password",required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),label="Password",error_messages={'error':"Password Can not be empty"},max_length=12)



