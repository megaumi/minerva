# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class MagazineIssue(models.Model):
    u'''Выпуск журнала'''
    number = models.PositiveIntegerField(unique=True)
    original_published_date = models.DateField(null=True, blank=True)
    original_pdf = models.FileField(upload_to='pdf', blank=True)
    translators = models.ManyToManyField(User, related_name='translator_in', blank=True)
    proofreaders = models.ManyToManyField(User, related_name='proofreader_in', blank=True)
    designers = models.ManyToManyField(User, related_name='designer_in', blank=True)
    contributors = models.ManyToManyField(User, related_name='contributor_in', blank=True)
    translation_published = models.BooleanField()
    
    def __unicode__(self):
        return u'Выпуск #%d' % self.number

    
class Article(models.Model):
    u'''Статья для перевода'''
    magazine_issue = models.ForeignKey(MagazineIssue)
    original_title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=255, blank=True)
    
    def __unicode__(self):
        return u'%s: %s' % (self.magazine_issue, self.original_title)


class EnglishParagraph(models.Model):
    u'''Абзац английского текста'''
    article = models.ForeignKey(Article)
    text = models.TextField(blank=True)
    translation = models.OneToOneField('TranslatedParagraph', null=True, blank=True)
    number = models.PositiveSmallIntegerField()
    
    @property
    def words(self):
        return len(self.text.split())

    @property
    def chars(self):
        return len(''.join(self.text.split()))
    
    @property
    def chars_with_spaces(self):
        return len(self.text)
    
    def __unicode__(self):
        return self.text.lstrip()[:50]

        
class TranslatedParagraph(models.Model):
    u'''Перевод абзаца'''
    text = models.TextField()
    author = models.ForeignKey(User)
    last_changed = models.DateTimeField(auto_now=True)
       
    @property
    def words(self):
        return len(self.text.split())

    @property
    def chars(self):
        return len(''.join(self.text.split()))
    
    @property
    def chars_with_spaces(self):
        return len(self.text)
    
    def __unicode__(self):
        return self.text.lstrip()[:50]
