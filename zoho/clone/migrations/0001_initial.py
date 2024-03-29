# Generated by Django 4.0.5 on 2022-06-14 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('emp_cnt', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='emp_personal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(blank=True, max_length=10)),
                ('email', models.CharField(blank=True, help_text='Employee personal email id', max_length=100)),
                ('birth_date', models.DateField()),
                ('martial_status', models.CharField(choices=[('single', 'Single'), ('married', 'Married')], max_length=100)),
                ('communication_add', models.TextField()),
                ('permanent_add', models.TextField()),
                ('postal_code', models.CharField(blank=True, max_length=6)),
                ('pan_no', models.CharField(blank=True, max_length=11)),
                ('aadhar_no', models.CharField(blank=True, max_length=20)),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female')], max_length=10)),
                ('hiring_src', models.CharField(blank=True, choices=[('campus drive', 'Campus Drive'), ('off campus drive', 'Off Campus Drive'), ('emp referal', 'Employee Referal'), ('online application', 'Online Application')], max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='harshit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Harshit', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='leave_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('paid', 'Paid Leave'), ('unpaid', 'Leave without pay')], help_text='Leave name', max_length=255, unique=True)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Leave Type',
            },
        ),
        migrations.CreateModel(
            name='leaves_create_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('cnt_leave', models.IntegerField(default=0)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('reason', models.TextField(max_length=500)),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clone.leave_type')),
            ],
            options={
                'verbose_name_plural': 'Create Leave',
            },
        ),
        migrations.CreateModel(
            name='LeavesAndHolidays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curr_avail_paid_leave', models.IntegerField(default=0, help_text='Currently available paid leaves')),
                ('curr_booked_paid_leave', models.IntegerField(default=0, help_text='Currently booked paid leave')),
                ('curr_booked_unpaid_leave', models.IntegerField(default=0, verbose_name='Currently booked unpaid leave')),
                ('hrm_id', models.CharField(blank=True, help_text='Employee HRM ID', max_length=255, null=True)),
                ('is_leave_approved', models.BooleanField(default=False, help_text='Set to True whenever Reporting manager of the employee approve the leave. By default it is True')),
                ('leave_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clone.leaves_create_model')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Leaves and Holiday',
            },
        ),
        migrations.CreateModel(
            name='emp_self',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hrm_id', models.CharField(blank=True, max_length=100)),
                ('office_loc', models.CharField(choices=[('jaipur', 'Jaipur'), ('noida', 'Noida'), ('ajmer', 'Ajmer'), ('jodhpur', 'Jodhupur'), ('pune', 'Pune'), ('gurgaon', 'Gurgaon'), ('ahmedabad', 'Ahmedabad'), ('remote', 'Remote')], default='jaipur', max_length=255)),
                ('position', models.CharField(choices=[('associate', 'Associate'), ('jr associate', 'Junior Associate'), ('consultant', 'Consultant'), ('sr consultant', 'Senior Consultant'), ('hr', 'H.R'), ('engineer', 'Engineer'), ('analyst', 'Analyst')], max_length=255)),
                ('type', models.CharField(choices=[('3', 'Intern'), ('2', 'Trainee'), ('1', 'General')], max_length=255)),
                ('status', models.CharField(choices=[('active', 'Active'), ('notice', 'Notice Period')], max_length=100)),
                ('joining_date', models.DateTimeField()),
                ('working_status', models.CharField(blank=True, choices=[('WFH', 'Working from home'), ('WFO', 'Working from office'), ('hybrid', 'Working Hybrid')], max_length=100)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clone.department')),
                ('personal', models.ForeignKey(help_text='Employee Personal Data', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personal_data', to='clone.emp_personal')),
                ('rm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporting_manager_id', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'employee info',
            },
        ),
    ]
