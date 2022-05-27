from django.conf.urls import url
from django.urls import path
from .import views
from django.urls import include, path
from rest_framework import routers
from rest_framework import authtoken
from synapapp import views
import requests
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

# employee register
router.register(r'employeedetails', views.EmployeeDetailsViewSet)

# home price
router.register(r'paymentpricing', views.PaymentPricingViewSet)

# new page
router.register(r'subscribers', views.SubscribersViewSet)

# hospital details
router.register(r'timezone_data', views.TimeZoneViewSet)

# currency
router.register(r'currency_details', views.CurrencyDetailViewSet)

# profile
router.register(r'smspost_get', views.SmsSettingsViewSet)
router.register(r'empeducationaldetails', views.EmpeducationaldetailsViewSet)
router.register(r'employeeprofessional', views.EmployeeProfessionalViewSet)
router.register(r'employeetraining', views.EmployeeTrainingViewSet)
router.register(r'employeeteachexperience', views.EmployeeTeachExperienceViewSet)
router.register(r'employeeexperience', views.EmployeeExperienceViewSet)
router.register(r'employeerestriction', views.EmployeeRestrictionViewSet)

urlpatterns = [
url('', include(router.urls)),
# organization register
url(r'organization_register/', views.OrganizationRegister),
url(r'verify_org/',views.verify_org),
url(r'validatepassword/',views.ValidatePassword),

# multi product
url(r'sendrazor/',views.sendrazor),
url(r'payment_update/',views.Payment_Update),
url(r'discountcalculate/', views.discountcalculate),
url(r'upgradeplanchecking/', views.upgradeplanchecking),
url(r'discount_details/',views.Discount_Details),
url(r'buy_expire_calculate/',views.buy_expire_calculate),
url(r'monthlyyearcalculations/',views.monthlyyearcalculations),


# sign up
url(r'employee_login/',views.EmployeeLogin),
url(r'verify/',views.verify),
url(r'checkemployee/',views.checkemployee),
url(r'sendotp/',views.sendOTP),

# sms setting
path('sms_template/',views.SmsTemplate),
path('sms_template/<int:pk>/',views.SmsTemplateEdit),
url(r'smspayment/',views.smspayment),
url(r'amount_calculation/', views.SMSAmountCalculation),
path('smspost/',views.SmsPost),
path('smspost_get/',views.SmsGetDetails),
path('smspost/<int:pk>/',views.Sms_detail),
url(r'sms_history_detail/',views.sms_history_detail),
url(r'recharge_sms/',views.RechargeSms),
url(r'sms_template_filter/',views.SmsTemplateFilter),

# sign in
url(r'twofactorsendOTP/',views.TwoFactorsendOTP),
url(r'twofactorverifyOTP/',views.TwoFactorverifyOTP),


# roles
url(r'geunique_roles/',views.GeUnique_roles),
path('gecategorylist/',views.GECategorylist),
url(r'gerolesupdate/',views.RolesUpdate),
url(r'gerole_search/',views.Role_search),
url(r'gerole_post/',views.Role_post),
url(r'gemodules/',views.Modules),
url(r'geunique_list/',views.GetUniqueList),
url(r'roles_working_enable/',views.RolesWorkingUpdate),


# profile
url(r'check_employee_forms/',views.Check_Employee_forms),
url(r'emp_educational_details/',views.Emp_educational_details),
url(r'emp_professional/',views.Emp_professional),
url(r'emp_training/',views.Emp_training),
url(r'allform_details/',views.Allform_details),
url(r'emp_experience/',views.Emp_experience),
url(r'emp_teach_exp/',views.Emp_teach_exp),
url(r'emp_restriction/',views.Emp_restriction),
url(r'emp_profile_update/',views.Emp_profile_update),
url(r'emp_edit_details/',views.Emp_edit_details),
url(r'emp_document/',views.Empdocument),
# url(r'access_role/',views.AccessRole),
url(r'hospital_list/',views.Hospitallist),
url(r'clinic_detail/',views.Clinic_Details),
url(r'role_checkdetails/',views.Role_checkdetails),
url(r'employee_working_edit/',views.Employee_working_edit),
# url(r'employee_working_update/',views.Employee_working_update),
url(r'employeedoc_get/',views.Employeedoc_get),
path('get_clinic_workinghours/',views.getClinicWorkingHours),
path('edit_employee/',views.EditEmployeeDetails),


# otp setting
url(r'get_employeerole/',views.Get_Employeerole),
url(r'get_smspost_details/',views.Get_Smspost_Details),



# hospital details
url(r'hospital_working_details_edit/',views.Hospital_Working_Details_Edit),
url(r'hospital_working_details_update/',views.Hospital_Working_Details_Update),
url(r'logo_hospital_update/',views.Logo_hospital_update),
url(r'logo_hos_get/',views.Logo_hos_get),
url(r'hospital_master_detailpost/',views.Hospital_Master_Post),
url(r'doctor_master_update/',views.Doctor_Master_update),
url(r'check_plan_detail/',views.Check_Plan_CentreDetails),
url(r'hospital_info/',views.HospitalInfo),


# home price
url(r'employee_details_set/',views.Employee_Product_Set),


# home page
url(r'paymenthistory_details/',views.Payment_History),
url(r'CheckAllDetail/',views.CheckAllDetail),
url(r'settingscondition/',views.SettingsCondition),
url(r'checkgeneral_setting/',views.CheckGeneralSettings),
url(r'payment_check/',views.Checkpayment_home),
url(r'PaymentandHistoryUpdate/',views.PaymentandHistoryUpdate),


# generate otp
url(r'forgetpassword/',views.ForgotPassword),
url(r'forgotusername/',views.ForgotUsername),


# employee register
url(r'employee_active/',views.Employee_active),
url(r'getimage/',views.GetImage),
url(r'employee_registeration/',views.EmployeeMasterNew),
# url(r'doctoremployee_post/',views.DoctorEmployee_Post),
# url(r'Employee_working_post/',views.Employee_working_post),
url(r'delete_employees/',views.Delete_employees),
url(r'employee_update/',views.EmployeeUpdateRegister),
url(r'doctordetails_update/',views.Doctordetails_update),
url(r'employee_register_sms/',views.EmployeeRegisterSMS),
url(r'organiz_products/',views.organiz_products),
url(r'employeelists/',views.EmployeesListForHospital),
url(r'get_workinghours/',views.GetEmployeeWorkinghours),

path('gedoctordetails/',views.GeDoctorDetailsPost),
path('gedoctordetails/<int:pk>/',views.GeDoctorDetails_detail),
path('employeelog_delete/',views.Employeelog_delete),
url(r'imageupload/',views.ImageUpload),
path('add_employee_limit/',views.AddEmployeeLimit),





# forget password
url(r'forgetchangepassword/',views.ForgotChangePassword),

# currency details
url(r'currency_detail_search/',views.Currency_Detail_Search),
path('currencydetails/',views.CurrencyDetailsPost),
path('currencydetails/<int:pk>/',views.CurrencyDetails),
url(r'currencyhospital_details/',views.Currencyhospital_details),

# clinic details
url(r'clinic_timing_validation/',views.Clinic_Timing_Validation),
url(r'hospital_details/',views.HospitalDetails),
url(r'clinicalmasterpost/',views.clinicalworkpost),
url(r'clinical_working_edit/',views.Clinical_Working_Details_Edit),
url(r'clinic_working_update/',views.Clinic_working_Update),
url(r'clinical_list/',views.Clinical_List),

# change plan
url(r'changepassword/',views.ChangePasswordRegister),
path('access_check/',views.AccessCheck),

# buy product
url(r'payment_hospital_update/',views.Payment_Hospital_Update),

# token check
path('employees_tokencheck/', views.EmployeesTokenCheck),

# app products
path('app_product_post/',views.AppProductDetailsPost),
path('app_product_post/<app_prod_n_key>/',views.AppProductDetails_update),
path('app_product_list/',views.List_Products_App),
path('get_product_details/',views.Product_Details_Get),

path('doctor_calendar_search/',views.DoctorCalendarSearch),
path('medical_college_search/',views.MedicalCollegeSearch),
path('couponcode_post/',views.CouponCodePost),
path('list_promocode/',views.ListPromocode),
path('couponcode_post/<int:pk>/',views.PromoCodeUpdate),
path('patient_calendar_search/',views.PatientCalendarSearch),
path('get_orgplan/',views.GetOrgPlan),
path('cancel_orgplan/',views.Cancel_plan),
path('emp_otherdoc/',views.EmpOtherDocPost),
path('get_portaldetails/',views.GetPortalDetails),
path('enable_disable_online_practice/',views.Enable_Disable_Online_Practice),
path('get_online_practice/',views.Get_Online_Practice),
path('subscriptionstatus/',views.subscriptionstatus),

path('appointment_search/',views.Appointment_search),

# path('bloodbankpost/',views.BloodBank_Details_Post),
# path('bloodbankedit/',views.BloodBank_Detaile_Edit),
# path('bloodbankupdate/',views.BloodBank_Details_Update),
path('orgwisebloodbank/',views.BoodBank_Wise_GetData),
# path('bloodbanklogoupdate/',views.BloodBank_Logo_Update),



path('cashfree_link/', views.CreatePaymentLink.as_view()),
path('cashfree_status/', views.CashfreeStatus),
# path('org_currentplan/', views.ORGcurrentPlan),
path('payment_history_list/', views.PaymentHistory),
path('Billing_Session_Report/',views.Billing_Session_Report),
path('careme_appoint_report/',views.BillAppointmentWiseReport),
path('patient_date_report/',views.PatientDateReport),
path('attendance_report/',views.AttendanceReport),
path('organizationinvoicepost/',views.OrganisationInvoice),
path('userlimitcheck/',views.UserLimitCheck),
path('subscribed_plan/',views.SubscribedPlan),
path('org_bbname/',views.GetBloodBankName),
path('patient_uhid/',views.PatientUhid),

#BloodBankdetails
url(r'bloodbank_master_detailpost/',views.BloodBank_Master_Post),
url(r'bloodbank_details_edit/',views.BloodBank_WorkingDetails_Edit),
url(r'bloodbank_details_update/',views.BloodBank_WorkingDetails_Update),
url(r'bloodbank_limt_check/',views.BloodBank_Limit_Check),
url(r'bloodbank_logo_update/',views.BloodBank_Logo_Update),
url(r'bloodbank_logo_get/',views.BloodBank_Logo_get),
url(r'organisationwise_getdata/',views.OrganisationWise_GetData),

url(r'followupcountcheck/',views.FollowupCountCheck),
path('add_credits_app/',views.AddCreditsSessionAppoint),
path('new_credits_app/',views.NewCreditsSessionAppoint),
path('credits_payment/',views.creditsPaymentCheck),
url(r'careteam_book_appointment/',views.CareTeam_Book_Appointment),
path('product_group/',views.ProductGroup),


url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
