# 

#

#
# NOTE: IDS requires that you pass the schema name (cannot pass None)

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_190_ColumnsTable_01(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_190)

  def run_test_190(self):
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)
    server = IfxPy.server_info( conn )

    if conn:
      if (server.DBMS_NAME[0:3] == 'Inf'):
        result = IfxPy.columns(conn,None,config.user,"employee")
      else:
        result = IfxPy.columns(conn,None,None,"EMPLOYEE")

      row = IfxPy.fetch_tuple(result)
      while ( row ):
        str = row[1] + "/" + row[3]
        print(str)
        row = IfxPy.fetch_tuple(result)
      print("done!")
    else:
      print("no connection:", IfxPy.conn_errormsg())

#__END__
#__LUW_EXPECTED__
#%s/EMPNO
#%s/FIRSTNME
#%s/MIDINIT
#%s/LASTNAME
#%s/WORKDEPT
#%s/PHONENO
#%s/HIREDATE
#%s/JOB
#%s/EDLEVEL
#%s/SEX
#%s/BIRTHDATE
#%s/SALARY
#%s/BONUS
#%s/COMM
#done!
#__ZOS_EXPECTED__
#%s/EMPNO
#%s/FIRSTNME
#%s/MIDINIT
#%s/LASTNAME
#%s/WORKDEPT
#%s/PHONENO
#%s/HIREDATE
#%s/JOB
#%s/EDLEVEL
#%s/SEX
#%s/BIRTHDATE
#%s/SALARY
#%s/BONUS
#%s/COMM
#done!
#__SYSTEMI_EXPECTED__
#%s/EMPNO
#%s/FIRSTNME
#%s/MIDINIT
#%s/LASTNAME
#%s/WORKDEPT
#%s/PHONENO
#%s/HIREDATE
#%s/JOB
#%s/EDLEVEL
#%s/SEX
#%s/BIRTHDATE
#%s/SALARY
#%s/BONUS
#%s/COMM
#done!
#__IDS_EXPECTED__
#%s/empno
#%s/firstnme
#%s/midinit
#%s/lastname
#%s/workdept
#%s/phoneno
#%s/hiredate
#%s/job
#%s/edlevel
#%s/sex
#%s/birthdate
#%s/salary
#%s/bonus
#%s/comm
#done!
