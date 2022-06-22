# Standard Library
from datetime import datetime

# Local Imports
from clone.models import (
   LeavesCreateModel as apply_leave,
   LeavesAndHolidays as leaves_and_holidays,
   LeaveType as l_type
)


class Leave:
   
   def apply_leave(self,request,**kwargs):
      leave_type = request.POST.get('leave_type')
      reason = request.POST.get('leave-reason')

      parsed_from_date = datetime.strptime(request.POST.get('from-date'),"%Y-%m-%d")
      parsed_to_date = datetime.strptime(request.POST.get('to-date'),"%Y-%m-%d") 
      
      last_leave_app = leaves_and_holidays.objects.filter(user=request.user).order_by("-id")[0]
      get_last_leave_app_data = leaves_and_holidays.objects.get(id=last_leave_app.id)
      cnt_leave_taken = ( parsed_to_date.day - parsed_from_date.day + 1 ) 
      get_aval_paid_leave = get_last_leave_app_data.curr_avail_paid_leave
                  
      if leave_type == "1": # paid leave
         

         is_paid_leave_created = self.create_paid_leave(
            request.user,
            get_aval_paid_leave,
            cnt_leave_taken,
            leave_type,
            from_date = parsed_from_date,
            to_date=parsed_to_date,
            reason=reason,
            booked_leave=get_last_leave_app_data.curr_booked_paid_leave)
         return is_paid_leave_created
         
      elif leave_type == "2": #unpaid leave
            is_unpaid_leave_created = self.create_unpaid_leave(
               request.user,
               get_aval_paid_leave,
               cnt_leave_taken,
               leave_type,
               booked_paid_leave = get_last_leave_app_data.curr_booked_paid_leave, 
               booked_unpaid_leave = get_last_leave_app_data.curr_booked_unpaid_leave,
               from_date = parsed_from_date,
               to_date = parsed_to_date,
               reason = reason
            )
            return is_unpaid_leave_created

   def create_paid_leave(self,user,available_leave,leave_taken,leave_type,**kwargs):
         if leave_taken > available_leave:
            print("Not enough paid leave balance available.")
            # Not enough paid leave balance
            return False

         elif (leave_taken < available_leave) or (leave_taken == available_leave):
            # employee has enough balance to apply for paid leave 
            
            create_leave = apply_leave.objects.create(
               leave_type = l_type.objects.get(id=leave_type),
               title = None,
               from_date = kwargs["from_date"],
               to_date = kwargs["to_date"],
               reason = kwargs["reason"]
            )
            leave_id = create_leave.id
            create_leave.save()
            print("Paid Leave Created")
            remaining_paid_leave_balance = available_leave - leave_taken
            create_leave_record = leaves_and_holidays.objects.create(
               user = user,
               leave_id = apply_leave.objects.get(id=leave_id),
               curr_avail_paid_leave = remaining_paid_leave_balance,
               curr_booked_paid_leave =kwargs["booked_leave"]  + leave_taken,
               curr_booked_unpaid_leave = kwargs["curr_booked_paid_leave"]
            )
            create_leave_record.save()
            return (True if create_leave_record.id is not None else False)
   
   def create_unpaid_leave(self,user,available_leave,leave_taken,leave_type,**kwargs):
         create_leave = apply_leave.objects.create(
               leave_type = l_type.objects.get(id=leave_type),
               title = None,
               from_date = kwargs["from_date"],
               to_date = kwargs["to_date"],
               reason = kwargs["reason"]
            )
         leave_id = create_leave.id
         create_leave.save()
         print("UnPaid Leave Created")

         create_leave_record = leaves_and_holidays.objects.create(
            user = user,
            leave_id = apply_leave.objects.get(id=leave_id),
            curr_avail_paid_leave = available_leave,
            curr_booked_paid_leave = kwargs["booked_paid_leave"],
            curr_booked_unpaid_leave = kwargs["booked_unpaid_leave"] + leave_taken
         )
         create_leave_record.save()
         return (True if create_leave_record.id is not None else False)