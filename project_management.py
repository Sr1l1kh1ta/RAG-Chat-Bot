import core

class Task(core.Resource):
    def __init__(self, name, created_at) -> None:
        super().__init__(name, created_at)

class TaskMember(core.user):
    def __init__(self, user_id, name, role) -> None:
        super().__init__(user_id, name, role)

