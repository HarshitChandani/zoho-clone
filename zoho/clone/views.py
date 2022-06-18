# Standard Library
from datetime import datetime,date
import json

# Django
from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User

# Local Imports
from .models import (
   EmpSelf as employee,
   LeaveType as l_type,
   LeavesCreateModel as apply_leave,
   LeavesAndHolidays as leaves_and_holidays
) 
from .services.time_tracker import (
   save_timesheet_data,
   get_all_time_sheet_data,
   get_date_time_log
)
from .services.attendence import record_attendence
from .services.self_service import emp_self_data


def home(request,hrmportalid:str):
   return render(request,'home.html')

def self_service(request):
   if request.method == "GET":
      hrm_id = request.session["employee_hrm_id"]
      context = emp_self_data(request,hrm_id = hrm_id)
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
      if user is not None:
         login(request, user)
         emp_details = employee.objects.filter(id=request.user.id).get()
         request.session['employee_hrm_id'] = emp_details.hrm_id
         return redirect('zoho:home',hrmportalid = emp_details.hrm_id)
      else:
         # messages.error(request,"Invalid Credentials")
         return redirect("zoho:login")

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

      hrm_id = request.POST.get('hrm_id')

      # leave create process
      leave_type = request.POST.get('leave_type')
      reason = request.POST.get('leave-reason')

      parsed_from_date = datetime.strptime(request.POST.get('from-date'),"%Y-%m-%d")
      parsed_to_date = datetime.strptime(request.POST.get('to-date'),"%Y-%m-%d") 
      
      last_leave_app = leaves_and_holidays.objects.filter(user=request.user).order_by("-id")[0]
      get_last_leave_app_data = leaves_and_holidays.objects.get(id=last_leave_app.id)
      cnt_leave_taken = ( parsed_to_date.day - parsed_from_date.day + 1 ) 
         
      if leave_type == "1": # paid leave
         
         get_aval_paid_leave = get_last_leave_app_data.curr_avail_paid_leave
         
         if cnt_leave_taken > get_aval_paid_leave:
            # Not enough paid leave balance
            messages.add_message(request,messages.error,"Not enough paid leave balance available.")

         elif (cnt_leave_taken < get_aval_paid_leave) or (cnt_leave_taken == get_aval_paid_leave):
            # employee has enough balance to apply for paid leave 
            
            create_leave = apply_leave.objects.create(
               leave_type = l_type.objects.get(id=leave_type),
               title = None,
               from_date = parsed_from_date,
               to_date = parsed_to_date,
               reason = reason
            )
            leave_id = create_leave.id
            create_leave.save()
            print("Paid Leave Created")
            remaining_paid_leave_balance = get_aval_paid_leave - cnt_leave_taken
            create_leave_record = leaves_and_holidays.objects.create(
               user = request.user,
               leave_id = apply_leave.objects.get(id=leave_id),
               curr_avail_paid_leave = remaining_paid_leave_balance,
               curr_booked_paid_leave =get_last_leave_app_data.curr_booked_paid_leave  + cnt_leave_taken,
               curr_booked_unpaid_leave = get_last_leave_app_data.curr_booked_paid_leave,
               hrm_id = hrm_id
            )
            create_leave_record.save()
            print("Leave application successfully created.")
            messages.add_message(request,messages.SUCCESS,"Leave application successfully created.")

      elif leave_type == "2": #unpaid leave
            create_leave = apply_leave.objects.create(
               leave_type = l_type.objects.get(id=leave_type),
               title = None,
               from_date = parsed_from_date,
               to_date = parsed_to_date,
               reason = reason
            )
            leave_id = create_leave.id
            create_leave.save()
            print("UnPaid Leave Created")

            create_leave_record = leaves_and_holidays.objects.create(
               user = request.user,
               leave_id = apply_leave.objects.get(id=leave_id),
               curr_avail_paid_leave = get_last_leave_app_data.curr_avail_paid_leave,
               curr_booked_paid_leave = get_last_leave_app_data.curr_booked_paid_leave,
               curr_booked_unpaid_leave = get_last_leave_app_data.curr_booked_unpaid_leave + cnt_leave_taken,
               hrm_id = hrm_id
            )
         
            create_leave_record.save()
            print("UnPaid leave Application successfully created.")
            messages.add_message(request,messages.SUCCESS,"Leave application successfully created.")

      return redirect("zoho:leaver-tracker")
      
class TimeTrackerView(View):
   def get(self, request):
      get_all_time_sheet_data(request)
      return render(request,"time-tracker.html")
      
   def post(self, request):
      timesheet_data = request.POST.get("data",None)
      if timesheet_data != None:
         job_dict = json.loads(timesheet_data)
         if save_timesheet_data(request,job_dict):
            print("data created")
            return HttpResponse(json.dumps({
               'recorded':True,}),
               content_type="application/json")

def daily_log(request):
   _date = datetime.now().date()
   data = get_date_time_log(request,log_date=_date)
   if data is not None:
      context = {
         'time_log_data':data
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

