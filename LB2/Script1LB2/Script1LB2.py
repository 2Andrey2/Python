#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[47]:


import sys
import argparse
import os
import datetime
import shutil
 
def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-so', '--source', default=r'C:\Users\Andrey\Desktop\Учеба\питон\LB2\Script1LB2')
    parser.add_argument ('-d', '--days', default=1)
    parser.add_argument ('-s', '--size', type=int, default=100)
    return parser

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])
#print(namespace)
#print(dir(namespace))
#print(namespace.size)
#print(namespace.source)

os.chdir(namespace.source)
dir1 = os.listdir()
for temp in dir1:
    t = os.path.getmtime(temp)
    t = datetime.datetime.fromtimestamp(t)
    if os.stat(temp).st_size < namespace.size:
        print('++++++++++')
        
        if os.path.isdir(namespace.source+'\Small') == False:
            os.mkdir('Small')
            print('!!!!!!!!!!!!')
        shutil.move(temp,namespace.source+r'\Small')
    if (t - datetime.datetime.now()).days > namespace.days:
        print('----------')
        if os.path.isdir(namespace.source+'\Archive') == False:
            os.mkdir('Archive')
            print('----------')
        shutil.move(shutil.move(temp,namespace.source+r'\Archive')


# In[45]:


#import datetime
#import os
#pyth=r'C:\Users\Andrey\Desktop\Учеба\питон\LB2\Script1LB2'
#os.chdir(pyth)
#print(pyth+'\Small')
#if os.path.isdir(pyth+'\Small') == False:
#    os.mkdir('Small')
#    print('!!!!!!!!!!!!')
#t = os.path.getmtime(r'C:\Users\Andrey\Desktop\Учеба\питон\LB2\Script1LB2\temp1.docx')
#t = datetime.datetime.fromtimestamp(t)
#t = t - datetime.datetime.now()
#print(type(t))
#print(dir(t))
#print(t.days)
#print(os.path.isdir(r'C:\Users\Andrey\Desktop\Учеба\питон\LB2\Script1LB2\Small'))


# In[ ]:




