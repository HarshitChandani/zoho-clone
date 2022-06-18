# Standard Library
from datetime import datetime
import json

# Local imports
from ..models import (
   TimeTracker as time_tracker
)

def save_timesheet_data(request,data:dict):
   
   get_date = data["date"]
   data.pop('date')

   # If timesheet is already saved then update that timesheet
   if time_tracker.objects.filter(date=get_date).exists():
      time_tracker.objects.filter(date=get_date).update(
         jobs = json.dumps(data)
      ) 
      return True
   # If timesheet data is new then create a new record.
   else:
      create_timesheet = time_tracker.objects.create(
         date= get_date,
         user = request.user,
         jobs = json.dumps(data)
      )
      return True

def get_all_time_sheet_data(request):
   time_tracker.objects.filter(user = request.user).order_by('-date').all()
   

def get_date_time_log(request,*args,**kwargs):
   log_date = kwargs.get('log_date')
   timesheet_data = time_tracker.objects.filter(user=request.user,date=log_date) 
   if timesheet_data.exists():
      
      # TimeSheet data already in the Database
      data = timesheet_data.values('jobs')[0]
      return json.loads(data["jobs"])
   else:
      # Data not existed
      return None 