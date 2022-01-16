from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import SubmitRiddleForm
from django.contrib.auth.models import User

from django.utils import timezone

def landing(request):
	return render(request, 'home.html')


def index(request):
	current_user = request.user

	# user not logged in
	if current_user.is_anonymous:
		print("Hello")
		return redirect('/accounts/login')

	try:
		user_data = UserData.objects.get(user = current_user)
		context = {
			"score": user_data.score,
			"hints_taken": user_data.hints_taken
		}
	except:
		context = {}

	return render(request, 'index.html', context = context)


def riddle(request):
	current_user = request.user

	# user not logged in
	if current_user.is_anonymous:
		return render(request, 'index.html')

	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = SubmitRiddleForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			data = form.cleaned_data

			# check answer
			try:
				riddle = Riddle.objects.get(ques_no = data['ques_no'])
				user_ans = data['answer']
				correct_ans = riddle.answer

				if (user_ans == correct_ans):
					# update the end time for ques
					hist = History.objects.get(user = current_user, ques = riddle)
					hist.end_time = timezone.now()
					hist.save()

					# calculate score according to time taken
					time_taken = hist.end_time - hist.start_time
					print(time_taken.total_seconds())

					# score algo
					score = 5

					user_data = UserData.objects.get(user = current_user)
					user_data.score += score
					user_data.save()

					return render(request, 'correct.html')
				else:
					return render(request, 'incorrect.html')

			except Exception as e:
				print(e)
				return HttpResponse("Riddle not found")

			# redirect to a new URL:
			return redirect('/riddle')

	# if a GET (or any other method) we'll create a blank form
	else:
		# find the last solved question
		try:
			history = History.objects.filter(user = current_user, end_time__isnull = False)
			last_ques = history.last().ques.ques_no
		except Exception as e:
			print(e)
			last_ques = 0

		# get the next ques
		curr_ques = last_ques + 1
		try:
			curr_riddle = Riddle.objects.get(ques_no = curr_ques)
		except Exception as e:
			print(e)
			return HttpResponse("All riddles solved")

		# start timer for current riddle
		try:
			hist = History.objects.create(user = current_user, ques = curr_riddle)
			hist.save()
		except Exception as e:
			print(e)

		form = SubmitRiddleForm()

	context = {
		'form': form,
		'ques_no': curr_riddle.ques_no,
		'riddle': curr_riddle.riddle
	}

	return render(request, 'riddle.html', context)