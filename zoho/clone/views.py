# Standard Library
from datetime import datetime

# Django
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User

# Local Django
from .models import (
   EmpEelf as employee,
   LeaveType as l_type,
   LeavesCreateModel as apply_leave,
   LeavesAndHolidays as leaves_and_holidays
) 


def home(request,hrmportalid:str):
   return render(request,'home.html')

def self_service(request):
   if request.method == "GET":
      hrm_id = request.session["employee_hrm_id"]
      working_status_dict = {
         'WFH':'work from home',
         'WFO':'work from office',
         'hybrid':'working hybrid'
      }
      emp_data = employee.objects \
                        .select_related('dept','personal','rm') \
                        .get(hrm_id=hrm_id)
      context = {
         'zoho':{
            'index':['about_me','personal','work']
         },
         'about_me':{
            'department':emp_data.dept.name,
            'position':emp_data.position,
            'location':emp_data.office_loc,
            'type':emp_data.type,
         },
         'personal':{
            'name':"{} {}".format(request.user.first_name,request.user.last_name),
            'f_name':request.user.first_name,
            'l_name':request.user.last_name,
            'gender':emp_data.personal.gender,
            'no':emp_data.personal.no,
            'mail': emp_data.personal.email,
            'birth_date':emp_data.personal.birth_date,
            'martial_status':emp_data.personal.martial_status,
            'comm_addr':emp_data.personal.communication_add,
            'permanent_add':emp_data.personal.permanent_add,
            'postal_code':emp_data.personal.postal_code,
            'pan_no':emp_data.personal.pan_no,
            'aadhar_no':emp_data.personal.aadhar_no,
            'hiring_source':emp_data.personal.hiring_src
         },
         'work':{
            'reporting_manager':"{} {}".format(emp_data.rm.first_name,emp_data.rm.last_name),
            'hrm_id':hrm_id,
            'office_mail':request.user.email,
            'joining_date':emp_data.joining_date,
            'status':emp_data.status,
            'working_status':working_status_dict[emp_data.working_status]
         },

      }
      return render(request,'self.html',context)

class loginView(View):
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
      return render(request,'components/create-leave.html',context)

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
      
      """ 
         create messages 
      """

      