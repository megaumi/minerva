from django.contrib import admin
from reversion.admin import VersionAdmin
from minerva.main.models import MagazineIssue, Article, EnglishParagraph, TranslatedParagraph

admin.site.register(MagazineIssue)
