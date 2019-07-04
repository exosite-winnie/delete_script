# !/usr/bin/env python
import json
import re
import requests


class Murano_Script(object):

    def __init__(self):
        self.BP_HOST = "bizapi-staging.hosted.exosite.io"
        self.EMAIL = "testing@exosite.com"
        self.PASSWORD = "1234eszxcv++"
        self.HEADER = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        self.HOST = "https://{}/api:1".format(self.BP_HOST)

    def get_business(self, token):
        route = "/user/{}/membership/".format(self.EMAIL)
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

    def delete_business(self, businessInfo):
        self.overdue = {}
        print "     - Delete Business: {0} -> {1}".format(businessInfo['bizid'], businessInfo['name'])
        resp = requests.delete(
            "{}/business/{}".format(self.HOST, businessInfo['bizid']),
            headers=self.HEADER)
        if resp.status_code != 205:
            if resp.status_code == 409 and resp.error == 'overdue':
                self.overdue.update(
                        {businessInfo['bizid']: businessInfo['name']})
            print "      * Delete Failed: {0} -> {1}".format(resp.status_code, resp.content)
            return False
        return True

    def delete_business_by_list(self, deleteList):
        token = self.get_user_token()
        business_IDs = self.get_business(token)
        for item in deleteList:
            re_item = re.compile(item)
            testing_members = filter(lambda i: re_item.search(i['name']) is not None, business_IDs)
            print '-- There are {0} test business meet the rules: {1}'.format(len(testing_members), item)
            print '-- # Start to delete business, please be patient...'
            output = map(self.delete_business, testing_members)
            print '-- Delete: {0}, Failed: {1}'.format(output.count(True), output.count(False))
            print 'Overdue business: {0}'.format(self.overdue)


murano = Murano_Script()

deleteList = [
    "^testing\d+",
    "^testing-\d+",
    "\<script\>alert\(Test update script\)\</script\>"
]
data = murano.delete_business_by_list(deleteList)
