from django import forms

class SubmitRiddleForm(forms.Form):
	ques_no = forms.IntegerField()
	answer = forms.CharField(max_length=250)