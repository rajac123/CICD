from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
from django.utils.timezone import now
from django_jsonfield_backport.models import JSONField
# Create your models here.

# employee register
class EmployeesMaster(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_n_key = models.CharField(max_length=30,blank=True,unique=True)
    hospital_short_name = models.CharField(max_length=30, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    clinical_n_key = models.CharField(max_length=30,blank=True,null=True)
    is_new_user = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    designation = models.TextField(blank=True, null=True)
    prefix = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=100)
    user_id = models.IntegerField(blank=True, null=True)
    profile_summary = models.TextField(blank=True, null=True)
    languages_known =models.TextField(blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=30, blank=True, null=True)
    emergency_person_name = models.CharField(max_length=30, blank=True, null=True)
    emergency_contact_no = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    dial_code = models.CharField(max_length=15, blank=True, null=True)
    phone_number = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    user_name = models.CharField(max_length=45, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    role = models.CharField(max_length=30, blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)
    bloodbank = models.CharField(max_length=5, blank=True, null=True)
    g_ehr = models.CharField(max_length=5, blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    facebook_link = models.TextField(blank=True, null=True)
    instagram_link = models.TextField(blank=True, null=True)
    twitter_link = models.TextField(blank=True, null=True)
    linkedin_link = models.TextField(blank=True, null=True)
    speciality = models.JSONField(blank=True, null=True)
    type_of_employement = models.CharField(max_length=100, blank=True, null=True)
    suburb = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    address_line_one = models.TextField(blank=True, null=True)
    address_line_two = models.TextField(blank=True, null=True)
    pin_code = models.IntegerField(blank=True, null=True)
    permanent_address_line_one = models.TextField(blank=True, null=True)
    permanent_address_line_two = models.TextField(blank=True, null=True)
    permanent_country = models.CharField(max_length=100, blank=True, null=True)
    permanent_state = models.CharField(max_length=100, blank=True, null=True)
    permanent_city = models.CharField(max_length=100, blank=True, null=True)
    permanent_suburb = models.CharField(max_length=100, blank=True, null=True)
    permanent_pincode = models.IntegerField(blank=True, null=True)
    bloodbank_n_key = models.CharField(max_length=45, blank=True, null=True)
    product_name = models.JSONField(blank=True, null=True)
    product_details = models.JSONField(blank=True, null=True)
    bloodbank_role = models.CharField(max_length=45, blank=True, null=True)
    mode_of_telehealth = models.JSONField(blank=True, null=True)
    treatment_approach = models.JSONField(blank=True, null=True)
    age_group = models.JSONField(blank=True, null=True)
    home_visible = models.IntegerField(null=True)
    class Meta:
        managed = False
        ordering = ['employee_id']
        db_table = 'md_employees_master'
@receiver(post_save, sender=EmployeesMaster)
def generate_employee_unique_key(sender, instance, created, **kwargs):
   post_save.disconnect(generate_employee_unique_key, sender=EmployeesMaster)
   instance.employee_n_key = "ORG{}-EMP-{}".format(instance.org_n_key[6:], instance.employee_id)
   instance.hospital_short_name = "{}{}".format(instance.org_n_key[0:3], instance.employee_id)
   if instance.user_name =='' or instance.user_name ==None:
    instance.user_name = "MYR202010000{}".format(instance.employee_id)
   instance.user_id = instance.employee_id
   instance.save()
   post_save.connect(generate_employee_unique_key, sender=EmployeesMaster)

# class GeAccess(models.Model):
#     access_id = models.AutoField(primary_key=True)
#     employee_n_key = models.CharField(max_length=30, blank=True, null=True)
#     hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
#     org_n_key = models.CharField(max_length=30, blank=True, null=True)
#     access_type = models.CharField(max_length=30, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'ge_access'

# class BbAccess(models.Model):
#     access_id = models.AutoField(primary_key=True)
#     employee_n_key = models.CharField(max_length=30, blank=True, null=True)
#     bloodbank_details_n_key = models.CharField(max_length=30, blank=True, null=True)
#     org_n_key = models.CharField(max_length=30, blank=True, null=True)
#     access_type = models.CharField(max_length=30, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'bb_access'

class GeDoctorDetails(models.Model):
    doct_id = models.AutoField(primary_key=True)
    doctor_n_key = models.CharField(max_length=30, unique=True,blank=True)
    employee_n_key =  models.ForeignKey('EmployeesMaster',db_column='employee_n_key',to_field='employee_n_key',on_delete=models.CASCADE)
    org_n_key = models.CharField(max_length=30,blank=True,null=True)
    clinical_n_key = models.CharField(max_length=30,blank=True,null=True)
    hospital_n_key = models.CharField(max_length=30,blank=True,null=True)
    prefix = models.CharField(max_length=10, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    dial_code = models.CharField(max_length=15, blank=True, null=True)
    phone_number = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    blood_group = models.CharField(max_length=30, blank=True, null=True)
    designation = models.CharField(max_length=250, blank=True, null=True)
    role = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    confirm_password = models.CharField(max_length=30, blank=True, null=True)
    licence_number = models.CharField(max_length=50, blank=True, null=True)
    primary_qualification = models.CharField(max_length=250, blank=True, null=True)
    primary_year = models.CharField(max_length=100, blank=True, null=True)
    primary_yearawarded = models.CharField(max_length=30, blank=True, null=True)
    primary_university = models.CharField(max_length=250, blank=True, null=True)
    medical_qualification = models.CharField(max_length=250, blank=True, null=True)
    medical_year = models.CharField(max_length=100, blank=True, null=True)
    medical_yearawarded = models.CharField(max_length=30, blank=True, null=True)
    medical_university = models.CharField(max_length=250, blank=True, null=True)
    speciality_qualification = models.CharField(max_length=250, blank=True, null=True)
    speciality_year = models.CharField(max_length=100, blank=True, null=True)
    speciality_yearawarded = models.CharField(max_length=30, blank=True, null=True)
    speciality_institution = models.CharField(max_length=250, blank=True, null=True)
    higher_qualification = models.CharField(max_length=250, blank=True, null=True)
    higher_yearawarded = models.CharField(max_length=30, blank=True, null=True)
    higher_institution = models.CharField(max_length=250, blank=True, null=True)
    membership_fromdate = models.CharField(max_length=250, blank=True, null=True)
    membership_todate = models.CharField(max_length=250, blank=True, null=True)
    organization = models.CharField(max_length=250, blank=True, null=True)
    training_date = models.CharField(max_length=50, blank=True, null=True)
    training_courses = models.CharField(max_length=250, blank=True, null=True)
    emp_training_fromdate = models.CharField(max_length=50, blank=True, null=True)
    emp_training_todate = models.CharField(max_length=50, blank=True, null=True)
    emp_institution = models.CharField(max_length=250, blank=True, null=True)
    emp_position = models.CharField(max_length=250, blank=True, null=True)
    exp_fromdate = models.CharField(max_length=250, blank=True, null=True)
    exp_todate = models.CharField(max_length=250, blank=True, null=True)
    exp_institution = models.CharField(max_length=250, blank=True, null=True)
    exp_position = models.CharField(max_length=250, blank=True, null=True)
    res_practice = models.CharField(max_length=250, blank=True, null=True)
    res_comments = models.TextField(blank=True, null=True)
    clinical_practice = models.CharField(max_length=250, blank=True, null=True)
    clinical_comments = models.TextField(blank=True, null=True)
    profile = models.TextField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30, blank=True, null=True)
    created_by_name = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ge_doctor_details'
@receiver(post_save, sender=GeDoctorDetails)
def generate_GeDoctorDetails_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_GeDoctorDetails_unique_key, sender=GeDoctorDetails)
   instance.doctor_n_key = "ORG{}-DD-{}".format(instance.org_n_key[6:], instance.doct_id)
   instance.save()
   post_save.connect(generate_GeDoctorDetails_unique_key, sender=GeDoctorDetails)

class MdAccess(models.Model):
    access_id = models.AutoField(primary_key=True)
    emp_n_key = models.CharField(max_length=30,blank=True)
    role_name = models.CharField(max_length=45, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    clinical_n_key = models.CharField(max_length=30, blank=True, null=True)
    bloodbank_n_key = models.CharField(max_length=30, blank=True, null=True)
    product_name = models.CharField(max_length=15, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'md_access'
class DoctorWorkingDetails(models.Model):
    doc_work_id = models.AutoField(primary_key=True)
    doc_work_n_key = models.CharField(blank=True,max_length=30)
    doctor_n_key = models.CharField(max_length=50,blank=True, null=True)
    hospital_n_key = models.CharField(max_length=50,blank=True, null=True)
    clinical_n_key = models.CharField(max_length=50,blank=True, null=True)
    org_n_key = models.CharField(max_length=50,blank=True, null=True)
    working_days = models.CharField(max_length=30,blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=30)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=50,blank=True, null=True)
    modified_by_name = models.CharField(max_length=50,blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['doc_work_id']
        db_table = 'md_doctor_working_details'
@receiver(post_save, sender=DoctorWorkingDetails)
def generate_DoctorWorkingDetails_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_DoctorWorkingDetails_unique_key, sender=DoctorWorkingDetails)
   instance.doc_work_n_key = "DOC-WORK-{}".format(instance.doc_work_id)
   instance.save()
   post_save.connect(generate_DoctorWorkingDetails_unique_key, sender=DoctorWorkingDetails)
class DoctorSpecialHours(models.Model):
    doc_spec_id = models.AutoField(primary_key=True)
    doc_spec_n_key = models.CharField(blank=True,max_length=30)
    doctor_n_key = models.CharField(max_length=50,blank=True, null=True)
    hospital_n_key = models.CharField(max_length=50,blank=True, null=True)
    org_n_key = models.CharField(max_length=50,blank=True, null=True)
    clinical_n_key = models.CharField(max_length=50,blank=True, null=True)
    special_date = models.DateField(blank=True, null=True)
    available = models.CharField(max_length=20,blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=30)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=50,blank=True, null=True)
    modified_by_name = models.CharField(max_length=50,blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['doc_spec_id']
        db_table = 'md_doctor_special_hours'
@receiver(post_save, sender=DoctorSpecialHours)
def generate_DoctorSpecialHours_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_DoctorSpecialHours_unique_key, sender=DoctorSpecialHours)
   instance.doc_spec_n_key = "DOC-SPEC-{}".format(instance.doc_spec_id)
   instance.save()
   post_save.connect(generate_DoctorSpecialHours_unique_key, sender=DoctorSpecialHours)

class EmployeeLogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    employee_n_key = models.ForeignKey('EmployeesMaster',db_column='employee_n_key',to_field='employee_n_key',on_delete=models.CASCADE)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    role = models.CharField(max_length=30, blank=True, null=True)
    firebase_token = models.TextField(blank=True, null=True)
    last_login = models.DateTimeField()

    class Meta:
        managed = False
        ordering = ['log_id']
        db_table = 'md_employee_logs'

# hospital details
class MdTimeZone(models.Model):
    timezone_id = models.AutoField(primary_key=True)
    timezone_name = models.CharField(max_length=50, blank=True, null=True)
    timezone_code = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'glo_timezone'

class HospitalMaster(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    hospital_n_key = models.CharField(blank=True, max_length=30,unique=True)
    org_n_key = models.CharField(max_length=30)
    employee_n_key = models.CharField(max_length=30)
    hospital_short = models.CharField(max_length=10, blank=True, null=True)
    hospital_short_name = models.CharField(unique=True, max_length=20)   
    hospital_name = models.CharField(max_length=100)
    accreditation = models.TextField(blank=True, null=True)
    provider_type = models.CharField(max_length=100)
    provider_type_others = models.CharField(max_length=200, blank=True, null=True)
    hospital_phoneno = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    licence_no = models.CharField(max_length=50)
    hospital_address_line_one = models.TextField()
    hospital_address_line_two = models.TextField(blank=True, null=True)
    hospital_logo = models.CharField(max_length=255, blank=True, null=True)
    gst_no = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    suburb = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.IntegerField()
    telephone_no = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    emergency_no = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    ambulance_no = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    foreign_patientcare = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    tollfree_no = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    helpline = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    hospital_fax_no = models.CharField(max_length=100, blank=True, null=True)
    pri_email_id = models.CharField(max_length=100, blank=True, null=True)
    sec_email_id = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=30, blank=True, null=True)
    establised_year = models.IntegerField()
    medical_insurance = models.CharField(max_length=100, blank=True, null=True)
    medical_insurance_others = models.CharField(max_length=200, blank=True, null=True)
    total_doctors = models.IntegerField()
    total_experts = models.IntegerField(blank=True, null=True)
    total_beds = models.IntegerField(blank=True, null=True)
    total_wards = models.IntegerField(blank=True, null=True)
    specialties_others = models.CharField(max_length=200, blank=True, null=True)
    medical_specialty = models.CharField(max_length=450)
    facilities_others = models.CharField(max_length=200, blank=True, null=True)
    facilities = models.TextField(blank=True, null=True)
    aayush = models.CharField(max_length=100, blank=True, null=True)
    dial_code = models.CharField(max_length=10, blank=True, null=True)
    bloodbank = models.CharField(max_length=5, blank=True, null=True)
    g_ehr = models.CharField(max_length=5, blank=True, null=True)
    twenty_four_hours = models.CharField(max_length=5)
    time_zone = models.CharField(max_length=50, blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=30)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=30, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    facebook_link = models.TextField(blank=True, null=True)
    instagram_link = models.TextField(blank=True, null=True)
    twitter_link = models.TextField(blank=True, null=True)
    linkedin_link = models.TextField(blank=True, null=True)
    googlemap_link = models.TextField(blank=True, null=True)
    banner_image = models.TextField(blank=True, null=True)
    about_us = models.TextField(blank=True, null=True)
    whatsapp_number = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    whatsapp_dialcode = models.CharField(max_length=30, blank=True, null=True)
    online_practice_status = models.CharField(max_length=20, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['hospital_id']
        db_table = 'md_hospital_master'
@receiver(post_save, sender=HospitalMaster)
def generate_HospitalMaster_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and centre_master_id
   """
   post_save.disconnect(generate_HospitalMaster_unique_key, sender=HospitalMaster)
   instance.hospital_n_key = "{}-HOS-{}".format(instance.hospital_short, instance.hospital_id)
   instance.hospital_short_name = "{}{}".format(instance.hospital_short, instance.hospital_id)
   instance.save()
   post_save.connect(generate_HospitalMaster_unique_key, sender=HospitalMaster)

class HospitalWorkingDetails(models.Model):
    hos_work_id = models.AutoField(primary_key=True)
    hos_work_n_key = models.CharField(blank=True,max_length=30)
    hospital_n_key = models.CharField(max_length=50,blank=True, null=True)
    org_n_key = models.CharField(max_length=50,blank=True, null=True)
    working_days = models.CharField(max_length=30,blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=30)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=50,blank=True, null=True)
    modified_by_name = models.CharField(max_length=50,blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['hos_work_id']
        db_table = 'md_hospital_working_details'
@receiver(post_save, sender=HospitalWorkingDetails)
def generate_HospitalWorkingDetails_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_HospitalWorkingDetails_unique_key, sender=HospitalWorkingDetails)
   instance.hos_work_n_key = "HOS-WORK-{}".format(instance.hos_work_id)
   instance.save()
   post_save.connect(generate_HospitalWorkingDetails_unique_key, sender=HospitalWorkingDetails)

class HospitalSpecialHours(models.Model):
    hos_spec_id = models.AutoField(primary_key=True)
    hos_spec_n_key = models.CharField(blank=True,max_length=30)
    hospital_n_key = models.CharField(max_length=50,blank=True, null=True)
    org_n_key = models.CharField(max_length=50,blank=True, null=True)
    special_date = models.DateField(blank=True, null=True)
    available = models.CharField(max_length=20,blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=30)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=50,blank=True, null=True)
    modified_by_name = models.CharField(max_length=50,blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['hos_spec_id']
        db_table = 'md_hospital_special_hours'
@receiver(post_save, sender=HospitalSpecialHours)
def generate_HospitalSpecialHours_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_HospitalSpecialHours_unique_key, sender=HospitalSpecialHours)
   instance.hos_spec_n_key = "HOS-SPEC-{}".format(instance.hos_spec_id)
   instance.save()
   post_save.connect(generate_HospitalSpecialHours_unique_key, sender=HospitalSpecialHours)

# documents
class Attachments(models.Model):
    document_id = models.AutoField(primary_key=True)
    document_attachment = models.FileField(max_length=255, upload_to='Files/', blank=True, null=True, default='')
    donor_employee_id = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['document_id']
        db_table = 'ge_attachments'


# buy product
# class PaymentPricing(models.Model):
#     payment_pricing_id = models.AutoField(primary_key=True)
#     payment_pricing_n_key = models.CharField(blank=True, max_length=30)
#     org_n_key = models.CharField(max_length=30, blank=True, null=True)
#     current_plan = models.CharField(max_length=50, blank=True, null=True)
#     subscrib_type = models.CharField(max_length=50, blank=True, null=True)
#     currentplan_ammount = models.IntegerField(blank=True, null=True)
#     paid_ammount = models.IntegerField(blank=True, null=True)
#     plan_name = models.CharField(max_length=50, blank=True, null=True)
#     full_name = models.CharField(max_length=100, blank=True, null=True)
#     adjustments = models.IntegerField(blank=True, null=True)
#     reason = models.CharField(max_length=250, blank=True, null=True)
#     project_name = models.CharField(max_length=50, blank=True, null=True)
#     short_name = models.CharField(max_length=50, blank=True, null=True)
#     payment_date = models.DateField(blank=True, null=True)
#     expire_date = models.DateField(blank=True, null=True)
#     gst = models.CharField(max_length=20, blank=True, null=True)
#     status = models.CharField(max_length=20, blank=True, null=True)
#     created_by_id = models.CharField(max_length=30)
#     created_by_name = models.CharField(max_length=30)
#     created_on = models.DateTimeField(blank=True, null=True)
#     modified_by_id = models.CharField(max_length=30, blank=True, null=True)
#     modified_by_name = models.CharField(max_length=30, blank=True, null=True)
#     modified_on = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'md_payment_pricing'
# @receiver(post_save, sender=PaymentPricing)
# def generate_PaymentPricing_unique_key(sender, instance, created, **kwargs):
#    """
#        Generate unique n_key as an combination of primary key and hospitalmaster_id
#    """
#    post_save.disconnect(generate_PaymentPricing_unique_key, sender=PaymentPricing)
#    instance.payment_pricing_n_key = "{}-PAY-{}".format("ORGID", instance.payment_pricing_id)
#    instance.save()
#    post_save.connect(generate_PaymentPricing_unique_key, sender=PaymentPricing)

# class PaymentHistory(models.Model):
#     payment_history_id = models.AutoField(primary_key=True)
#     payment_history_n_key = models.CharField(blank=True, max_length=30)
#     org_n_key = models.CharField(max_length=30, blank=True, null=True)
#     short_name = models.CharField(max_length=50, blank=True, null=True)
#     project_name = models.CharField(max_length=50, blank=True, null=True)
#     current_plan = models.CharField(max_length=50, blank=True, null=True)
#     subscrib_type = models.CharField(max_length=50, blank=True, null=True)
#     currentplan_ammount = models.IntegerField(blank=True, null=True)
#     paid_ammount = models.IntegerField(blank=True, null=True)
#     plan_name = models.CharField(max_length=50, blank=True, null=True)
#     full_name = models.CharField(max_length=100, blank=True, null=True)
#     discount_amount = models.IntegerField(blank=True, null=True)
#     adjustments = models.IntegerField(blank=True, null=True)
#     reason = models.CharField(max_length=250, blank=True, null=True)
#     payment_date = models.DateField(blank=True, null=True)
#     expire_date = models.DateField(blank=True, null=True)
#     gst = models.CharField(max_length=20, blank=True, null=True)
#     status = models.CharField(max_length=20, blank=True, null=True)
#     created_by_id = models.CharField(max_length=30)
#     created_by_name = models.CharField(max_length=30)
#     created_on = models.DateTimeField(blank=True, null=True)
#     modified_by_id = models.CharField(max_length=30, blank=True, null=True)
#     modified_by_name = models.CharField(max_length=30, blank=True, null=True)
#     modified_on = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'md_payment_history'
# @receiver(post_save, sender=PaymentHistory)
# def generate_PaymentHistory_unique_key(sender, instance, created, **kwargs):
#    """
#        Generate unique n_key as an combination of primary key and hospitalmaster_id
#    """
#    post_save.disconnect(generate_PaymentHistory_unique_key, sender=PaymentHistory)
#    instance.payment_history_n_key = "{}-PAYHIS-{}".format("ORGID", instance.payment_history_id)
#    instance.save()
#    post_save.connect(generate_PaymentHistory_unique_key, sender=PaymentHistory)   

# organization register
class OrganizationMaster(models.Model):
    organization_id = models.AutoField(primary_key=True)
    org_n_key = models.CharField(max_length=30,blank=True,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    dial_code = models.CharField(max_length=10, blank=True, null=True)
    phone_num = models.IntegerField()
    job_function = models.CharField(max_length=60)
    bloodbank = models.CharField(max_length=5, blank=True, null=True)
    g_ehr = models.CharField(max_length=5, blank=True, null=True)
    speciality = models.CharField(max_length=60)
    org_name = models.CharField(max_length=100, blank=True, null=True)
    no_of_providers = models.CharField(max_length=60)
    confirmation = models.CharField(max_length=8, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    online_practice = models.CharField(max_length=8, blank=True, null=True)
    online_bloodbank = models.CharField(max_length=8, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'md_organization_master'
@receiver(post_save, sender=OrganizationMaster)
def generate_orgmas_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_orgmas_unique_key, sender=OrganizationMaster)
   instance.org_n_key = "ORGID-{}".format(instance.organization_id)
   instance.save()
   post_save.connect(generate_orgmas_unique_key, sender=OrganizationMaster)
   
   
   
# sms settings
class SmsTemplateSettings(models.Model):
    sms_tmp_id = models.AutoField(primary_key=True)
    sms_tmp_n_key = models.CharField(max_length=30,blank=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    template_content = models.TextField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30, blank=True, null=True)
    created_by_name = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['sms_tmp_id']
        db_table = 'md_sms_template'
@receiver(post_save, sender=SmsTemplateSettings)
def generate_SmsTemplateSettings_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_SmsTemplateSettings_unique_key, sender=SmsTemplateSettings)
   instance.sms_tmp_n_key = "{}-SMSTMP-{}".format(instance.sms_tmp_id, instance.sms_tmp_id)
   instance.save()
   post_save.connect(generate_SmsTemplateSettings_unique_key, sender=SmsTemplateSettings)

class SmsSettings(models.Model):
    sms_settings_id = models.AutoField(primary_key=True)
    sms_n_key = models.CharField(max_length=30,blank=True)
    org_n_key = models.CharField(max_length=30,blank=True,null=True)
    sender_id = models.CharField(max_length=10)
    thanks_sms_content = models.TextField(blank=True, null=True)
    reminder_sms_content = models.TextField(blank=True, null=True)
    reminder_choice = models.CharField(max_length=100, blank=True, null=True)
    days_or_hours = models.CharField(max_length=50, blank=True, null=True)
    how_before = models.CharField(max_length=30, blank=True, null=True)
    sender_id_status = models.CharField(max_length=45, blank=True, null=True)
    sender_id_create_on = models.DateField(blank=True, null=True)
    org_name = models.CharField(max_length=50, blank=True, null=True)
    remaining_sms = models.CharField(max_length=10, blank=True, null=True)
    total_count = models.IntegerField(blank=True, null=True)
    enable_sms = models.CharField(max_length=10, blank=True, null=True)
    enable_thanks_sms = models.CharField(max_length=10, blank=True, null=True)
    enable_followup_sms = models.CharField(max_length=10, blank=True, null=True)
    enable_registration_sms = models.CharField(max_length=10, blank=True, null=True)
    enable_birthday_sms = models.CharField(max_length=10, blank=True, null=True)
    twofactor_globally = models.CharField(max_length=10, blank=True, null=True)
    registration_sms_content = models.TextField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=50)
    created_on = models.DateTimeField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['sms_settings_id']
        db_table = 'md_sms_settings'
@receiver(post_save, sender=SmsSettings)
def generate_SmsSettings_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_SmsSettings_unique_key, sender=SmsSettings)
   instance.sms_n_key = "ORG-SMS-{}".format(instance.sms_settings_id)
   instance.save()
   post_save.connect(generate_SmsSettings_unique_key, sender=SmsSettings)
class SmsHistory(models.Model):
    sms_history_id = models.AutoField(primary_key=True)
    hospital_n_key = models.CharField(max_length=30,blank=True,null=True)
    org_n_key = models.CharField(max_length=30,blank=True,null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    sms_status = models.CharField(max_length=45, blank=True, null=True)
    sms_type = models.CharField(max_length=45, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    created_time = models.TimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['sms_history_id']
        db_table = 'md_sms_history'


# multi product
class Discounts(models.Model):
    discount_id = models.AutoField(primary_key=True)
    discount_details = models.CharField(max_length=50, blank=True, null=True)
    discount_code = models.CharField(max_length=50, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    discount_percentage = models.CharField(max_length=50, blank=True, null=True)
    discount_status = models.CharField(max_length=50, blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'md_discounts'



class PlanDetails(models.Model):
    plan_details_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=200, blank=True, null=True)
    plan_display_name = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    sms = models.TextField(blank=True, null=True)
    order = models.CharField(max_length=20, blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    users = models.CharField(max_length=50, blank=True, null=True)
    centres = models.CharField(max_length=20, blank=True, null=True)
    product_logo = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    employees = models.CharField(max_length=250, blank=True, null=True)
    hospitals = models.CharField(max_length=250, blank=True, null=True)
    specification = models.JSONField(blank=True,null=True)
    class Meta:
        managed = False
        db_table = 'md_plan_details'

class SmsPaymentHistory(models.Model):
    sms_payment_history_id = models.AutoField(primary_key=True)
    hospital_n_key = models.CharField(max_length=30,blank=True,null=True)
    org_n_key = models.CharField(max_length=30,blank=True,null=True)
    payment_amount = models.IntegerField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    purchased_sms = models.CharField(max_length=45, blank=True, null=True)
    payment_status = models.CharField(max_length=45, blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['sms_payment_history_id']
        db_table = 'md_sms_payment_history'

  
# roles
class GERoles(models.Model):
    role_id = models.AutoField(primary_key=True)
    roles_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    role_check = models.CharField(max_length=30, blank=True, null=True)
    page_name = models.CharField(max_length=100, blank=True, null=True)
    urls = models.TextField(blank=True, null=True)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    document = models.CharField(max_length=200, blank=True, null=True)
    working_enable = models.CharField(max_length=10, blank=True, null=True)
    pdashboard_appointment = models.CharField(max_length=10, blank=True, null=True)
    calendar_appointment = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'md_roles'
class GeModules(models.Model):
    module_id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    page_name = models.CharField(max_length=50, blank=True, null=True)
    urls = models.CharField(max_length=50, blank=True, null=True)
    success = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'glo_modules'
class RoleNames(models.Model):
    role_id =  models.AutoField(primary_key=True)
    roles = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bb_role_names'
class BBRoles(models.Model):
    role_id = models.AutoField(primary_key=True)
    roles_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    page_name = models.CharField(max_length=100, blank=True, null=True)
    role_check = models.CharField(max_length=30, blank=True, null=True)
    urls = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    hospital_short_name = models.CharField(max_length=45, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=50)
    created_on = models.DateField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'md_roles'

# class BBModules(models.Model):
#     module_id = models.AutoField(primary_key=True)
#     category = models.CharField(max_length=100, blank=True, null=True)
#     page_name = models.CharField(max_length=100, blank=True, null=True)
#     project_name = models.CharField(max_length=50, blank=True, null=True)
#     urls = models.CharField(max_length=100, blank=True, null=True)
#     success = models.CharField(max_length=50, blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'bb_modules'

# home page
class BbBloodbankDetails(models.Model):
    bloodbank_details_id = models.AutoField(primary_key=True)
    bloodbank_details_n_key = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    hospital_short_name = models.CharField(max_length=30)
    org_n_key = models.CharField(max_length=30)
    bloodbank_name = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=30, blank=True, null=True)
    gst_number = models.CharField(max_length=30, blank=True, null=True)
    working_days = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.CharField(max_length=30, blank=True, null=True)
    end_time = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    district = models.CharField(max_length=30, blank=True, null=True)
    taluk = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    bloodbank_logo = models.CharField(max_length=200, blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=30)
    created_on = models.DateField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=30, blank=True, null=True)
    modified_on = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bb_bloodbank_details'
@receiver(post_save, sender=BbBloodbankDetails)
def generate_BbBloodbankDetails_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_BbBloodbankDetails_unique_key, sender=BbBloodbankDetails)
   instance.bloodbank_details_n_key = "{}-BBD-{}".format(instance.hospital_short_name, instance.bloodbank_details_id)
   instance.save()
   post_save.connect(generate_BbBloodbankDetails_unique_key, sender=BbBloodbankDetails)

# clinic details
class ClinicalMaster(models.Model):
    clinical_id = models.AutoField(primary_key=True,unique=True)
    clinical_n_key = models.CharField(max_length=30,blank=True,unique=True)
    hospital_n_key = models.CharField(max_length=30,blank=True, null=True)
    org_n_key = models.CharField(max_length=30,blank=True, null=True)
    clinical_name = models.CharField(max_length=45)
    clinical_short = models.CharField(max_length=20, blank=True, null=True)
    clinical_short_name = models.CharField(unique=True, max_length=20)
    doctor_n_key = models.CharField(max_length=30, blank=True, null=True)
    assigned_doctor = models.CharField(max_length=30, blank=True, null=True)
    clinical_phone_number = models.BigIntegerField()
    licence_number = models.CharField(max_length=30)
    gst_number = models.CharField(max_length=30)
    speciality = models.CharField(max_length=30)
    twenty_four_hours = models.CharField(max_length=5, blank=True, null=True)
    allow_online_appointments = models.CharField(max_length=10, blank=True, null=True)
    clinical_address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    taluk = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    pincode = models.IntegerField(blank=True, null=True)
    created_by_id = models.CharField(max_length=50, blank=True, null=True)
    created_by_name = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=50, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['clinical_id']
        db_table = 'ge_clinical_master'
@receiver(post_save, sender=ClinicalMaster)
def generate_clinicalmaster_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and centre_master_id
   """
   post_save.disconnect(generate_clinicalmaster_unique_key, sender=ClinicalMaster)
   instance.clinical_n_key = "{}-CLI-{}".format(instance.clinical_short, instance.clinical_id)
   instance.clinical_short_name = "{}{}".format(instance.clinical_short, instance.clinical_id)
   instance.save()
   post_save.connect(generate_clinicalmaster_unique_key, sender=ClinicalMaster)

class ClinicalWorkingDetails(models.Model):
    clin_work_id = models.AutoField(primary_key=True)
    clin_work_n_key = models.CharField(blank=True,max_length=30)
    hospital_n_key = models.CharField(max_length=50,blank=True, null=True)
    clinical_n_key = models.CharField(max_length=50,blank=True, null=True)
    org_n_key = models.CharField(max_length=50,blank=True, null=True)
    working_days = models.CharField(max_length=30,blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=30)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=50,blank=True, null=True)
    modified_by_name = models.CharField(max_length=50,blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['clin_work_id']
        db_table = 'md_clinic_working_details'
@receiver(post_save, sender=ClinicalWorkingDetails)
def generate_ClinicalWorkingDetails_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_ClinicalWorkingDetails_unique_key, sender=ClinicalWorkingDetails)
   instance.clin_work_n_key = "CLI-WORK-{}".format(instance.clin_work_id)
   instance.save()
   post_save.connect(generate_ClinicalWorkingDetails_unique_key, sender=ClinicalWorkingDetails)

class ClinicalSpecialHours(models.Model):
    clin_spec_id = models.AutoField(primary_key=True)
    clin_spec_n_key = models.CharField(blank=True,max_length=30)
    hospital_n_key = models.CharField(max_length=50,blank=True, null=True)
    clinical_n_key = models.CharField(max_length=50,blank=True, null=True)
    org_n_key = models.CharField(max_length=50,blank=True, null=True)
    special_date = models.DateField(blank=True, null=True)
    available = models.CharField(max_length=20,blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=30)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=50,blank=True, null=True)
    modified_by_name = models.CharField(max_length=50,blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['clin_spec_id']
        db_table = 'md_clinic_special_hours'
@receiver(post_save, sender=ClinicalSpecialHours)
def generate_ClinicalSpecialHours_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_ClinicalSpecialHours_unique_key, sender=ClinicalSpecialHours)
   instance.clin_spec_n_key = "CLI-SPEC-{}".format(instance.clin_spec_id)
   instance.save()
   post_save.connect(generate_ClinicalSpecialHours_unique_key, sender=ClinicalSpecialHours)


# currency details
class CurrencyTable(models.Model):
    currency_id = models.CharField(primary_key=True,max_length=30)
    currency_name = models.CharField(max_length=100,blank=True, null=True)
    currency_country_name = models.CharField(max_length=100,blank=True, null=True)
    currency_alphabetic_code = models.CharField(max_length=100,blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['currency_id']
        db_table = 'glo_currency_tbl'
class CurrencyDetails(models.Model):
    currency_details_id = models.AutoField(primary_key=True)
    currency_details_n_key = models.CharField(blank=True, max_length=30)
    currency_id = models.ForeignKey('CurrencyTable',db_column='currency_id',to_field='currency_id',on_delete=models.CASCADE)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    clinical_short_name = models.CharField(max_length=20, blank=True, null=True)
    currency_alphabetic_code = models.CharField(max_length=10, blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'md_currency_details'
@receiver(post_save, sender=CurrencyDetails)
def generate_CurrencyDetails_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_CurrencyDetails_unique_key, sender=CurrencyDetails)
   instance.currency_details_n_key = "{}-CUR-{}".format(instance.org_n_key[:3], instance.currency_details_id)
   instance.save()
   post_save.connect(generate_CurrencyDetails_unique_key, sender=CurrencyDetails)

# new page   
class SubscribersMaster(models.Model):
    subscribers_id = models.AutoField(primary_key=True)
    subscribers_email = models.CharField(max_length=30)

    class Meta:
        managed = False
        ordering = ['subscribers_id']
        db_table = 'md_subscribers'

# profile
class CalendarSettings(models.Model):
    cal_id = models.AutoField(primary_key=True)
    cal_n_key = models.CharField(max_length=30,blank=True)
    employee_n_key = models.CharField(max_length=30,blank=True, null=True)
    org_n_key = models.CharField(max_length=30,blank=True, null=True)
    interval = models.IntegerField(blank=True, null=True)
    sync_mail = models.CharField(max_length=5, blank=True, null=True)
    allow_overlap = models.CharField(max_length=5, blank=True, null=True)
    outpatient = models.CharField(max_length=30, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    allow_appointment = models.CharField(max_length=5, blank=True, null=True)
    created_by_id = models.CharField(max_length=50, blank=True, null=True)
    created_by_name = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=50, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ge_calendar_settings'
@receiver(post_save, sender=CalendarSettings)
def generate_CalendarSettings_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and clinicalmaster_id
   """
   post_save.disconnect(generate_CalendarSettings_unique_key, sender=CalendarSettings)
   instance.cal_n_key = "{}-CAL-{}".format(instance.org_n_key[:3], instance.cal_id)
   instance.save()
   post_save.connect(generate_CalendarSettings_unique_key, sender=CalendarSettings)        

class Employeedocuments(models.Model):
    emp_document_id = models.AutoField(primary_key=True)
    # document_type = models.CharField(blank=True,max_length=50)
    doctor_n_key = models.CharField(blank=True,max_length=30)
    emp_attachment = models.FileField(max_length=255, upload_to='Files/', blank=True, null=True, default='')

    class Meta:
        managed = False
        ordering = ['emp_document_id']
        db_table = 'ge_employee_documents'

class Empeducationaldetails(models.Model):
    emp_edu_id = models.AutoField(primary_key=True)
    edu_n_key = models.CharField(max_length=30, blank=True)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    employee_n_key = models.CharField(max_length=30, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    qualification_title = models.CharField(max_length=100, blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    controlling_university = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    document_attachment = models.FileField(max_length=255, upload_to='Files/', blank=True, null=True, default='')
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['emp_edu_id']
        db_table = 'ge_emp_education_details'
@receiver(post_save, sender=Empeducationaldetails)
def generate_Empeducationaldetails_unique_key(sender, instance, created, **kwargs):

   post_save.disconnect(generate_Empeducationaldetails_unique_key, sender=Empeducationaldetails)
   instance.edu_n_key = "{}-EDU-{}".format(instance.org_n_key[:3], instance.emp_edu_id)
   instance.save()
   post_save.connect(generate_Empeducationaldetails_unique_key, sender=Empeducationaldetails)

class EmployeeProfessional(models.Model):
    emp_pro_id = models.AutoField(primary_key=True)
    pro_n_key = models.CharField(max_length=30, blank=True)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    employee_n_key = models.CharField(max_length=30, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    organisation = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    document_attachment = models.FileField(max_length=255, upload_to='Files/', blank=True, null=True, default='')
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['emp_pro_id']
        db_table = 'ge_emp_professional'
@receiver(post_save, sender=EmployeeProfessional)
def generate_EmployeeProfessional_unique_key(sender, instance, created, **kwargs):

   post_save.disconnect(generate_EmployeeProfessional_unique_key, sender=EmployeeProfessional)
   instance.pro_n_key = "{}-PRO-{}".format(instance.org_n_key[:3], instance.emp_pro_id)
   instance.save()
   post_save.connect(generate_EmployeeProfessional_unique_key, sender=EmployeeProfessional)


class EmployeeTraining(models.Model):
    emp_training_id = models.AutoField(primary_key=True)
    training_n_key = models.CharField(max_length=30, blank=True)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    employee_n_key = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    courses = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    document_attachment = models.FileField(max_length=255, upload_to='Files/', blank=True, null=True, default='')
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['emp_training_id']
        db_table = 'ge_emp_training'
@receiver(post_save, sender=EmployeeTraining)
def generate_EmployeeTraining_unique_key(sender, instance, created, **kwargs):

   post_save.disconnect(generate_EmployeeTraining_unique_key, sender=EmployeeTraining)
   instance.training_n_key = "{}-TRA-{}".format(instance.org_n_key[:3], instance.emp_training_id)
   instance.save()
   post_save.connect(generate_EmployeeTraining_unique_key, sender=EmployeeTraining)





class EmployeeExperience(models.Model):
    emp_exp_id = models.AutoField(primary_key=True)
    exp_n_key = models.CharField(max_length=30, blank=True)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    employee_n_key = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    employment_type = models.CharField(max_length=50, blank=True, null=True)
    hos_name = models.CharField(max_length=100, blank=True, null=True)
    currently_working = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.CharField(max_length=20, blank=True, null=True)
    end_date = models.CharField(max_length=20, blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['emp_exp_id']
        db_table = 'ge_emp_experience'
@receiver(post_save, sender=EmployeeExperience)
def generate_EmployeeExperience_unique_key(sender, instance, created, **kwargs):

   post_save.disconnect(generate_EmployeeExperience_unique_key, sender=EmployeeExperience)
   instance.exp_n_key = "{}-EXP-{}".format(instance.org_n_key[:3], instance.emp_exp_id)
   instance.save()
   post_save.connect(generate_EmployeeExperience_unique_key, sender=EmployeeExperience)





class EmployeeTeachExperience(models.Model):
    exp_teach_id = models.AutoField(primary_key=True)
    exp_teach_n_key = models.CharField(max_length=30, blank=True)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    employee_n_key = models.CharField(max_length=30, blank=True, null=True)
    institution = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['exp_teach_id']
        db_table = 'ge_emp_exp_teaching'
@receiver(post_save, sender=EmployeeTeachExperience)
def generate_EmployeeTeachExperience_unique_key(sender, instance, created, **kwargs):

   post_save.disconnect(generate_EmployeeTeachExperience_unique_key, sender=EmployeeTeachExperience)
   instance.exp_teach_n_key = "{}-TEACH-{}".format(instance.org_n_key[:3], instance.exp_teach_id)
   instance.save()
   post_save.connect(generate_EmployeeTeachExperience_unique_key, sender=EmployeeTeachExperience)


class EmployeeRestriction(models.Model):
    emp_practice_id = models.AutoField(primary_key=True)
    practice_n_key = models.CharField(max_length=30, blank=True)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    employee_n_key = models.CharField(max_length=30, blank=True, null=True)
    restriction_if_any = models.CharField(max_length=20, blank=True, null=True)
    inv_practice = models.CharField(max_length=20, blank=True, null=True)
    res_comments = models.TextField(blank=True, null=True)
    inv_comments = models.TextField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['emp_practice_id']
        db_table = 'ge_emp_practice_restriction'
@receiver(post_save, sender=EmployeeRestriction)
def generate_EmployeeRestriction_unique_key(sender, instance, created, **kwargs):

   post_save.disconnect(generate_EmployeeRestriction_unique_key, sender=EmployeeRestriction)
   instance.practice_n_key = "{}-RES-{}".format(instance.org_n_key[:3], instance.emp_practice_id)
   instance.save()
   post_save.connect(generate_EmployeeRestriction_unique_key, sender=EmployeeRestriction)

class AppProductDetails(models.Model):
    app_prod_id = models.AutoField(primary_key=True)
    app_prod_n_key = models.CharField(max_length=30, blank=True)
    hospital_n_key = models.CharField(max_length=20, blank=True, null=True)
    org_n_key = models.CharField(max_length=20, blank=True, null=True)
    product_title = models.CharField(max_length=150)
    product_image = models.TextField(blank=True, null=True)
    product_short_discription = models.CharField(max_length=300, blank=True, null=True)
    product_long_discription = models.TextField(blank=True, null=True)
    faqs = models.TextField(blank=True, null=True)
    program_icon_one = models.TextField(blank=True, null=True)
    program_icon_two = models.TextField(blank=True, null=True)
    program_icon_three = models.TextField(blank=True, null=True)
    program_icon_four = models.TextField(blank=True, null=True)
    program_icon_five = models.TextField(blank=True, null=True)
    program_icon_six = models.TextField(blank=True, null=True)
    payment_type = models.CharField(max_length=50, blank=True, null=True)
    single_plan = models.TextField(blank=True, null=True)
    plan_a = models.TextField(blank=True, null=True)
    plan_b = models.TextField(blank=True, null=True)
    plan_c = models.TextField(blank=True, null=True)
    top_button = models.CharField(max_length=30)
    center_button = models.CharField(max_length=30)
    bottom_button = models.CharField(max_length=30)
    doctor_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30,blank=True,null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=100, blank=True)
    created_on = models.DateTimeField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['app_prod_id']
        db_table = 'app_product_details'
@receiver(post_save, sender=AppProductDetails)
def generate_AppProductDetails_unique_key(sender, instance, created, **kwargs):
   post_save.disconnect(generate_AppProductDetails_unique_key, sender=AppProductDetails)
   instance.app_prod_n_key = "APP_PROD-{}".format(instance.app_prod_id)
   instance.save()
   post_save.connect(generate_AppProductDetails_unique_key, sender=AppProductDetails)


class MedicalCollege(models.Model):
    sno = models.AutoField(primary_key=True)
    country_name = models.CharField(blank=True,max_length=150,null=True)
    medical_school_name = models.TextField()
    city_name = models.CharField(blank=True,max_length=150,null=True)

    class Meta:
        managed = False
        ordering = ['sno']
        db_table = 'glo_medical_college'

class PromoCodeDetails(models.Model):
    promo_id = models.AutoField(primary_key=True)
    promo_code = models.CharField(max_length=100)
    expire_date = models.DateTimeField(blank=True, null=True)
    percentage = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    user = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    promo_type = models.CharField(max_length=50, blank=True, null=True)
    patient_name = models.CharField(max_length=100, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=50, blank=True, null=True)
    org_n_key = models.CharField(max_length=50, blank=True, null=True)
    created_by_id = models.CharField(max_length=60, blank=True, null=True)
    created_on = models.DateTimeField(max_length=30, blank=True, null=True)
    promo_code_two = models.CharField(max_length=100,blank=True, null=True)
    promo_code_three = models.CharField(max_length=100,blank=True, null=True)
    percentage_two = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    percentage_three = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    promo_details = models.JSONField(blank=True, null=True)
    payment_type = models.CharField(max_length=50,blank=True, null=True)
    product = models.CharField(max_length=50,blank=True, null=True)
    product_type = models.CharField(max_length=50,blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['promo_id']
        db_table = 'app_promocode'

class PatientMaster(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_n_key = models.CharField(max_length=30,blank=True,unique=True)
    unique_health_n_key = models.CharField(max_length=30,blank=True, null=True)
    clinical_short_name = models.CharField(max_length=30,blank=True, null=True)
    hospital_n_key = models.ForeignKey('HospitalMaster',db_column='hospital_n_key',to_field='hospital_n_key',on_delete=models.CASCADE)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    dial_code = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    home_phone = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    work_phone = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=30, blank=True, null=True)
    age = models.CharField(max_length=20)
    date_of_birth = models.DateField(blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)   
    pincode = models.IntegerField(blank=True, null=True)
    address_line_one = models.TextField(blank=True, null=True)
    address_line_two = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    suburb = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    adhaar_number = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.TextField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50,blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['patient_id']
        db_table = 'ge_patient_master'
    @property
    def full_name(self):
        return self.first_name +' '+ self.last_name if self.last_name != None else self.first_name 


class MedicalSpecialty(models.Model):
    id = models.AutoField(primary_key=True)
    speciality = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'glo_medical_speciality'

class EmployeeOtherDocument(models.Model):
    odoc_id = models.AutoField(primary_key=True)
    employee_n_key = models.CharField(max_length=30, blank=True, null=True)
    document_name = models.CharField(max_length=100, blank=True, null=True)
    document_image = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hospital_n_key = models.ForeignKey('HospitalMaster',db_column='hospital_n_key',to_field='hospital_n_key',on_delete=models.CASCADE)
    org_n_key = models.CharField(max_length=50, blank=True, null=True)
    created_by_id = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ge_emp_other_docs'

class GeAppointmentServices(models.Model):
    id = models.AutoField(primary_key=True)
    service_n_key = models.CharField(max_length=50,unique=True,blank=True)
    org_n_key = models.CharField(max_length=20, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=50)
    payment = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    colour = models.CharField(max_length=50, blank=True, null=True)
    service_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)
    cancel_type = models.CharField(max_length=50, blank=True, null=True)
    cancel_message = models.TextField(blank=True, null=True)
    changes_type = models.CharField(max_length=45, blank=True, null=True)
    changes_message = models.TextField(blank=True, null=True)
    patient_cancellations = models.CharField(max_length=50, blank=True, null=True)
    patient_changes = models.CharField(max_length=50, blank=True, null=True)
    discount = models.CharField(max_length=45, blank=True, null=True)
    allow_online_appointment = models.CharField(max_length=5, blank=True, null=True)
    hospital_share = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    doctor_share = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    hospital_amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    doctor_amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    hospital_discount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    doctor_discount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    hospital_discount_amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    doctor_discount_amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    product_amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    tax = models.CharField(max_length=20, blank=True, null=True)
    inclusive_of_tax = models.CharField(max_length=45, blank=True, null=True)
    tax_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    sale_amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    sale_discount_amount = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    final_amount_without_tax = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    final_tax_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    final_amount_with_tax = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_by_id = models.CharField(max_length=20, blank=True, null=True)
    created_by_name = models.CharField(max_length=30, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=20, blank=True, null=True)
    modified_by_name = models.CharField(max_length=30, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ge_appointment_service'



#new bloodbank master
class BloodBank_Master(models.Model):
    bloodbank_id = models.AutoField(primary_key=True)
    bloodbank_n_key = models.CharField(blank=True, max_length=30,unique=True)
    org_n_key = models.CharField(max_length=30)
    state = models.CharField(max_length=100)
    suburb = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.IntegerField()
    dial_code = models.CharField(max_length=10, blank=True, null=True)
    facebook_link = models.TextField(blank=True, null=True)
    instagram_link = models.TextField(blank=True, null=True)
    twitter_link = models.TextField(blank=True, null=True)
    linkedin_link = models.TextField(blank=True, null=True)
    googlemap_link = models.TextField(blank=True, null=True)
    banner_image = models.TextField(blank=True, null=True)
    bloodbank_logo = models.CharField(max_length=200, blank=True, null=True)
    about_us = models.TextField(blank=True, null=True)
    whatsapp_number = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    whatsapp_dialcode = models.CharField(max_length=10, blank=True, null=True)
    bloodbank_name = models.CharField(max_length=100)
    facility = models.JSONField(blank=True, null=True)
    bloodbank_phoneno = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    licence_no = models.CharField(max_length=50)
    gst_no = models.CharField(max_length=50)
    emergency_no = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    time_zone = models.CharField(max_length=50, blank=True, null=True)
    bloodbank_address_line_one = models.TextField()
    bloodbank_address_line_two = models.TextField(blank=True, null=True)
    twenty_four_hours = models.CharField(max_length=5)
    tollfree_no = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    helpline = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    bloodbank_fax_no= models.CharField(max_length=100, blank=True, null=True)
    pri_email_id = models.CharField(max_length=100, blank=True, null=True)
    sec_email_id = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=30, blank=True, null=True)
    establised_year = models.IntegerField()
    online_practice_status = models.CharField(max_length=20, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=30)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=30, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['bloodbank_id']
        db_table = 'md_blood_bank_master'
@receiver(post_save, sender=BloodBank_Master)
def generate_BloodBank_Master_unique_key(sender, instance, created, **kwargs):
   """
       Generate unique n_key as an combination of primary key and centre_master_id
   """
   post_save.disconnect(generate_BloodBank_Master_unique_key, sender=BloodBank_Master)
   instance.bloodbank_n_key = "ORG-BB-{}".format(instance.bloodbank_id)
   instance.save()
   post_save.connect(generate_BloodBank_Master_unique_key, sender=BloodBank_Master)



class BloodBankWorkingDetails(models.Model):
    bb_work_id = models.AutoField(primary_key=True)
    bb_work_n_key = models.CharField(blank=True,max_length=30)
    bloodbank_n_key = models.CharField(max_length=50,blank=True, null=True)
    org_n_key = models.CharField(max_length=50,blank=True, null=True)
    working_days = models.CharField(max_length=30,blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=30)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=50,blank=True, null=True)
    modified_by_name = models.CharField(max_length=50,blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['bb_work_id']
        db_table = 'md_bloodbank_working_details'
@receiver(post_save, sender=BloodBankWorkingDetails)
def generate_BloodBankWorkingDetails_unique_key(sender, instance, created, **kwargs):
    post_save.disconnect(generate_BloodBankWorkingDetails_unique_key, sender=BloodBankWorkingDetails)
    instance.bb_work_n_key = "BB-WORK-{}".format(instance.bb_work_id)
    instance.save()
    post_save.connect(generate_BloodBankWorkingDetails_unique_key, sender=BloodBankWorkingDetails)
class BloodBankSpecialHours(models.Model):
    bb_spec_id = models.AutoField(primary_key=True)
    bb_spec_n_key = models.CharField(blank=True,max_length=30)
    bloodbank_n_key = models.CharField(max_length=50,blank=True, null=True)
    org_n_key = models.CharField(max_length=50,blank=True, null=True)
    special_date = models.DateField(blank=True, null=True)
    available = models.CharField(max_length=20,blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=30)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=50,blank=True, null=True)
    modified_by_name = models.CharField(max_length=50,blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['bb_spec_id']
        db_table = 'md_bloodbank_special_hours'
@receiver(post_save, sender=BloodBankSpecialHours)
def generate_BloodBankSpecialHours_unique_key(sender, instance, created, **kwargs):
   post_save.disconnect(generate_BloodBankSpecialHours_unique_key, sender=BloodBankSpecialHours)
   instance.bb_spec_n_key = "BB-SPEC-{}".format(instance.bb_spec_id)
   instance.save()
   post_save.connect(generate_BloodBankSpecialHours_unique_key, sender=BloodBankSpecialHours)

class AppointmentMaster(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    appointment_n_key = models.CharField(max_length=30,blank=True,unique=True)
    clinical_short_name = models.CharField(max_length=20, blank=True, null=True)
    patient_n_key = models.ForeignKey('PatientMaster',db_column='patient_n_key',to_field='patient_n_key',on_delete=models.CASCADE)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    clinical_n_key = models.CharField(max_length=30,blank=True,null=True)
    encounter_id = models.CharField(max_length=30, blank=True, null=True)
    patient_type = models.CharField(max_length=30, blank=True, null=True)
    reschedule_reason = models.TextField(blank=True, null=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(blank=True, null=True)
    clinical_name = models.CharField(max_length=30, blank=True, null=True)
    appointment_end_time = models.TimeField(blank=True, null=True)
    chief_complaints = models.TextField(blank=True, null=True)
    front_office_checkout_id = models.CharField(max_length=30, blank=True, null=True)
    doc_app_id = models.CharField(max_length=30, blank=True, null=True)
    front_office_check_in_time = models.TimeField(blank=True, null=True)
    checkout_time = models.DateTimeField(blank=True, null=True)
    front_office_status = models.CharField(max_length=50, blank=True, null=True)
    service_name = models.CharField(max_length=45, blank=True, null=True)
    doctor_check_in_time = models.DateTimeField(blank=True, null=True)
    doctor_check_out_time = models.DateTimeField(blank=True, null=True)
    doctor_status = models.CharField(max_length=20, blank=True, null=True)
    appointment_type = models.CharField(max_length=10, blank=True, null=True)
    appointment_show = models.CharField(max_length=20, blank=True, null=True)
    overall_status = models.CharField(max_length=50)
    patient_ip_op_type = models.CharField(max_length=20, blank=True, null=True)
    colour = models.CharField(max_length=30, blank=True, null=True)
    rescheduled_time = models.DateTimeField(blank=True, null=True)
    arrived_date_time = models.DateTimeField(blank=True, null=True)
    cancelled_date_time = models.DateTimeField(blank=True, null=True)
    cancelled_reason = models.TextField(blank=True, null=True)
    noshow_reason = models.TextField(blank=True, null=True)
    no_show_time = models.DateTimeField(blank=True, null=True)
    with_doctor_time = models.TimeField(blank=True, null=True)
    left_without_seen_time = models.DateTimeField(blank=True, null=True)
    left_without_seen_reason = models.TextField(blank=True, null=True)
    payment_type = models.CharField(max_length=45, blank=True, null=True)
    appointment_name = models.CharField(max_length=45, blank=True, null=True)
    created_by_id = models.CharField(max_length=30, blank=True, null=True)
    created_by_name = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    mode_of_telehealth = models.CharField(max_length=30, blank=True, null=True)
    choose_by_mode = models.CharField(max_length=30, blank=True, null=True)
    meeting_id = models.TextField(blank=True, null=True)
    room_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ['appointment_id']
        db_table = 'ge_appointment_master'

class AppointmentCredits(models.Model):
    credit_id = models.AutoField(primary_key=True)
    patient_n_key = models.CharField(max_length=50, blank=True, null=True)
    appointment_n_key = models.CharField(max_length=30, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=50, blank=True, null=True)
    org_n_key = models.CharField(max_length=50, blank=True, null=True)
    reason = models.TextField(null=True,blank=True)
    app_payment_n_key = models.CharField(max_length=45,blank=True,null=True)
    created_by_id = models.CharField(max_length=45)
    created_by_name = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'app_appointment_credits'

class AppSessionDetails(models.Model):
    app_session_id = models.AutoField(primary_key=True)
    app_session_n_key = models.CharField(max_length=50, blank=True, unique=True)
    patient_n_key = models.CharField(max_length=50, blank=True, null=True)
    app_payment_n_key = models.CharField(max_length=50, blank=True, null=True)
    app_prod_n_key = models.CharField(max_length=50, blank=True, null=True)
    appointment_n_key = models.TextField(blank=True, null=True)
    doc_app_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    org_n_key = models.CharField(max_length=50, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    payment_details = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['app_session_id']
        db_table = 'app_session_details'
@receiver(post_save, sender=AppSessionDetails)
def generate_AppSessionDetails_unique_key(sender, instance, created, **kwargs):
   post_save.disconnect(generate_AppSessionDetails_unique_key, sender=AppSessionDetails)
   instance.app_session_n_key = "APP-SESS-{}".format(instance.app_session_id)
   instance.save()
   post_save.connect(generate_AppSessionDetails_unique_key, sender=AppSessionDetails)


class InvoiceBillDetails(models.Model):
    invoice_bill_details_id = models.AutoField(primary_key=True)
    invoice_bill_details_n_key = models.CharField(blank=True, max_length=30, unique=True)
    invoice_no = models.ForeignKey('InvoiceBillPayment',db_column='invoice_no',to_field='invoice_no',on_delete=models.CASCADE)
    patient_n_key = models.ForeignKey('PatientMaster',db_column='patient_n_key',to_field='patient_n_key',on_delete=models.CASCADE)
    hospital_n_key = models.CharField(max_length=30, blank=True, null=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    appointment_n_key = models.CharField(max_length=30)
    advance_used = models.IntegerField(blank=True, null=True)
    adjustment = models.IntegerField(blank=True, null=True)
    encounter_id = models.CharField(max_length=30)
    comments = models.TextField(blank=True, null=True)
    patient_name = models.CharField(max_length=250, blank=True, null=True)
    balance_amount = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=250, blank=True, null=True)
    cash_amt = models.IntegerField(blank=True, null=True)
    credit_amt = models.IntegerField(blank=True, null=True)
    debit_amt = models.IntegerField(blank=True, null=True)
    cheque_amt = models.IntegerField(blank=True, null=True)
    return_amount = models.IntegerField(blank=True, null=True)
    write_off_amount = models.IntegerField(blank=True, null=True)
    write_off_reason = models.TextField(blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=50)
    created_on = models.DateTimeField()
    modified_by_id = models.CharField(max_length=30, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'ge_bill_invoice_bill_summary'
@receiver(post_save, sender=InvoiceBillDetails)
def generate_InvoiceBillDetails_unique_key(sender, instance, created, **kwargs):
    post_save.disconnect(generate_InvoiceBillDetails_unique_key, sender=InvoiceBillDetails)
    instance.invoice_bill_details_n_key = "{}-BILL-{}".format(instance.hospital_n_key[:3], instance.invoice_bill_details_id)
    instance.save()
    post_save.connect(generate_InvoiceBillDetails_unique_key, sender=InvoiceBillDetails)


class InvoiceBillPayment(models.Model):
    inv_bill_payment_id = models.AutoField(primary_key=True)
    inv_bill_payment_n_key = models.CharField(blank=True, max_length=30, unique=True)
    invoice_no = models.CharField(max_length=30,blank=True, unique=True)
    appointment_n_key = models.CharField(max_length=50)
    patient_n_key = models.CharField(max_length=50, blank=True, null=True)
    encounter_id = models.CharField(max_length=30)
    billing_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    rate = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    tax = models.CharField(max_length=100, blank=True, null=True)
    central_tax = models.CharField(max_length=100, blank=True, null=True)
    state_tax = models.CharField(max_length=100, blank=True, null=True)
    taxperone = models.CharField(max_length=100, blank=True, null=True)
    doctor_share = models.CharField(max_length=100, blank=True, null=True)
    sub_total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=100, blank=True, null=True)
    org_n_key = models.CharField(max_length=100, blank=True, null=True)
    return_balance = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    finalized = models.CharField(max_length=30, blank=True, null=True)
    inclusive_of_tax = models.CharField(max_length=100, blank=True, null=True)
    doctor_name = models.CharField(max_length=250, blank=True, null=True)
    s_discount = models.CharField(max_length=200, blank=True, null=True)
    s_dis_amt = models.CharField(max_length=100, blank=True, null=True)
    d_amt = models.CharField(max_length=100, blank=True, null=True)
    d_discount = models.CharField(max_length=200, blank=True, null=True)
    d_dis_amt = models.CharField(max_length=100, blank=True, null=True)
    h_amt = models.CharField(max_length=100, blank=True, null=True)
    h_discount = models.CharField(max_length=200, blank=True, null=True)
    h_dis_amt = models.CharField(max_length=100, blank=True, null=True)
    product_amount = models.CharField(max_length=100, blank=True, null=True)
    created_by_id = models.CharField(max_length=50)
    created_by_name = models.CharField(max_length=100)
    created_on = models.DateTimeField()
    modified_by_id = models.CharField(max_length=50, blank=True, null=True)
    modified_by_name = models.CharField(max_length=100, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)
    app_payment_n_key = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ge_bill_invoice_bill_items'

@receiver(post_save, sender=InvoiceBillPayment)
def generate_InvoiceBillPayment_unique_key(sender, instance, created, **kwargs):
   post_save.disconnect(generate_InvoiceBillPayment_unique_key, sender=InvoiceBillPayment)
   instance.inv_bill_payment_n_key = "{}-PAY-{}".format(instance.hospital_n_key[:3], instance.inv_bill_payment_id)
   instance.invoice_no = "{}-INV-{}".format(instance.hospital_n_key[:3], instance.inv_bill_payment_id)
   instance.save()
   post_save.connect(generate_InvoiceBillPayment_unique_key, sender=InvoiceBillPayment)


class AppPaymentDetails(models.Model):
    app_payment_id = models.AutoField(primary_key=True)
    app_payment_n_key = models.CharField(blank=True,max_length=30)
    app_prod_n_key = models.CharField(max_length=50, blank=True, null=True)
    patient_n_key = models.ForeignKey('PatientMaster',db_column='patient_n_key',to_field='patient_n_key',on_delete=models.CASCADE)
    appointment_n_key = models.CharField(max_length=50, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=50, blank=True, null=True)
    org_n_key = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)
    amount = models.CharField(max_length=50, blank=True, null=True)
    payment_details = models.TextField(blank=True, null=True)
    total_session = models.CharField(max_length=50, blank=True, null=True)
    split_session = models.JSONField(blank=True, null=True)
    uuid_token = models.TextField(blank=True, null=True)
    created_on = models.TextField(blank=True, null=True)
    product_amount = models.TextField(blank=True, null=True)
    discount = models.TextField(blank=True, null=True)
    discount_amount = models.TextField(blank=True, null=True)
    product = models.CharField(max_length=50, blank=True, null=True)
    invoice = models.TextField(blank=True, null=True)
    invoice_discount = models.TextField(blank=True, null=True)
    doctors = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    app_prod_grp_key = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['app_payment_id']
        db_table = 'app_payment_details'
@receiver(post_save, sender=AppPaymentDetails)
def generate_AppPaymentDetails_unique_key(sender, instance, created, **kwargs):
    post_save.disconnect(generate_AppPaymentDetails_unique_key, sender=AppPaymentDetails)
    instance.app_payment_n_key = "APPPAY-{}".format(instance.app_payment_id)
    instance.save()
    post_save.connect(generate_AppPaymentDetails_unique_key, sender=AppPaymentDetails)


class MdPaymentPricing(models.Model):
    payment_pricing_id = models.AutoField(primary_key=True)
    org_n_key = models.CharField(max_length=50, blank=True, null=True)
    current_plan = models.CharField(max_length=50, blank=True, null=True)
    subscrib_type = models.CharField(max_length=50, blank=True, null=True)
    currentplan_amount = models.IntegerField(blank=True, null=True)
    paid_amount = models.IntegerField(blank=True, null=True)
    # plan_name = models.CharField(max_length=50, blank=True, null=True)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    # short_name = models.CharField(max_length=50, blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    created_by_id = models.CharField(max_length=50, blank=True, null=True)
    created_by_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(blank=True, null=True)
    modified_by_id = models.CharField(max_length=50, blank=True, null=True)
    modified_by_name = models.CharField(max_length=50, blank=True, null=True)
    modified_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'md_org_payment_pricing'

class MdPaymentHistory(models.Model):
    payment_history_id = models.AutoField(primary_key=True)
    org_n_key = models.CharField(max_length=50, blank=True, null=True)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    current_plan = models.CharField(max_length=50, blank=True, null=True)
    subscrib_type = models.CharField(max_length=50, blank=True, null=True)
    currentplan_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_id = models.CharField(max_length=45, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    adjustments = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    reason = models.CharField(max_length=250, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    # expire_date = models.DateTimeField(blank=True, null=True)
    gst = models.CharField(default='18',max_length=20, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    created_by_id = models.CharField(max_length=30)
    created_by_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'md_org_payment_history'

class ChatHistory(models.Model):
    chat_id = models.AutoField(primary_key=True)
    patient_n_key = models.CharField(max_length=50, blank=True, null=True)
    channelid = models.TextField(blank=True, null=True)
    type_of_chat = models.CharField(max_length=50, blank=True, null=True)
    messages = models.JSONField(blank=True, null=True)
    app_payment_n_key = models.CharField(max_length=50, blank=True, null=True)
    org_n_key = models.CharField(max_length=50, blank=True, null=True)
    hospital_n_key = models.CharField(max_length=50, blank=True, null=True)
    employee_n_key = models.JSONField(blank=True, null=True)
    created_on = models.DateTimeField()
    modified_on = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        ordering = ['chat_id']
        db_table = 'app_chat_history'

class AudioCallBalance(models.Model):
    bal_id= models.AutoField(primary_key=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    Amount = models.CharField(max_length=100, blank=True, null=True)
    #tax_amount = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_by_name = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ge_audiocallbalance'

#audiocalllog
class AudioCallLogs(models.Model):
    audio_id= models.AutoField(primary_key=True)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    callfrom = models.CharField(max_length=100, blank=True, null=True)
    callto = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    billsec = models.CharField(max_length=100, blank=True, null=True)
    credits = models.CharField(max_length=100, blank=True, null=True)
    callfromstatus = models.CharField(max_length=100, blank=True, null=True)
    calltostatus = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    telecom_provider = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'ge_audiocallogs'

class ProductGroupDetails(models.Model):
    app_prod_cat_id = models.AutoField(primary_key=True)
    app_prod_grp_key = models.CharField(max_length=30)
    hospital_n_key = models.CharField(max_length=30)
    org_n_key = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    product_amount = models.IntegerField()
    amount = models.IntegerField()
    discount_amount = models.IntegerField()
    discount = models.CharField(max_length=150)
    created_by = models.ForeignKey('EmployeesMaster',db_column='created_by_id',to_field='employee_n_key',on_delete=models.CASCADE)
    created_by_name = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField()
    minutes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'app_product_group_details'
