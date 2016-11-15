#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# util.py, v1.0
#
# Jaemok Jeong, 2016/11/15

import re
from datetime import date, timedelta

def parsedate(q):
    dow_str = ['mon', 'tue', 'wed', 'thr', 'fri', 'sat', 'sun']

    dow_pt = re.compile(' *(mon|tue|wed|thr|fri|sat|sun)')
    day_pt = re.compile(' *(\d+)[\.\-/](\d+)([\.\-/](\d+))*')
    add_pt = re.compile(' *(\d+)([dw])*')

    today = date.today()

    next = dow_pt.match(q)
    if next:
        dows = next.group(1)
        ts = date.today().weekday()
        ws = dow_str.index(dows)
        nextday = (ws - ts + 7) % 7
        ret = today + timedelta(days=nextday)
        return ret

    next = day_pt.match(q)
    if next:
        (month, day, year) = [x and int(x) for x in next.group(1,2,4)]
        if year == None:
            ret = date(today.year, month, day)
        else:
            if year<100: year+= 2000
            ret = date(year, month, day)
        return ret
    
    next = add_pt.match(q)
    if next:
        (num, metric) = next.group(1,2)
        if metric == 'w':
            ret = today + timedelta(weeks=int(num))
        else:
            ret = today + timedelta(days=int(num))
        return ret
    
    
    return None

def parse(q):
    
    title_pt = re.compile('([^#>:]*)[#>:]*.*$')
    tag_pt = re.compile('#(\w+)')
    day_pt = re.compile('>(.*)$')
    note_pt = re.compile('::([^>#]*)')

    title = ''.join(title_pt.findall(q))
    tag = ','.join(tag_pt.findall(q))
    day = parsedate(''.join(day_pt.findall(q)))
    note = ''.join(note_pt.findall(q))

    return (title, tag, day, note)