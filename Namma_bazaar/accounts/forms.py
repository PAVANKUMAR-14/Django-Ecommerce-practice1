from django import forms
from accounts.models import Accounts

class RegistrationForm (forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter the password','class':'form-control'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter the confirm password'}))
    class Meta :
        model=Accounts
        fields=['first_name','last_name','email','password','phone_number']

    def __init__(self, *args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean (self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password= cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError ('Check password again')