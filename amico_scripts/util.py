##########################################################################
# Copyright (C) 2012 Phani Vadrevu                                        #
# pvadrevu@uga.edu                                                        #
#                                                                         #
# Distributed under the GNU Public License                                #
# http://www.gnu.org/licenses/gpl.txt                                     #   
#                                                                         #
# This program is free software; you can redistribute it and/or modify    #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation; either version 2 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
###########################################################################

"""
Utitily functions should be added here
"""
import psycopg2
import etld
import re

from config import *

def connect_to_db():
    try:
        conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s"
            %(db_name, db_host, db_user, db_password))
    except:
        print "Unable to connect to database: "+db_name
    conn.set_isolation_level(0)
    return conn

# Reorder the subdomains in the host name such that
# the TLD comes first. Eg: com.google.www
def reorder_domain(host):
    if host is None:
        return
    host = host.split(':')[0]  # in case host string contains port
    ipreg = re.compile("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$")
    if ipreg.match(host) is None:
        ordered_host = ""
        host += '.'
        domains = re.findall('.*?\.', host)
        for i in range(len(domains)):
            ordered_host += domains[len(domains) - i - 1]
        ordered_host = ordered_host[:-1]
        return ordered_host
    else:
        return host

def is_ip(string):
    ipreg = re.compile("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$")
    if ipreg.match(string) is not None:
        return True
    else:
        return False

def extract_extension(url):
    file_name = url.split('?')[0].split('/')[-1]
    if '.' in file_name:
        ext = file_name.split('.')[-1]
        return ext
    else:
        return None
    
def extract_twold(url):
    etld_obj = etld.etld()
    registered = ''
    suffix = ''
    registered, suffix = etld_obj.parse(url)
    twold = '.'.join([registered.split('.')[-1], suffix])
    #print "twold: ", twold 
    return twold
