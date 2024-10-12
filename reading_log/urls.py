from django.urls import path
from . import views

app_name = 'reading_log'

urlpatterns = [
    #path('', views.ReadingLogList.as_view(), name='reading_log_list'),
    path('', views.UserGuide.as_view(), name='user_guide'),
    path('book_create', views.BookCreate.as_view(), name='book_create'),
    path('reading_log_create', views.ReadingLogCreate.as_view(), name='reading_log_create'),
    path('reading_log_update/<int:pk>', views.ReadingLogUpdate.as_view(), name='reading_log_update'),
    path('reading_log_delete/<int:pk>', views.ReadingLogDelete.as_view(), name='reading_log_delete'),
    path('individual_log/<int:user_id>', views.IndividualLog.as_view(), name='individual_log'),
    path('dashboard/<int:user_id>', views.Dashboard.as_view(), name='dashboard'),
]
