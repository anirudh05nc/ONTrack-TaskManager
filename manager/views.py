from django.shortcuts import render
from .models import *
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import date, timedelta
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from decouple import config
import requests

# Create your views here.

def todo_to_ongo(request, id):
    toDo_obj = get_object_or_404(toDoTasks, id=id)
    now = timezone.now()

    status = "DELAY" if now > toDo_obj.startDate else "INTIME"

    ongo = onGoingTasks.objects.create(
        user = toDo_obj.user,
        title = toDo_obj.title,
        description=toDo_obj.description,
        startDate=toDo_obj.startDate,
        startedDate=now,
        endDate=toDo_obj.endDate,
        priority=toDo_obj.priority,
        statusOfBeginning=status
    )

    toDo_obj.delete()

    return redirect('home')

def ongo_to_comp(request, id):
    onGoing_obj = get_object_or_404(onGoingTasks, id = id)
    now = timezone.now()
    
    status = 'DELAY' if now > onGoing_obj.endDate else 'INTIME'

    comp = Completed.objects.create(
        user = onGoing_obj.user,
        title = onGoing_obj.title,
        description = onGoing_obj.description,
        scheduledDate = onGoing_obj.startDate,
        startedDate = onGoing_obj.startedDate,
        statusOfBeginning = onGoing_obj.statusOfBeginning,
        deadLine = onGoing_obj.endDate,
        completedDate = now,
        priority = onGoing_obj.priority,
        statusOfCompletion = status
    )
#     if status == "INTIME":
#         send_telegram_message(f'''🎉 MISSION ACCOMPLISHED! 🎉  
# ✅ Task Completed: {onGoing_obj.title}  
# 🕒 Finished Right in Time — You’re a beast!  
# 🔥 You're not just OnTrack, you're ahead of the game by {onGoing_obj.endDate - now}.  

# 🎖 Keep dominating, legend!
# ''')
#     else:
#         send_telegram_message(f'''⏰ TASK COMPLETED... but late! 😓  
# ⚠ Task: { onGoing_obj.title }
# 🧾 Deadline was: { onGoing_obj.endDate }  
# ⛔ You made it — but the train left the station a bit early.

# 🛠 Learn. Adapt. Destroy the next one. ''')

    onGoing_obj.delete()

    return redirect('home')


def todo_to_comp(request, id):
    toDo_obj = get_object_or_404(toDoTasks, id=id)
    now = timezone.now()

    statusOfBeginning = "DELAY" if now > toDo_obj.startDate else "INTIME"
    statusOfCompletion = 'DELAY' if now > toDo_obj.endDate else 'INTIME'

    comp = Completed.objects.create(
        user = toDo_obj.user,
        title = toDo_obj.title,
        description = toDo_obj.description,
        scheduledDate = toDo_obj.startDate,
        startedDate = now,
        statusOfBeginning = statusOfBeginning,
        deadLine = toDo_obj.endDate,
        completedDate = now,
        priority = toDo_obj.priority,
        statusOfCompletion = statusOfCompletion
    )
#     if statusOfCompletion == "INTIME":
#         send_telegram_message(f'''🎉 MISSION ACCOMPLISHED! 🎉  
# ✅ Task Completed: {toDo_obj.title}  
# 🕒 Finished Right in Time — You’re a beast!  
# 🔥 You're not just OnTrack, you're ahead of the game by {toDo_obj.endDate - now}.  

# 🎖 Keep dominating, legend!
# ''')
#     else:
#         send_telegram_message(f'''⏰ TASK COMPLETED... but late! 😓  
# ⚠ Task: { toDo_obj.title }
# 🧾 Deadline was: { toDo_obj.endDate }  
# ⛔ You made it — but the train left the station a bit early.

# 🛠 Learn. Adapt. Destroy the next one. ''')

    toDo_obj.delete()
    
    return redirect('home')

def deleteTask_todo(request, id):
    if request.method == 'POST':
        obj = get_object_or_404(toDoTasks, id=id)
        obj.delete()
        return redirect('home')

def deleteTask_ongo(request, id):
    if request.method == 'POST':
        obj = get_object_or_404(onGoingTasks, id=id)
        obj.delete()
        return redirect('home')

def deleteTask_comp(request, id):
    if request.method == 'POST':
        obj = get_object_or_404(Completed, id=id)
        obj.delete()
        return redirect('home')

def ongo_todo(request, id):
    onGoing_Obj = get_object_or_404(onGoingTasks, id=id)

    todo = toDoTasks.objects.create(
        user = onGoing_Obj.user,
        title = onGoing_Obj.title,
        description = onGoing_Obj.description,
        startDate = onGoing_Obj.startDate,
        endDate = onGoing_Obj.endDate,
        priority = onGoing_Obj.priority
    )

    onGoing_Obj.delete()
    return redirect('home')


def comp_ongo(request, id):
    comp_Obj = get_object_or_404(Completed, id=id)

    ongo = onGoingTasks.objects.create(
        user = comp_Obj.user,
        title = comp_Obj.title,
        description = comp_Obj.description,
        startDate = comp_Obj.scheduledDate,
        startedDate = comp_Obj.startedDate,
        endDate = comp_Obj.deadLine,
        priority = comp_Obj.priority,
        statusOfBeginning = comp_Obj.statusOfBeginning
    )

    comp_Obj.delete()
    return redirect('home')

def comp_todo(request, id):
    comp_Obj = get_object_or_404(Completed, id=id)

    todo = toDoTasks.objects.create(
        user = comp_Obj.user,
        title = comp_Obj.title,
        description = comp_Obj.description,
        startDate = comp_Obj.scheduledDate,
        endDate = comp_Obj.deadLine,
        priority = comp_Obj.priority
    )

    comp_Obj.delete()
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username = username)

        if not user.exists():
            messages.success(request, 'Invalid Username')
            return redirect('login')
        
        user = authenticate(username = username, password = password)

        if not user:
            messages.warning(request, 'Incorrect Password')
            return redirect('login')
        
        login(request, user)
        return redirect('/')

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name') 
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        if user.exists():
            messages.warning(request, "User Name is not Available Try with Another")
            # return render(request, 'login.html', {'show_register' : True})
            return redirect('login')
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('/')
    
    return render(request, 'login.html')


@login_required(login_url='login')
def home(request):
    toDo = toDoTasks.objects.filter(user = request.user)
    onGo = onGoingTasks.objects.filter(user = request.user)
    comp = Completed.objects.filter(user = request.user)
    context = {'toDo' : toDo,'onGo' : onGo, 'comp' : comp}

    now = localtime()

#     if now.hour == 8 and now.minute == 30:
#         today_start = ''
#         for task in toDo:
#             if task.startDate.date() == now.date():
#                 today_start += (task.title + "\n")

#         today_end = ''
#         for task in toDo:
#             if task.endDate.date() == now.date():
#                 today_end += (task.title + "\n")
#         for task in onGo:
#             if task.endDate.date() == now.date():
#                 today_end += (task.title + "\n")
#         send_telegram_message(f'''🔴 ⏳ Deadline Day Has Arrived for 
# these Tasks!
                              
# 📌 Final Call Tasks (Due Today):                       
# { today_end }

# ______________________________________________________________________

# 🟢🚀 New Day, New Grind!
# These missions launch today — no more waiting, it's time to crush them! 💪🔥

# Tasks Scheduled for Today  
# { today_start }''')


#     if now.hour == 9 and now.minute == 00:
#         todo_tasks = ''
#         for task in toDo:
#             todo_tasks += (task.title + "\n")
#         ongo_tasks = ''
#         for task in toDo:
#             ongo_tasks += (task.title + "\n")
        
#         send_telegram_message(f'''💡 📝Tasks in Queue

# {todo_tasks}
# ______________________________________________________________________

# 🚧 🔥Currently In Action

# {ongo_tasks}
# ''')

#     for task in toDo:
#         task_deadLine = task.endDate
#         time_diff = task_deadLine - now
#         if timedelta(hours=23, minutes=59) < time_diff <= timedelta(days=1):
#             send_telegram_message(f'''⚡ HEADS UP, CHAMP!  
# 📌 Task: { task.title }  
# 🕓 24 Hours Left till Deadline!  
# ''')
#         elif timedelta(hours=4, minutes=9) < time_diff <= timedelta(hours=5):
#             send_telegram_message(f'''🚨 THE CLOCK IS TICKING!  
# 🔥 Task: { task.title }  
# 🕔 Only 5 Hours Remaining!  
# ''')
#         elif timedelta(minutes=9) < time_diff <= timedelta(minutes=10):
#             send_telegram_message(f'''🚨 FINAL ALERT!  
# ⏳ Task: { task.title }  
# ⏰ 10 MINUTES TO DEADLINE!
# ''')
            

#     for task in onGo:
#         task_deadLine = task.endDate
#         time_diff = task_deadLine - now
#         if timedelta(hours=23, minutes=59) < time_diff <= timedelta(days=1):
#             send_telegram_message(f'''⚡ HEADS UP, CHAMP!  
# 📌 Task: { task.title }  
# 🕓 24 Hours Left till Deadline!  
# ''')
#         elif timedelta(hours=4, minutes=9) < time_diff <= timedelta(hours=5):
#             send_telegram_message(f'''🚨 THE CLOCK IS TICKING!  
# 🔥 Task: { task.title }  
# 🕔 Only 5 Hours Remaining!  
# ''')
#         elif timedelta(minutes=9) < time_diff <= timedelta(minutes=10):
#             send_telegram_message(f'''🚨 FINAL ALERT!  
# ⏳ Task: { task.title }  
# ⏰ 10 MINUTES TO DEADLINE!
# ''')


    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        priority = request.POST.get('priority')

        todo = toDoTasks.objects.create(
            user = request.user,
            title = title,
            description = description,
            startDate = startDate,
            endDate = endDate,
            priority = priority
        )
#         send_telegram_message(f'''Hey {request.user.first_name}
# 🔥 NEW MISSION UNLOCKED!
# 🎯 Task Created: { title }
# 💡 Description: { description }
# 🚀 Deadline: { endDate }
# 🔥{priority} Priority Task

# 💥 LET'S GET THIS DONE, CHAMP! 💥
# — ONTRACK is watching you...succeed.💪''')
        return redirect('home')

    return render(request, 'home.html', context)


def edit_task_todo(request, task_id):
    task = get_object_or_404(toDoTasks, id=task_id)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.startDate = request.POST.get('startDate')
        task.endDate = request.POST.get('endDate')
        task.priority = request.POST.get('priority')
        task.save()
        return redirect('home')  # your main task list view

    return render(request, 'home.html')

def edit_task_ongo(request, task_id):
    task = get_object_or_404(onGoingTasks, id=task_id)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.startDate = request.POST.get('startDate')
        task.endDate = request.POST.get('endDate')
        task.priority = request.POST.get('priority')
        task.save()
        return redirect('home')  # your main task list view

    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# def send_telegram_message(text):
#     bot_token = config('TELEGRAM_BOT_TOKEN')
#     chat_id = config('TELEGRAM_CHAT_ID')
#     url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

#     payload = {
#         'chat_id': chat_id,
#         'text': text
#     }

#     try:
#         response = requests.post(url, data=payload)
#         return response.json()
#     except Exception as e:
#         print("Telegram Error:", e)