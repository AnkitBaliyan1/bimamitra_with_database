from django.shortcuts import render, HttpResponse, redirect
from dotenv import load_dotenv
from .forms import InputForm
from openai._client import OpenAI
import os
import time
from django.contrib.auth.models import User
from django.contrib import messages
import markdown
from IPython.display import HTML
from html import unescape
import re

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
assistant_id = 'asst_gja1V67PclQreusUebPq7Sq1'


# Create your views here.
def base(request):
    return render(request, "application_insure/abc.html")

def home(request):
    return render(request, "application_insure/home.html")


def generate_response(user_input):
    
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role="user",
        content = user_input
    )
    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistant_id,
        #instructions = "Response should end with I hope you liked the response. Let's try another one."
    )
    print("generating resposne")
    to_run=True
    while to_run:
        # converge run id and thread id to overlap with assistant.
        run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )
        #time.sleep(0.01)
        if run.status == 'completed':
            to_run=False

    # reterive messages from from assistant
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )
    print("response received.")
    print(message.content[0].text.value)
    for i in reversed(messages.data):
        print(i.role + " :")
        markdown_answer = markdown.markdown(i.content[0].text.value)
        #markdown_answer = i.content[0].text.value
        print("writing markdown resposne.")

        text = re.sub(r'<.*?>', '', markdown_answer)
        text = unescape(text)

        if i.role=="assistant":
            return markdown_answer, text



from .models import SearchRecord

def bimabot(request):
    chat_history = []
    response_text = None
    
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']     
            response_text, text_db = generate_response(user_input)
            #response_text = f"i have got the resposne.{user_input}"
            SearchRecord.objects.create(
                    username = 'admin',
                    user_input=user_input,
                    response=text_db
                    )

            form=InputForm()
            
    else:
        form=InputForm()


    
    chat_db = SearchRecord.objects.filter(username="admin")
    for i in chat_db:
        conversation_dict = {
                "You": i.user_input,
                "BimaBot": i.response
            }
        chat_history.insert(0,conversation_dict)
        
    
    return render(request, "application_insure/bimabot.html", {'form':form, 'response': response_text, 'chat_history':chat_history})


from application_insure.code.data_connection_script import main_fun
#from .code.data_connection_script import main_fun
#from langchain_community.document_loaders import PyPDFDirectoryLoader
def generate_response_rag(user_input):
    resposne = main_fun(query = user_input, k=4)   
    return resposne

def bimabot_rag(request):
    chat_history = []
    response_text = None
    user='admin_rag'
    
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']     
            response_text = generate_response_rag(user_input)
            #response_text = f"i have got the resposne.{user_input}"
            SearchRecord.objects.create(
                    username = user,
                    user_input=user_input,
                    response=response_text
                    )

            form=InputForm()
            
    else:
        form=InputForm()


    
    chat_db = SearchRecord.objects.filter(username=user)
    for i in chat_db:
        conversation_dict = {
                "You": i.user_input,
                "BimaBot": i.response
            }
        chat_history.insert(0,conversation_dict)
        
    
    return render(request, "application_insure/bimabot.html", {'form':form, 'response': response_text, 'chat_history':chat_history})


def about(request):
    return render(request, "application_insure/about.html")

'''
def contactus(request):
    return render(request, 'application_insure/contactus.html')
'''


# since admin contact us is not working, hence removing this one. 

from .forms import ContactUsForm
def contactus(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()  # This will save the form data to the ContactUs model
            # Redirect to a success page or return a response
            return render(request, "application_insure/contactus.html")  # Replace 'success_page' with the URL name of your success page
    else:
        form = ContactUsForm()

    return render(request, 'application_insure/contactus.html', {'form': form})



from django.contrib.auth import authenticate, login

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']  # Fixed: Use 'lname' for last name
        email = request.POST['email']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return render(request, "application_insure/signup.html")

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, "application_insure/signup.html")

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        # Log the user in after successful registration
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)

        messages.success(request, "Your account has been successfully created.")

        return render(request, "application_insure/signin.html")

    return render(request, "application_insure/signup.html")


def signin(request):

    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            fname = user.first_name

            return render(request, 'application_insure/home.html', {'fname': fname})
        else:
            messages.error(request, "Bad Credentials!")

            return render(request, "application/signin.html")

    return render(request, "application_insure/signin.html")

def signout(request):
    return render(request, "application_insure/signout.html")

