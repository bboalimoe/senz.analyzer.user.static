# -*- encoding=utf-8 -*-
__author__ = 'zhongziyuan'

import json
import requests
import settings
import leancloud

class LeancloudHandler(object):
    # base = r'https://cn.avoscloud.com'
    base = r'https://leancloud.cn'
    base_classes = base+r'/1.1/classes/'
    base_patch = base+r'/1.1/batch'
    Users = base+r'/1.1/users'
    app_settings = [settings.avos_app_id, settings.avos_app_key]

    @classmethod
    def headers(cls):
        """
        get the request header
        :return: header dict
        """
        return {
            "X-AVOSCloud-Application-Id": cls.app_settings[0],
            "X-AVOSCloud-Application-Key": cls.app_settings[1],
            "Content-Type": "application/json"
        }

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

# Test
if __name__ == '__main__':
    lc = LeancloudHandler()
    print lc.get_all("app_dict")