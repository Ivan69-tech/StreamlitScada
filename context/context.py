class Context:
    def __init__(self):
        self.context = {}

    def add(self, key, value):
        self.context[key] = value

    def get(self, key):
        return self.context[key]
    
    def remove(self, key):
        del self.context[key]

    def clear(self):
        self.context.clear()

def newContext():
    return Context()