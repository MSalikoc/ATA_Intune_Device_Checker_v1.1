# ATA_Intune_Device_Checker_v1.1

## ATA-Intune-Device-Checker_v1.1
# Medium Blog 
[https://medium.com/@m365alikoc/ata-intune-device-checker-tool-c9ee8ea6b0f9](https://medium.com/@m365alikoc/ata-intune-device-checker-tool-c9ee8ea6b0f9)

# Prerequisite

Düzenlemek için Python uygulamasına ihtiyaç duymaktasınız.
Kod Python ile yazılmıştır, bu yüzden sisteminizde Python 3.x sürümü kurulu olmalıdır.
Python'un kurulu olup olmadığını şu komut ile terminal veya komut satırında kontrol edebilirsiniz:
'python --version'

# Microsoft Azure App Registration
Azure Active Directory'de bir App Registration yapmanız gerekmektedir.
Client ID ve Tenant ID bilgileri bu kodda zaten tanımlanmış durumda. Ancak bu bilgilerin gerçek ve doğru olduğundan emin olmanız gerekir. Eğer kendi uygulamanızı kullanacaksanız, aşağıdaki adımları izleyerek bir App Registration oluşturun:
Azure Portal'a gidin ve Azure Active Directory bölümüne girin.
App Registrations altından yeni bir uygulama kaydedin.
Kaydettikten sonra, Application (client) ID ve Directory (tenant) ID bilgilerinizi alabilirsiniz.
# Kodda scopes olarak kullanılan izinleri 
- Device.Read.All
- DeviceManagementManagedDevices.Read.All
- DeviceManagementManagedDevices.PrivilegedOperations.All
- DeviceManagementManagedDevices.ReadWrite.All
uygulamanızın izinlerine eklemeniz gerekir.
# Microsoft Graph API Erişim Yetkileri
Azure portalında uygulamanızın API permissions bölümüne gidin ve aşağıdaki izinleri eklediğinizden emin olun:
- Device.Read.All
- DeviceManagementManagedDevices.Read.All
- DeviceManagementManagedDevices.PrivilegedOperations.All
- DeviceManagementManagedDevices.ReadWrite.All
Gerekli izinleri ekledikten sonra admin consent verildiğinden emin olun.

# Kullanıcı Hesabı
Bu uygulama, cihaz bilgilerine erişmek için kullanıcı kimliğiyle Microsoft Graph API'ye kimlik doğrulaması yapacak. Bu nedenle, uygulamanın çalıştığı ortamda Microsoft 365'e bağlı bir kullanıcı hesabı olmalıdır.
Uygulama çalışırken kullanıcıdan kimlik doğrulaması yapması istenir. Uygulama, cihaz bilgilerini çekmek için kullanıcıya bir doğrulama kodu sağlar.

## Setup

- Uygulamayı çalıştırın (Ataversion1.1.exe)
- Daha sonra Tenant ID ve Client ID bilgilerinizi girerek Authorization işlemlerini başlatın
- Authorization sonrası sorgulamak istediğiniz cihaz ismi veya kullanıcı ismini girerek detaylara erişebilirsiniz.

## UI 

https://www.youtube.com/watch?v=fclQSSk4Rvg&t
