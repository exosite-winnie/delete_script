#!/usr/bin/env python

import json
import re
import time
import sys
import requests
import smtplib
import csv


class Murano_Script(object):
    def __init__(self):
        self.COMPANY = 'dqa-adc-testing'
        self.COMPANY_ID = '9i0iddvy9ro'
        self.SOLUTION_HOST = 'apps.exosite-staging.io'
        self.BP_HOST = "bizapi-staging.hosted.exosite.io"
        self.EMAIL = 'testing@exosite.com'
        self.PASSWORD = '1234eszxcv++'

        self.HEADER = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        self.HOST = "https://%s/api:1" % self.BP_HOST

    def main(self, domainList):
        self.set_user_token()
        self.businessId = self.COMPANY_ID
        self.delete_solution_by_list(domainList)
        print("    ###########################    ")

    def delete_solution(self, solutionInfo):
        resp = 500
        route = "/business/%s/solution/%s" % (self.businessId, solutionInfo['sid'])
        response = requests.delete(self.HOST + route, headers=self.HEADER)
        resp = response.status_code
        print ' # Delete {0} Done And Response : {1}'.format(solutionInfo['label'], resp)
        return True if resp == 204 else False

    def set_user_token(self):
        route = "/token/"
        data = {"email": "%s" % self.EMAIL, "password": "%s" % self.PASSWORD}
        response = requests.post(
            self.HOST + route,
            headers=self.HEADER,
            data=json.dumps(data)
        )
        response = json.loads(response.content)
        token = response['token']
        self.HEADER.update({'authorization': 'token %s' % token})
        return token

    def get_solutions(self):
        route = "/business/%s/solution/" % self.businessId
        response = requests.get(self.HOST + route, headers=self.HEADER)
        r = json.loads(response.content)
        return r

    def delete_solution_by_list(self, domainList):
        solutions = self.get_solutions()

        for item in domainList:
            re_item = re.compile(item)
            testingSolution = filter(lambda i: re_item.search(i['label']), solutions)
            print '-- There are {0} test solution in {1} need to delete.'.format(len(testingSolution), self.COMPANY)
            output = map(self.delete_solution, testingSolution)
            print '-- Delete: {0}, Failed: {1}'.format(output.count(True), output.count(False))


murano = Murano_Script()

domainList = [
    'testing[0-9]*', 'qa[0-9]*', 'test*[a-z]*/i'
]

data = murano.main(domainList)
