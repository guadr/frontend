class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.id)
