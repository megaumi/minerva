from django.db import models
from django import forms
from minerva.main.models import MagazineIssue, Article, EnglishParagraph, TranslatedParagraph

class ArticleForm(forms.Form):
    magazine_issue = forms.ModelChoiceField(queryset=MagazineIssue.objects.all())
    original_title = forms.CharField(max_length=255)
    authors = forms.CharField(max_length=255, required=False)
    url = forms.URLField(max_length=255, required=False)
    text = forms.CharField(widget=forms.Textarea)
