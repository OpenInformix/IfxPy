# 

#

#

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_133_ExecuteLongInputParams(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_133)

  def run_test_133(self):
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)

    if (not conn):
      print("Connection failed.")
      return 0

    IfxPy.autocommit(conn, IfxPy.SQL_AUTOCOMMIT_OFF)

    print("Starting test ...")
    res = ''
    sql =  "INSERT INTO animals (id, breed, name, weight) VALUES (?, ?, ?, ?)"
    try:
      stmt = IfxPy.prepare(conn, sql)
      res = IfxPy.execute(stmt,(128, 'hacker of human and technological nature', 'Wez the ruler of all things PECL', 88.3))
      
      stmt = IfxPy.prepare(conn, "SELECT breed, name FROM animals WHERE id = ?")
      res = IfxPy.execute(stmt, (128,))
      row = IfxPy.fetch_assoc(stmt)
      
      for i in row:
	         print(i)

      IfxPy.rollback(conn)
      print("Done")
    except:
      print("SQLSTATE: %s" % IfxPy.stmt_error(stmt))
      print("Message: %s" % IfxPy.stmt_errormsg(stmt))

    try:
        stmt = IfxPy.prepare(conn, "SELECT breed, name FROM animals WHERE id = ?")
        res = IfxPy.execute(stmt, (128,))
        row = IfxPy.fetch_assoc(stmt)
        if (row):
            for i in row:
                print(i)
        print(res)
        print("SQLSTATE: %s" % IfxPy.stmt_error(stmt))
        print("Message: %s" % IfxPy.stmt_errormsg(stmt))
    except:
        print("An Exception is not expected")
        print("SQLSTATE: %s" % IfxPy.stmt_error(stmt))
        print("Message: %s" % IfxPy.stmt_errormsg(stmt))

    IfxPy.rollback(conn)
    print("Done")

#__END__
#__IDS_EXPECTED__
#Starting test ...
#
#SQLSTATE: 22001
#Message: [Informix][Informix ODBC Driver]String data right truncation. SQLCODE=-11023
#True
#SQLSTATE: 
#Message: 
#Done
