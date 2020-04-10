////////////////////////////////////////////////////////////////////////////
// Copyright 2017-2020  OpenInformix
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http ://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
/*
+----------------------------------------------------------------------+
| Authors: Sathyanesh Krishnan, Javier Sagrera, Rohit Pandey           |
|                                                                      |
+----------------------------------------------------------------------+
////////////////////////////////////////////////////////////////////////////
+----------------------------------------------------------------------+
| Authors: Manas Dadarkar, Abhigyan Agrawal, Rahul Priyadarshi,        |
|          Saba Kauser                                                 | 
+----------------------------------------------------------------------+
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#ifdef _WIN32
#include <windows.h>
#define strdup _strdup
#endif

#ifdef DRIVER_MANAGER 
#include "sql.h"
#include "sqlext.h"
#else
#include "infxcli.h"
#endif

#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#else
#include <Python.h>
#endif

#include <structmember.h>

// For compatibility with python < 2.5
#if PY_VERSION_HEX < 0x02050000 && !defined(PY_SSIZE_T_MIN)
typedef int Py_ssize_t;
#define PY_SSIZE_T_MAX INT_MAX
#define PY_SSIZE_T_MIN INT_MIN
#endif

// Combability changes for Python 3

// defining string methods 
#if  PY_MAJOR_VERSION < 3
#define PyBytes_Check               PyString_Check
#define StringOBJ_FromASCII(str)    PyString_FromString(str)
#define PyBytes_AsString            PyString_AsString
#define PyBytes_FromStringAndSize   PyString_FromStringAndSize
#define StringObj_Format            PyString_Format
#define StringObj_Size              PyString_Size
#define PyObject_CheckBuffer        PyObject_CheckReadBuffer
#define PyVarObject_HEAD_INIT(type, size)   PyObject_HEAD_INIT(type) size,

#define Py_TYPE(ob)            (((PyObject*)(ob))->ob_type)
#define MOD_RETURN_ERROR        
#define MOD_RETURN_VAL(mod)            
#define INIT_IfxPy                initIfxPy
#else
#define PyInt_Check                PyLong_Check
#define PyInt_FromLong             PyLong_FromLong
#define PyInt_AsLong               PyLong_AsLong
#define PyInt_AS_LONG              PyLong_AsLong
#define StringOBJ_FromASCII(str)   PyUnicode_DecodeASCII(str, strlen(str), NULL)
#define PyString_Check             PyUnicode_Check
#define StringObj_Format           PyUnicode_Format
#define StringObj_Size             PyUnicode_GET_SIZE
#define MOD_RETURN_ERROR           NULL
#define MOD_RETURN_VAL(mod)        mod
#define INIT_IfxPy                PyInit_IfxPy
#endif

#define NUM2LONG(data)    PyInt_AsLong(data)
#define STR2CSTR(data)    PyString_AsString(data)
#define NIL_P(ptr)        (ptr == NULL)
#define ALLOC_N(type, n)  PyMem_New(type, n)
#define ALLOC(type)       PyMem_New(type, 1)

#define TYPE(data)        _python_get_variable_type(data)

//  Python types 
#define PYTHON_FIXNUM    1
#define PYTHON_TRUE      2
#define PYTHON_FALSE     3
#define PYTHON_FLOAT     4
#define PYTHON_STRING    5
#define PYTHON_NIL       6
#define PYTHON_UNICODE   7
#define PYTHON_DECIMAL   8
#define PYTHON_COMPLEX   9
#define PYTHON_DATE      10
#define PYTHON_TIME      11
#define PYTHON_TIMESTAMP 12
#define PYTHON_TIMEDELTA 13

#ifndef SQL_ATTR_GET_GENERATED_VALUE 
#define SQL_ATTR_GET_GENERATED_VALUE 2578
#endif

//  strlen(" SQLCODE=") added in 
#define DB_MAX_ERR_MSG_LEN (SQL_MAX_MESSAGE_LENGTH + SQL_SQLSTATE_SIZE + 10)

//  Default initail LOB buffer size 
#define INIT_BUFSIZ     10240
 
//  Used in _python_parse_options 
#define IDS_ERRMSG      1
#define IDS_ERR         2
#define IDS_WARNMSG     3

// ******* Makes code compatible with the options used by the user 
#define BINARY          1
#define CONVERT         2
#define PASSTHRU        3
#define PARAM_FILE      11

//  fetch 
#define FETCH_INDEX     0x01
#define FETCH_ASSOC     0x02
#define FETCH_BOTH      0x03

//  Change column case 
#define ATTR_CASE       3271982
#define CASE_NATURAL    0
#define CASE_LOWER      1
#define CASE_UPPER      2

//  data type switch for performance 
#define USE_WCHAR       100
#define WCHAR_YES       1
#define WCHAR_NO        0

//  maximum sizes 
#define USERID_LEN      16
#define ACCTSTR_LEN     200
#define APPLNAME_LEN    32
#define WRKSTNNAME_LEN  18

/////////////////// Dummy fields ///////////////////////////
#define SQL_ATTR_PING_DB 0
#define SQL_FILE_READ 0
//#define SQL_DATABASE_CODEPAGE 0
//#define SQL_APPLICATION_CODEPAGE 0
//#define SQL_CONNECT_CODEPAGE 0

// Note: The below definitions comes from ODBC component of CSDK 4.50.xC1 release i..e INFORMIXDIR\incl\cli\infxcli.h file.
// Smart trigger feature is supported in Informix CSDK from 4.50.xC1 release onward.
// The below hard coded values are being used to avoid failure of the Python driver build if any lower version of CSDK is used.
// The idea is not to fail the build, however in the lower verison (<4.50.xC1) of CSDK at "run time" Smart Trigger will not work.
// Since the implementation for Smart Trigger is from 4.50.xC1 release onward.
#define PY_IFMX_OPEN_SMART_TRIGGER              2284 // SQL_INFX_ATTR_OPEN_SMART_TRIGGER
#define PY_IFMX_JOIN_SMART_TRIGGER              2285 // SQL_INFX_ATTR_JOIN_SMART_TRIGGER
#define PY_IFMX_GET_LO_FILE_DESC_SMART_TRIGGER  2286 // SQL_INFX_ATTR_GET_LO_FILE_DESC_SMART_TRIGGER
#define PY_IFMX_GET_SESSION_ID_SMART_TRIGGER    2287 // SQL_INFX_ATTR_GET_SESSION_ID_SMART_TRIGGER
#define PY_IFMX_REGISTER_SMART_TRIGGER          2288 // SQL_INFX_ATTR_REGISTER_SMART_TRIGGER
#define PY_IFMX_GET_DATA_SMART_TRIGGER_LOOP     2289 // SQL_INFX_ATTR_GET_DATA_SMART_TRIGGER_LOOP
#define PY_IFMX_GET_DATA_SMART_TRIGGER_NO_LOOP  2290 // SQL_INFX_ATTR_GET_DATA_SMART_TRIGGER_NO_LOOP
#define PY_IFMX_DELETE_SMART_TRIGGER            2291 // SQL_INFX_ATTR_DELETE_SMART_TRIGGER

// Currently, it has provision to register 10 smart triggers. Depending on need it could be increased with other relevant code changes in the code.
#define NUM_OF_SMART_TRIGGER_REGISTRATION 10

// Enum for Decfloat Rounding Modes
enum
{
    ROUND_HALF_EVEN = 0,
    ROUND_HALF_UP,
    ROUND_DOWN,
    ROUND_CEILING,
    ROUND_FLOOR
}ROUNDING_MODE;

struct _IfxPy_globals {
    int  bin_mode;
    char __python_conn_err_msg   [DB_MAX_ERR_MSG_LEN + 1];
    char __python_conn_err_state [SQL_SQLSTATE_SIZE  + 1];
    char __python_stmt_err_msg   [DB_MAX_ERR_MSG_LEN + 1];
    char __python_stmt_err_state [SQL_SQLSTATE_SIZE  + 1];
    char __python_conn_warn_msg  [DB_MAX_ERR_MSG_LEN + 1];
    char __python_conn_warn_state[SQL_SQLSTATE_SIZE  + 1];
    char __python_stmt_warn_msg  [DB_MAX_ERR_MSG_LEN + 1];
    char __python_stmt_warn_state[SQL_SQLSTATE_SIZE  + 1];
};


// Client Information
typedef struct {
    PyObject_HEAD
    PyObject *DRIVER_NAME;
    PyObject *DRIVER_VER;
    PyObject *DATA_SOURCE_NAME;
    PyObject *DRIVER_ODBC_VER;
    PyObject *ODBC_VER;
    PyObject *ODBC_SQL_CONFORMANCE;
    // PyObject *APPL_CODEPAGE;
    // PyObject *CONN_CODEPAGE;
} le_client_info;

static PyMemberDef le_client_info_members[] = {
    {"DRIVER_NAME",             T_OBJECT_EX, offsetof(le_client_info, DRIVER_NAME),         0, "Driver Name"},
    {"DRIVER_VER",              T_OBJECT_EX, offsetof(le_client_info, DRIVER_VER),          0, "Driver Version"},
    {"DATA_SOURCE_NAME",        T_OBJECT_EX, offsetof(le_client_info, DATA_SOURCE_NAME),    0, "Data Source Name"},
    {"DRIVER_ODBC_VER",         T_OBJECT_EX, offsetof(le_client_info, DRIVER_ODBC_VER),     0, "Driver ODBC Version"},
    {"ODBC_VER",                T_OBJECT_EX, offsetof(le_client_info, ODBC_VER),            0, "ODBC Version"},
    {"ODBC_SQL_CONFORMANCE",    T_OBJECT_EX, offsetof(le_client_info, ODBC_SQL_CONFORMANCE),0, "ODBC SQL Conformance"},
    // {"APPL_CODEPAGE",        T_OBJECT_EX, offsetof(le_client_info, APPL_CODEPAGE),       0, "Application Codepage"},
    // {"CONN_CODEPAGE",        T_OBJECT_EX, offsetof(le_client_info, CONN_CODEPAGE),       0, "Connection Codepage"},
    {NULL} //  Sentinel 
};

static PyTypeObject client_infoType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        "IfxPy.IFXClientInfo",              // tp_name           
        sizeof(le_client_info),                 // tp_basicsize      
        0,                                      // tp_itemsize       
        0,                                      // tp_dealloc        
        0,                                      // tp_print          
        0,                                      // tp_getattr        
        0,                                      // tp_setattr        
        0,                                      // tp_compare        
        0,                                      // tp_repr           
        0,                                      // tp_as_number      
        0,                                      // tp_as_sequence    
        0,                                      // tp_as_mapping     
        0,                                      // tp_hash           
        0,                                      // tp_call           
        0,                                      // tp_str            
        0,                                      // tp_getattro       
        0,                                      // tp_setattro       
        0,                                      // tp_as_buffer      
        Py_TPFLAGS_DEFAULT,                     // tp_flags          
        "Informix Server Client Information object", // tp_doc      
        0,                                      // tp_traverse       
        0,                                      // tp_clear          
        0,                                      // tp_richcompare    
        0,                                      // tp_weaklistoffset 
        0,                                      // tp_iter           
        0,                                      // tp_iternext       
        0,                                      // tp_methods            
        le_client_info_members,                 // tp_members        
        0,                                      // tp_getset         
        0,                                      // tp_base           
        0,                                      // tp_dict           
        0,                                      // tp_descr_get      
        0,                                      // tp_descr_set      
        0,                                      // tp_dictoffset     
        0,                                      // tp_init           
};


// Server Information
typedef struct {
    PyObject_HEAD
    PyObject *DBMS_NAME;
    PyObject *DBMS_VER;
    // PyObject *DB_CODEPAGE;
    PyObject *DB_NAME;
    PyObject *INST_NAME;
    PyObject *SPECIAL_CHARS;
    PyObject *KEYWORDS;
    PyObject *DFT_ISOLATION;
    PyObject *ISOLATION_OPTION;
    PyObject *SQL_CONFORMANCE;
    PyObject *PROCEDURES;
    PyObject *IDENTIFIER_QUOTE_CHAR;
    PyObject *LIKE_ESCAPE_CLAUSE;
    PyObject *MAX_COL_NAME_LEN;
    PyObject *MAX_IDENTIFIER_LEN;
    PyObject *MAX_INDEX_SIZE;
    PyObject *MAX_PROC_NAME_LEN;
    PyObject *MAX_ROW_SIZE;
    PyObject *MAX_SCHEMA_NAME_LEN;
    PyObject *MAX_STATEMENT_LEN;
    PyObject *MAX_TABLE_NAME_LEN;
    PyObject *NON_NULLABLE_COLUMNS;
} le_server_info;


static PyMemberDef le_server_info_members[] = {
    {"DBMS_NAME",               T_OBJECT_EX, offsetof(le_server_info, DBMS_NAME),               0, "Database Server Name"},
    {"DBMS_VER",                T_OBJECT_EX, offsetof(le_server_info, DBMS_VER),                0, "Database Server Version"},
    // {"DB_CODEPAGE",             T_OBJECT_EX, offsetof(le_server_info, DB_CODEPAGE),             0, "Database Codepage"},
    {"DB_NAME",                 T_OBJECT_EX, offsetof(le_server_info, DB_NAME),                 0, "Database Name"},
    {"INST_NAME",               T_OBJECT_EX, offsetof(le_server_info, INST_NAME),               0, "Database Server Instance Name"},
    {"SPECIAL_CHARS",           T_OBJECT_EX, offsetof(le_server_info, SPECIAL_CHARS),           0, "Characters that can be used in an identifier"},
    {"KEYWORDS",                T_OBJECT_EX, offsetof(le_server_info, KEYWORDS),                0, "Reserved words"},
    {"DFT_ISOLATION",           T_OBJECT_EX, offsetof(le_server_info, DFT_ISOLATION),           0, "Default Server Isolation"},
    {"ISOLATION_OPTION",        T_OBJECT_EX, offsetof(le_server_info, ISOLATION_OPTION),        0, "Supported Isolation Levels "},
    {"SQL_CONFORMANCE",         T_OBJECT_EX, offsetof(le_server_info, SQL_CONFORMANCE),         0, "ANSI/ISO SQL-92 Specification Conformance"},
    {"PROCEDURES",              T_OBJECT_EX, offsetof(le_server_info, PROCEDURES),              0, "True if CALL statement is supported by database server"},
    {"IDENTIFIER_QUOTE_CHAR",   T_OBJECT_EX, offsetof(le_server_info, IDENTIFIER_QUOTE_CHAR),   0, "Character to quote an identifier"},
    {"LIKE_ESCAPE_CLAUSE",      T_OBJECT_EX, offsetof(le_server_info, LIKE_ESCAPE_CLAUSE),      0, "TRUE if the database server supports the use of % and _ wildcard characters"},
    {"MAX_COL_NAME_LEN",        T_OBJECT_EX, offsetof(le_server_info, MAX_COL_NAME_LEN),        0, "Maximum length of column name supported by the database server in bytes"},
    {"MAX_IDENTIFIER_LEN",      T_OBJECT_EX, offsetof(le_server_info, MAX_IDENTIFIER_LEN),      0, "Maximum length of an SQL identifier supported by the database server, expressed in characters"},
    {"MAX_INDEX_SIZE",          T_OBJECT_EX, offsetof(le_server_info, MAX_INDEX_SIZE),          0, "Maximum size of columns combined in an index supported by the database server, expressed in bytes"},
    {"MAX_PROC_NAME_LEN",       T_OBJECT_EX, offsetof(le_server_info, MAX_PROC_NAME_LEN),       0, "Maximum length of a procedure name supported by the database server, expressed in bytes"},
    {"MAX_ROW_SIZE",            T_OBJECT_EX, offsetof(le_server_info, MAX_ROW_SIZE),            0, "Maximum length of a row in a base table supported by the database server, expressed in bytes"},
    {"MAX_SCHEMA_NAME_LEN",     T_OBJECT_EX, offsetof(le_server_info, MAX_SCHEMA_NAME_LEN),     0, "Maximum length of a schema name supported by the database server, expressed in bytes"},
    {"MAX_STATEMENT_LEN",       T_OBJECT_EX, offsetof(le_server_info, MAX_STATEMENT_LEN),       0, "Maximum length of an SQL statement supported by the database server, expressed in bytes"},
    {"MAX_TABLE_NAME_LEN",      T_OBJECT_EX, offsetof(le_server_info, MAX_TABLE_NAME_LEN),      0, "Maximum length of a table name supported by the database server, expressed in bytes"},
    {"NON_NULLABLE_COLUMNS",    T_OBJECT_EX, offsetof(le_server_info, NON_NULLABLE_COLUMNS),    0, "Connectionf the database server supports columns that can be defined as NOT NULL "},
    {NULL} //  Sentinel 
};

static PyTypeObject server_infoType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        "IfxPy.IFXServerInfo",              // tp_name           
        sizeof(le_server_info),                 // tp_basicsize      
        0,                                      // tp_itemsize       
        0,                                      // tp_dealloc        
        0,                                      // tp_print          
        0,                                      // tp_getattr        
        0,                                      // tp_setattr        
        0,                                      // tp_compare        
        0,                                      // tp_repr           
        0,                                      // tp_as_number      
        0,                                      // tp_as_sequence    
        0,                                      // tp_as_mapping     
        0,                                      // tp_hash           
        0,                                      // tp_call           
        0,                                      // tp_str            
        0,                                      // tp_getattro       
        0,                                      // tp_setattro       
        0,                                      // tp_as_buffer      
        Py_TPFLAGS_DEFAULT,                     // tp_flags          
        "Informix Server Information object",   // tp_doc            
        0,                                      // tp_traverse       
        0,                                      // tp_clear          
        0,                                      // tp_richcompare    
        0,                                      // tp_weaklistoffset 
        0,                                      // tp_iter           
        0,                                      // tp_iternext       
        0,                                      // tp_methods        
        le_server_info_members,                 // tp_members        
        0,                                      // tp_getset         
        0,                                      // tp_base           
        0,                                      // tp_dict           
        0,                                      // tp_descr_get      
        0,                                      // tp_descr_set      
        0,                                      // tp_dictoffset     
        0,                                      // tp_init           
};

#define IFX_G(v) (IfxPy_globals->v)

static void _python_IfxPy_clear_stmt_err_cache(void);
static void _python_IfxPy_clear_conn_err_cache(void);
static int _python_get_variable_type(PyObject *variable_value);

// ////////////////////////////// from here c ////////////////////////
static void _python_IfxPy_check_sql_errors(
    SQLHANDLE handle,
    SQLSMALLINT hType,
    int rc,
    int cpy_to_global,
    char* ret_str,
    int API,
    SQLSMALLINT recno);

static int _python_IfxPy_assign_options(
    void* handle,
    int type,
    long opt_key,
    PyObject *data);

static SQLWCHAR* getUnicodeDataAsSQLWCHAR(
    PyObject *pyobj,
    int *isNewBuffer);

static PyObject* getSQLWCharAsPyUnicodeObject(
    SQLWCHAR* sqlwcharData,
    SQLLEN sqlwcharBytesLen);

// Defines a linked list structure for error messages
typedef struct _error_msg_node
{
    char                    err_msg [DB_MAX_ERR_MSG_LEN];
    struct _error_msg_node  *next;
} error_msg_node;


// Defines a linked list structure for caching param data
typedef struct _param_cache_node
{
    SQLSMALLINT     data_type;              // Datatype
    SQLULEN         param_size;             // param size
    SQLSMALLINT     nullable;               // is Nullable
    SQLSMALLINT     scale;                  // Decimal scale
    SQLUINTEGER     file_options;           // File options if PARAM_FILE
    SQLLEN          bind_indicator;         // indicator variable for SQLBindParameter
    int             param_num;              // param number in stmt
    int             param_type;             // Type of param - INP/OUT/INP-OUT/FILE
    int             size;                   // Size of param
    char            *varname;               // bound variable name
    PyObject        *var_pyvalue;           // bound variable value
    SQLLEN          ivalue;                 // Temp storage value SQLINTEGER->SQLLEN
    double          fvalue;                 // Temp storage value
    char            *svalue;                // Temp storage value
    SQLWCHAR        *uvalue;                // Temp storage value
    DATE_STRUCT     *date_value;            // Temp storage value
    TIME_STRUCT     *time_value;            // Temp storage value
    TIMESTAMP_STRUCT *ts_value;             // Temp storage value
    SQL_INTERVAL_STRUCT *interval_value;    // Temp storage value
    struct _param_cache_node *next;         // Pointer to next node
} param_node;


// Connection Handle
typedef struct _conn_handle_struct
{
    PyObject_HEAD
        SQLHANDLE   henv;
    SQLHANDLE   hdbc;
    long        auto_commit;
    long        c_bin_mode;
    long        c_case_mode;
    long        c_cursor_type;
    long        c_use_wchar;
    int         handle_active;
    SQLSMALLINT error_recno_tracker;
    SQLSMALLINT errormsg_recno_tracker;
    int         flag_pconnect; // Indicates that this connection is persistent
} conn_handle;

static void _python_IfxPy_free_conn_struct(conn_handle *handle);

static PyTypeObject conn_handleType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "IfxPy.IFXConnection",              // tp_name
    sizeof(conn_handle),                    // tp_basicsize
    0,                                      // tp_itemsize
    (destructor)_python_IfxPy_free_conn_struct, // tp_dealloc
    0,                                      // tp_print
    0,                                      // tp_getattr
    0,                                      // tp_setattr
    0,                                      // tp_compare
    0,                                      // tp_repr
    0,                                      // tp_as_number
    0,                                      // tp_as_sequence
    0,                                      // tp_as_mapping
    0,                                      // tp_hash
    0,                                      // tp_call
    0,                                      // tp_str
    0,                                      // tp_getattro
    0,                                      // tp_setattro
    0,                                      // tp_as_buffer
    Py_TPFLAGS_DEFAULT,                     // tp_flags
    "Informix Server connection object",    // tp_doc
    0,                                      // tp_traverse
    0,                                      // tp_clear
    0,                                      // tp_richcompare
    0,                                      // tp_weaklistoffset
    0,                                      // tp_iter
    0,                                      // tp_iternext
    0,                                      // tp_methods
    0,                                      // tp_members
    0,                                      // tp_getset
    0,                                      // tp_base
    0,                                      // tp_dict
    0,                                      // tp_descr_get
    0,                                      // tp_descr_set
    0,                                      // tp_dictoffset
    0,                                      // tp_init
};

typedef union
{
    SQLINTEGER          i_val;
    SQLDOUBLE           d_val;
    SQLFLOAT            f_val;
    SQLSMALLINT         s_val;
    SQLCHAR             *str_val;
    SQLREAL             r_val;
    SQLWCHAR            *w_val;
    TIMESTAMP_STRUCT    *ts_val;
    DATE_STRUCT         *date_val;
    TIME_STRUCT         *time_val;
    SQL_INTERVAL_STRUCT *interval_val;
} IfxPy_row_data_type;


typedef struct
{
    SQLLEN               out_length;
    IfxPy_row_data_type data;
} IfxPy_row_type;

typedef struct _IfxPy_result_set_info_struct
{
    SQLCHAR       *name;
    SQLSMALLINT   type;
    SQLULEN       size;
    SQLSMALLINT   scale;
    SQLSMALLINT   nullable;
    unsigned char *mem_alloc;  // Mem free
} IfxPy_result_set_info;

typedef struct _row_hash_struct
{
    PyObject *hash;
} row_hash_struct;


// Statement Handle
typedef struct _stmt_handle_struct
{
    PyObject_HEAD
    SQLHANDLE   hdbc;
    SQLHANDLE   hstmt;
	conn_handle	*connhandle;
    long        s_bin_mode;
    long        cursor_type;
    long        s_case_mode;
    long        s_use_wchar;
    SQLSMALLINT error_recno_tracker;
    SQLSMALLINT errormsg_recno_tracker;

    // Parameter Caching variables
    param_node  *head_cache_list;
    param_node  *current_node;

    int         num_params; // Number of Params
    int         file_param; // if option passed in is FILE_PARAM
    int         num_columns;
    IfxPy_result_set_info  *column_info;
    IfxPy_row_type         *row_data;
} stmt_handle;

static void _python_IfxPy_free_stmt_struct(stmt_handle *handle);

static PyTypeObject stmt_handleType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "IfxPy.IFXStatement",   // tp_name
    sizeof(stmt_handle),        // tp_basicsize
    0,                          // tp_itemsize
    (destructor)_python_IfxPy_free_stmt_struct, // tp_dealloc
    0,                          // tp_print
    0,                          // tp_getattr
    0,                          // tp_setattr
    0,                          // tp_compare
    0,                          // tp_repr
    0,                          // tp_as_number
    0,                          // tp_as_sequence
    0,                          // tp_as_mapping
    0,                          // tp_hash
    0,                          // tp_call
    0,                          // tp_str
    0,                          // tp_getattro
    0,                          // tp_setattro
    0,                          // tp_as_buffer
    Py_TPFLAGS_DEFAULT,         // tp_flags
    "Informix Server cursor object", // tp_doc
    0,                          // tp_traverse
    0,                          // tp_clear
    0,                          // tp_richcompare
    0,                          // tp_weaklistoffset
    0,                          // tp_iter
    0,                          // tp_iternext
    0,                          // tp_methods
    0,                          // tp_members
    0,                          // tp_getset
    0,                          // tp_base
    0,                          // tp_dict
    0,                          // tp_descr_get
    0,                          // tp_descr_set
    0,                          // tp_dictoffset
    0,                          // tp_init
};

