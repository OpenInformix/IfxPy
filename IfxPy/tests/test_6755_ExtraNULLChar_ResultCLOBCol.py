# 

#

#

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_6755_ExtraNULLChar_ResultCLOBCol(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_6755)

  def run_test_6755(self):
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)
    server = IfxPy.server_info( conn )
    
    if conn:
      drop = 'DROP TABLE table_6755'
      result = ''
      try:
        result = IfxPy.exec_immediate(conn, drop)
      except:
        pass

      if (server.DBMS_NAME[0:3] == 'Inf'):
        create = 'CREATE TABLE table_6755 (col1 VARCHAR(20), col2 CLOB)'
        insert = "INSERT INTO table_6755 VALUES ('database', FILETOCLOB('C:\\work\\IfxPy\\IfxPy\\tests\\data\\test_6755.txt','client'))"
      else:
        create = 'CREATE TABLE table_6755 (col1 VARCHAR(20), col2 CLOB(20))'
        insert = "INSERT INTO table_6755 VALUES ('database', FILETOCLOB('C:\\work\\IfxPy\\IfxPy\\tests\\data\\test_6755.txt','client'))"
      result = IfxPy.exec_immediate(conn, create)
      result = IfxPy.exec_immediate(conn, insert)
      statement = "SELECT col1, col2 FROM table_6755"
    
      result = IfxPy.prepare(conn, statement)
      IfxPy.execute(result)
    
      row = IfxPy.fetch_tuple(result)
      while ( row ):
        #printf("\"%s\" from VARCHAR is %d bytes long, \"%s\" from CLOB is %d bytes long.\n",
        #    row[0], row[0].length,
        #    row[1], row[1].length)
        print("\"%s\" from VARCHAR is %d bytes long, \"%s\" from CLOB is %d bytes long." % (row[0], len(row[0]), row[1], len(row[1])))
        row = IfxPy.fetch_tuple(result)
      
      IfxPy.close(conn)
    else:
      print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#"database" from VARCHAR is 8 bytes long, "database" from CLOB is 8 bytes long.
#__ZOS_EXPECTED__
#"database" from VARCHAR is 8 bytes long, "database" from CLOB is 8 bytes long.
#__SYSTEMI_EXPECTED__
#"database" from VARCHAR is 8 bytes long, "database" from CLOB is 8 bytes long.
#__IDS_EXPECTED__
#"database" from VARCHAR is 8 bytes long, "database" from CLOB is 8 bytes long.
