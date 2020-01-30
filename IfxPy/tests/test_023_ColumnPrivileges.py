# 

#

#
# NOTE: IDS requires that you pass the schema name (cannot pass nil)
#
# NOTE: IDS will not return any rows from column_privileges unless
#       there have been privileges granted to another user other
#       then the user that is running the script.  This test assumes
#       that no other user has been granted permission and therefore
#       will return no rows.

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):
  
  def test_023_ColumnPrivileges(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_023)

  def run_test_023(self):
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)
    server = IfxPy.server_info( conn )

    if (conn != 0):
      stmt = IfxPy.column_privileges(conn, None, config.user, 'animals')
      row = IfxPy.fetch_tuple(stmt)
      if row:
        print(row[0])
        print(row[1])
        print(row[2])
        print(row[3])
        print(row[4])
        print(row[5])
        print(row[6])
        print(row[7])
      IfxPy.close(conn)
    else:
      print(IfxPy.conn_errormsg())
      print("Connection failed\n\n")

#__END__
#__IDS_EXPECTED__
#stores7
#informix
#animals
#breed
#informix
#public
#INSERT
#NO
