# 

#

#

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_180_StmtErrMsg(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_180)

  def run_test_180(self):
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)
    if conn:
      result = ''
      result2 = ''
      try:
        result = IfxPy.exec_immediate(conn,"insert int0 t_string values(123,1.222333,'one to one')")
      except:
        pass
      if result:
        cols = IfxPy.num_fields(result)
        print("col:", cols,", ") 
        rows = IfxPy.num_rows(result)
        print("affected row:", rows)
      else:
        print(IfxPy.stmt_errormsg())
      try:
        result = IfxPy.exec_immediate(conn,"delete from t_string where a=123")
      except:
        pass
      if result:
        cols = IfxPy.num_fields(result)
        print("col:", cols,", ")
        rows = IfxPy.num_rows(result)
        print("affected row:", rows)
      else:
        print(IfxPy.stmt_errormsg())
    
    else:
      print("no connection")

#__END__
#__LUW_EXPECTED__
#[IBM][CLI Driver][DB2/%s] SQL0104N  An unexpected token "insert int0 t_string" was found following "BEGIN-OF-STATEMENT".  Expected tokens may include:  "<space>".  SQLSTATE=42601 SQLCODE=-104col: 0 , affected row: 0
#__ZOS_EXPECTED__
#[IBM][CLI Driver][DB2%s] SQL0104N  An unexpected token "INT0" was found following "".  Expected tokens may include:  "INTO".  SQLSTATE=42601 SQLCODE=-104col: 0 , affected row: 0
#__SYSTEMI_EXPECTED__
#[IBM][CLI Driver][AS] SQL0104N  An unexpected token "INT0" was found following "".  Expected tokens may include:  "INTO".  SQLSTATE=42601 SQLCODE=-104col: 0 , affected row: 0
#__IDS_EXPECTED__
#[Informix][Informix ODBC Driver][Informix]A syntax error has occurred. SQLCODE=-201col: 0 , affected row: 0
