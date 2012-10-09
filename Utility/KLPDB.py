import psycopg2
import os
import sys
import traceback
from ConfigParser import SafeConfigParser

def getConfigValue(section,key,rootdir):
  try:
    config = SafeConfigParser()
    config_fp = open(rootdir+'/config/klpconfig.ini','r')
    print config_fp
    config.readfp(config_fp)
    value = config.get(section,key)
    config_fp.close()
    return value
  except:
    print "Unexpected error:", sys.exc_info()
    print "Exception in user code:"
    print '-'*60
    traceback.print_exc(file=sys.stdout)
    print '-'*60


def getConnection():
  db = getConfigValue('Status_Database','dbname',os.getcwd())
  username = getConfigValue('Status_Database','user',os.getcwd())
  passwd = getConfigValue('Status_Database','passwd',os.getcwd())
  dsn = "dbname="+db+" user="+username+" host='localhost' password="+passwd
  connection = psycopg2.connect(dsn)
  return connection

def getklpConnection():
  rootdir=os.path.dirname(sys.argv[0])
  db = getConfigValue('KLP_Database','dbname',rootdir)
  username = getConfigValue('KLP_Database','user',rootdir)
  passwd = getConfigValue('KLP_Database','passwd',rootdir)
  dsn = "dbname="+db+" user="+username+" host='localhost' password="+passwd
  connection = psycopg2.connect(dsn)
  return connection

