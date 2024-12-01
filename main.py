from library import Book,Member,Librarian
from inventory import InventoryItem,Employee,WarehouseManager
from employee_management import EmployeeRecord,HR,Manager
import concurrent.futures
import threading
import time

class LibraryManagementSystemDemo:
    @staticmethod
    def run():
        library_manager = Librarian("l1","natty","admin")

        
        library_manager.add_book(Book("ISBN1", "Book 1", "Author 1", 2020,True))
        library_manager.add_book(Book("ISBN2", "Book 2", "Author 2", 2019,True))
        library_manager.add_book(Book("ISBN3", "Book 3", "Author 3", 2021,True))

     
        library_manager.register_member(Member("M1", "John Doe","member", "john@example.com"))
        library_manager.register_member(Member("M2", "Jane Smith","member", "jane@example.com"))

        library_manager.request_resource("M1", "Book 1")
        library_manager.request_resource("M2", "Book 2")

        library_manager.return_resource("M1", "ISBN1")

        search_results = library_manager.search_books("Book")
        print("Search Results:")
        for book in search_results:
            print(f"{book.title} by {book.author}")

class InventoryManagementSystemDemo:
    def run():
        inventory_manager = WarehouseManager("u10", "Rishi", "manager")
        e1 = Employee("id_11", "Ravi", "employee")
        e2 = Employee("id_12", "Raasi", "employee")
        e3 = Employee("id_13", "Rahul", "employee")
        
        def add_employees():
            inventory_manager.add_employee(e1)
            inventory_manager.add_employee(e2)
            inventory_manager.add_employee(e3)
            print("Employees added.")

        def add_items():
            inventory_manager.add_item(InventoryItem("i1", "Rice", "11-02-2024", 10))
            inventory_manager.add_item(InventoryItem("i2", "Dal", "11-02-2024", 100))
            inventory_manager.add_item(InventoryItem("i3", "Paneer", "11-02-2024", 10))
            print("Items added.")

        def manager_request():
            inventory_manager.request_resource("i1", 30)
            print(f"Manager {inventory_manager.name} requested 30 units of Rice.")

        def employee_request():
            e1.request_resource("i1", 50)
            print(f"Employee {e1.name} requested 50 units of Rice.")

        def return_resource_by_manager():
            try:
                inventory_manager.return_resource("i2")
                print(f"Manager {inventory_manager.name} returned resource i2")
            except KeyError as e:
                print(f"KeyError in return_resource_by_manager: {e}")

        def return_resource_by_employee():
            try:
                e1.return_resource("i1")
                print(f"Employee {e1.name} returned resource Rice.")
            except KeyError as e:
                print(f"KeyError in return_resource_by_employee: {e}")

        def update_stock():
            inventory_manager.update_stock("i2", 50)
            print("Stock of Dal updated to 50.")

        def terminate_employee():
            inventory_manager.terminate_employee("id_12")
            print("Employee Raasi terminated.")

        # Create and start threads
        threads = [
            threading.Thread(target=add_employees),
            threading.Thread(target=add_items),
            threading.Thread(target=manager_request),
            threading.Thread(target=employee_request),
            threading.Thread(target=return_resource_by_manager),
            threading.Thread(target=return_resource_by_employee),
            threading.Thread(target=update_stock),
            threading.Thread(target=terminate_employee),
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

class EmployeeManagementSystemDemo:
    def run():
        hr = HR("h1","Riya","hr")
        m1 = Manager("m1","ravi","manager","Riya","123")
        hr.add_manager(Manager("m1","ravi","manager","Riya","123"))

        hr.add_employee(EmployeeRecord("e1","mani","jan 2024","20000","ravi","Riya",False,""))
        hr.add_employee(EmployeeRecord("e2","mouni","jan 2024","20000","ravi","Riya",False,""))
        hr.add_employee(EmployeeRecord("e3","maneesh","jan 2024","20000","ravi","Riya",False,""))

        # m1.request_resource("e1","123")
        # m1.return_resource("e1")

        # hr.terminate_employee("e1")
        hr.terminate_manager("m1")

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

        pool.submit(hr.add_manager(Manager("m1","ravi","manager","Riya","123")))
        pool.submit(hr.add_employee(EmployeeRecord("e1","mani","jan 2024","20000","ravi","Riya",False,"")))
        pool.submit(hr.add_employee(EmployeeRecord("e2","mouni","jan 2024","20000","ravi","Riya",False,"")))
        pool.submit(hr.terminate_manager("m1"))
        pool.submit(hr.add_employee(EmployeeRecord("e3","maneesh","jan 2024","20000","ravi","Riya",False,"")))
        

        pool.shutdown(wait=True)

        print("Main thread continuing to run")

class ProjectManagementDemo:
    def run():
        pass

if __name__ == "__main__":
    # LibraryManagementSystemDemo.run()
    InventoryManagementSystemDemo.run()
    # EmployeeManagementSystemDemo.run()
    # ProjectManagementDemo.run()
    