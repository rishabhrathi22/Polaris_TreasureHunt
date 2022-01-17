from django.contrib import admin
from .models import History, UserData, Riddle

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ques', 'start_time', 'end_time')

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'ques_solved', 'score', 'hints_taken')
    ordering = ('-ques_solved', '-score', 'hints_taken')

class RiddleAdmin(admin.ModelAdmin):
    list_display = ('ques_no', 'answer', 'correct_points', 'hint_points')

admin.site.register(History, HistoryAdmin)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(Riddle, RiddleAdmin)