from django.contrib import admin
from .models import ExpertAdvisor, Review

#design admin panel
class ExpertAdvisorAdmin(admin.ModelAdmin):
    list_display = ('ea_name', 'category', 'approved')
    list_filter = ('category', 'approved')
    search_fields = ('ea_name', 'personal_review')

class ReviewAdmin(admin.ModelAdmin):
    #display Expert advisor name
    def advisor_name(self, obj):
        return obj.advisor.ea_name
    #display user name
    def user_name(self, obj):
        return obj.user.username
    list_display = ('advisor_name', 'user_name', 'comment', 'approved', 'posted_date')

admin.site.register(ExpertAdvisor, ExpertAdvisorAdmin)
admin.site.register(Review, ReviewAdmin)

