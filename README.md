### ATA-Intune-Device-Checker_v1.1

## Release Update
# What is News ?
With this tool, you can access details such as 𝐂𝐨𝐦𝐩𝐥𝐢𝐚𝐧𝐜𝐞 𝐒𝐭𝐚𝐭𝐮𝐬, 𝐋𝐚𝐬𝐭 𝐒𝐲𝐧𝐜 𝐃𝐚𝐭𝐞, 𝐒𝐞𝐫𝐢𝐚𝐥 𝐍𝐮𝐦𝐛𝐞𝐫, and more. You can also take actions on these devices, which was not possible in the first version. With this update, you can now take action on devices.

📢 What are these actions?
- ✔️Sync
- ✔️Delete
- ✔️Retire
- ✔️Wipe
- .

You can apply these actions to a single device or multiple devices at once.
- 🔥 The updated interface is now simpler and more user-friendly.


# Medium Blog 
https://medium.com/@m365alikoc/ata-intune-device-checker-tool-release-update-version-1-1-a0fba2bfc25f
# Prerequisite

To make adjustments, you need a Python application. The code is written in Python, so you must have Python 3.x installed on your system. You can check if Python is installed by running the following command in your terminal or command prompt: python --version.

# Microsoft Azure App Registration
You will need to create an App Registration in Azure Active Directory. The Client ID and Tenant ID are already defined in the code, but you should ensure these values are accurate. 

If you’re using your own application, follow the steps below to create an App Registration: Go to the Azure Portal, navigate to the Azure Active Directory section, and select App Registrations to register a new application. 

After registering, you can obtain your Application (client) ID and Directory (tenant) ID.

# Permissions used as scopes in the scripti 
- Device.Read.All
- DeviceManagementManagedDevices.Read.All
- DeviceManagementManagedDevices.PrivilegedOperations.All
- DeviceManagementManagedDevices.ReadWrite.All
uygulamanızın izinlerine eklemeniz gerekir.
# Microsoft Graph API Access Authorizations
In the Azure portal, go to the API permissions section of your application and make sure to add the following permissions:
- Device.Read.All
- DeviceManagementManagedDevices.Read.All
- DeviceManagementManagedDevices.PrivilegedOperations.All
- DeviceManagementManagedDevices.ReadWrite.All

After adding the necessary permissions, make sure admin consent is granted.

# User Account
This app will authenticate to the Microsoft Graph API with the user ID to access device information. Therefore, there must be a user account connected to Microsoft 365 in the environment where the app is running.

When the app is running, the user will be prompted to authenticate. The app provides the user with a verification code to pull device information.

## Setup
- Run the application (Ataversion1.1.exe)
- Then enter your Tenant ID and Client ID information and start Authorization process
- After authorization, you can access the details by entering the device name or user name you want to query.

## UI 

https://www.youtube.com/watch?v=fclQSSk4Rvg&t
