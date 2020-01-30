# 

#

#

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_064_Tables_05(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_064)

  def run_test_064(self):
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
    
    result = IfxPy.tables(conn, None, 't')
    
    for i in range(0, IfxPy.num_fields(result)):
      print("%s, " % IfxPy.field_name(result, i))
    print()
    print()
  
    i = 0
    row = IfxPy.fetch_tuple(result)
    while ( row ):
      IfxPy.num_fields(result)
      if (i < 4):
        print(", " + row[1] + ", " + row[2] + ", " + row[3] + ", ,\n")
      i = i + 1
      row = IfxPy.fetch_tuple(result)

    IfxPy.free_result(result)

    IfxPy.exec_immediate(conn, 'DROP TABLE t.t1')
    IfxPy.exec_immediate(conn, 'DROP TABLE t.t2')
    IfxPy.exec_immediate(conn, 'DROP TABLE t.t3')
    IfxPy.exec_immediate(conn, 'DROP TABLE t.t4')

#__END__ 
#__IDS_EXPECTED__
#TABLE_CAT, TABLE_SCHEM, TABLE_NAME, TABLE_TYPE, REMARKS, 
#
#, t, t1, TABLE, ,
#, t, t2, TABLE, ,
#, t, t3, TABLE, ,
#, t, t4, TABLE, ,
