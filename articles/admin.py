from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, ScopeArticle, Tag


class ScopeArticleInlineFormset(BaseInlineFormSet):
    def clean(self):
        _list = []
        for form in self.forms:
            if form.cleaned_data:
                _list.append(form.cleaned_data['is_main'])

        count_top = _list.count(True)
        if count_top > 1:
            raise ValidationError('Выберите один основной раздел')
        elif count_top < 1:
            raise ValidationError('Основной раздел не указан!')
        return super().clean()


class ScopeArticleInline(admin.TabularInline):
    model = ScopeArticle
    formset = ScopeArticleInlineFormset
    extra = 5


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'published_at']
    list_display_links = ['id', 'title']
    inlines = [ScopeArticleInline,]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']