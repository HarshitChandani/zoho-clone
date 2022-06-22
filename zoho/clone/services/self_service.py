# Local import
from clone.models import EmpSelf as employee


def emp_self_data(request,**kwargs):
      working_status_dict = {
            'WFH':'work from home',
            'WFO':'work from office',
            'hybrid':'working hybrid'
         }
      emp_data = employee.objects \
                        .select_related('dept','personal','rm') \
                        .get(user=request.user)
      response = {
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
            'office_mail':request.user.email,
            'joining_date':emp_data.joining_date,
            'status':emp_data.status,
            'working_status':working_status_dict[emp_data.working_status]
         },
      }
      return response