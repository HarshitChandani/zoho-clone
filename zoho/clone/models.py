# Django
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Local imports
from .services.choices import (
   martial_status,
   positions,
   emp_type,
   off_loc,
   emp_status,
   genders,
   working_status,
   hiring_sources,
   leave_type
)


def create_hrm(instance,**kwargs):
   """Function will create a new HRM id of new joinee

      Foramt: department id + month of join + employee id 
   Args:
       instance (_type_): instance of newly created record
   """
   dept_id = instance.dept.id
   join_month = instance.joining_date.strftime('%m')
   emp_id = instance.id
   hrm_id = "HRM{}{}{}".format(dept_id,join_month,emp_id)
   return hrm_id

class Department(models.Model):
   name = models.CharField(max_length=255,null=False,blank=True)
   emp_cnt = models.IntegerField(null=False,blank=False,default=0) 

class EmpPersonal(models.Model):
   """
      Class stores all the personal data of the employee
   """
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   no = models.CharField(max_length=10,null=False,blank=True)
   email=models.EmailField(max_length=254,help_text='Employee personal email id',null=False,blank=True)
   birth_date = models.DateField()
   martial_status = models.CharField(max_length=100,choices=martial_status)
   communication_add = models.TextField()
   permanent_add = models.TextField()
   postal_code = models.CharField(max_length=6,null=False,blank=True)
   pan_no = models.CharField(max_length=11,null=False,blank=True)
   aadhar_no = models.CharField(max_length=20,null=False,blank=True)
   gender = models.CharField(max_length=10,null=False,blank=True,choices=genders)
   hiring_src = models.CharField(max_length=100,null=False,blank=True,choices=hiring_sources)

   def str(self):
      return self.user
   
class EmpSelf(models.Model):
   """
      Class contains all the employee data in one class.
   """
   user = models.ForeignKey(User,related_name="employee_id",on_delete=models.CASCADE)
   dept = models.ForeignKey(Department,on_delete=models.CASCADE)
   rm = models.ForeignKey(User,related_name='reporting_manager_id',on_delete=models.CASCADE)
   personal = models.ForeignKey(EmpPersonal,related_name='personal_data',on_delete=models.CASCADE,null=True,help_text="Employee Personal Data")
   hrm_id = models.CharField(max_length=100,null=False,blank=True)
   office_loc = models.CharField(max_length=255,default='jaipur',choices=off_loc)
   position = models.CharField(max_length=255,choices=positions)
   type = models.CharField(max_length=255,choices=emp_type)
   status = models.CharField(max_length=100,choices=emp_status)
   joining_date = models.DateTimeField()
   working_status = models.CharField(max_length=100,null=False,blank=True,choices=working_status)

   class Meta:
      verbose_name_plural = 'employee info'

class LeaveType(models.Model):
   name = models.CharField(max_length=255,help_text="Leave name",choices = leave_type,unique=True)
   timestamp = models.DateTimeField()

   class Meta:
      verbose_name_plural = 'Leave Type'

   def str(self):
      return self.name

class LeavesCreateModel(models.Model):
   """
   Whenever user apply for the leave the details will be recorded in this model.
   """
   title = models.CharField(max_length=100,null=True,blank=True)
   leave_type = models.ForeignKey(LeaveType,on_delete=models.CASCADE)
   cnt_leave = models.IntegerField(null=False,default=0)
   from_date = models.DateField()
   to_date = models.DateField()
   reason = models.TextField(max_length=500)

   class Meta:
      verbose_name_plural = 'Create Leave'

   def save(self,*args,**kwargs):
      self.cnt_leave = count_leave_days(self)
      return super(LeavesCreateModel,self).save(**kwargs)

class LeavesAndHolidays(models.Model):
   """
   This model will record all the leave details of user.
   The records in this table will be inserted by the admin of the zoho.
      As admin has the right to decide the available paid leaves to the employee.
   """
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   leave_id = models.ForeignKey(LeavesCreateModel,on_delete=models.CASCADE,null=True,blank=True)
   curr_avail_paid_leave  = models.IntegerField(help_text="Currently available paid leaves",default=0,null=False)
   curr_booked_paid_leave = models.IntegerField(help_text="Currently booked paid leave",default=0,null=False) 
   curr_booked_unpaid_leave = models.IntegerField("Currently booked unpaid leave",default=0,null=False)
   hrm_id = models.CharField(max_length=255,help_text="Employee HRM ID",null=True,blank=True)
   is_leave_approved = models.BooleanField(help_text="Set to True whenever Reporting manager of the employee approve the leave. By default it is True",default=False)
   
   class Meta:
      verbose_name_plural = "Leaves and Holiday"

class Attendence(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   date = models.DateField()
   checkin_time = models.TimeField(auto_now=False)
   checkout_time = models.TimeField(auto_now=False)
   ttl_work_time = models.TimeField(auto_now=False)
   

class TimeTracker(models.Model):
   date = models.DateField()
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   jobs = models.TextField()
   ttl_hours = models.CharField(max_length = 50,null=False,blank=True)


######## Function & Signals
def count_leave_days(instance):
   from_day,from_month = int(instance.from_date.strftime("%d")),int(instance.from_date.strftime("%m"))
   to_day,to_month = int(instance.to_date.strftime("%d")),int(instance.from_date.strftime("%m"))
   if from_month == to_month:
      diff = to_day - from_day
   else:
      pass
   return (diff+1)
   

@receiver(post_save,sender=EmpSelf)
def process_emp(sender,instance,created,**kwargs):
   if created:
      hrm_id = create_hrm(instance)
      emp_id = instance.id
      EmpSelf.objects.filter(id = emp_id).update(hrm_id=hrm_id)

      
     
