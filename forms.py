from django.db import models
from django import forms
from minerva.main.models import MagazineIssue, Article, EnglishParagraph, TranslatedParagraph

class ArticleForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
           
    class Meta:
        model = Article
