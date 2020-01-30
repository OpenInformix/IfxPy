# 

#

#

import unittest, sys
import IfxPy
import config
from testfunctions import IfxPyTestFunctions

class IfxPyTestCase(unittest.TestCase):

  def test_066_TableObjects(self):
    obj = IfxPyTestFunctions()
    obj.assert_expect(self.run_test_066)

  def run_test_066(self):
    conn = IfxPy.connect(config.ConnStr, config.user, config.password)
    server = IfxPy.server_info( conn )

    result = IfxPy.tables(conn, None, config.user.lower(), 'animals')
      
#    NOTE: This is a workaround
#    function fetch_object() to be implemented...
#    row = IfxPy.fetch_object(result)
#    JS: check .lower() functionatily  
  
    class Row:
        pass

    data = IfxPy.fetch_assoc(result)
    while ( data ):
      row = Row()
      row.table_schem = data['TABLE_SCHEM']
      row.table_name = data['TABLE_NAME']
      row.table_type = data['TABLE_TYPE']
      row.remarks = data['REMARKS']
          
      print("Schema:  %s" % row.table_schem)
      print("Name:    %s" % row.table_name)
      print("Type:    %s" % row.table_type)
      print("Remarks: %s\n" % row.remarks)
#      row = IfxPy.fetch_object(result)
      data = IfxPy.fetch_assoc(result)

    result = IfxPy.tables(conn, None, config.user.lower(), 'animal_pics')
    
#    row = IfxPy.fetch_object(result)
    data = IfxPy.fetch_assoc(result)
    while (data ):
      row = Row()
      row.table_schem = data['TABLE_SCHEM']
      row.table_name = data['TABLE_NAME']
      row.table_type = data['TABLE_TYPE']
      row.remarks = data['REMARKS']
        
      print("Schema:  %s" % row.table_schem)
      print("Name:    %s" % row.table_name)
      print("Type:    %s" % row.table_type)
      print("Remarks: %s\n" % row.remarks)
      data = IfxPy.fetch_assoc(result)
      
    result = IfxPy.tables(conn, None, config.user.lower(), 'anime_cat')
    
#    row = IfxPy.fetch_object(result)
    data = IfxPy.fetch_assoc(result)
    while ( data ): 
      row = Row()
      row.table_schem = data['TABLE_SCHEM']
      row.table_name = data['TABLE_NAME']
      row.table_type = data['TABLE_TYPE']
      row.remarks = data['REMARKS']
        
      print("Schema:  %s" % row.table_schem)
      print("Name:    %s" % row.table_name)
      print("Type:    %s" % row.table_type)
      print("Remarks: %s\n" % row.remarks)
#      row = IfxPy.fetch_object(result)
      data = IfxPy.fetch_assoc(result)
    
    IfxPy.free_result(result)
    IfxPy.close(conn)

#__END__
#__LUW_EXPECTED__
#Schema:  %s
#Name:    ANIMALS
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    ANIMAL_PICS
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    ANIME_CAT
#Type:    VIEW
#Remarks: None
#__ZOS_EXPECTED__
#Schema:  %s
#Name:    ANIMALS
#Type:    TABLE
#Remarks: 
#
#Schema:  %s
#Name:    ANIMAL_PICS
#Type:    TABLE
#Remarks: 
#
#Schema:  %s
#Name:    ANIME_CAT
#Type:    VIEW
#Remarks: 
#__SYSTEMI_EXPECTED__
#Schema:  %s
#Name:    ANIMALS
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    ANIMAL_PICS
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    ANIME_CAT
#Type:    VIEW
#Remarks: None
#__IDS_EXPECTED__
#Schema:  %s
#Name:    animals
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    animal_pics
#Type:    TABLE
#Remarks: None
#
#Schema:  %s
#Name:    anime_cat
#Type:    VIEW
#Remarks: None
