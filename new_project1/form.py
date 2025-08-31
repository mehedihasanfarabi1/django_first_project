from django import forms

class usersForm(forms.Form):
    name = forms.CharField(label='Name 33',required=False,widget= forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Mail 24',required=True,widget= forms.TextInput(attrs={'class':'form-control'}))
    phone = forms.CharField(label='Phone')