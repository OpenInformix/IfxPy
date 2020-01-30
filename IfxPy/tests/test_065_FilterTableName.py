# 

#

#

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_065_FilterTableName(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_065)

  def run_test_065(self):
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
    
    result = IfxPy.tables(conn, None, '%', "t3")
    columns = IfxPy.num_fields(result)
    
    for i in range(0, columns):
      print("%s, " % IfxPy.field_name(result, i))
    print("\n\n")
   
    row = IfxPy.fetch_tuple(result) 
    while ( row ):
      final = ", " + row[1] + ", " + row[2] + ", " + row[3] + ", ,";
      row = IfxPy.fetch_tuple(result)

    print(final)
    
    IfxPy.free_result(result)

    IfxPy.exec_immediate(conn, 'DROP TABLE t.t1')
    IfxPy.exec_immediate(conn, 'DROP TABLE t.t2')
    IfxPy.exec_immediate(conn, 'DROP TABLE t.t3')
    IfxPy.exec_immediate(conn, 'DROP TABLE t.t4')

#__END__
#__IDS_EXPECTED__
#TABLE_CAT, TABLE_SCHEM, TABLE_NAME, TABLE_TYPE, REMARKS, 
#
#, t, t3, TABLE, ,
