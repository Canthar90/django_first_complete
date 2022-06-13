from django.contrib import admin

from .models import Question, Choice

class Site(admin.AdminSite):
    site_header = "Polls template side"
    site_title = "Polls administration side"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldset = [
        (None,                          {'fields': ['question_text']}),
        ('Date information',            {'fields': ['pub_date'],
        'classes': 'collapse'}),
        ]
    inlines = [ChoiceInline] 
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']



admin_site = Site(name='admin')
admin.site.register(Question, QuestionAdmin)

