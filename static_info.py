# -*- encoding:utf-8 -*-
__author__ = 'zhongziyuan'

import json
from math import sqrt
from sys import maxint
from util.lean_storage import LeancloudHandler


class InfoGetter:

    def __init__(self, dict_file=None):
        if None != dict_file:
            self.judge_dict = InfoGetter.load_dict_local(dict_file)
        else:
            self.judge_dict = InfoGetter.load_dict_online()

    @staticmethod
    def load_dict_local(dict_file):
        f = open(dict_file, 'r')
        content = f.read()
        f.close()
        res = json.loads(content, encoding="utf-8")
        return res

    @staticmethod
    def load_dict_online():
        res = {}
        data = LeancloudHandler().get_all('app_dict')
        for d in data:
            print d
            if d[u'label'] not in res.keys():
                res[d[u'label']] = {}
                yes = {}
                no = {}
                if d[u'degree'] > 0:
                    yes[d[u'app']] = 1
                    no[d[u'app']] = 0
                else:
                    yes[d[u'app']] = 0
                    no[d[u'app']] = 1
                res[d[u'label']]['yes'] = yes
                res[d[u'label']]['no'] = no
            else:
                if d[u'degree'] > 0:
                    res[d[u'label']]['yes'][d[u'app']] = 1
                    res[d[u'label']]['no'][d[u'app']] = 0
                else:
                    res[d[u'label']]['yes'][d[u'app']] = 0
                    res[d[u'label']]['no'][d[u'app']] = 1
        print "n\n"
        print res
        print "n\n"
        return res

    def get_labels(self, info):
        if not isinstance(info, list):
            print 'Input data must be list !'
            return {}
        res = {}
        for label, classes in self.judge_dict.items():
            label_class = InfoGetter.get_class(classes, info) #  compare the classes with info
            res[label] = label_class

        return res

    @staticmethod
    def get_class(classes, info):
        info_vec = {}
        degrees = classes.values()[0].keys()
        for app in degrees:
            if app in info:
                info_vec[app] = 1
            else:
                info_vec[app] = 0

        max_sim = -maxint
        max_class = ''
        for oneClass, value in classes.items():
            v1 = 0
            v2 = 0
            v1_v2 = 0
            for k, v in value.items():
                v1 += v ** 2
                v2 += (info_vec[k])**2
                v1_v2 += v * info_vec[k]
            sim = v1_v2/sqrt(v1*v2+0.001)
            if sim > max_sim:
                max_sim = sim
                max_class = oneClass

        print "max_class"
        print max_class
        return max_class


if __name__ == '__main__':
    i = InfoGetter()
    print i.get_labels(["com.kplus.car", "cn.buding.martin"])

    # r = InfoGetter().load_dict_online()
    # for rk, rv in r.items():
    #     print ''
    #     print rk
    #     print '-------------------------------------------------------'
    #     for kk, vv in rv.items():
    #         print '-----' + kk + ":"
    #         for kkk, vvv in vv.items():
    #             print kkk + ":" + str(vvv)