from django.urls import path

from clone.views import (
   home,
   loginView,
   # self_service,
   # leave_tracker,
   # CreateLeaveView
)

app_name = 'zoho'

urlpatterns = [
   path('',loginView.as_view(),name="main"),    
   # path('home/<str:hrmportalid>',home,name='home'),
   # path('self/',self_service,name="self"),
   # path('login/',loginView.as_view(),name="login"),
   # path('leave-tracker/',leave_tracker,name="leaver-tracker"),
   # path('apply-leave/',CreateLeaveView.as_view(),name="apply-leave")
]

