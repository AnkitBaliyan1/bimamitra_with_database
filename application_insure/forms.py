# forms.py
from django import forms
from .models import ContactUs

'''
class InputForm(forms.Form):
    user_input = forms.CharField(
        label='Prompt your query here..', 
        max_length=1200, 
        widget=forms.Textarea(attrs={'class': 'large-input', 'row':15,'style': 'width: 90%; height: 50px;'})
    )
'''

class InputForm(forms.Form):
    user_input = forms.CharField(
        label='Prompt your query here..', 
        max_length=1200, 
        widget=forms.Textarea(attrs={'class': 'large-input autosize-textarea'})
    )


# this is form for contact us section which takes model 

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']


