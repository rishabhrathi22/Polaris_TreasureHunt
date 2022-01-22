from django.contrib import admin
from .models import History, UserData, Riddle, HintData

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ques', 'start_time', 'end_time')

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'ques_solved', 'score', 'hints_taken')
    ordering = ('-ques_solved', '-score', 'hints_taken')

class HintDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'ques')

class RiddleAdmin(admin.ModelAdmin):
    list_display = ('ques_no', 'answer', 'hint', 'correct_points', 'hint_points')

admin.site.register(History, HistoryAdmin)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(HintData, HintDataAdmin)
admin.site.register(Riddle, RiddleAdmin)