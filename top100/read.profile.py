#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File:read.profile.py
# @Author: Feng
# @Date:2019/9/18
# @Desc:

import pstats

p = pstats.Stats('movie2.out')
p.sort_stats('time').print_stats()
