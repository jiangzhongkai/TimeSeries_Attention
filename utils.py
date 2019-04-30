"""-*- coding: utf-8 -*-
 DateTime   : 2019/4/30 12:07
 Author  : Peter_Bonnie
 FileName    : utils.py
 Software: PyCharm
"""

from __future__ import absolute_import,division,print_function
import time



def compute_runing_time(start,end):
    """计算运行时间

    Args:
        start(time)
        end(time)

    Returns:
        hours,mins,secs
    """
    diff_time=int(end-start)
    hours,seconds=divmod(diff_time,3600)
    mins,secs=divmod(seconds,60)

    return "it costs:{0}小时:{1}分钟:{2}秒".format(hours,mins,secs)

