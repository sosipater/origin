from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import sys
import json
from django.shortcuts import render
from .models import Chatbot, Message
import os
from django.conf import settings
from .chatbot.views import chat

config_file = os.path.join(settings.BASE_DIR, 'config.json')
with open(config_file, 'r') as f:
    config = json.load(f)
    api_key = config['openai_api_key']
    openai.api_key = api_key

def fetch_history(request):
    if request.method == 'GET':
        conversation_history = Message.objects.all().order_by('created_at')
        serialized_history = []
        for message in conversation_history:
            serialized_history.append({
                "role": message.role,
                "content": message.content
            })
        return JsonResponse({'conversation_history': serialized_history})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        print("Raw POST data:", request.body, file=sys.stderr)  # Add this line to print the raw POST data
        print("Parsed POST data:", json.loads(request.body), file=sys.stderr)  # Add this line to print the parsed POST data

        data = json.loads(request.body)
        user_input = data.get('message')

        # Call ChatGPT API and store the response
        # Save the message and response to the database
        # Return the response to the frontend

        return JsonResponse({'response': 'Chatbot response'})

    return JsonResponse({'error': 'Invalid request method'})

def home(request):
    return HttpResponse("Welcome to Origin!")

def chat_view(request):
    return render(request, 'origin_app/chat.html')

def chatbot_list(request):
    chatbots = Chatbot.objects.all()
    chatbot_id = chatbots[0].id if chatbots else None  # Get the ID of the first chatbot, or None if there are none
    return render(request, 'origin_app/chatbot_list.html', {'chatbots': chatbots, 'chatbot_id': chatbot_id})

def chat_interface(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        chatbot_id = request.GET.get('chatbot_id')  # Get chatbot_id from the request
        chatbot = Chatbot.objects.get(id=chatbot_id)  # Get the chatbot based on the id
        conversation_history = Message.objects.filter(chatbot=chatbot)  # Filter the messages for this chatbot
        conversation_history = conversation_history.order_by('-created_at')[:20][::-1]
        serialized_history = []
        for message in conversation_history:
            serialized_history.append({
                "role": message.role,
                "content": message.content
            })
        return JsonResponse({"conversation_history": serialized_history})

    else:
        chatbots = Chatbot.objects.all()
        if chatbots.exists():
            default_chatbot = chatbots.first()
            conversation_history = Message.objects.filter(chatbot=default_chatbot)
            conversation_history = conversation_history.order_by('-created_at')[:20][::-1]
        else:
            default_chatbot = None
            conversation_history = []
        return render(request, 'chat_interface.html', {
            'chatbots': chatbots,
            'chatbot_id': default_chatbot.id if default_chatbot else None,
            'conversation_history': conversation_history
        })
@csrf_exempt
def chat(request):
    print("Request headers:", request.headers, file=sys.stderr)
    print("Request body:", request.body, file=sys.stderr)

    if request.method == 'POST':
        user_message = request.POST.get('message')
        chatbot_id = request.POST.get('chatbot_id')

        print("User message:", user_message)
        print("Chatbot ID:", chatbot_id)

        if not chatbot_id:  # Check if chatbot_id is not empty
            return JsonResponse({'error': 'Invalid chatbot_id'}, status=400)

        chatbot = Chatbot.objects.get(pk=chatbot_id)
        Message.objects.create(role='user', content=user_message, chatbot=chatbot)  # Save the user's message to the database

        conversation_history = Message.objects.filter(chatbot=chatbot).order_by('created_at')

        messages = [
            {"role": "system", "content": "You are a helpful assistant with access to the conversation history."},
            *[
                {"role": message.role.strip(), "content": message.content}
                for message in conversation_history
            ],
            {"role": "user", "content": user_message},
        ]

        # Choose the model based on the chatbot's name
        model = "gpt-3.5-turbo" if chatbot.name == "GPT-3.5 Turbo" else "gpt-4"

        # Call the OpenAI Chat API
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )
        assistant_message = response['choices'][0]['message']['content']

        Message.objects.create(role='assistant', content=assistant_message, chatbot=chatbot)  # Save the assistant's message to the database

        return JsonResponse({'message': assistant_message})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
