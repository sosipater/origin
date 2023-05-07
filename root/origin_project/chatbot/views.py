from django.http import JsonResponse
from .gpt3_chat import chat_with_gpt_3_5_turbo

def chat(request):
    incoming_msg = request.POST.get('message', '').lower()

    # Initialize the conversation history with a system message
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

    # Append user message to the conversation history
    conversation_history.append({"role": "user", "content": incoming_msg})

    # Get the chatbot's response and append it to the conversation history
    chatbot_response = chat_with_gpt_3_5_turbo(conversation_history)
    conversation_history.append({"role": "assistant", "content": chatbot_response})

    return JsonResponse({"response": chatbot_response})
