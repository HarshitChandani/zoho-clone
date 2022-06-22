# Standard Library
from datetime import datetime
import json

# Django
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Local Imports
from .models import (
   LeaveType as l_type,
   LeavesAndHolidays as leaves_and_holidays
) 
from .services.time_tracker import (
   save_timesheet_data,
   get_all_time_sheet_data,
   get_date_time_log
)
from .services.leave_tracker import apply_leave
from .services.attendence import record_attendence
from .services.self_service import emp_self_data


@login_required(login_url='/login/')
def home(request):
   return render(request,'home.html')

def self_service(request):
   if request.method == "GET":
      context = emp_self_data(request)
      return render(request,'self.html',context)

class LoginView(View):
   def get(self,request):
      if request.user.is_authenticated:
         logout(request)
      return render(request,'login.html')

   def post(self, request):
      loginUsername = request.POST.get('username')
      loginPassword =  request.POST.get('password')
      user = authenticate(username=loginUsername, password=loginPassword)
      if user is None:
         return render(request,'login.html',status=401)
      else:
         login(request,user)
         return redirect('zoho:home')

def leave_tracker(request):
   get_emp_leave_status = leaves_and_holidays.objects.filter(user=request.user).order_by("-id")[0]
   
   leave_history_data = leaves_and_holidays.objects \
                     .select_related('leave_id') \
                     .filter(user=request.user) \
                     .order_by('-leave_id__from_date','-leave_id__to_date') \
                     .all()

   context = {
      'available_paid_leave' : get_emp_leave_status.curr_avail_paid_leave,
      'booked_paid_leave': get_emp_leave_status.curr_booked_paid_leave,
      'booked_unpaid_leave':get_emp_leave_status.curr_booked_unpaid_leave,
      'all_leave_data': leave_history_data
   }
   return render(request,"leave-tracker.html",context)


class CreateLeaveView(View):
   
   def get(self, request):
      get_leave_type = l_type.objects.only('name','id')
      context = {
         'leave_type':get_leave_type
      }
      return render(request,'create-leave.html',context)

   def post(self, request):

      # leave create process
      is_leave_created = apply_leave(request)
      print(is_leave_created)
      print("Leave application successful" if is_leave_created else "Leave application failed")    
      return redirect("zoho:leaver-tracker")


class TimeTrackerView(View):
   def get(self, request):
      get_all_time_sheet_data(request)
      return render(request,"time-tracker.html")
      
   def post(self, request):
      timesheet_data = request.POST.get("job_data")
      ttl_work_hr = request.POST.get('ttl_work_hr')
      if timesheet_data != None:
         job_dict = json.loads(timesheet_data)
         if save_timesheet_data(request,job_dict,total_work_hrs = ttl_work_hr):
            print("data created")
            return HttpResponse(json.dumps({
               'recorded':True,}),
               content_type="application/json")

def daily_log(request):
   _date = datetime.now().date()
   data = get_date_time_log(request,log_date=_date)
   
   if data is not None:
      context = {
         'time_log_data':data["job_data"],   
         'ttl_work_hrs':data["ttl_work_hours"]
      }   
   else:
      context = {
         'time_log_data':None
      }
   return render(request,'day_log.html',context)


class AttendenceView(View):
   def get(self, request):
     pass
   
   def post(self, request):
       return record_attendence(request)

