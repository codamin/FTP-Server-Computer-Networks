class User:
    def __init__(self, id, password, size = None, email = None, alert = None):
        self.id = id
        self.password = password
        self.size = size
        self.email = email
        self.alert = alert
    
    def print(self):
        print('id = ', self.id)
        print('password = ', self.password)
        if not self.size is None:
            print('size = ', self.size)
        if not self.email is None:
            print('email = ', self.email)
        if not self.alert is None:
            print('alert = ', self.alert)