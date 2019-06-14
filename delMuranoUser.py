# !/usr/bin/env python
import json
import re
import requests
import time
import sys


class Murano_User(object):

    def __init__(self):
        self.BP_HOST = "bizapi-staging.hosted.exosite.io"
        self.COMPANY_ID = 'loz8gtd7hcmims4i'
        self.EMAIL = "testing@exosite.com"
        self.PASSWORD = "1234eszxcv++"
        self.HEADER = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        self.HOST = "https://{}/api:1".format(self.BP_HOST)

    def get_user(self, token):
        route = "/business/{}/member/".format(self.COMPANY_ID)
        self.HEADER.update({'authorization': 'token {}'.format(token)})
        response = requests.get(self.HOST + route, headers=self.HEADER)
        response = json.loads(response.content)
        return response

    def get_user_token(self):
        route = "/token/"
        data = {"email": "{}".format(
            self.EMAIL), "password": "{}".format(self.PASSWORD)}
        response = requests.post(
            self.HOST + route,
            headers=self.HEADER,
            data=json.dumps(data)
        )
        response = json.loads(response.content)
        token = response['token']
        return token

    def delete_user(self, userInfo):
        print "     - Delete User: {0} -> {1}".format(userInfo['email'], userInfo['role'])
        resp = requests.delete(
            "{}/business/{}/member/{}".format(self.HOST, self.COMPANY_ID, userInfo['email']),
            headers=self.HEADER)
        if resp.status_code != 205:
            print "      * Delete Failed: {0} ".format(resp.status_code, resp.content)
            return False
        return True

    def delete_user_by_list(self, deleteList):
        token = self.get_user_token()
        users = self.get_user(token)

        for item in deleteList:
            re_item = re.compile(item)
            testing_members = filter(lambda i: re_item.search(i['email']), users)
            print '-- There are {0} test user meet the rules: {1}'.format(len(testing_members), item)
            print '-- # Start to delete user, please be patient...'
            output = map(self.delete_user, testing_members)
            print '-- Delete: {0}, Failed: {1}'.format(output.count(True), output.count(False))


murano = Murano_User()

deleteList = [
    "testing\+\d*\+qa@"
]
data = murano.delete_user_by_list(deleteList)
