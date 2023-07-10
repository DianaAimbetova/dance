from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('enroll-class/', views.StudentEnrollClassView.as_view(), name='student_enroll_class'),
    path('course/<pk>/', views.StudentClassDetailView.as_view(), name='student_class_detail'),
    path('', views.ClassListView.as_view(), name='class'),
    path('create/', views.ClassCreateUpdateView.as_view(), name='class_create'),
    path('<slug:slug>/', views.ClassDetailView.as_view(), name='class_detail'),
    path('edit/<id>/', views.ClassCreateUpdateView.as_view(), name='class_update'),
    
    
]