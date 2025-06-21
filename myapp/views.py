from venv import logger
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import  check_password
from django.views import View
from myapp.forms import  UserRegistrationForm, UserLoginForm, AddDoctorForm, AdminRegistrationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from deepface import DeepFace
import cv2
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import json 
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
import os
import speech_recognition as sr
from .models import Word
import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import DoctorDetails
from datetime import datetime, timedelta, timezone
from .forms import ConsultationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .models import Word
import logging
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
#STORY Management
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import os
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from gtts import gTTS
import fitz  # PyMuPDF
from .models import Story
from PIL import Image
import pytesseract
import speech_recognition as sr
from django.http import JsonResponse
from pydub import AudioSegment  # For converting audio files to WAV format
import wave
from django.conf import settings
from django.http import HttpResponse
from gtts import gTTS
import fitz  # PyMuPDF
from .models import Story
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm  # Use the correct form
from django.contrib.auth import authenticate, login as auth_login
from .forms import UserLoginForm
from .models import Consultation
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User  # Assuming you're using the default User model
from .forms import AddDoctorForm  # Assuming AddDoctorForm is handling DoctorDetails
from .models import DoctorDetails, UserRegistration  # Assuming UserRegistration is a separate model
from django.contrib import messages
from .forms import AddDoctorForm  # Assuming AddDoctorForm handles DoctorDetails fields
from .models import DoctorDetails, UserRegistration  # Models you provided
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils import timezone  # Import Django's timezone utility
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import DoctorDetails, Consultation  # Replace with your actual model imports
import os
from django.http import JsonResponse
from gtts import gTTS
import fitz  # PyMuPDF
from .models import Story
from PIL import Image
import pytesseract
import io
import os
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from gtts import gTTS
import fitz  # PyMuPDF
from .models import Story
# Home page view

def landing_page(request):
    return render(request, 'landing_page.html')

def services(request):
    return render(request, 'services.html')

# Contact page view (if needed)
def contact(request):
    return render(request, 'contact.html')

def authentification(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)  # Use the correct form
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.save()
            print(f"User {user.email} registered with role: {user.role}")  # Debug print

            # Send email verification
            send_verification_email(user, request)

            
            return redirect('home')  # After successful registration, redirect to home page
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors.')
    else:
        form = UserRegistrationForm()  # Use the correct form

    return render(request, 'authentification.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:  # Ensure the user's email is verified or active
                    auth_login(request, user)
                    print(f"User role is: {user.role}")

                    # Redirect based on the role stored in the database
                    if user.role == 'doctor':
                        return redirect('doctor_dashboard')  # Example: Redirect to doctor dashboard
                    elif user.role == 'admin':
                        return redirect('admin_dashboard')  # Example: Redirect to admin dashboard
                    else:
                        return redirect('home')  # Default redirect for normal users
                else:
                    messages.error(request, "Your account is inactive. Please verify your email.")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

# Email verification view
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserRegistration.objects.get(pk=uid)
    except (UserRegistration.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your email has been verified successfully!")
        return redirect('home')
    else:
        return render(request, 'verification_failed.html')

# Send email verification link
def send_verification_email(user, request):
    uid = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)
    verification_link = request.build_absolute_uri(reverse('verify_email', args=[uid, token]))

    subject = "Email Verification"
    html_message = f"""
    <html>
    <body>
        <p>Dear {user.username},</p>
        <p>Thank you for registering! Please verify your email by clicking the link below:</p>
        <p><a href="{verification_link}">Verify Email</a></p>
        <p>Best regards,<br>Your Website Team</p>
    </body>
    </html>
    """
    
    send_mail(
        subject,
        "Please verify your email", 
        settings.DEFAULT_FROM_EMAIL, 
        [user.email], 
        html_message=html_message
    )

def home(request):
    role = request.GET.get('role', 'user')
    return render(request, 'home.html',{'role': role,})

def activities(request):
    return render(request, 'activities.html')

def maincontact(request):
    return render(request, 'maincontact.html')

def mainservices(request):
  return render(request, 'mainservices.html')

def stories(request):
    stories = Story.objects.all()
    return render(request, 'stories.html', {
        'stories': stories,
    })

@login_required
@csrf_exempt
def book_consultation(request):
    if request.method == "POST":
        # Get POST data
        doctor_id = request.POST.get('doctor_id')
        consultation_type = request.POST.get('consultation_type')
        consultation_time = request.POST.get('consultation_time')

        if not doctor_id or not consultation_type or not consultation_time:
            messages.error(request, "All fields are required.")
            return redirect('consultation')  # Redirect back to the consultation page

        try:
            # Use Django's timezone.now() for timezone-aware datetime
            today_date = timezone.now().date()  # Get today's date
            consult_datetime = datetime.strptime(f"{today_date} {consultation_time}", '%Y-%m-%d %I:%M %p')
            consult_time = consult_datetime.strftime('%Y-%m-%d %H:%M')
        except ValueError:
            messages.error(request, "Invalid time format. Please use the 12-hour format (e.g., 9:09 AM).")
            return redirect('consultation')  # Redirect back to the consultation page

        # Get the doctor object
        doctor = get_object_or_404(DoctorDetails, id=doctor_id)

        # Check if the selected time slot is already booked
        existing_consultation = Consultation.objects.filter(
            doctor=doctor,
            consultation_time=consult_time,
        ).first()

        if existing_consultation:
            messages.error(request, "This time slot is already booked.")
            return redirect('consultation')  # Redirect back to the consultation page

        # Create the consultation record
        consultation = Consultation.objects.create(
            user=request.user,
            doctor=doctor,
            consultation_type=consultation_type,
            consultation_time=consult_time,
        )

        # Add success message
        messages.success(request, "Consultation booked successfully.")
        return redirect('consultation')  # Redirect back to the consultation page

    else:
        messages.error(request, "Invalid request method. Use POST.")
        return redirect('consultation')  # Redirect back to the consultation page
    
from datetime import datetime, timedelta


def generate_slots_for_doctor(doctor):
    # Debug: Print the doctor's details
    print(f"Doctor: {doctor.name}, Start Time: {doctor.start_time}, End Time: {doctor.end_time}")

    # Get all booked time slots for the doctor
    booked_times = Consultation.objects.filter(
        doctor=doctor,
    ).values_list('consultation_time', flat=True)

    # Debug: Print the booked times
    print("Booked Times:", list(booked_times))

    # Convert the doctor's start_time and end_time to datetime objects
    today = datetime.today().date()  # Use today's date for the datetime object
    start_time = datetime.combine(today, doctor.start_time)  # Combine date and time
    end_time = datetime.combine(today, doctor.end_time)

    # Debug: Print the start and end times
    print("Start Time (Datetime):", start_time)
    print("End Time (Datetime):", end_time)

    # Generate available time slots in 30-minute intervals
    available_slots = []
    current_time = start_time
    while current_time < end_time:
        # Format the time as a string (e.g., "09:00 AM")
        slot_time = current_time.strftime('%I:%M %p')

        # Debug: Print the current slot being checked
        print(f"Checking Slot: {slot_time}")

        # Check if the slot is already booked
        if slot_time not in booked_times:
            available_slots.append(slot_time)
            # Debug: Print if the slot is available
            print(f"Slot Available: {slot_time}")
        else:
            # Debug: Print if the slot is booked
            print(f"Slot Booked: {slot_time}")

        # Increment by 30 minutes
        current_time += timedelta(minutes=30)

    # Debug: Print the final list of available slots
    print("Available Slots:", available_slots)

    return available_slots


def consultation(request):
    """
    View to display available slots for doctors.
    """
    doctors = DoctorDetails.objects.all()
    doctor_slots = {}

    for doctor in doctors:
        # Get all booked time slots for the doctor
        booked_slots = Consultation.objects.filter(
            doctor=doctor,
        ).values_list('consultation_time', flat=True)

        # Convert booked slots to a list of strings (e.g., "09:00 AM")
        booked_slots = [timezone.localtime(slot).strftime('%I:%M %p') for slot in booked_slots]

        # Store booked slots in the dictionary
        doctor_slots[doctor.id] = booked_slots

    # Convert the dictionary to a JSON string
    doctor_slots_json = json.dumps(doctor_slots, cls=DjangoJSONEncoder)

    return render(request, 'consultation.html', {
        'doctors': doctors,
        'doctor_slots': doctor_slots_json,  # Pass as JSON
    })


@staff_member_required
def admin_dashboard(request):
      return render(request, 'admin_dashboard.html')
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddDoctorForm
from .models import UserRegistration, DoctorDetails

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_doctor(request):
    if request.method == 'POST':
        print("Form data:", request.POST)  # Debugging
        form = AddDoctorForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debugging
            try:
                # Extract form data
                doctor_data = form.cleaned_data
                # Create the user
                user = UserRegistration.objects.create_user(
                    email=doctor_data['email'],
                    username=doctor_data['username'],
                    password=doctor_data['password'],
                    role='doctor'
                )
                if not user:
                    raise ValueError("User creation failed.")

                # Create DoctorDetails and link to the user
                DoctorDetails.objects.create(
                    user=user,
                    doctor_name=doctor_data['doctor_name'],
                    specialization=doctor_data['specialization'],
                    contact_number=doctor_data['contact_number'],
                    clinic_address=doctor_data['clinic_address'],
                    qualifications=doctor_data['qualifications'],
                    experience_years=doctor_data['experience_years'],
                    available_days=doctor_data['available_days'],
                    start_time=doctor_data['start_time'],
                    end_time=doctor_data['end_time']
                )

                messages.success(request, 'Doctor account created successfully.')
                return redirect('admin_dashboard')

            except Exception as e:
                messages.error(request, f'Error creating doctor account: {str(e)}')
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors.')

    else:
        form = AddDoctorForm()

    return render(request, 'add_doctor.html', {'form': form})

def doctor_list(request):
    doctors = DoctorDetails.objects.all()  # Get all doctors from the database
    return render(request, 'doctor_list.html', {'doctors': doctors})
@login_required
@user_passes_test(lambda u: u.is_superuser)
def modify_doctor(request, id):
    doctor = get_object_or_404(DoctorDetails, id=id)
    print("Form data:", id)  # Debugging
    if request.method == 'POST':
        print("Form data:", request.POST)  # Debugging
        form = AddDoctorForm(request.POST)
            # Access the cleaned data from the form
        # Access form fields directly from request.POST
        doctor.doctor_name = request.POST.get('doctor_name')
        doctor.specialization = request.POST.get('specialization')
        doctor.email = request.POST.get('email')
        doctor.contact_number = request.POST.get('contact_number')
        doctor.clinic_address = request.POST.get('clinic_address')
        doctor.qualifications = request.POST.get('qualifications')
        doctor.experience_years = request.POST.get('experience_years')
        doctor.available_days = request.POST.get('available_days')
        doctor.start_time = request.POST.get('start_time')
        doctor.end_time = request.POST.get('end_time')
        doctor.save()
        messages.success(request, 'Doctor details updated successfully.')
        return redirect('doctor_list')
      
    else:
        form = AddDoctorForm(initial={
            'doctor_name': doctor.doctor_name,
            'specialization': doctor.specialization,
            'email': doctor.user.email,  # Assuming email is stored in the user model
            'contact_number': doctor.contact_number,
            'clinic_address': doctor.clinic_address,
            'qualifications': doctor.qualifications,
            'experience_years': doctor.experience_years,
            'available_days': doctor.available_days,
            'start_time': doctor.start_time,
            'end_time': doctor.end_time,
        })
    return render(request, 'modify_doctor.html', {'form': form, 'doctor': doctor})


# Delete Doctor View
def delete_doctor(request, id):
    doctor = get_object_or_404(DoctorDetails, id=id)
    try:
        # Delete the associated user
        user = doctor.user  # Assuming `DoctorDetails` has a `user` ForeignKey to `UserRegistration`
        user.delete()
        
        messages.success(request, f'Doctor "{doctor.doctor_name}" and associated user account deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error deleting doctor: {str(e)}')

    return redirect('doctor_list')

@login_required
def doctor_dashboard(request):
    # Fetch the doctor's consultations
    consultations = Consultation.objects.filter(doctor__user=request.user).order_by('consultation_time')
    return render(request, 'doctor_dashboard.html', {'consultations': consultations})

# FACIAL EXPRESSIONS DETECTION CODE

def facial_expression_view(request):
    if request.method == "POST":
        # Capture the video frame from the POST request
        video_capture = cv2.VideoCapture(0)  # Use the default camera
        
        ret, frame = video_capture.read()
        if not ret:
            return JsonResponse({"error": "Could not capture video frame"}, status=400)
        
        # Analyze facial expression
        try:
            result = DeepFace.analyze(frame, actions=['emotion'])
            detected_emotion = result[0]['dominant_emotion']
            
            # Check if the detected expression matches the required one
            required_expression = request.POST.get("required_expression")
            if detected_emotion.lower() == required_expression.lower():
                return JsonResponse({"success": True, "message": "Expression matched!"})
            else:
                return JsonResponse({"success": False, "message": "Expression did not match.", "detected": detected_emotion})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        finally:
            video_capture.release()
    else:
        return render(request, 'facial_expression.html')

@csrf_exempt  # To handle POST requests without CSRF token (use carefully in production)
def check_expression(request):
    if request.method == "POST":
        data = json.loads(request.body)
        required_expression = data['required_expression'].lower().strip()  # Convert to lowercase and strip spaces
        frame = data['frame']  # The base64 image from the frontend
        
        # Decode the base64 image
        img_data = base64.b64decode(frame.split(",")[1])  # Remove the header part of base64 string
        img = Image.open(BytesIO(img_data))

        # Convert the image to a numpy array that DeepFace can use
        img = np.array(img)
        
        # If the image has an alpha channel (transparency), we remove it
        if img.shape[-1] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        # Define the emotion map to handle variations in DeepFace's predicted emotion
        emotion_map = {
            "surprise": "surprised",
            "neutral": "neutral",
            "happy": "happy",
            "sad": "sad",
            "angry": "angry",
            # Add other mappings here if necessary
        }

        try:
            # Analyze the image for emotion
            result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
            
            # Extract the predicted emotion (ensure it's in the correct format)
            predicted_emotion = result[0]['dominant_emotion'].lower().strip()  # Convert to lowercase and strip spaces
            
            # Use the emotion map to normalize any variations (like 'surprise' -> 'surprised')
            predicted_emotion = emotion_map.get(predicted_emotion, predicted_emotion)

            # Check if the predicted emotion matches the required expression
            if predicted_emotion == required_expression:
                response = {"message": "Correct expression!"}
            else:
                response = {"message": f"Incorrect expression! You made a {predicted_emotion}."}
            
        except Exception as e:
            response = {"message": f"Error: {str(e)}"}
        
        return JsonResponse(response)

    return JsonResponse({"message": "Invalid request method."}, status=400)

# PRONUNCIATION CORRECTION CODE

@csrf_exempt
def get_word(request):
    # Get a random word and its associated image
    words = list(Word.objects.all())
    word = random.choice(words)
    return JsonResponse({'word': word.word, 'image': word.image.url})

@csrf_exempt
def speak_word(request):
    # Receive word data, generate speech, and return audio file path
    data = json.loads(request.body)
    word = data.get('word')
    tts = gTTS(text=word, lang='en')
    audio_path = f'media/audio/{word}.mp3'  # Save audio to 'media/audio/{word}.mp3'
    tts.save(audio_path)
    return JsonResponse({'audio_path': audio_path})

import os
import speech_recognition as sr
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pydub import AudioSegment  # For converting audio files to WAV format

import wave

@csrf_exempt
def assess_pronunciation(request):
    if request.method == 'POST':
        # Receive audio file and expected word
        audio_file = request.FILES['audio']
        expected_word = request.POST['expected_word']

        # Check if the uploaded file is a valid WAV file
        try:
            with wave.open(audio_file, 'rb') as wf:
                # Verify that the file is a valid WAV and has the correct format
                if wf.getsampwidth() != 2:  # Check sample width (16-bit PCM is standard)
                    raise ValueError("Invalid WAV format. Expected 16-bit PCM WAV.")
                if wf.getnchannels() != 1:  # Ensure mono audio
                    raise ValueError("Invalid WAV format. Expected mono audio.")
        except Exception as e:
            return JsonResponse({'feedback': f"Invalid audio file: {str(e)}"})

        # Proceed with transcription and comparison as before
        # Save the uploaded audio temporarily
        audio_path = 'temp_audio.wav'
        with open(audio_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        # Transcribe audio using speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        try:
            transcription = recognizer.recognize_google(audio).lower()
            if transcription == expected_word.lower():
                feedback = "Correct!"
            else:
                feedback = f"Incorrect. You said '{transcription}', but the correct word is '{expected_word}'."
        except sr.UnknownValueError:
            feedback = "Could not understand your pronunciation. Please try again."

        if os.path.exists(audio_path):
             os.remove(audio_path)

        return JsonResponse({'feedback': feedback})

def pronunciation_view(request):
    # Fetch a random word from the database
    word = Word.objects.order_by('?').first()  # Random word

    if word:
        # Construct the image URL for the word
        image_url = word.image.url  # The image path stored in the database
    else:
        word = "No Word Found"  # Default word if none is found
        image_url = "/media/images/default.jpg"  # Fallback image if no image is found

    # Pass the word and image URL to the template
    return render(request, 'pronunciation.html', {'word': word.word, 'image_url': image_url})


#  STORY READING CODE

# Extract text from a PDF where the text is selectable
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    pages_text = [page.get_text("text").strip() for page in document if page.get_text("text").strip()]
    document.close()
    return pages_text

# Generate audio files for each page of the story
def generate_audio_for_story(story):
    audio_files = []
    pages_text = extract_text_from_pdf(story.pdf.path)
    for i, text in enumerate(pages_text):
        audio_filename = f"story_{story.id}_page_{i + 1}.mp3"
        audio_path = os.path.join(settings.MEDIA_ROOT, 'stories', 'audio', audio_filename)
        tts = gTTS(text, lang='en')
        tts.save(audio_path)
        audio_files.append(audio_filename)
    story.audio_files = audio_files
    story.save()

# Serve audio files
def serve_audio(request, filename):
    audio_file_path = os.path.join(settings.MEDIA_ROOT, 'stories', filename)
    if os.path.exists(audio_file_path):
        with open(audio_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="audio/mpeg")
            response['Content-Disposition'] = f'inline; filename={filename}'
            return response
    return HttpResponse(status=404)

# Story detail view
import json
import logging

logger = logging.getLogger(__name__)
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

def story_detail(request, story_id):
    # Fetch the story object
    story = get_object_or_404(Story, pk=story_id)

    # Log the audio files for debugging purposes
    logger.debug(f"Audio files: {story.audio_files}")

    # If the story does not have audio files, regenerate them
    if not story.audio_files:
        try:
            generate_audio_for_story(story)
        except Exception as e:
            logger.error(f"Error generating audio files: {e}")

    # Construct the full URL for the PDF
    pdf_url = f"{settings.MEDIA_URL}{story.pdf}" if story.pdf else None

    # Parse and ensure audio_files is a JSON-compatible list
    audio_files = []
    if story.audio_files:
        try:
            audio_files = json.loads(story.audio_files) if isinstance(story.audio_files, str) else story.audio_files
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in story.audio_files")

    # Parse and ensure questions is a JSON-compatible list
    questions = []
    if story.questions:
        try:
            questions = json.loads(story.questions) if isinstance(story.questions, str) else story.questions
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in story.questions")

    # Render the HTML template with the story data
    return render(
        request,
        'story_detail.html',
        {
            'story': story,
            'pdf_url': pdf_url,
            'audio_files': json.dumps(audio_files),  # Ensure valid JSON for JavaScript
            'questions': json.dumps(questions),     # Ensure valid JSON for JavaScript
        }
    )

def check_answer(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    question_index = int(request.GET.get('question_index'))
    user_answer = request.GET.get('answer')
    correct_answer = story.questions[question_index]["correct_answer"]

    response_data = {
        'result': user_answer == correct_answer,
        'correct_answer': correct_answer if user_answer != correct_answer else None,
    }
    return JsonResponse(response_data)

#STORY Management
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def manage_stories(request):
    stories = Story.objects.all()
    return render(request, 'manage_stories.html', {'stories': stories})

def add_story(request):
    if request.method == 'POST':
        title = request.POST.get('name')
        pdf = request.FILES.get('pdf')
        quiz_questions = request.POST.get('quiz_questions')

        try:
            quiz_questions = json.loads(quiz_questions) if quiz_questions else []
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON for quiz questions.'})

        if not title or not pdf:
            return JsonResponse({'status': 'error', 'message': 'Missing title or PDF file.'})

        story = Story.objects.create(title=title, pdf=pdf, questions=quiz_questions)
        return JsonResponse({'status': 'success', 'story': {'id': story.id, 'name': story.title}})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def update_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if request.method == 'POST':
        title = request.POST.get('name')
        pdf = request.FILES.get('pdf')
        quiz_questions = request.POST.get('quiz_questions')

        # Handle quiz questions (if any)
        try:
            quiz_questions = json.loads(quiz_questions) if quiz_questions else []
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON for quiz questions.'})

        # Update the story's title
        if title:
            story.title = title
        
        # If a new PDF is uploaded, process it
        if pdf:
            # Clear old audio files before saving the new PDF
            audio_folder = os.path.join(settings.MEDIA_ROOT, 'stories', 'audio')
            for filename in os.listdir(audio_folder):
                if filename.startswith(f"story_{story.id}_") and filename.endswith(".mp3"):
                    file_path = os.path.join(audio_folder, filename)
                    os.remove(file_path)

            # Save the new PDF and clear old audio files
            story.pdf = pdf
            story.audio_files= [] # Clear old audio files before generating new ones

        # Update quiz questions
        story.questions = quiz_questions
        story.save()  # Save the updated story

        return JsonResponse({'status': 'success', 'story': {'id': story.id, 'name': story.title}})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def delete_story(request, story_id):
    try:
        # Get the story by ID
        story = get_object_or_404(Story, id=story_id)

        # Define the path to the audio folder
        audio_folder = os.path.join(settings.MEDIA_ROOT, 'stories', 'audio')

        # Delete audio files related to the story
        deleted_files = []
        for filename in os.listdir(audio_folder):
            if filename.startswith(f"story_{story.id}_") and filename.endswith(".mp3"):
                file_path = os.path.join(audio_folder, filename)
                try:
                    os.remove(file_path)
                    deleted_files.append(file_path)
                except Exception as e:
                    continue  # Ignore errors in deleting individual files

        # Delete the story itself
        story.delete()

        return JsonResponse({'status': 'success', 'message': 'Story and associated audios deleted successfully.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'An error occurred while deleting the story'}, status=500)
    
# MANAGE WORDS

def manage_words(request):
    return render(request, 'manage_words.html')

@csrf_exempt
def get_words(request):
    """Fetch all words."""
    if request.method == 'GET':
        words = Word.objects.all()
        word_list = [
            {
                "id": word.id,
                "word": word.word,
                "image": word.image.url if word.image else "",  # Serialize the image URL
                "difficulty": word.difficulty,
            }
            for word in words
        ]
        return JsonResponse(word_list, safe=False)
    
    
def file_exists(file_path):
    """Check if a file already exists in the specified path."""
    return os.path.exists(file_path)
    
@csrf_exempt
def add_word(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        difficulty = request.POST.get('difficulty')
        image = request.FILES.get('image')

        if not word or not difficulty or not image:
            return JsonResponse({'status': 'error', 'message': 'All fields are required!'})

     # Use the word as-is for naming the files
        file_safe_word = word.strip().lower()  # Strip whitespace for safety

        # Check if the image already exists
        image_name = f'{file_safe_word}'

        # Save the uploaded image to the specified folder
        fs = FileSystemStorage(location='media/images/')
        image_name = fs.save(f"{image_name}.jpg", image)

      #  image_name = fs.save(image.name, image)

        # Save the word and image path in the database
        Word.objects.create(
            word=word,
            difficulty=difficulty,
            image=f'images/{image_name}',
        )

        return JsonResponse({'status': 'success', 'message': 'Word added successfully!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})

@csrf_exempt
def edit_word(request, word_id=None):
    """Add or edit a word, checking for existing image/audio."""
    if request.method == 'POST':
        # If word_id is provided, we are editing an existing word
        if word_id:
            word = get_object_or_404(Word, id=word_id)
        else:
            word = Word()  # If no word_id, it's a new word (creating)


        word_data = request.POST

        new_word = word_data.get('word', word.word)  # New word text from request

        # Handle audio deletion if the word changes
        if new_word != word.word:
            # Define the old audio file path
            old_audio_filename = f'{word.word.capitalize()}.mp3'
            old_audio_path = os.path.join(settings.MEDIA_ROOT, 'audio', old_audio_filename)
            if os.path.exists(old_audio_path):
                os.remove(old_audio_path)  # Delete the old audio file


        word.word = word_data.get('word', word.word)
        word.difficulty = word_data.get('difficulty', word.difficulty)

        # Handle image upload
        if 'image' in request.FILES:
            image = request.FILES['image']
            image_path = os.path.join(settings.MEDIA_ROOT, 'images', image.name)

            if not file_exists(image_path):
                fs = FileSystemStorage(location='media/images/')
                image_name = fs.save(image.name, image)
                word.image = f'images/{image_name}'  # Save the new image path
            else:
                word.image = f'images/{image.name}'  # Use the existing image

        # Check and set the audio file path based on the word
        audio_filename = f'{word.word.capitalize()}.mp3'  # Capitalize the first letter of the word and add .mp3
        audio_path = os.path.join(settings.MEDIA_ROOT, 'audio', audio_filename)

        if file_exists(audio_path):
            word.audio = f'audio/{audio_filename}'  # Use the existing audio

        word.save()  # Save the word to the database

        return JsonResponse({
            "status": "success",
            "message": "Word added/updated successfully",
            "word": word.word,
            "difficulty": word.difficulty,
            "image": word.image if word.image else "",
            "audio": word.audio if word.audio else ""
        })
    
    return JsonResponse({"status": "error", "message": "Invalid request method!"})


@csrf_exempt
def delete_word(request, word_id):
    try:
        word = get_object_or_404(Word, id=word_id)

        # Delete the image if it exists
        if word.image:
            image_path = os.path.join('media', word.image.path)  # Get the full path to the image
            if os.path.exists(image_path):
                os.remove(image_path)  # Delete the image from the file system

        # Delete the audio file
        audio_path = os.path.join('media', 'audio', f"{word.word.capitalize()}.mp3")
        if os.path.exists(audio_path):
            os.remove(audio_path)  # Delete the corresponding audio file

        word.delete()  # Delete the word record from the database

        return JsonResponse({
            "status": "success",
            "message": "Word and related files deleted successfully"
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        })