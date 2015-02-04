#coding=utf-8
#!/usr/bin/python

from django import forms


class CreateUserForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField()
    passowrd2 = forms.CharField()
