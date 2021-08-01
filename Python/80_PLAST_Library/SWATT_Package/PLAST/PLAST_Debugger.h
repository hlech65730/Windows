#ifndef PLAST_DEBUGGER_H
#define PLAST_DEBUGGER_H

#include "swatt_Std_Types.h"
#include "ctester.h"
#include "stdarg.h" // for variadic functions
#include "windows.h"
#include "PLAST_Common.h"

#define USE_DBG_SWATT_ERROR_HANDLER



extern void PLAST_Debugger_Init(void);
extern void PLAST_Debugger_DummyInit(void);

enum SWATT_DBG_ERROR_HANDLING_BEHAVIOR
{
    /** generate fatal error and stop execution if cannot connect to a debugger_Python_Object, missing function or variable */
    DBG_SWATT_HALT_IF_CONNECT_AND_MISSING_CODE,

    /** generate fatal error and stop execution if cannot connect to a debugger_Python_Object, continue on missing function or variable */
    DBG_SWATT_HALT_IF_CONNECT,

    /** generate fatal error and stop execution if cannot connect to a debugger_Python_Object, continue on missing function or variable */
    DBG_SWATT_HALT_IF_ANY_ERROR,

    /** do not generate fatal error, allow test skip instead of failure */
    DBG_SWATT_HALT_NONE
};

enum SWATT_DBG_ERROR_CODE
{
    /** success */
    DBG_E_OK_SWATT,

    /** Not connected */
    DBG_E_NOT_CONNECTED_SWATT,

    /** cannot connect to the emulator */
    DBG_E_CANNOT_CONNECT_SWATT,

    /** cannot execute a step */
    DBG_E_CANNOT_STEP_SWATT,

    /** cannot set a breakpoint */
    DBG_E_CANNOT_SET_BREAKPOINT_SWATT,

    /* cannot clear a breakpoint */
    DBG_E_CANNOT_CLEAR_BREAKPOINT_SWATT,

    /** did not stopped at the breakpoint in the time period mentioned as expected */
    DBG_E_DID_NOT_STOPED_SWATT,

    /** the variable, function or configuration option was not found by the debugger_Python_Object */
    DBG_E_SYMBOL_NOT_FOUND_SWATT,

    /** the checked condition is not true */
    DBG_E_CHECK_FAILED_SWATT,

    /** general failure maybe emulator in a wrong state */
    DBG_E_FAILED_SWATT
};

/* Type definitions for interface functions */
typedef int (*Type_SWATT_DBG_FNC_simple)(void);
typedef int (*Type_SWATT_DBG_FNC_string)(const char*);
typedef int (*Type_SWATT_DBG_FNC_string_uint)(const char*, unsigned int);
typedef int (*Type_SWATT_DBG_FNC_string_address)(const char*, void**);
typedef int (*Type_SWATT_DBG_FNC_uint)(unsigned int);
typedef int (*Type_SWATT_DBG_FNC_configure)(const char*,const char*);
typedef int (*Type_SWATT_DBG_FNC_string_string_string)(const char*,const char*,const char*);
typedef int (*Type_SWATT_DBG_FNC_string_string_string_string)(const char*,const char*,const char*,const char*);
typedef int (*Type_SWATT_DBG_FNC_string_string_string_variadic)(const char*,const char*,const char*,...);

//typedef int (*Type_SWATT_DBG_FNC_variable_vaiadic)(enum PLAST_BASIC_TYPE_IDS,const char*,...);
typedef int (*Type_SWATT_DBG_FNC_enum)(enum SWATT_DBG_ERROR_HANDLING_BEHAVIOR);

struct debugger_SWATT_breakpoints_api
{

       /**
        * Set a breakpoint on a named function
        * \param nameOfTheFunction
        * \return int, value DBG_E_OK_SWATT in case of success, otherwise error (DBG_E_CANNOT_SET_BREAKPOINT_SWATT)
       */
       Type_SWATT_DBG_FNC_string setOnFunction;


       /**
        * Set a breakpoint on a specified line
        * \param nameOfTheFile
        * \param number of the line
        * \return int, value DBG_E_OK_SWATT in case of success, otherwise error (DBG_E_CANNOT_SET_BREAKPOINT_SWATT)
       */
       Type_SWATT_DBG_FNC_string_uint setOnLineNumber;


       /**
        * Clear a breakpoint on a function
        * \param nameOfTheFunction
        * \return int, value DBG_E_OK_SWATT in case of success, otherwise error (DBG_E_CANNOT_CLEAR_BREAKPOINT_SWATT)
       */
       Type_SWATT_DBG_FNC_string  clearOnFunction;


       /**
        * Clear all breakpoints
        * \param nameOfTheFunction
        * \return int, value DBG_E_OK_SWATT in case of success
       */
       Type_SWATT_DBG_FNC_simple clearAll;
};


struct debugger_SWATT_variables_api
{
//       /**
//        * Check if a variable equals the expected value
//        * \param ID of the type of the variable (e.g. TYPE_ID_SWATT_UINT32)
//        * \param const char* VariableName - the name of the variable
//        * \param value - the value of the variable to check against
//        * \return int, value DBG_E_OK_SWATT in case of success, otherwise error (DBG_E_SYMBOL_NOT_FOUND_SWATT, DBG_E_CHECK_FAILED_SWATT)
//       */
//        Type_SWATT_DBG_FNC_variable_vaiadic checkEquals;
//
//
//        /**
//         * Save the value of a variable in a local variable in the test
//         * \param ID of the type of the variable (e.g. TYPE_ID_SWATT_UINT32)
//         * \param const char* VariableName - the name of the variable
//         * \param &localVar - the address of the local variable in which we store the value
//         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error (DBG_E_SYMBOL_NOT_FOUND_SWATT)
//        */
//        Type_SWATT_DBG_FNC_variable_vaiadic getValue;
//
//
//        /**
//         * Evaluate an expression on the emulator and check if is different than zero (TRUE)
//         * \param const char* expression - the expression to evaluate
//         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error (DBG_E_CHECK_FAILED_SWATT)
//        */
//        Type_SWATT_DBG_FNC_string checkTrue;
//
//
//        /**
//         * Save the value of a variable in a local variable in the test
//         * \param ID of the type of the variable (e.g. TYPE_ID_SWATT_UINT32)
//         * \param const char* VariableName - the name of the variable
//         * \param value - the address of the local variable in which we store the value
//         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error (DBG_E_SYMBOL_NOT_FOUND_SWATT)
//        */
//        Type_SWATT_DBG_FNC_variable_vaiadic set;
//

};


struct debugger_SWATT_api
{
        /**
         * Connect to the debugger_Python_Object
         * \param void
         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error (DBG_E_CANNOT_CONNECT_SWATT)
         */
        Type_SWATT_DBG_FNC_simple connect;


        /**
         * Download the files configured in the debugger_Python_Object
         * \param void
         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error
         */
        Type_SWATT_DBG_FNC_simple download;


        /**
         * Perform a reset
         * \param void
         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error
         */
        Type_SWATT_DBG_FNC_simple reset;


        /**
         * Let the code execution start or continue
         * \param void
         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error
         */
        Type_SWATT_DBG_FNC_simple run;


        /**
         * Stop the code execution
         * \param void
         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error
         */
        Type_SWATT_DBG_FNC_simple stop;


        /**
         * Execute one step, if is a function, enter in the code of the function
         * \param void
         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error
         */
        Type_SWATT_DBG_FNC_simple stepInto;


        /**
         * Execute one step, if is a function, continue after execution of the code of the function
         * \param void
         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error
         */
        Type_SWATT_DBG_FNC_simple stepOver;


        /**
         * Execute the code until a return is encountered or the end of the current function
         * \param void
         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error
         */
        Type_SWATT_DBG_FNC_simple stepReturn;


        struct debugger_SWATT_breakpoints_api breakpint;

        /**
         * Execute the code until a breakpoint or a maximum time period
         * \param uint32 timeToWait maximum time to wait until execution is stopped
         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error (DBG_E_DID_NOT_STOPED_SWATT)
         */
        Type_SWATT_DBG_FNC_uint waitUnitlStopped;

        struct debugger_SWATT_variables_api variable;


        /**
          * Get the address of a symbol
          * \param const char* Name - the name of the symbol
          * \param void** localAddr - address of a pointer to save
          * \return int, value DBG_E_OK_SWATT in case of success, otherwise error (DBG_E_SYMBOL_NOT_FOUND_SWATT)
          */
        Type_SWATT_DBG_FNC_string_address getAddressOfSymbol;

        /**
         * configure the debugger_Python_Object
         * \param const char* name of the configuration
         * \param const char* value of the configuration
         * \return int DBG_E_OK_SWATT in case of success, otherwise error code (DBG_E_SYMBOL_NOT_FOUND_SWATT)
         */
        Type_SWATT_DBG_FNC_configure configure;


        /**
         * disconnect the debugger_Python_Object interface
         * \return int DBG_E_OK_SWATT in case of success
         */
        Type_SWATT_DBG_FNC_simple disconnect;
        /**
         * set the debugger error handling behavior
         * \param SWATT_DBG_ERROR_HANDLING_BEHAVIOR behavior - error handling behavior
         * \return int, value DBG_E_OK_SWATT in case of success, otherwise error (DBG_E_FAILED_SWATT)
         */
        Type_SWATT_DBG_FNC_enum setErrorHandlerBehaviour;

        /**
         * Modify an expression
         * \param const char* accesType Type fRealTime, fMonitor
         * \param const char* variableName
         * \param const char* variableValue
         * \return int DBG_E_OK_SWATT in case of success, otherwise error code (DBG_E_SYMBOL_NOT_FOUND_SWATT)
         */
        Type_SWATT_DBG_FNC_string_string_string modify;
        /**
         * Evaluate an expression
         * \param const char* accesType  fRealTime, fMonitor, etc.
         * \param const char* expressionName
         * \param const char* expressionType type of expression return value  may be int,long,float,double,uin8,uint16,uint32,sint8,sint16,sint32
         * \param something* - pointer to return value
         * \return int DBG_E_OK_SWATT in case of success, otherwise error code (DBG_E_SYMBOL_NOT_FOUND_SWATT)
         */
        Type_SWATT_DBG_FNC_string_string_string_variadic evaluate;

        /**
         * Writes a value to a register
         * \param const char* accesType Type fRealTime, fMonitor
         * \param const char* registerName
         * \param const char* registerValue
         * \param const char* retgisterType may be uint8,uint16,uint32,uint63
         * \return int DBG_E_OK_SWATT in case of success, otherwise error code (DBG_E_SYMBOL_NOT_FOUND_SWATT)
         */
        Type_SWATT_DBG_FNC_string_string_string_string writeRegister;
        /**
         * Reads register value
         * \param const char* accesType  fRealTime, fMonitor, etc.
         * \param const char* registerName
         * \param const char* registerType type of register return value  may be int,long,float,double,uin8,uint16,uint32,sint8,sint16,sint32
         * \param something* - pointer to return value
         * \return int DBG_E_OK_SWATT in case of success, otherwise error code (DBG_E_SYMBOL_NOT_FOUND_SWATT)
         */
        Type_SWATT_DBG_FNC_string_string_string_variadic readRegister;

};


/**
    Structure for the debugger_Python_Object interface instance
*/
struct SWATT_debugger
{
        const char* file;
        unsigned int line;
        enum SWATT_DBG_ERROR_HANDLING_BEHAVIOR errorHandlingBehaviorOption;
        struct debugger_SWATT_api dbg_api;
};

extern struct SWATT_debugger SWATT_Debugger_instance;

#define dbg (SWATT_Debugger_instance.file=__FILE__, SWATT_Debugger_instance.line=__LINE__,&SWATT_Debugger_instance)->dbg_api

#ifdef __CDT_PARSER__
#define SWATT_DBG_INLINE inline
#else
#define SWATT_DBG_INLINE static __attribute__((always_inline))
#endif


#ifdef USE_DBG_SWATT_ERROR_HANDLER

SWATT_DBG_INLINE void ZSWATT_DBG_ErrorHandlingBehavior(enum SWATT_DBG_ERROR_CODE err_code);
SWATT_DBG_INLINE void ZSWATT_DBG_ErrorHandlingBehavior(enum SWATT_DBG_ERROR_CODE err_code)
{
    SWATT_number_of_assertions_executed++;
    if (DBG_E_OK_SWATT == err_code)
    {
        return;
    }

    SWATT_number_of_assertions_failed++;
    switch (SWATT_Debugger_instance.errorHandlingBehaviorOption)
    {
        case DBG_SWATT_HALT_NONE:
            break;
        case DBG_SWATT_HALT_IF_CONNECT_AND_MISSING_CODE:
            if ((err_code == DBG_E_CANNOT_CONNECT_SWATT) || (err_code == DBG_E_NOT_CONNECTED_SWATT) || (err_code == DBG_E_SYMBOL_NOT_FOUND_SWATT) )
            {
                SWATT_abort_executable("ERROR: Missing code");
            }
            break;
        case DBG_SWATT_HALT_IF_CONNECT:
            if ((err_code == DBG_E_CANNOT_CONNECT_SWATT) || (err_code == DBG_E_NOT_CONNECTED_SWATT) )
            {
                SWATT_abort_executable("ERROR: Debugger connection error");
            }
            break;
        case DBG_SWATT_HALT_IF_ANY_ERROR:
            SWATT_abort_executable("ERROR: Fatal debugger error");
            break;
        default:
            break;
    }

}
#endif

#endif
