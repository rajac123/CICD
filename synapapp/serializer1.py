from synapapp import models
from rest_framework import serializers
# employee register
class GeDoctorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GeDoctorDetails
        fields = '__all__'
class EmployeesMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.EmployeesMaster
        fields='__all__'
class DoctorWorkingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.DoctorWorkingDetails
        fields='__all__'
class DoctorSpecialHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.DoctorSpecialHours
        fields='__all__'
class EmployeeLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.EmployeeLogs
        fields='__all__'

# hospital details
class TimeZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.MdTimeZone
        fields='__all__'

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.HospitalMaster
        fields='__all__'
class HospitalMasterSerializer(serializers.ModelSerializer):
   class Meta:
       model=models.HospitalMaster
       fields='__all__'

class Attachmentsserializer(serializers.ModelSerializer):
    class Meta:
        model=models.Attachments
        fields='__all__'

class HospitalWorkingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.HospitalWorkingDetails
        fields='__all__'

class HospitalSpecialHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.HospitalSpecialHours
        fields='__all__'                

# roles        
class GeModulesSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.GeModules
        fields='__all__'

class BBRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.BBRoles
        fields='__all__'        

# class BBModulesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.BBModules
#         fields='__all__'        

class RoleNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.RoleNames
        fields='__all__'

class GERolesSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.GERoles
        fields='__all__'
class MdAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.MdAccess
        fields='__all__'

# buy product        
# class PaymentPricingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.PaymentPricing
#         fields='__all__'

# class PaymentHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.PaymentHistory
#         fields='__all__'

class PlanDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.PlanDetails
        fields='__all__'        


# organisation register
class OrganizationMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.OrganizationMaster
        fields='__all__'


# sms settings
class SMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SmsSettings
        fields = '__all__'
class SmsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SmsHistory
        fields = '__all__'
class SmsPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SmsPaymentHistory
        fields = '__all__'
class SmsTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.SmsTemplateSettings
        fields='__all__'


# clinic details
class ClinicalMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ClinicalMaster
        fields='__all__'

class ClinicalWorkingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ClinicalWorkingDetails
        fields='__all__'

class ClinicalSpecialHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ClinicalSpecialHours
        fields='__all__'

# currency details
class CurrencyTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CurrencyTable
        fields = '__all__'
class CurrencyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CurrencyDetails
        fields='__all__'
class CurrencyDetailsTableSerializer(serializers.ModelSerializer):
    currency_id = CurrencyTableSerializer(read_only=True)
    class Meta:
        model = models.CurrencyDetails
        fields = '__all__'

# new page       
class SubScribersSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.SubscribersMaster
        fields='__all__'

# profile
class EmployeedocumentsSerializer(serializers.ModelSerializer):
   class Meta:
       model=models.Employeedocuments
       fields='__all__'

class EmpeducationaldetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.Empeducationaldetails
        fields='__all__'
class EmployeeProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.EmployeeProfessional
        fields='__all__'
class EmployeeTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.EmployeeTraining
        fields='__all__'
class EmployeeExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.EmployeeExperience
        fields='__all__'
class EmployeeTeachExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.EmployeeTeachExperience
        fields='__all__'
class EmployeeRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.EmployeeRestriction
        fields='__all__'

class CalendarSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CalendarSettings
        fields='__all__'

class AppProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.AppProductDetails
        fields='__all__'

class AppProductDetailsSerializer_GET(serializers.ModelSerializer):
    class Meta:
        model =models.AppProductDetails
        exclude = ('hospital_n_key','org_n_key','created_by_id','created_by_name','created_on','modified_by_id','modified_by_name','modified_on')

class MedicalCollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.MedicalCollege
        fields='__all__'

class PromoCodeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model =models.PromoCodeDetails
        fields='__all__'
        
class PatientMasterSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    class Meta:
        model=models.PatientMaster
        fields='__all__'

class EmployeeOtherDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.EmployeeOtherDocument
        fields='__all__'

# class BloodBankMasterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=models.BloodBankMaster
#         fields='__all__'
class BloodBankWorkingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.BloodBankWorkingDetails
        fields='__all__'
class BloodBankSpecialHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.BloodBankSpecialHours
        fields='__all__' 

class AppointmentCreditsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.AppointmentCredits
        fields='__all__'

class MdPaymentPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.MdPaymentPricing
        fields='__all__'
class MdPaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.MdPaymentHistory
        fields='__all__'

class AppointmentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppointmentMaster
        fields = '__all__'
    def create(self, validated_data):
        appoint = models.AppointmentMaster.objects.create(**validated_data)
        if appoint.clinical_n_key != None and appoint.clinical_n_key != '':
            appoint.appointment_n_key = appoint.clinical_n_key[:3]+"-APT-"+str(appoint.appointment_id)
        else:
            appoint.appointment_n_key = appoint.hospital_n_key[:3]+"-APT-"+str(appoint.appointment_id)
        appoint.encounter_id = "ENC-"+str(appoint.appointment_id)
        appoint.save()
        return appoint

class AppSessionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppSessionDetails
        fields = '__all__'

class InvoiceBillPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.InvoiceBillPayment
        fields='__all__'

class InvoiceBillDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.InvoiceBillDetails
        fields='__all__'

#new BloodBank_post
class BloodBankMasterSerializer(serializers.ModelSerializer):
   class Meta:
       model=models.BloodBank_Master
       fields='__all__'

class AppPaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.AppPaymentDetails
        fields='__all__'

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model =models.ChatHistory
        fields='__all__'

class AppointmentSortSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.AppointmentMaster
        fields=('appointment_id','appointment_n_key','patient_n_key','appointment_date','appointment_time','appointment_end_time','doc_app_id','service_name','appointment_type','overall_status','payment_type')
        