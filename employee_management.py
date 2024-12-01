import core
import csv
import os
import pandas as pd

class EmployeeRecord(core.Resource):
    def __init__(self, id,name, created_at,salary, manager_name, hr_name,in_project,project_id) -> None:
        super().__init__(name, created_at)
        self.employeeID = id
        self.joining = created_at
        self.salary = salary
        self.manager = manager_name
        self.hr = hr_name
        self.in_project = in_project
        self.project_id = project_id

    def allocate(self,proid):
        self.in_project = True
        self.project_id = proid

    def release(self):
        self.in_project = False
        self.project_id = ""

    def get_status(self):
        return self.in_project
    

class Manager(core.user):
    def __init__(self, user_id, name, role,hr_name,project_id) -> None:
        super().__init__(user_id, name, role)
        self.hr = hr_name
        self.employee_id = user_id
        self.project_id = project_id

    def request_resource(self,employee_id,proid):
        if HR.employees[employee_id].in_project == False:
            HR.employees[employee_id].allocate(proid)
            self.request_update_employee_in_csv(employee_id)
        else:
            print("Resource not free")

    
    def request_update_employee_in_csv(self, employee_id):
        df = pd.read_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv')
        if employee_id in df['employeeID'].values:
            df.loc[df['employeeID'] == employee_id, ['in_project', 'project_id']] = [
                True,
                HR.employees[employee_id].project_id
            ]
            df.to_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv', index=False)
        else:
            print("Employee not found in CSV")

    def return_resource(self, employee_id):
        if employee_id in HR.employees:
            HR.employees[employee_id].release()
            self.update_employee_in_csv(employee_id)
            print("Resource returned")
        else:
            print("Employee not found")

    def update_employee_in_csv(self, employee_id):
        df = pd.read_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv')
        
        if employee_id in df['employeeID'].values:
            df.loc[df['employeeID'] == employee_id, ['in_project', 'project_id']] = [
                False,  
                ''      
            ]
            df.to_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv', index=False)
        else:
            print("Employee not found in CSV")


    def view_status(self, employee_id):
        return HR.employees[employee_id].in_project
    
class HR(core.user):
    
    employees = {}
    managers = {}


    def load_from_csv(self, employee_file_path, manager_file_path):
        if os.path.exists(employee_file_path):
            df = pd.read_csv(employee_file_path)
            if df.empty:
                print("Employee CSV file is empty.")
            else:
                for _, row in df.iterrows():
                    employee = EmployeeRecord(
                    id=row['employeeID'],
                    name=row['name'],
                    created_at=row['joining'],
                    salary=float(row['salary']),
                    manager_name=row['manager'],
                    hr_name=row['hr'],
                    in_project=row['in_project'] ,  # Convert string to boolean
                    project_id=row['project_id']
                )
                    HR.employees[employee.employeeID] = employee
        else:
            print(f"Employee file not found: {employee_file_path}")

        if os.path.exists(manager_file_path):
            df = pd.read_csv(manager_file_path)
            if df.empty:
                print("Manager CSV file is empty.")
                
            else:
                for _, row in df.iterrows():
                    manager = Manager(
                    user_id=row['employee_id'],
                    name=row['name'],
                    role=row['role'],
                    hr_name=row['hr'],
                    project_id=row['project_id']
                )
                    HR.managers[manager.employee_id] = manager
                
        else:
            print(f"Manager file not found: {manager_file_path}")

    def __init__(self, user_id, name, role) -> None:
        super().__init__(user_id, name, role)
        self.load_from_csv(r"C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv",r"C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\managers.csv")
        
    def add_employee(self, employee: EmployeeRecord):
        HR.employees[employee.employeeID] = employee
        self.update_employee_csv(employee)
        print("New Employee joined")


    def update_employee_csv(self, employee: EmployeeRecord):
        file_exists = os.path.isfile('employees.csv')
        with open(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'employeeID', 'name', 'joining', 'salary', 'manager', 'hr', 'in_project', 'project_id'
            ])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                'employeeID': employee.employeeID,
                'name': employee.name,
                'joining': employee.joining,
                'salary': employee.salary,
                'manager': employee.manager,
                'hr': employee.hr,
                'in_project': employee.in_project,
                'project_id': employee.project_id})
        

    def add_manager(self, manager: Manager):
        HR.managers[manager.employee_id] = manager
        with open(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\managers.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                manager.employee_id,
                manager.name,
                manager.role,
                manager.hr,
                manager.project_id
            ])
        print("New Manager appointed")

    def terminate_manager(self, manager_id):
        if manager_id in HR.managers:
            HR.managers.pop(manager_id)
            print(f"Manager with ID {manager_id} has been terminated.")
            self.update_manager_csv(manager_id)
        else:
            print(f"No manager found with ID {manager_id}.")

    def update_manager_csv(self, terminated_manager_id):
        if os.path.exists(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\managers.csv'):
            df = pd.read_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\managers.csv')
        
            df = df[df['employee_id'] != terminated_manager_id]
        
            df.to_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\managers.csv', index=False)
            print(f"Managers CSV updated. Manager with ID {terminated_manager_id} removed.")
        else:
            print("Managers CSV file does not exist.")


    def terminate_employee(self, employee_id):
        if employee_id in HR.employees:
            HR.employees.pop(employee_id)

            self.remove_employee_from_csv(employee_id)
            print("Employee terminated")
        else:
            print("Employee not found")
    
    
    def remove_employee_from_csv(self, employee_id):
        df = pd.read_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv')
        df = df[df['employeeID'] != employee_id]
        df.to_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv', index=False)
    

    def request_resource(self,employee_id,proid):
        if HR.employees[employee_id].in_project == False:
            HR.employees[employee_id].allocate(proid)
            self.request_update_employee_in_csv(employee_id)
        else:
            print("Resource not free")

    
    def request_update_employee_in_csv(self, employee_id):
        df = pd.read_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv')
        if employee_id in df['employeeID'].values:
            df.loc[df['employeeID'] == employee_id, ['in_project', 'project_id']] = [
                True,
                HR.employees[employee_id].project_id
            ]
            df.to_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv', index=False)
        else:
            print("Employee not found in CSV")

    def return_resource(self, employee_id):
        if employee_id in HR.employees:
            HR.employees[employee_id].release()
            self.update_employee_in_csv(employee_id)
            print("Resource returned")
        else:
            print("Employee not found")

    def update_employee_in_csv(self, employee_id):
        df = pd.read_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv')
        
        if employee_id in df['employeeID'].values:
            df.loc[df['employeeID'] == employee_id, ['in_project', 'project_id']] = [
                False,  
                ''      
            ]
            df.to_csv(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\employees.csv', index=False)
        else:
            print("Employee not found in CSV")

    def view_status(self, employee_id):
        return HR.employees[employee_id].in_project
    