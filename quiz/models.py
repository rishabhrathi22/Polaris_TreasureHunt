from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default = 0)
    hints_taken = models.IntegerField(default = 0)
    ques_solved = models.IntegerField(default = 0)

class Riddle(models.Model):
    ques_no = models.IntegerField()
    # riddle = models.CharField(max_length = 10000)
    answer = models.CharField(max_length = 1000)
    correct_points = models.IntegerField()
    hint_points = models.IntegerField()

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ques = models.ForeignKey(Riddle, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add = True)
    end_time = models.DateTimeField(null = True)

    class Meta:
        unique_together = (('user', 'ques'),)