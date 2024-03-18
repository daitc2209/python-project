def user_serializer(todo) -> dict:
    return {
        "id":str(todo["_id"]),
        "name":todo["name"],
        "description": todo["description"],
        "completed": todo["completed"]
    }

def users_serializer(todos) -> list:
    return [user_serializer(todo) for todo in todos]