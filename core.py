class Resource:
    def __init__(self,name,created_at) -> None:
        self.name = name
        self.created_at = created_at
    def allocate(self):
        pass
    def release(self):
        pass
    def get_status(self):
        pass


class user:
    def __init__(self,user_id,name,role) -> None:
        self.user_id = user_id
        self.name = name
        self.role = role
    def request_resource(self):
        pass
    def return_resource(self):
        pass
    def view_status(self):
        pass

