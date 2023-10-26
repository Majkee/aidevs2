class Message:
    def __init__(self, role: str, content: str, name: str = None):
        self.role = role
        self.content = content
        self.name = name