from django.shortcuts import render
import google.generativeai as genai
from django.http import JsonResponse
import re 

# Create your views here.

history = []
# Configure Gemini API
google_api_key = 'AIzaSyAmb11uMRSOS9sAwFSqZbJaOqmFrDpsxTM'
genai.configure(api_key=google_api_key)

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# system_prompt = """
  
#   You are a highly empathetic AI assistant designed to provide emotional and mental health support for students. 
#     Your responsibilities:
    
#     1. **Greeting**: Begin by warmly greeting the user and asking how they are feeling.
#     2. **Emotional Understanding**: Based on the user's response, assess their emotional state (e.g., sad, anxious, stressed, happy).
#     3. **Support**: Offer comforting words, mental health advice, or suggestions for managing stress or anxiety.
#     4. **Structured Response**: Your response should include friendly language, appropriate breaks, and even emojis to make the conversation comforting.
#     5. **Actionable Advice**: If the user is facing challenges, suggest exercises, mindfulness techniques, or professional help where applicable.
#     6. **Response format**: You should include headings, breaks, paragraphs, and emojis for a clean, friendly text.

    
# """

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings
)

#chat with bot

def chat(request):
     prompt = "Extract emotional support resources based on this message: I want to kill myself."
    
     result = model.generate_content(prompt)
     
     print(result.text)
    # Debug: Print the entire result to check its structure
     temp = bold_asterisk_text(result.text)
    
    # Initialize suggestions and resources
     print(temp)
     return render(request, 'chatbot/chat.html', {'result': temp})
   

def bold_asterisk_text(sentence):
    # Replace *word* with <strong>word</strong>
   
    
    while '*' in sentence:
        start = sentence.find('*')
        end = sentence.find('*', start + 1)
        
        if start != -1 and end != -1:
            # Replace the asterisks and make it bold
            sentence = sentence[:start] + '<strong>' + sentence[start + 1:end] + '</strong>' + sentence[end + 1:]
        else:
            break
            
    return sentence
def signup(request):
    return render(request,'chatbot/signup.html')

def login(request):
    return render(request,'chatbot/login.html')

def moodTracker(request):
    return render(request,'chatbot/moodTracker.html')
