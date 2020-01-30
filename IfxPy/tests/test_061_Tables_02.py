# 

#

#

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_061_Tables_02(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_061)

  def run_test_061(self):
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
      server = IfxPy.server_info( conn )
      op = {IfxPy.ATTR_CASE: IfxPy.CASE_UPPER}
      IfxPy.set_option(conn, op, 1)

      result = IfxPy.tables(conn, None, 't');
      i = 0
      row = IfxPy.fetch_both(result)
      while ( row ):
        str = row['TABLE_SCHEM'] + row['TABLE_NAME'] + row['TABLE_TYPE']
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
      print("no connection: %s" % IfxPy.conn_errormsg())

#__END__
#__IDS_EXPECTED__
#tt1TABLE
#tt2TABLE
#tt3TABLE
#tt4TABLE
#done!
