class User:
    def __init__(self,browser,username):
        self.browser = browser
        self.username = username

    def get_user(self):
        return self.username

    def get_browser(self):
        return self.browser