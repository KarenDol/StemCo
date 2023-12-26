# importing render and redirect
from django.shortcuts import render, redirect
# importing the openai API
import openai
# import the generated API key from the secret_key file
from .secret_key import API_KEY
# loading the API key from the secret_key file
openai.api_key = API_KEY
from .models import Problem, Hint, Question_Creator
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import datetime


# this is the home view for handling home page logic
def home(request):
    context = "Provide short and comprehensive responses:"
    try:
        # if the session does not have a messages key, create one
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": context},
            ]
        if 'mes' not in request.session:
            request.session['mes'] = [
                {"role": "system", "content": context},
            ]
        # "You are now chatting with a user, provide them with comprehensive, short and concise answers."
        if request.method == 'POST':
            # get the prompt from the form
            key = request.POST.get('prompt')
            #parse the problemID from the prompt
            problem = Problem.objects.get(pk=key)
            #Get the problem content
            problem_context = "In the context of the following problem:" + problem.content + "Give me a really SMALL hint, but do not solve it for me, I want to solve it by myself."
            # get the temperature from the form
            temperature = float(request.POST.get('temperature', 0.1))
            # append the prompt to the messages list
            request.session['messages'].append({"role": "user", "content": problem_context})
            request.session['mes'].append({"role": "user", "content": key})
            # set the session as modified
            request.session.modified = True
            # call the openai API
            response = openai.ChatCompletion.create(model="gpt-4",
            messages=request.session['messages'],
            temperature=temperature,
            max_tokens=1000)
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            hints=[]
            hints.append(formatted_response)
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session['mes'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            for i in range(2):
                request.session['messages'].append({"role": "user", "content": problem_context})
                request.session['mes'].append({"role": "user", "content": "give me another small hint that differs from your previous hint, but still do not solve the problem fully, I want to solve it by myself"})
                request.session.modified = True
                response = openai.ChatCompletion.create(model="gpt-4",
                                                        messages=request.session['messages'],
                                                        temperature=temperature,
                                                        max_tokens=1000)
                formatted_response = response['choices'][0]['message']['content']
                hints.append(formatted_response)
                request.session['messages'].append({"role": "assistant", "content": formatted_response})
                request.session['mes'].append({"role": "assistant", "content": formatted_response})
                request.session.modified = True
            hint=Hint(problem_ID=key, hint1=hints[0], hint2=hints[1], hint3=hints[2])
            hint.save()
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
                'mes': request.session['mes'],
            }
            return render(request, 'home.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'mes': request.session['mes'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'home.html', context)
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
        return render(request, 'error.html')

def new_chat(request):
    # clear the messages list
    request.session.pop('messages', None)
    request.session.pop('mes', None)
    return redirect('home')

def image(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            qc = Question_Creator.objects.get(user=request.user)
            if qc.last_update!=datetime.date.today():
                qc.balance=5
                qc.last_update=datetime.date.today()
                qc.save()
            if qc.balance==0:
                messages.error(request, "Your balance is zero. Come tomorrow for new images")
                return redirect('image')
            else:
                qc.balance -= 1
                qc.save()
                prompt = request.POST.get('prompt')
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512",
                )
                response=response['data'][0]['url']
                return render(request, "none.html", {'link': response})
        else:
            return render(request, "none.html", {'link': None})
    else:
        return redirect('login_user')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('image')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('image')
            else:
                messages.error(request, "Login failed. Please check your username and password.")
                return redirect('login_user')
        else:
            return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')