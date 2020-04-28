#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2020-04-28
# @Author  : pamxy
# @FileName: checkmodify.py
# @Web     : www.pamxy.com

import emccanon
import linuxcnc
# import interpreter
from interpreter import *
import gcode
# import emctask

# import pydevd
# pydevd.settrace('localhost', port=51234, stdoutToServer=True, stderrToServer=True, suspend=False)


def init_stdglue(self):
    pass

#插入参数给ngc
def insert_param(self, **words):
    try:
        print("@@@PYTHON insert_param call level=%s"%self.call_level)
        self.params["myname"]=125
        self.params[int(1)]=345
        self.params[int(2)]=678
        print("@@@PYTHON #2=%s" % self.params[int(2)])
        print("@@@PYTHON #5401=%s" % self.params[int(5401)])
        print("@@@PYTHON #5220=%s" % self.params[int(5220)])
        # self.execute("o<testparam> call",0)
    except Exception as e:
        return "@@@PYTHON insert_param exception:%s"%e
    # return interpreter.INTERP_OK          #import interpreter时使用
    return INTERP_OK
    pass


#从ngc取回参数
def retrieve_param(self, **words):
    try:
        print("@@@PYTHON retrieve_param call level=%s"%self.call_level)
        print("@@@PYTHON #1=%s"%self.params[int(1)])
        print("@@@PYTHON #2=%s"%self.params[int(2)])
        print("@@@PYTHON #5401=%s"%self.params[int(5401)])
        print("@@@PYTHON #5220=%s"%self.params[int(5220)])
        print("@@@PYTHON self.params.locals=%s"%self.params.locals())
        print("@@@PYTHON self.params.globals=%s"%self.params.globals())
        print("@@@PYTHON abc=%s" % self.params["abc"])
        print("@@@PYTHON def=%s" % self.params["def"])
        print("@@@PYTHON ghi=%s" % self.params["ghi"])
        print("@@@PYTHON jkl=%s" % self.params["jkl"])
        print("@@@PYTHON 5420=%s" % self.params[5420])

        print("@@@456PYTHON result=%s"%self.params["result"])
    except Exception as e:
        #如果没有#<result>命名参数,就会抛出异常
        return "@@@PYTHON testparam forgot to assign #<result>"
    # return interpreter.INTERP_OK
    return INTERP_OK
    pass
