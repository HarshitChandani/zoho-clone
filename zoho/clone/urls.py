### Local Imports
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
   daily_log,
   attendence_data
)

# Django Imports
from django.urls import path


app_name = 'zoho'

urlpatterns = [
   path('',LoginView.as_view(),name="main"),    
   path('home/',home,name='home'),
   path('self/',self_service,name="self"),
   path('login/',LoginView.as_view(),name="login"),
   path('leave-tracker/',leave_tracker,name="leaver-tracker"),
   path('apply-leave/',CreateLeaveView.as_view(),name="apply-leave"),
   path('time-tracker/',TimeTrackerView.as_view(),name="time-tracker"),
   path('daily-log/',daily_log,name="daily-log"),
   path('attendence/',AttendenceView.as_view(),name="attendence"), # POST
   path('attendence/data/listview/',AttendenceView.as_view(),name='attendence-list-view'),
   path('attendence-by-date/',attendence_data,name="attendence-by-date")

]