# 

#

#

import unittest, sys, os
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_144_BindParamInsertStmtPARAM_FILE(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_144)

  def run_test_144(self):
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)
    
    if conn:
      # Drop the test table, in case it exists
      drop = 'DROP TABLE pictures'
      try:
        result = IfxPy.exec_immediate(conn, drop)
      except:
        pass
      
      # Create the test table
      create = 'CREATE TABLE pictures (id INTEGER, picture BLOB)'
      result = IfxPy.exec_immediate(conn, create)
      
      stmt = IfxPy.prepare(conn, "INSERT INTO pictures VALUES (0, ?)")
      
      picture = os.path.dirname(os.path.abspath(__file__)) + "/pic1.jpg"
      rc = IfxPy.bind_param(stmt, 1, picture, IfxPy.SQL_PARAM_INPUT)
    
      rc = IfxPy.execute(stmt)
      
      num = IfxPy.num_rows(stmt)
      
      print(num)
    else:
      print("Connection failed.")

#__END__
#__LUW_EXPECTED__
#1
#__ZOS_EXPECTED__
#1
#__SYSTEMI_EXPECTED__
#1
#__IDS_EXPECTED__
#1
