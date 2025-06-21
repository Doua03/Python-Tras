from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('services/', views.services, name='services'), 
    path('home/', views.home, name='home'), 
    path('authentification/', views.authentification, name='authentification'),
    path('login/', views.login_view, name='login'),
    path('contact/', views.contact, name='contact'),   
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('activities/', views.activities, name='activities'),
    path('consultation/', views.consultation, name='consultation'),
    path('book_consultation/', views.book_consultation, name='book_consultation'),
    path('service/', views.mainservices, name='mainservices'), 
    path('contacts/', views.maincontact, name='maincontact'),
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('doctor/list/', views.doctor_list, name='doctor_list'),
    path('doctor/modify/<int:id>/', views.modify_doctor, name='modify_doctor'),
    path('doctor/delete/<int:id>/', views.delete_doctor, name='delete_doctor'),
    path('detect-expression/', views.facial_expression_view, name='facial_expression'),
    path('check_expression/', views.check_expression, name='check_expression'),
    path('get-word/', views.get_word, name='get_word'),
    path('speak-word/', views.speak_word, name='speak_word'),
    path('assess-pronunciation/', views.assess_pronunciation, name='assess_pronunciation'),
    path('pronunciation/', views.pronunciation_view, name='pronunciation'),
  
    path('story/<int:story_id>/check_answer/', views.check_answer, name='check_answer'),
    path('audio/<str:filename>/', views.serve_audio, name='serve_audio'),  # Servir les fichiers audio
     #Stories management
  #Stories management
    path('stories/', views.stories, name='stories'),
    path('stories/<int:story_id>/', views.story_detail, name='story_detail'),
    path('manage_stories/', views.manage_stories, name='manage_stories'),
    path('add-story/', views.add_story, name='add_story'),
    path('update-story/<int:story_id>/', views.update_story, name='update_story'),
    path('delete-story/<int:story_id>/', views.delete_story, name='delete_story'),
    # PRONUNCIATION MANAGEMENT
    path('manage_words/', views.manage_words, name='manage_words'),
    path('words/', views.get_words, name='get_words'),
    path('words/add/', views.add_word, name='add_word'),
    path('words/edit/<int:word_id>/', views.edit_word, name='edit_word'),
    path('words/delete/<int:word_id>/', views.delete_word, name='delete_word'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
