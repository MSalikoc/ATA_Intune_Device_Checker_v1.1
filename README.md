### ATA-Intune-Device-Checker_v1.1

## Release Update
# What is News ?
With this tool, you can access details such as 𝐂𝐨𝐦𝐩𝐥𝐢𝐚𝐧𝐜𝐞 𝐒𝐭𝐚𝐭𝐮𝐬, 𝐋𝐚𝐬𝐭 𝐒𝐲𝐧𝐜 𝐃𝐚𝐭𝐞, 𝐒𝐞𝐫𝐢𝐚𝐥 𝐍𝐮𝐦𝐛𝐞𝐫, and more. You can also take actions on these devices, which was not possible in the first version. With this update, you can now take action on devices.

📢 What are these actions?
- ✔️Sync
- ✔️Delete
- ✔️Retire
- ✔️Wipe

You can apply these actions to a single device or multiple devices at once.
- 🔥 The updated interface is now simpler and more user-friendly.


# Medium Blog 
https://medium.com/@m365alikoc/ata-intune-device-checker-tool-release-update-version-1-1-a0fba2bfc25f
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
