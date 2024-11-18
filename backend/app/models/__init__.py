
import importlib

def dynamic_import(model_name: str):
    return importlib.import_module(f'app.models.{model_name}')

AuditInfo = dynamic_import("auditinfo").AuditInfo
AuditInfoCreate = dynamic_import("auditinfo").AuditInfoCreate
AuditInfoUpdate = dynamic_import("auditinfo").AuditInfoUpdate
Currency = dynamic_import("currency").Currency
CurrencyFormat = dynamic_import("currency").CurrencyFormat
CustomizationInfo = dynamic_import("customizationinfo").CustomizationInfo
CustomizationInfoCreate = dynamic_import("customizationinfo").CustomizationInfoCreate
CustomizationInfoUpdate = dynamic_import("customizationinfo").CustomizationInfoUpdate
GeoIP = dynamic_import("networklocationdata").GeoIP
IPAddress = dynamic_import("networklocationdata").IPAddress
IPAddressUpdate = dynamic_import("networklocationdata").IPAddressUpdate
Item = dynamic_import("items").Item
ItemCreate = dynamic_import("items").ItemCreate
ItemUpdate = dynamic_import("items").ItemUpdate
ItemPublic = dynamic_import("items").ItemPublic
ItemsPublic = dynamic_import("items").ItemsPublic
PageView = dynamic_import("engagementmetrics").PageView
Post = dynamic_import("engagementmetrics").Post
Comment = dynamic_import("engagementmetrics").Comment
SocialConnection = dynamic_import("engagementmetrics").SocialConnection
OTP = dynamic_import("otp").OTP
Payment = dynamic_import("payments").Payment
PaymentStatus = dynamic_import("payments").PaymentStatus
PaymentProvider = dynamic_import("payments").PaymentProvider
PaymentCreate = dynamic_import("payments").PaymentCreate
PaymentUpdate = dynamic_import("payments").PaymentUpdate
Professional = dynamic_import("professional").Professional
Profile = dynamic_import("profile").Profile
Role = dynamic_import("role").Role
Service = dynamic_import("service").Service
Settings = dynamic_import("settings").Settings
SettingsCreate = dynamic_import("settings").SettingsCreate
SettingsUpdate = dynamic_import("settings").SettingsUpdate
Status = dynamic_import("settings").Status
StatusCreate = dynamic_import("settings").StatusCreate
StatusUpdate = dynamic_import("settings").StatusUpdate
Theme = dynamic_import("theme").Theme
ThemeCreate = dynamic_import("theme").ThemeCreate
ThemeUpdate = dynamic_import("theme").ThemeUpdate
User = dynamic_import("user").User
UserCreate = dynamic_import("user").UserCreate
UserUpdate = dynamic_import("user").UserUpdate
UserUpdateMe = dynamic_import("user").UserUpdateMe
UserPublic= dynamic_import("user").UserPublic
UsersPublic = dynamic_import("user").UsersPublic
UserRegister = dynamic_import("user").UserRegister
UserRole = dynamic_import("userrole").UserRole
Token = dynamic_import("user").Token
TokenPayload = dynamic_import("user").TokenPayload
Territory = dynamic_import("user").Territory
Message = dynamic_import("user").Message
NewPassword = dynamic_import("user").NewPassword
UpdatePassword = dynamic_import("user").UpdatePassword
