# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/attend/', views.attend_event, name='attend_event'),

    path('profile/<str:username>/', views.user_profile, name='view_profile'),
    path('profile/', views.user_profile, name='user_profile'),  

    path('signup/', views.signup, name='signup'),
    # Login/Logout จัดการใน myproject/urls.py

    path('quiz/', views.butterfly_quiz_view, name='butterfly_quiz'),
    path('quiz/result/<slug:slug>/', views.butterfly_result_view, name='butterfly_result_page_slug'),

    path('dashboard/', views.dashboard_page, name='dashboard'), # ตรวจสอบว่ามี view นี้จริง
]