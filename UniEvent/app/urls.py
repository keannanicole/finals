from django.urls import path
from . import views

urlpatterns = [
    # Ensure the name matches what you use in redirect()
    path('', views.event_dashboard, name='event_dashboard'),
    path('add-time/<int:event_id>/', views.add_extra_schedule, name='add_extra_schedule'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]