# Standard Library
from datetime import datetime
import json

# Local imports
from clone.models import (
   TimeTracker as time_tracker
)


def save_timesheet_data(request,data:dict,**kwargs):
   
   get_date = data["date"]
   data.pop('date')
   ttl_work_hrs = kwargs["total_work_hrs"]
   
   # If timesheet is already saved then update that timesheet
   if time_tracker.objects.filter(date=get_date).exists():
      time_tracker.objects.filter(date=get_date).update(
         jobs = json.dumps(data),
         ttl_hours = ttl_work_hrs
      )
      return True
   # If timesheet data is new then create a new record.
   else:
      create_timesheet = time_tracker.objects.create(
         date= get_date,
         user = request.user,
         jobs = json.dumps(data),
         ttl_hours = ttl_work_hrs
      )
      return True

def get_all_time_sheet_data(request):
   time_tracker.objects.filter(user = request.user).order_by('-date').all()
   

def get_date_time_log(request,*args,**kwargs):
   log_date = kwargs.get('log_date')
   timesheet_data = time_tracker.objects.filter(user=request.user,date=log_date) 
   if timesheet_data.exists():
      
      # TimeSheet data already in the Database
      data = timesheet_data.values('jobs','ttl_hours')[0]
      response = {
         'job_data': json.loads(data["jobs"]),
         'ttl_work_hours':data["ttl_hours"]
      }
      return response
   else:
      # Data not existed
      return None 