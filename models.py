class Destination:
    def __init__(self, id, name, description, location):
        self.id = id
        self.name = name
        self.description = description
        self.location = location

class Itinerary:
    def __init__(self, id, destination_id, activity):
        self.id = id
        self.destination_id = destination_id
        self.activity = activity

class Expense:
    def __init__(self, id, destination_id, expense_category, amount):
        self.id = id
        self.destination_id = destination_id
        self.expense_category = expense_category
        self.amount = amount
