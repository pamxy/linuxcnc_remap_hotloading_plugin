#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @Time    : 2020-04-28
# @Author  : pamxy
# @FileName: checkmodify.py
# @Web     : www.pamxy.com

import imp

import os,sys
import time
from threading import *


class RepeatingTimer(Thread):
    def __init__(self,interval,callable,*args,**kwargs):
        Thread.__init__(self)
        self.interval=interval
        self.callable=callable
        self.args=args
        self.kwargs=kwargs
        self.event=Event()
        self.event.set()
        pass

    def run(self):
        while self.event.is_set():
            t=Timer(self.interval,self.callable,self.args,self.kwargs)
            t.start()
            t.join()
        pass

    def cancel(self):
        self.event.clear()
        pass

    pass



class CheckModify(object):
    def __init__(self,file):
        self.debug=False
        self.last_modify_secode = 0
        self.count = 0

        self.filename = file
        # 判断文件是否存在
        if os.path.exists(self.filename):
            # 获取文件信息
            info = os.stat(self.filename)
            # 记录开始时文件的修改时间
            self.last_modify_secode = info.st_mtime
        else:
            print("Can not find file %s"%self.filename)
        pass

    def __del__(self):
        pass

    def reload_module(self,path_file_name):
        is_success=False
        # file_prefix=path_file_name
        #去掉路径
        file_prefix=os.path.basename(path_file_name)
        #去掉后缀
        (file_prefix,file_suffix)=os.path.splitext(file_prefix)

        # module=None
        # #如果sys.modules缓存里有此模块,说明已经加载过
        # if sys.modules.has_key(file_prefix):
        #     module=sys.modules[file_prefix]
        #     #就直接reload
        #     if module is not None:
        #         imp.reload(module)
        # #如果没有加载过,就进行第一次加载
        # else:
        #     module=imp.find_module(file_prefix)
        #     module=imp.load_module(file_prefix,*module)
        # pass

        import linuxcnc
        s=linuxcnc.stat()
        c=linuxcnc.command()
        s.poll()

        if s.task_mode==linuxcnc.MODE_MDI:
            c.mode(linuxcnc.MODE_MDI)
            c.wait_complete()
            c.mdi(";py,import imp;imp.reload(%s)"%file_prefix)
            is_success=True
        else:
            print("reload module no success! task_mode:%s"%s.task_mode)
            is_success=False

        return is_success

    def check(self,file):
        # print("In check")

        try:
            filename=file
            # 判断文件是否存在,在修改时有可能会不存在的,或导致崩溃
            if os.path.exists(filename):
                # 获取文件信息
                info = os.stat(filename)
                # 如果最新的修改时间大于上一次的修改时间1秒,就认为是修改过
                if (info.st_mtime - self.last_modify_secode) > 1:
                    # 重新加载模块
                    is_success=self.reload_module(filename)
                    if is_success:
                        # 重新赋值上一次的修改时间
                        self.last_modify_secode = info.st_mtime
                        print("hot reloaded!")
        except Exception as e:
            print e
            pass
        pass

    def start_check(self,secode):
        # 如果不是调试模式,不执行热更新
        if not self.debug:
            # 如果没__debug__选项,但有import pydevd,也认为能热加载
            if sys.modules.has_key("pydevd"):
                pass
            else:
                print ("##### Don't check")
                return
        print("######start modify check")
        timer=RepeatingTimer(secode,CheckModify.check,self,self.filename)
        timer.start()
        pass


if __name__=="__main__":

    print("########checkmodify:%s"%sys.argv)

    module=""
    debug=False

    print("__debug__:%s"%__debug__)
    if __debug__:
        debug=True

    #python checkmodify.py remap.py
    if len(sys.argv) > 1:
        debug=True
        if sys.argv[1].endswith(".py"):
            module=sys.argv[1]
        pass

    try:
        if len(module)<=0:
            module="hotmodule.py"
        check=CheckModify(module)
        check.debug=debug
        check.start_check(1)

        def has_linuxcnc_runtime():
            is_has=False
            try:
                import linuxcnc
                linuxcnc.stat().poll()
                is_has=True
            except Exception as e:
                print e
                print("################No linuxcnc runtime")

            return is_has

        while has_linuxcnc_runtime():
            #;
            pass
    except Exception as e:
        print e
        pass
    print("#####Exit!")
    pass