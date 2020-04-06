class User:
    def __init__(self, user_name, password, size = None, email = None, alert = None):
        self.user_name = user_name
        self.password = password
        self.size = size
        self.email = email
        self.alert = alert
        self.dir = './'
    
    def print(self):
        print('user_name = ', self.user_name)
        print('password = ', self.password)
        if not self.size is None:
            print('size = ', self.size)
        if not self.email is None:
            print('email = ', self.email)
        if not self.alert is None:
            print('alert = ', self.alert)