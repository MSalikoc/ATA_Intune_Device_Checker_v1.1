import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import msal
import requests
import logging
import csv
import os

# Global variables
DEVICE_DATA = []
GRAPH_API_URL = 'https://graph.microsoft.com/v1.0/'

# Logging configuration
logging.basicConfig(level=logging.INFO, filename="device_operations_log.log", 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Page class as a base class for different pages in the app
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

# Function to authenticate with Microsoft Graph
def authenticate(client_id, tenant_id):
    authority = f'https://login.microsoftonline.com/{tenant_id}'
    app = msal.PublicClientApplication(client_id, authority=authority)

    # Try to acquire token silently
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(["Device.Read.All", "DeviceManagementManagedDevices.ReadWrite.All", 
                                           "DeviceManagementManagedDevices.PrivilegedOperations.All"], account=accounts[0])
        if result and "access_token" in result:
            return result["access_token"]

    # If silent acquisition fails, initiate device flow
    scopes = ["Device.Read.All", "DeviceManagementManagedDevices.ReadWrite.All", "DeviceManagementManagedDevices.PrivilegedOperations.All"]
    flow = app.initiate_device_flow(scopes=scopes)

    if "user_code" not in flow:
        messagebox.showerror("Error", "Failed to create device flow")
        return None

    web_auth_button = messagebox.askyesno("Open Browser", "Do you want to open the browser for authentication?")
    if web_auth_button:
        import webbrowser
        webbrowser.open(flow['verification_uri'])
    
    messagebox.showinfo("Authenticate", f"Please authenticate using this code: {flow['user_code']}")
    
    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        return result["access_token"]
    else:
        messagebox.showerror("Error", f"Authentication failed: {result.get('error_description', 'Unknown error')}")
        return None

# Data Fetch Page with action capabilities
class DataPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Device Information Check", font=("Arial", 18), pady=10)
        label.pack(side="top", fill="both", expand=True)

        # Dropdown menu for action selection
        self.action_var = tk.StringVar(value="Sync")
        actions = ["Delete", "Retire", "Wipe", "Sync"]
        self.action_menu = tk.OptionMenu(self, self.action_var, *actions)
        self.action_menu.pack(pady=5)

        # Search Section
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        self.search_input = tk.Entry(search_frame, width=30)
        self.search_input.grid(row=0, column=0, padx=5)

        tk.Button(search_frame, text="Search by Device Name", command=self.search_by_device_name).grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Search by User Principal Name", command=self.search_by_user_name).grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Get All Devices", command=self.get_all_devices).grid(row=0, column=3, padx=5)

        # Action and Export Buttons
        action_frame = tk.Frame(self)
        action_frame.pack(pady=10)

        self.action_button = tk.Button(action_frame, text="Apply Action", command=self.apply_selected_action, pady=5, padx=20)
        self.action_button.grid(row=0, column=0, padx=10)

        self.export_button = tk.Button(action_frame, text="Export to CSV", command=self.export_to_csv, pady=5, padx=20)
        self.export_button.grid(row=0, column=1, padx=10)

        # Table Section
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="lightgrey")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar_x = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        scrollbar_y = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y.pack(side="right", fill="y")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="lightblue")
        style.configure("Treeview", font=("Arial", 10), background="white", foreground="black", rowheight=25)

        self.tree = ttk.Treeview(canvas, columns=("Device Name", "Model", "Compliance Status", "Last Sync Date Time", 
                                                  "Device Manufacturer", "Operating System", "OS Version", 
                                                  "Serial Number", "Ownership", "Device ID"), show="headings", selectmode="extended")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        canvas.create_window((0, 0), window=self.tree, anchor="nw")
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"), xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    def fetch_device_details(self, token, filter_query=""):
        global DEVICE_DATA
        DEVICE_DATA.clear()
        headers = {'Authorization': f'Bearer {token}'}
        url = GRAPH_API_URL + 'deviceManagement/managedDevices'
        if filter_query:
            url += f"?$filter={filter_query}"

        while url:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                DEVICE_DATA.extend(data.get('value', []))
                url = data.get('@odata.nextLink', None)
            else:
                messagebox.showerror("Error", f"Failed to fetch devices: {response.text}")
                return False
        self.display_data()
        return True

    def display_data(self):
        self.tree.delete(*self.tree.get_children())
        for i, device in enumerate(DEVICE_DATA):
            values = [
                device.get("deviceName", 'N/A'),
                device.get("model", 'N/A'),
                device.get("complianceState", 'N/A'),
                device.get("lastSyncDateTime", 'N/A'),
                device.get("manufacturer", 'N/A'),
                device.get("operatingSystem", 'N/A'),
                device.get("osVersion", 'N/A'),
                device.get("serialNumber", 'N/A'),
                device.get("ownership", 'N/A'),
                device.get("id", 'N/A')
            ]
            self.tree.insert("", tk.END, values=values)

    def search_by_device_name(self):
        token = self.master.token
        device_name = self.search_input.get()
        if device_name:
            self.fetch_device_details(token, f"deviceName eq '{device_name}'")
        else:
            messagebox.showerror("Error", "Please enter a device name")

    def search_by_user_name(self):
        token = self.master.token
        user_name = self.search_input.get()
        if user_name:
            self.fetch_device_details(token, f"userPrincipalName eq '{user_name}'")
        else:
            messagebox.showerror("Error", "Please enter a user name")

    def get_all_devices(self):
        token = self.master.token
        self.fetch_device_details(token)

    def apply_selected_action(self):
        token = self.master.token
        selected_items = self.tree.selection()
        action = self.action_var.get()

        if not selected_items:
            messagebox.showerror("Error", "No devices selected for the action")
            return

        for selected_item in selected_items:
            device_id = self.tree.item(selected_item)["values"][-1]  # Fetching the last column value (Device ID)
            confirmation = messagebox.askyesno("Confirmation", f"Do you want to {action} the device with ID: {device_id}?")
            if confirmation:
                if action == "Sync":
                    self.sync_device_via_graph(token, device_id)
                elif action == "Retire":
                    self.retire_device_via_graph(token, device_id)
                elif action == "Delete":
                    self.delete_device_via_graph(token, device_id)
                elif action == "Wipe":
                    self.wipe_device_via_graph(token, device_id)

    # Action functions for each operation
    def sync_device_via_graph(self, token, device_id):
        url = f"{GRAPH_API_URL}deviceManagement/managedDevices/{device_id}/syncDevice"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(url, headers=headers)
        self.handle_response(response, "Sync")

    def retire_device_via_graph(self, token, device_id):
        url = f"{GRAPH_API_URL}deviceManagement/managedDevices/{device_id}/retire"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(url, headers=headers)
        self.handle_response(response, "Retire")

    def delete_device_via_graph(self, token, device_id):
        url = f"{GRAPH_API_URL}deviceManagement/managedDevices/{device_id}"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(url, headers=headers)
        self.handle_response(response, "Delete")

    def wipe_device_via_graph(self, token, device_id):
        url = f"{GRAPH_API_URL}deviceManagement/managedDevices/{device_id}/wipe"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(url, headers=headers)
        self.handle_response(response, "Wipe")

    def handle_response(self, response, action_name):
        if response.status_code in (200, 204):
            messagebox.showinfo("Success", f"{action_name} action completed successfully.")
        else:
            error_message = response.json().get('error', {}).get('message', 'Unknown error occurred')
            messagebox.showerror("Error", f"Failed to {action_name} device: {error_message}")

    # Export the device list to CSV
    def export_to_csv(self):
        if not DEVICE_DATA:
            messagebox.showerror("Error", "No data available to export")
            return
        try:
            filepath = "C:\\device_data.csv"
            with open(filepath, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Device Name", "Model", "Compliance Status", "Last Sync Date Time", 
                                 "Device Manufacturer", "Operating System", "OS Version", 
                                 "Serial Number", "Ownership", "Device ID"])
                for device in DEVICE_DATA:
                    writer.writerow([
                        device.get("deviceName", 'N/A'),
                        device.get("model", 'N/A'),
                        device.get("complianceState", 'N/A'),
                        device.get("lastSyncDateTime", 'N/A'),
                        device.get("manufacturer", 'N/A'),
                        device.get("operatingSystem", 'N/A'),
                        device.get("osVersion", 'N/A'),
                        device.get("serialNumber", 'N/A'),
                        device.get("ownership", 'N/A'),
                        device.get("id", 'N/A')
                    ])
            messagebox.showinfo("Success", f"Data exported to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")

# Authentication Page
class AuthPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Intune Device Checker Authentication Page", font=("Arial", 18), pady=5)
        label.pack(side="top", fill="both", expand=True)

        self.client_id_label = tk.Label(self, text="Client ID:", pady=5)
        self.client_id_label.pack()
        self.client_id_entry = tk.Entry(self)
        self.client_id_entry.pack()

        self.tenant_id_label = tk.Label(self, text="Tenant ID:", pady=5)
        self.tenant_id_label.pack()
        self.tenant_id_entry = tk.Entry(self)
        self.tenant_id_entry.pack()

        self.auth_button = tk.Button(self, text="Authenticate", command=self.authenticate, pady=5, padx=20)
        self.auth_button.pack(pady=10)

    def authenticate(self):
        client_id = self.client_id_entry.get()
        tenant_id = self.tenant_id_entry.get()
        if not client_id or not tenant_id:
            messagebox.showerror("Error", "Client ID and Tenant ID are required!")
            return

        token = authenticate(client_id, tenant_id)
        if token:
            self.master.token = token
            messagebox.showinfo("Success", "Authentication Successful")
            self.master.device_page.show()

# Main Application
class MainApplication(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.token = None
        self.pack(fill="both", expand=True)

        # Create pages
        self.auth_page = AuthPage(self)
        self.device_page = DataPage(self)

        # Stack pages
        self.auth_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        self.device_page.place(in_=self, x=0, y=0, relwidth=1, relheight=1)

        self.auth_page.show()

# Initialize the application
root = tk.Tk()
root.geometry("800x600")  # Updated window size for better layout
root.title("ATA Microsoft Intune Device Checker")
app = MainApplication(root)
root.mainloop()
