# 

#

#

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_060_Tables_01(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_060)

  def run_test_060(self):
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)
    server = IfxPy.server_info( conn )
    
    create = 'CREATE SCHEMA AUTHORIZATION t'
    try:
      result = IfxPy.exec_immediate(conn, create)
    except:
      pass
    
    create = 'CREATE TABLE t.t1( c1 INTEGER, c2 VARCHAR(40))'
    try:
      result = IfxPy.exec_immediate(conn, create)
    except:
      pass
    
    create = 'CREATE TABLE t.t2( c1 INTEGER, c2 VARCHAR(40))'
    try:
      result = IfxPy.exec_immediate(conn, create) 
    except:
      pass
    
    create = 'CREATE TABLE t.t3( c1 INTEGER, c2 VARCHAR(40))'
    try:
      result = IfxPy.exec_immediate(conn, create) 
    except:
      pass
    
    create = 'CREATE TABLE t.t4( c1 INTEGER, c2 VARCHAR(40))'
    try:
      result = IfxPy.exec_immediate(conn, create) 
    except:
      pass
    
    if conn:
      result = IfxPy.tables(conn, None, 't')
      i = 0
      row = IfxPy.fetch_both(result)
      while ( row ):
        if (i < 4):
          print("/%s/%s" % (row[1], row[2]))
        i = i + 1
        row = IfxPy.fetch_both(result)

      IfxPy.exec_immediate(conn, 'DROP TABLE t.t1')
      IfxPy.exec_immediate(conn, 'DROP TABLE t.t2')
      IfxPy.exec_immediate(conn, 'DROP TABLE t.t3')
      IfxPy.exec_immediate(conn, 'DROP TABLE t.t4')

      print("done!")
    else:
      print("no connection: #{IfxPy.conn_errormsg}");    

#__END__
#__LUW_EXPECTED__
#/T/T1
#/T/T2
#/T/T3
#/T/T4
#done!
#__ZOS_EXPECTED__
#/T/T1
#/T/T2
#/T/T3
#/T/T4
#done!
#__SYSTEMI_EXPECTED__
#/T/T1
#/T/T2
#/T/T3
#/T/T4
#done!
#__IDS_EXPECTED__
#/t/t1
#/t/t2
#/t/t3
#/t/t4
#done!
