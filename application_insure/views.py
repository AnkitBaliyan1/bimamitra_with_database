from django.shortcuts import render, HttpResponse, redirect
from dotenv import load_dotenv
from .forms import InputForm
from openai._client import OpenAI
import os
import time

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
assistant_id = 'asst_gja1V67PclQreusUebPq7Sq1'


# Create your views here.

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
        instructions = "Response should end with I hope you liked the response. Let's try another one."
    )

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

    for i in reversed(messages.data):
        print(i.role + " :")
        final_answer = i.content[0].text.value
        print(final_answer)

        if i.role=="assistant":
            return i.content[0].text.value

    

chat_history = []
def bimabot(request):
    response_text = None
    
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']            
            response_text = generate_response(user_input)
            #response_text = "i have got the resposne."
            conversation_dict = {
                "You": user_input,
                "BimaBot": response_text
            }
            chat_history.insert(0,conversation_dict)
            form=InputForm()
            
    else:
        form=InputForm()

    return render(request, "application_insure/bimabot.html", {'form':form, 'response': response_text, 'chat_history':chat_history})


def about(request):
    return render(request, "application_insure/about.html")


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

'''