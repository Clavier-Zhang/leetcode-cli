
from .cache import cache
from .leetcode import leetcode
from .system import system
from .config import lang_dict
from .screen import screen
import click

class Client:

    # login methods
    def check_login(self):
        if (not cache.check_user_account_statue()):
            self.login()
        if (not cache.check_user_token_statue()):
            if not self.update_token():
                self.login()

    def login(self):
        while True:
            username = click.prompt('Please enter your username')
            password = click.prompt('Please enter your password', hide_input=True)
            cache.save_username_and_password(username, password)
            if leetcode.login(username, password):
                screen.print_login_success_message()
                break
            else:
                screen.print_login_fail_message()

    def logout(self):
        cache.clear_user()
        screen.print_logout_success_message()
        
    def update_token(self):
        username = cache.get_user_username()
        password = cache.get_user_password()
        return leetcode.login(username, password)

    def lang(self, lang):
        cache.save_user_lang(lang)
        screen.print_update_lang_message(lang)


    # question methods
    def submit(self, filename):
        leetcode.submit(filename)

    def show(self, start, end):
        if not cache.check_question_index_status():
            leetcode.fetch_all_questions()
        screen.print_question_summarys(cache.get_question_summarys_by_range(start, end))
        

    def detail(self, question_id):
        # check the index of problems
        if not cache.check_question_index_status():
            leetcode.fetch_all_questions()
        # use the problem index to convert question_id to title_slug
        problem_summary = cache.get_question_summary_by_question_id(question_id)
        if (problem_summary == None):
            print("the problem does not exist")
            return None
        problem_slug = problem_summary['stat']['question__title_slug']
        # if the detail is not in the cache, fetch from leetcode
        if not cache.check_question_detail_status_by_question_id(question_id):
            leetcode.fetch_question_detail(problem_slug)

        question_detail = cache.get_question_detail_by_question_id(question_id)
        screen.print_question_detail(question_detail)
        return question_detail
    
    def start(self, question_id):
        # check user's language
        if not cache.check_user_lang_status():
            lang = click.prompt('Please enter your preferred language')
            if lang not in lang_dict:
                print('does not support this language')
                return
            cache.save_user_lang(lang)
        lang = cache.get_user_lang()
        # check the index of problems
        if not cache.check_question_index_status():
            leetcode.fetch_all_questions()
        # use the problem index to convert question_id to title_slug
        problem_summary = cache.get_question_summary_by_question_id(question_id)
        if (problem_summary == None):
            print("the problem does not exist")
            return None
        problem_slug = problem_summary['stat']['question__article__slug']

        # if the detail is not in the cache, fetch from leetcode
        if not cache.check_question_detail_status_by_question_id(question_id):
            leetcode.fetch_question_detail(problem_slug)

        question_detail = cache.get_question_detail_by_question_id(question_id)
        if question_detail == None:
            return
        code_templates = question_detail['codeSnippets']
        sample_test_case = question_detail['sampleTestCase']
        for code_template in code_templates:
            if code_template['langSlug'] == lang:
                system.generate_code_file(str(question_id)+'-'+problem_slug, lang, code_template['code'], sample_test_case)

    def test(self, filename):
        leetcode.test(filename)

    def clean(self):
        cache.clean()
        screen.print_clean_message()

    def disscussion_list(self, question_id):
        discussion_list = leetcode.fetch_discussion_by_question_id(question_id)
        screen.print_discussion_list(discussion_list)
    
    def disscussion_post(self, question_id, rank):
        discussion_list = leetcode.fetch_discussion_by_question_id(question_id)
        post_ids = []
        for discussion in discussion_list:
            post_ids.append(discussion['node']['id'])
        discussion_post = leetcode.fetch_discussion_post(post_ids[rank-1])
        screen.print_discussion_post(discussion_post)
