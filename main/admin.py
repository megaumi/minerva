from django.contrib import admin
from minerva.main.models import MagazineIssue, Article, EnglishParagraph, TranslationHistory

admin.site.register(MagazineIssue)
admin.site.register(Article)
admin.site.register(EnglishParagraph)
admin.site.register(TranslationHistory)
