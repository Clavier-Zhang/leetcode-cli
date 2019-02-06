import requests
import json
from bs4 import BeautifulSoup

s = requests.session()

class Leetcode:

    session = None

    headers = {
        'Origin': 'https://leetcode.com',
        'Referer': 'https://leetcode.com',
        'X-Requested-With': 'XMLHttpRequest',
    }

    login_url = 'https://leetcode.com/accounts/login/'
    graphql = 'https://leetcode.com/graphql'

    def __init__(self, username, password):
        self.session = requests.session()
        self.login(username, password)

    def get_cookie(self, cookies, attribute):
        cookies = str(cookies)
        start = cookies.index(attribute)+1+len(attribute)
        cookies = cookies[start:len(cookies)]
        start = cookies.index(' ')
        return cookies[0:start]
    
    def get_first_CSRFtoken(self):
        response = s.head(self.login_url)
        return self.get_cookie(response.cookies, 'csrftoken')

    def login(self, username, password):
        CSRFtoken = self.get_first_CSRFtoken()
        self.headers['Cookie'] = 'csrftoken=' + CSRFtoken + ';'
        data = {
            'csrfmiddlewaretoken': CSRFtoken,
            'login': username,
            'password': password
        }
        s.post(self.login_url, data=data, headers=self.headers)
        sessionCSRF = self.get_cookie(s.cookies, 'csrftoken')
        sessionId = self.get_cookie(s.cookies, 'LEETCODE_SESSION')
        self.headers['Cookie'] = 'LEETCODE_SESSION=' + sessionId + ';csrftoken=' + sessionCSRF + ';'
        self.headers['X-CSRFToken'] = sessionCSRF

    def get_user_info(self):
        data = {
            'query': '\n'.join([
                '{',
                '  user {',
                '    username',
                '    isCurrentUserPremium',
                '  }',
                '}'
            ]),
            'variables': {}
        }
        response = s.post(self.graphql, data=data, headers=self.headers)
        print(response.text)
    
    def get_all_problems(self):
        data = {
            'query': '''
                query allQuestions {
                    allQuestions {
                        ...questionSummaryFields
                        __typename
                    }
                }
                fragment questionSummaryFields on QuestionNode {
                    title
                    titleSlug
                    translatedTitle
                    questionId
                    questionFrontendId
                    status
                    difficulty
                    isPaidOnly
                    __typename
                }
                ''',
            'variables': {}
        }
        response = s.post(self.graphql, data=data, headers=self.headers)
        print(response.text)

    def get_one_problem(self, titleSlug):
        data = {
            'operationName': "questionData",
            'query': '''
                    query questionData($titleSlug: String!) {
                    question(titleSlug: $titleSlug) {
                        questionId
                        title
                        content
                        isPaidOnly
                        difficulty
                        likes
                        dislikes
                        isLiked
                        similarQuestions
                        topicTags {
                        name
                        slug
                        }
                        codeSnippets {
                        lang
                        langSlug
                        code
                        }
                        stats
                        hints
                        solution {
                        id
                        canSeeDetail
                        }
                        status
                        sampleTestCase
                    }
                }
                ''',
            'variables': json.dumps({'titleSlug': titleSlug})
        }
        response = s.post(self.graphql, data=data, headers=self.headers)
        return(response.json()['data']['question']['content'])

# l = Leetcode('Clavier-Zhang', 'zyc990610')
# html = l.get_one_problem('two-sum')

# soup = BeautifulSoup(html, features="html.parser")
# print(soup.get_text())