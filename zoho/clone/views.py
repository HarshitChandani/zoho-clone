# Standard Library
from datetime import ( 
   datetime, 
   timedelta 
)
import datetime as dt
import json  
from sortedcontainers import SortedDict

# Django
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.views import View
from django.core import serializers
from django.contrib.auth import authenticate, login,logout
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
from .services.attendence import Attendence
from .services.self_service import emp_self_data
from .services.service_function import get_dates_ranges

@login_required(login_url='/login/')
def home(request):
   return render(request,'home.html')

def self_service(request):
   if request.method == "GET":
      context = emp_self_data(request)
      return render(request,'self.html',context)

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
            return JsonResponse({
               'recorded':True})

class AttendenceView(View):
   
   def __init__(self) -> None:
      self.attendence = Attendence()

   def post(self,request):
      action = request.POST.get('action')
      if action == 'in':
         data = {
            'date': request.POST.get('date'),
            'checkin': request.POST.get('checkin'),
            'action': action
         }
         is_checked_in = self.attendence.record_checkin(request.user,data)
         return is_checked_in
      else:
         data = {
            'checkout': request.POST.get('checkout'),
            'action':action,
            'record_id':request.POST.get('record_id'),
            'attendence_id':request.POST.get('attendence_id'),
            'ttl_work_hrs':request.POST.get('ttl_work_hrs'),
         }
         is_checked_out = self.attendence.record_checkout(data)
         return is_checked_out
   
   def get(self,request):
      # MONDAY TO SUNDAY
      total_hrs_dict = dict()
      swd = request.GET.get('startWeek',None)
      ewd = request.GET.get('endWeek',None)
      navigation = request.GET.get('nav',None)
      if swd is not None and ewd is not None:
         if navigation == "-1":
            startWeekDate = ( datetime.strptime(swd,"%d-%m-%Y") - timedelta(days = 7) ).date()
            endWeekDate = startWeekDate + timedelta(days = 6)
            
         else:
            startWeekDate = ( datetime.strptime(swd,"%d-%m-%Y") + timedelta(days = 7) ).date()
            endWeekDate = startWeekDate + timedelta(days = 6)
            
      else:
         curr_date = datetime.now().date()
         weekDay = curr_date.weekday()
         startWeekDate = curr_date - timedelta(days = weekDay)
         endWeekDate = startWeekDate + timedelta(days = 6)
         
      _startWeekDate = datetime.strftime(startWeekDate,"%d-%m-%Y")
      _endWeekDate = datetime.strftime(endWeekDate,"%d-%m-%Y")

      date_ranges = get_dates_ranges(startWeekDate)
      weekAttendenceData = self.attendence.get_attendence_by_weak(request.user,_startWeekDate,_endWeekDate) 

      for data in weekAttendenceData:
         date = data.attendence.date
         total_hrs = data.total_hours
         if date in total_hrs_dict.keys():
            hrs = total_hrs_dict[date]["total_hours"]
            total_hrs = (
                  datetime.combine(dt.date(1,1,1),hrs) + timedelta(hours=total_hrs.hour,minutes=total_hrs.minute,seconds=total_hrs.second)).time()

         total_hrs_dict[date] = {
            'total_hours':total_hrs,
            'attendence_id': data.attendence.id,
            'attendence_record_id':data.id 
         }
      
      remaining_dates = (date_ranges - total_hrs_dict.keys())

      final_attendence_data = SortedDict({
            **total_hrs_dict,
            **dict.fromkeys(
                  remaining_dates,{
                     'total_hours':datetime.strptime("00:00:00","%H:%M:%S"),
                     'attendence_id':"",
                     'attendence_record_id':""
                  }
               )
         })
      
      context = {
         'startWeekDate': _startWeekDate,
         'endWeekDate':_endWeekDate, 
         'data_dict':final_attendence_data
      }

      return render(request,"attendence.html",context)

def attendence_data(request):
   attendence = Attendence()
   attendence_id = request.GET.get('attendence_id',None)
   if attendence_id is not None:
      query_set = attendence.get_attendence_by_id(attendence_id)
      return JsonResponse(serializers.serialize('json',query_set),safe=False)
   else:
      return HttpResponse(None,content_type='text/plain')