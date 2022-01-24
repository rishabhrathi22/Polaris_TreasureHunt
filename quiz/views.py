from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .models import *
from .forms import SubmitRiddleForm
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import datetime
import pytz


def landing(request):
    current_user = request.user
    print(current_user)
    if current_user.is_anonymous:
        return redirect('/accounts/login')
    return render(request, 'home.html')


def home(request):
    current_user = request.user

    IST = pytz.timezone('Asia/Kolkata')

    targetDate = "2022-01-27 15:59:00"

    eventTime = datetime.fromisoformat(targetDate)
    eventTime = IST.localize(eventTime)
    curr = datetime.now(IST)

    if(curr < eventTime):
        return redirect("https://gdsc-treasure-hunt.netlify.app")

    # user not logged in
    if current_user.is_anonymous:
        return redirect('/accounts/login')

    try:
        user_data = UserData.objects.get(user=current_user)
    except Exception as e:
        print(e)
        user_data = UserData.objects.create(user=current_user)
        user_data.save()

    return render(request, 'index.html')


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
                riddle = Riddle.objects.get(ques_no=data['ques_no'])
                user_ans = data['answer'].strip().lower()
                correct_ans = riddle.answer.strip().lower()

                user_data = UserData.objects.get(user=current_user)

                if(user_data.ques_solved + 1 != data['ques_no']):
                    return redirect('/solve')

                if (user_ans == correct_ans):
                    # update the end time for ques
                    hist = History.objects.get(user=current_user, ques=riddle)
                    hist.end_time = timezone.now()
                    hist.save()

                    # calculate score according to time taken
                    time_taken = hist.end_time - hist.start_time
                    time_taken_mins = time_taken.total_seconds()//60

                    # score algo
                    max_points = riddle.correct_points
                    curr_score = max(
                        max_points//2, max_points - time_taken_mins*10)

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
            # return redirect('/solve')

        else:
            print("Incorrect form data")
            return render(request, 'incorrect.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        # find the last solved question
        try:
            user_data = UserData.objects.get(user=current_user)
            last_ques = user_data.ques_solved
            # history = History.objects.filter(user = current_user, end_time__isnull = False)
            # last_ques = history.last().ques.ques_no
        except Exception as e:
            print(e)
            last_ques = 0

        # get the next ques
        curr_ques = last_ques + 1
        try:
            curr_riddle = Riddle.objects.get(ques_no=curr_ques)
        except Exception as e:
            print(e)
            print("All riddles solved")
            return redirect('/leaderboard')

        # start timer for current riddle
        try:
            hist = History.objects.create(user=current_user, ques=curr_riddle)
            hist.save()
        except Exception as e:
            print(e)
            hist = History.objects.get(user=current_user, ques=curr_riddle)

        # check is user has already taken hint
        hintTaken = False
        try:
            hint_data = HintData.objects.get(
                user=current_user, ques=curr_riddle)
            if(hint_data):
                hintTaken = True
        except Exception as e:
            print(e)

        context = {
            'ques_no': curr_riddle.ques_no,
            'hint_points': curr_riddle.hint_points,
            'team_name': user_data.user,
            'score': user_data.score,
            'hints_taken': user_data.hints_taken,
            'start_time': hist.start_time.timestamp()*1000,
            'isHintTaken': hintTaken
        }

        return render(request, 'riddles/riddle' + str(curr_ques) + '.html', context)


def leaderboard(request):
    current_user = request.user

    # user not logged in
    if current_user.is_anonymous:
        return redirect('/accounts/login')

    try:
        # all_users = UserData.objects.all()
        all_users = UserData.objects.order_by(
            '-ques_solved', '-score', 'hints_taken')

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

    return render(request, 'leaderboard.html', context=context)


def get_hint(request):
    current_user = request.user

    # user not logged in
    if current_user.is_anonymous:
        return redirect('/accounts/login')

    # check if ques number provided
    if request.GET.get("ques", None) == None:
        return JsonResponse({"error": "Give question number"}, safe=False)

    # check if invalid question number
    ques_no = int(request.GET["ques"])
    if ques_no < 1 or ques_no > 8:
        return JsonResponse({"error": "Invalid question number"}, safe=False)

    try:
        riddle = Riddle.objects.get(ques_no=ques_no)
        hint = riddle.hint

        # check whether this ques hint already taken by user
        try:
            hint_data = HintData.objects.get(user=current_user, ques=riddle)
            return JsonResponse({"hint": hint}, safe=False)
        except Exception as e:
            print(e)

        user = UserData.objects.get(user=current_user)

        # check whether user has enough points
        if (user.score < riddle.hint_points):
            return JsonResponse({"error": "You don't have enough points"}, safe=False)

        user.score -= riddle.hint_points
        user.hints_taken += 1
        user.save()

        hint_data = HintData.objects.create(user=current_user, ques=riddle)
        hint_data.save()

        return JsonResponse({"hint": hint, "points": user.score}, safe=False)
    except Exception as e:
        print(e)

    return JsonResponse({"error": "Check Logs"}, safe=False)
