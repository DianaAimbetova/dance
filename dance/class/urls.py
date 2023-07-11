from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('enroll-class/', views.StudentEnrollClassView.as_view(), name='student_enroll_class'),
    path('course/<pk>/', views.StudentClassDetailView.as_view(), name='student_class_detail'),
    path('', views.ClassListView.as_view(), name='class'),
    path('favourite/', views.FavouriteClassListView.as_view(), name='favourite_class'),
    path('create/', views.ClassCreateUpdateView.as_view(), name='class_create'),
    path('<slug:slug>/', views.ClassDetailView.as_view(), name='class_detail'),
    path('edit/<id>/', views.ClassCreateUpdateView.as_view(), name='class_update'),
    path('remove', views.remove_class, name='class_remove'),
    path('like', views.class_like, name='class_like'),
    path('enrolled', views.EnrolledClassListView.as_view(), name='class_enrolled'),
    
    
]