
from .local import Local
from .leetcode import Leetcode
import click

class Client:

    local = Local()

    leetcode = Leetcode()

    def check_login(self):
        if (not self.local.fetch_account_status()):
            self.login()
        if (not self.local.fetch_token_status()):
            self.update_token()

    def login(self):
        click.echo('You need to login first')
        username = click.prompt('Please enter your username')
        password = click.prompt('Please enter your password', hide_input=True)
        self.local.save_username_and_password(username, password)
        self.update_token()
        print('Login success')

    def update_token(self):
        user = self.local.fetch_user()
        self.leetcode.login(user['username'], user['password'])

    def submit(self, filename):
        self.leetcode.submit(filename)

    def show(self, start, end):
        self.leetcode.get_all_problems()

    def detail(self, question_id):
        return
    
    def start(self, question_id):
        return