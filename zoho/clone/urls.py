from django.urls import path
from django.views.generic import TemplateView

# View Class
from clone.views import (
   LoginView,
   CreateLeaveView,
   TimeTrackerView,
   AttendenceView
)

# View Function 
from clone.views import (
   self_service,
   leave_tracker,
   home,
   daily_log
)

app_name = 'zoho'

urlpatterns = [
   path('',LoginView.as_view(),name="main"),    
   path('home/<str:hrmportalid>',home,name='home'),
   path('self/',self_service,name="self"),
   path('login/',LoginView.as_view(),name="login"),
   path('leave-tracker/',leave_tracker,name="leaver-tracker"),
   path('apply-leave/',CreateLeaveView.as_view(),name="apply-leave"),
   path('time-tracker/',TimeTrackerView.as_view(),name="time-tracker"),
   path('attendence/',AttendenceView.as_view(),name="attendence"),
   path('daily-log/',daily_log,name="daily-log")   
]

