from django.contrib import admin
from reversion.admin import VersionAdmin
from minerva.main.models import MagazineIssue, Article, EnglishParagraph, TranslatedParagraph

class TranslatedParagraphAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(MagazineIssue)
admin.site.register(Article)
admin.site.register(EnglishParagraph)
admin.site.register(TranslatedParagraph, TranslatedParagraphAdmin)
