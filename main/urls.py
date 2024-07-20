from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('portal/login', views.login_view, name='login'),
    path('portal/logout', views.logout_view, name='logout'),
    path('<slug:slug>', views.semester_details, name='semester_details'),
    path('subjects/<slug:slug>', views.subject_details, name='subject_details'),
    path('chapters/<slug:slug>', views.chapter_details, name='chapter_details'),
    path('assignments/<slug:slug>', views.assignment_details, name='assignment_details'),
    path('assignments/view_assignments/<slug:slug>', views.all_assignment_view, name='all_assignments'),
    path('assignments/user_assignents/', views.user_assignments, name='user_assignments'),
    path('submit/success', views.success, name='success')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)