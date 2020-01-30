# 

#

#
# NOTE: IDS requires that you pass the schema name (cannot pass None)

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_191_ColumnsTable_02(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_191)

  def run_test_191(self):
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)
    server = IfxPy.server_info( conn )

    if conn:
      result = IfxPy.columns(conn,None,config.user,"emp_photo");    

      i = 0
      row = IfxPy.fetch_both(result)
      while ( row ):
        if ( (row['COLUMN_NAME'] != 'emp_rowid') and (i < 3) ):
          print("%s,%s,%s,%s\n" % (row['TABLE_SCHEM'], 
          row['TABLE_NAME'], row['COLUMN_NAME'], row['IS_NULLABLE']))
        i = i + 1
        row = IfxPy.fetch_both(result)
      print("done!")
    else:
      print("no connection: ", IfxPy.conn_errormsg())    

#__END__
#__IDS_EXPECTED__
#%s,emp_photo,empno,NO
#%s,emp_photo,photo_format,NO
#%s,emp_photo,picture,YES
#done!
