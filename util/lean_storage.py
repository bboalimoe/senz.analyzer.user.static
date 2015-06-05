# -*- encoding=utf-8 -*-
__author__ = 'zhongziyuan'

import os
import json
import requests
import settings
import leancloud
APP_ID = os.environ.get("LC_APP_ID")
APP_KEY = os.environ.get("LC_APP_KEY")

leancloud.init(APP_ID,APP_KEY)



#todo the handler is unfinished

class LeancloudHandler(object):



    def __init__(self):
        pass

    @classmethod
    def get_data(cls, class_name, **kwargs):
        """
        generally get data from leancloud by any means, foundamental method
        :param class_name:
        :param kwargs:
        :return: raw results from leancloud
        """
        res = requests.get(
            cls.base_classes+class_name,
            headers=cls.headers(),
            params=kwargs,
            verify=True
        )
        if 'error' not in json.loads(res.content):
                return res.content
        else:
            print res.content

    @classmethod
    def get_field_by_condition(cls, class_name, field, **kwargs):
        """
        get the specific field of data by certain conditions
        :param class_name:
        :param field:
        :param kwargs:
        :return: data of specific field
        """
        cond = json.dumps(kwargs)
        res = cls.get_data(class_name, keys=field, where=cond)
        if res:
                results = json.loads(res)['results']
                if results:
                        return [result[field] for result in results]
        return []

    def get_all(self, class_name):
        """
        get all data of certain leancloud class
        :param class_name:
        :return:
        """
        res = self.get_data(class_name)
        if res:
            return json.loads(res)['results']




##### demo for gevent
#from gevent import monkey; monkey.patch_all()
import gevent
import urllib2
##### demo for gevent

# gevent demo
# def f(url):
#     print "GET:%s" %url
#     resp = urllib2.urlopen(url)
#     data = resp.read()
#     print len(data)
#
# gevent.joinall([
#     gevent.spawn(f,"https://baidu.com"),
#     gevent.spawn(f,"https://yahoo.com")
# ]
# )


# Test
if __name__ == '__main__':
    lc = LeancloudHandler()

    a = lc.get_all("app_dict")
    print len(a)
    for i in a:
        print i