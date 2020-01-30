# 

#

#

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_062_Tables_03(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_062)

  def run_test_062(self):
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)
    server = IfxPy.server_info( conn )

    create = 'CREATE SCHEMA AUTHORIZATION t'
    try:
      result = IfxPy.exec_immediate(conn, create) 
    except:
      pass
    
    create = 'CREATE TABLE t.t1( c1 integer, c2 varchar(40))'
    try:
      result = IfxPy.exec_immediate(conn, create) 
    except:
      pass
    
    create = 'CREATE TABLE t.t2( c1 integer, c2 varchar(40))'
    try:
      result = IfxPy.exec_immediate(conn, create) 
    except:
      pass
    
    create = 'CREATE TABLE t.t3( c1 integer, c2 varchar(40))'
    try:
      result = IfxPy.exec_immediate(conn, create) 
    except:
      pass
    
    create = 'CREATE TABLE t.t4( c1 integer, c2 varchar(40))'
    try:
      result = IfxPy.exec_immediate(conn, create) 
    except:
      pass
    
    if conn:
      schema = 't'
      result = IfxPy.tables(conn,None,schema);    
      i = 0
      row = IfxPy.fetch_both(result)
      while ( row ):
        str = row[1] + "/" + row[2] + "/" + row[3]
        if (i < 4):
          print(str)
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
#T/T1/TABLE
#T/T2/TABLE
#T/T3/TABLE
#T/T4/TABLE
#done!
#__ZOS_EXPECTED__
#T/T1/TABLE
#T/T2/TABLE
#T/T3/TABLE
#T/T4/TABLE
#done!
#__SYSTEMI_EXPECTED__
#T/T1/TABLE
#T/T2/TABLE
#T/T3/TABLE
#T/T4/TABLE
#done!
#__IDS_EXPECTED__
#t/t1/TABLE
#t/t2/TABLE
#t/t3/TABLE
#t/t4/TABLE
#done!
