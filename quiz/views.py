from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .models import *
from .forms import SubmitRiddleForm
from django.contrib.auth.models import User

from django.utils import timezone

def landing(request):
	return render(request, 'home.html')


def home(request):
	current_user = request.user

	# user not logged in
	if current_user.is_anonymous:
		return redirect('/accounts/login')

	try:
		user_data = UserData.objects.get(user = current_user)
	except Exception as e:
		print(e)
		user_data = UserData.objects.create(user = current_user)
		user_data.save()

	context = {
		"score": user_data.score,
		"hints_taken": user_data.hints_taken
	}

	return render(request, 'index.html', context = context)


def solve(request):
	current_user = request.user

	# user not logged in
	if current_user.is_anonymous:
		return redirect('/accounts/login')

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
					time_taken_mins = time_taken.total_seconds()//60

					# score algo
					max_points = riddle.correct_points
					curr_score = max(max_points//2, max_points - time_taken_mins*10)

					user_data = UserData.objects.get(user = current_user)
					user_data.score += curr_score
					user_data.ques_solved += 1
					user_data.save()

					return render(request, 'correct.html')
				else:
					return render(request, 'incorrect.html')

			except Exception as e:
				print(e)
				return HttpResponse("Riddle not found")

			# redirect to a new URL:
			return redirect('/solve')

		else:
			return HttpResponse("Incorrect form data")

	# if a GET (or any other method) we'll create a blank form
	else:
		# find the last solved question
		try:
			user_data = UserData.objects.get(user = current_user)
			last_ques = user_data.ques_solved
			# history = History.objects.filter(user = current_user, end_time__isnull = False)
			# last_ques = history.last().ques.ques_no
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
			hist = History.objects.get(user = current_user, ques = curr_riddle)

		context = {
			'ques_no': curr_riddle.ques_no,
			'team_name': user_data.user,
			'score': user_data.score,
			'hints_taken': user_data.hints_taken,
			'start_time': hist.start_time.timestamp()*1000
		}

		return render(request, 'riddles/riddle' + str(curr_ques) + '.html', context)


def rules(request):
	return render(request, 'rules.html')


def leaderboard(request):
	current_user = request.user

	# user not logged in
	if current_user.is_anonymous:
		return redirect('/accounts/login')

	try:
		all_users = UserData.objects.all()
		data = []
		curr_user_data = {}
		rank = 1

		for user in all_users:
			data.append({
				"rank": rank,
				"user": user.user.username,
				"ques_solved": user.ques_solved,
				"score": user.score,
				"hints_taken": user.hints_taken,
			})

			if(user.user == current_user):
				curr_user_data = {
					"rank": rank,
					"user": user.user.username,
					"ques_solved": user.ques_solved,
					"score": user.score,
					"hints_taken": user.hints_taken,
				}

			rank += 1

	except Exception as e:
		print(e)
		return HttpResponse("User not found")

	context = {
		"all_users": data,
		"curr_user": curr_user_data
	}

	return render(request, 'leaderboard.html', context = context)