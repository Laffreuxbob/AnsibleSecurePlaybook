#!/usr/bin/env python3
# author: Olivier Bricaud
# date: 2019-02-25
# description: get IP + login + password from slaves machine conf in /hosts_conf/

import yaml, os, re, errno

DIRNAME = os.path.dirname(os.path.abspath(__file__))
hosts_conf = os.path.join(DIRNAME, 'hosts_conf')

def symlinkForce(target, link):
  try:
    os.symlink(target, link)
  except OSError as e:
    if e.errno == errno.EEXIST:
      os.remove(link)
      os.symlink(target, link)
    else:
      raise e

def getStaticIP(file):
  with open(file, 'r') as stream:
    try:
      data = yaml.load(stream)
      if 'network' in data:
        if 'eth0-0' in data['network']:
          return data['network']['eth0-0'].split('/')[0]
    except yaml.YAMLError as exc:
      return
    return
for f in os.listdir(hosts_conf):
  filepath = os.path.join(hosts_conf, f)
  if os.path.isfile(filepath):
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", f):
      ip = getStaticIP(filepath)
      if ip:
        symlinkForce(filepath, os.path.join(host_vars, ip))


