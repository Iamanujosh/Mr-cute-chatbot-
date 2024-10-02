from django.shortcuts import render,redirect
import google.generativeai as genai
from django.http import JsonResponse
import re 
from django.core.files.storage import default_storage
import base64
from django.utils.safestring import mark_safe
import os
from .forms import CustomUserCreationForm


# Create your views here.

history = []
# Configure Gemini API
google_api_key = 'AIzaSyDwcpxJ34DnWKBEFPC78FAiQ5kKQd8yXC4'
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

system_prompt = """
  
 You are an empathetic AI assistant specializing in providing mental health support primarily for students.in every coversation to motivate students provide them quotes and for bold andimportant text use only **
 
Your key responsibilities include:

1.Greeting: Start with a warm greeting and ask the student how they're feeling.

2.Emotional Assessment: Based on their response, identify their emotional state (e.g., stressed, anxious, sad, happy) and adjust your tone and suggestions accordingly.

3.Support and Guidance:
Offer comforting words and mental health advice.
Suggest relaxation techniques, mindfulness exercises, or professional help if necessary.
Provide motivational quotes that align with the student’s emotional state or current challenge.

4.Motivational Media Suggestions:
Recommend inspiring movies, uplifting songs, or meaningful books that can help improve their mindset.
Tailor suggestions to their emotional needs (e.g., movies about overcoming adversity, songs that boost confidence).

5.Practical Advice: Offer actionable steps like journaling, breathing exercises, or time management tips to help with academic and emotional challenges.

6.Structured and Friendly Tone: Use simple, clear language with appropriate formatting. Include headings, breaks, and emojis to create a conversational, comforting experience.

Remember: Your primary users are students. They may often feel overwhelmed by academic pressure or life changes, so offer patient, encouraging, and practical guidance at all times. Always conclude your interactions with optimism and positivity.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=system_prompt
)

#chat with bot

def chat(request):
     
     context = {}

     if request.method == "POST":
        image_file = request.FILES.get('image', None)
        user_input = request.POST.get('user_input', None)

        # Check if an image was uploaded
        if image_file:
            # Save the uploaded image temporarily
            image_path = default_storage.save(f"temp/{image_file.name}", image_file)
            
            with open(image_path, "rb") as image:
                image_data = image.read()

            # Encode image data to Base64
            image_data_base64 = base64.b64encode(image_data).decode('utf-8')

            # Prepare image part
            image_part = {
                "mime_type": image_file.content_type,  # Ensure correct MIME type
                "data": image_data_base64  # Use Base64-encoded string
            }

            prompt_parts = [image_part, system_prompt] if not user_input else [user_input, image_part, system_prompt]

            # Generate response using the model
            response = model.generate_content(prompt_parts)
            
            if response:
                context['message'] = response.text
                print(response.text)
                return JsonResponse({'bot_response': response.text})

            # Clean up the temporary file
            os.remove(image_path)
        elif user_input:
            context['message'] = "No matching symptoms found. Please provide more details."
            chat_session = model.start_chat(history=history)
            response = chat_session.send_message(user_input)
            model_response = bold_asterisk_text(response.text)
            example_message = "<b>Hello!</b> This message is <i>italicized</i>."
           

            # Append user and bot messages to the history
            history.append({"role": "user", "parts": [user_input]})
            history.append({"role": "model", "parts": [model_response]})
            
            # Return JSON response for the bot's reply
            context = {
            'message': history,
            'example_message': mark_safe(example_message)  # Mark as safe for rendering
        }
            print(history)
            print("Doctor Card:", context.get('doctor_card'))  # Debug output

            return JsonResponse({
                'bot_response': model_response,
                'doctor_card': context.get('doctor_card'),  # Doctor details if found
                'history': history
            })
        
        else:
            # If neither image nor text is provided, show an error message
            context['error'] = "Please provide an image or text input for analysis."

     return render(request, 'chatbot/chat.html', context)

   

def bold_asterisk_text(sentence):
    # Replace *word* with <strong>word</strong>
   
    sentence = sentence.replace('\n','<br>')
    while '**' in sentence:
        start = sentence.find('**')
        end = sentence.find('**', start + 1)
        
        if start != -1 and end != -1:
            # Replace the asterisks and make it bold
            sentence = sentence[:start] + '<strong>' + sentence[start + 1:end] + '</strong>' + sentence[end + 1:]
        else:
            break
            
    return sentence
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect after successful registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'chatbot/signup.html', {'form': form})

def login(request):
    return render(request,'chatbot/login.html')

def moodTracker(request):
    return render(request,'chatbot/moodTracker.html')
