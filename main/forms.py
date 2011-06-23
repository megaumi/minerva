from django.db import models
from django import forms
from minerva.main.models import MagazineIssue, Article, EnglishParagraph, TranslatedParagraph

class ArticleForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    
    def save(self, *args, **kwargs):
        article = super(ArticleForm, self).save(*args, **kwargs)
        text = self.cleaned_data['text']
        paragraphs = text.split('\n')
        i = 0
        for p in paragraphs:
            if p.strip():
                ep = EnglishParagraph(article=article, text=p, position_in_article=i)
                ep.save()
                i += 1
        return article        

    class Meta:
        model = Article

class TranslatedParagraphForm(forms.ModelForm):
    class Meta:
        model = TranslatedParagraph
        fields = ('text',)
