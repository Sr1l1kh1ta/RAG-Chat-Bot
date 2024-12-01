import core
import csv
import os

class InventoryItem(core.Resource):
    def __init__(self, id,name, created_at, stock) -> None:
        super().__init__(name, created_at)
        self.item_id = id
        self.item_name = name
        self.stock = stock

    def allocate(self,required):
        if self.stock >= required:
            return True
        return False
    
    def release(self):
        self.stock = 0

    def get_status(self):
        return self.stock

class Employee(core.user):
    def __init__(self, user_id, name, role) -> None:
        super().__init__(user_id, name, role)
        self.employeeID = user_id

    def request_resource(self,item_id,amount):
        item = WarehouseManager.catalog[item_id]
        if item.allocate(amount):
            item.stock -= amount
            self.save_resources_to_csv()

    def return_resource(self,item_id):
        item = WarehouseManager.catalog[item_id]
        item.release()

    def view_status(self,item_id):
        item = WarehouseManager.catalog[item_id]
        return item.stock
    
    
    def load_resources_from_csv(self):
        try:
            with open(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\resources.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    item = InventoryItem(row['item_id'], row['item_name'], row['created_at'], int(row['stock']))
                    WarehouseManager.catalog[item.item_id] = item
        except FileNotFoundError:
            pass

    def save_resources_to_csv(self):
        with open(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\resources.csv', mode='a', newline='') as file:
            fieldnames = ['item_id', 'item_name', 'created_at', 'stock']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in WarehouseManager.catalog.values():
                writer.writerow({
                    'item_id': item.item_id,
                    'item_name': item.item_name,
                    'created_at': item.created_at,
                    'stock': item.stock
                })



class WarehouseManager(core.user):
    catalog = {}
    employees = {}
    def __init__(self, user_id, name, role) -> None:
        super().__init__(user_id, name, role)
        self.load_resources_from_csv()
        self.load_employees_from_csv()

    def load_resources_from_csv(self):
        try:
            with open(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\resources.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    item = InventoryItem(row['item_id'], row['item_name'], row['created_at'], int(row['stock']))
                    WarehouseManager.catalog[item.item_id] = item
        except FileNotFoundError:
            pass

    def save_resources_to_csv(self):
        with open(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\resources.csv', mode='w', newline='') as file:
            fieldnames = ['item_id', 'item_name', 'created_at', 'stock']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in WarehouseManager.catalog.values():
                writer.writerow({
                    'item_id': item.item_id,
                    'item_name': item.item_name,
                    'created_at': item.created_at,
                    'stock': item.stock
                })

    def load_employees_from_csv(self):
        try:
            with open(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\emp.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    employee = Employee(row['employeeID'], row['name'], row['role'])
                    WarehouseManager.employees[employee.employeeID] = employee
        except FileNotFoundError:
            pass

    def save_employees_to_csv(self):
        with open(r'C:\Users\srilikhita.balla\Desktop\Training\MPRMS\storage\emp.csv', mode='w', newline='') as file:
            fieldnames = ['employeeID', 'name', 'role']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for employee in WarehouseManager.employees.values():
                writer.writerow({
                    'employeeID': employee.employeeID,
                    'name': employee.name,
                    'role': employee.role
                })

    def add_item(self, item: InventoryItem):
        WarehouseManager.catalog[item.item_id] = item
        self.save_resources_to_csv()
        print("Added new item " + item.item_id)

    def del_item(self, item_id):
        WarehouseManager.catalog.pop(item_id, None)
        self.save_resources_to_csv()
        print("Deleted " + item_id)

    def update_stock(self, item_id, new_stock):
        WarehouseManager.catalog[item_id].stock = new_stock
        self.save_resources_to_csv()
        print("Stock of " + item_id + " updated to " + str(new_stock))

    def request_resource(self, item_id, amount):
        item = WarehouseManager.catalog[item_id]
        if item.allocate(amount):
            item.stock -= amount
            self.save_resources_to_csv()

    def return_resource(self, item_id):
        item = WarehouseManager.catalog[item_id]
        item.release()
        self.save_resources_to_csv()

    def view_status(self, item_id):
        item = WarehouseManager.catalog[item_id]
        return item.stock

    def add_employee(self, employee: Employee):
        WarehouseManager.employees[employee.employeeID] = employee
        self.save_employees_to_csv()
        print("New Employee joined")

    def terminate_employee(self, employee_id):
        WarehouseManager.employees.pop(employee_id, None)
        self.save_employees_to_csv()
        print("Employee Terminated")

    def view_status(self,item_id):
        item = WarehouseManager.catalog[item_id]
        return item.stock



    
