#!/usr/bin/env python

import json
import sys
import requests
import re


class ADCScript(object):

    def __init__(self):
        self.SESSION = requests.Session()
        self.COMPANY_ID = 'fj4ipocndtd'    # loz8gtd7hcmims4i
        self.BP_HOST = "bizapi-staging.hosted.exosite.io"
        self.EMAIL = 'testing@exosite.com'
        self.PASSWORD = '1234eszxcv++'

        self.HEADER = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        self.HOST = "https://%s/api:1" % self.BP_HOST

    def main(self):
        self.set_user_token()
        print("    ###########################    ")
        elements = self.getElement()
        pattern = ['element\d', 'elements\d', 'element-\d']
        self.filterDel(elements, pattern)
        for name, elementId in self.delList.items():
            self.delElement(name, elementId)

    def delElement(self, name, id):
        resp = 500
        route = "/exchange/%s/element/%s" % (self.COMPANY_ID, id)
        response = requests.delete(self.HOST + route, headers=self.HEADER)
        resp = response.status_code
        print ' # Delete {0} Done And Response : {1}'.format(name, resp)
        return True if resp == 200 else False

    def filterDel(self, lists, pattern):
        self.delList = {}
        for x in pattern:
            regx = re.compile(x)
            for i in range(len(lists)):
                if regx.match(lists[i]['name']) and lists[i]['bizid'] == self.COMPANY_ID:
                    self.delList.update(
                        {lists[i]['name']: lists[i]['elementId']})
        num = len(self.delList)
        if num >= 0:
            print 'Can delete Elements : {}'.format(len(self.delList))

    def getElement(self):
        route = "/exchange/%s/element/" % self.COMPANY_ID
        resp = self.SESSION.request(
            'get', self.HOST + route, headers=self.HEADER)
        resp = resp.json()
        elements = resp['items']
        print 'Get Elements : {}'.format(len(elements))
        return elements

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


adc = ADCScript()
adc.main()
