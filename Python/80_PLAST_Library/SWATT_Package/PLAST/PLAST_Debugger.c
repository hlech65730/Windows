/*============================================================================*/
/*                        I BS SOFTWARE GROUP                                 */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*/
/*!
 * $Source: PLAST_Debugger.c $
 * $Author: Mancas, Andrei04 (uidv4966) $
 */
/*============================================================================*/
/* DESCRIPTION :                                                              */
/** \file
    Wrappers for PLAST debugger module.
 */
/*============================================================================*/
/* COPYRIGHT (C) CONTINENTAL AUTOMOTIVE 2014                                  */
/* AUTOMOTIVE GROUP, Interior Division, Body and Security                     */
/* ALL RIGHTS RESERVED                                                        */
/*                                                                            */
/* The reproduction, transmission, or use of this document or its content is  */
/* not permitted without express written authority. Offenders will be liable  */
/* for damages.                                                               */
/* All rights, including rights created by patent grant or registration of a  */
/* utility model or design, are reserved.                                     */
/*                                                                            */
/*============================================================================*/

/* Includes */
/*============================================================================*/
#include "PLAST_Debugger.h"
//#include "PLAST_WinIdeaInterface.h"


/* Constants and types  */
/*============================================================================*/
#define ISYSTEM_MODULE "isystem.connect"


/* Variables */
/*============================================================================*/
struct SWATT_debugger SWATT_Debugger_instance;
static PyObject* handle_iSystem_WinIdea_Python_Module = NULL, *debugger_Python_Object = NULL;
static PyObject* handle_Helper_Python_Module = NULL, *debugger_Helper_Python_Object = NULL;
static uint8 iSystemDbg_Connected = 0;

/* Private functions prototypes */
/*============================================================================*/
uint8 PLAST_WinI_Connect(void);
uint8  PLAST_SaveAnyValue(PyObject* returnObj,const char* expressionType,va_list ap);
static void iSystem_SimpleMessage(const char* message);
static int iSystem_IsConnected(void);
int iSystem_Connect(void);
int iSystem_Configure(const char* param,const char*value);
int iSystem_Download(void);
int iSystem_Reset(void);
int iSystem_Run(void);
int iSystem_Stop(void);
int iSystem_StepInto(void);
int iSystem_StepOver(void);
int iSystem_StepReturn(void);
int iSystem_BpSetOnFunction(const char* functionName);
int iSystem_BpClearOnFunction(const char* functionName);
int iSystem_BpSetOnLineNumber(const char* fileName, unsigned int lineNr);
int iSystem_BpClearAll(void);
int iSystem_WaitUnitlStopped(unsigned int time);
int iSystem_Disconnect(void);
int iSystem_Modify(const char* accesType,const char* variableName,const char* variableValue);
int iSystem_Evaluate(const char* accesType,const char* expressionName,const char* expressionType,...);
int iSystem_ReadRegister(const char* accesType,const char* registerName,const char* registerType,...);
int iSystem_WriteRegister(const char* accesType,const char* registerName,const char* registerValue,const char* registerType);
int PLAST_Debugger_SetErrorHandlingBehaviour( enum SWATT_DBG_ERROR_HANDLING_BEHAVIOR behaviour);


/* Inline functions */
/*============================================================================*/

#define WinI_Download() ((PyObject_CallMethod(debugger_Python_Object, "download", NULL) != NULL) ? OK : N_OK)
#define WinI_Reset() ((PyObject_CallMethod(debugger_Python_Object, "reset", NULL) != NULL) ? OK : N_OK)
#define WinI_Run() ((PyObject_CallMethod(debugger_Python_Object, "run", NULL) != NULL) ? OK : N_OK)
#define WinI_Stop() ((PyObject_CallMethod(debugger_Python_Object, "stop", NULL) != NULL) ? OK : N_OK)
#define WinI_stepInto() ((PyObject_CallMethod(debugger_Python_Object, "stepHigh", NULL) != NULL) ? OK : N_OK)
#define WinI_stepOver() ((PyObject_CallMethod(debugger_Python_Object, "stepInst", NULL) != NULL) ? OK : N_OK)
#define WinI_stepReturn() ((PyObject_CallMethod(debugger_Python_Object, "runUntilReturn", NULL) != NULL) ? OK : N_OK)
#define WinI_SetEnableBreakpoint(name) ((PyObject_CallMethod(debugger_Python_Object, "setBP", "s", name) != NULL) ? OK : N_OK)
#define WinI_ClearSymbolBreakpoint(name) ((PyObject_CallMethod(debugger_Python_Object, "deleteBP", "s", name) != NULL) ? OK : N_OK)
#define WinI_SetLineBreakpoint(fileName, lineNr) (PyObject_CallMethod(debugger_Python_Object, "setBP", "O", Py_BuildValue("is", lineNr, fileName))) /* memory leak */
#define WinI_ClearAllBreakpoints() ((PyObject_CallMethod(debugger_Python_Object, "deleteAll", NULL) != NULL) ? OK : N_OK)
#define WinI_WaitForCpuStop(time) ((PyObject_CallMethod(debugger_Python_Object, "waitUntilStopped", "i", time) != NULL) ? OK : N_OK)
#define WinI_Modify(accessFlags,expression,value) ((PyObject_CallMethod(debugger_Helper_Python_Object, "modify", "(sss)",accessFlags,expression,value) != NULL) ? OK : N_OK)
#define WinI_Evaluate(accessFlags,expression,expressionType) (PyObject_CallMethod(debugger_Helper_Python_Object, "evaluate", "(sss)",accessFlags,expression,expressionType))
#define WinI_ReadRegister(accessFlags,registerName,expressionType) (PyObject_CallMethod(debugger_Helper_Python_Object, "readRegister", "(sss)",accessFlags,registerName,expressionType))
#define WinI_WriteRegister(accessFlags,registerName,registerValue,registerType) ((PyObject_CallMethod(debugger_Helper_Python_Object, "writeRegister", "(ssss)",accessFlags,registerName,registerValue,registerType) != NULL) ? OK : N_OK)


/* Private functions */
/*============================================================================*/

static void iSystem_SimpleMessage(const char* message)
{
    printf("%s: %d: %s \n",SWATT_Debugger_instance.file, SWATT_Debugger_instance.line, message);
}

uint8  PLAST_SaveAnyValue(PyObject* returnObj,const char* expressionType,va_list ap)
{

    uint8 winI_ErrCode=0;


    switch(expressionType[0]){
        case 's':
        {//signed integer
            switch(expressionType[4]){
                case '8'://8 bits
                {
                    sint8 *pVal = va_arg(ap, sint8*);
                    (*pVal)=(sint8)PyLong_AsLong(returnObj);
                }
                break;
                case '1'://16 bits
                {
                    sint16 *pVal = va_arg(ap, sint16*);
                    (*pVal)=(sint16)PyLong_AsLong(returnObj);

                }
                break;
                case '3'://32 bits
                {
                    sint32 *pVal = va_arg(ap, sint32*);
                    (*pVal)=(sint32)PyLong_AsLong(returnObj);

                }
                break;
            }
        }
        break;
        case 'u':
        {//signed integer
            switch(expressionType[4]){
                case '8'://8 bits
                {
                    uint8 *pVal = va_arg(ap, uint8*);
                    (*pVal)=(uint8)PyLong_AsLong(returnObj);
                }
                break;
                case '1'://16 bits
                {
                    uint16 *pVal = va_arg(ap, uint16*);
                    (*pVal)=(uint16)PyLong_AsLong(returnObj);

                }
                break;
                case '3'://32 bits
                {
                    uint32 *pVal = va_arg(ap, uint32*);
                    (*pVal)=(uint32)PyLong_AsLong(returnObj);

                }
                break;
            }
        }
        break;
        case 'i':
        {//integer
            int *pVal = va_arg(ap, int*);
            (*pVal)=(int)PyLong_AsLong(returnObj);
        }
        break;
        case 'l':
        {//integer
            long *pVal = va_arg(ap, long*);
            (*pVal)=PyLong_AsLong(returnObj);

        }
        break;
        case 'f':
        {//float
            float *pVal = va_arg(ap, float*);
            (*pVal)=(float)PyFloat_AsDouble(returnObj);
        }
        break;
        case 'd':
        {//float
            double *pVal = va_arg(ap, double*);
            (*pVal)=PyFloat_AsDouble(returnObj);
        }
        break;
        default:
        {
            iSystem_SimpleMessage("Type not yet supported");
            winI_ErrCode=1u;
        }
        break;



    }
    return winI_ErrCode;
}
uint8 PLAST_WinI_Connect(void)
{
    /* Objects we need to get a reference to a function or method */

    /*
	import isystem.connect as ic
	# Establish a connection and create a controller object
	cmgr = ic.ConnectionMgr()
	cmgr.connectMRU('')
	dbg = ic.CDebugFacade(cmgr)

     */

    PyObject *cmgr = NULL;//connection manager object
    PyObject *argList = NULL;
    uint8 retVal = 1;

    if(handle_iSystem_WinIdea_Python_Module!=NULL)
    {


        cmgr = PyObject_CallObject(PLAST_getDictionary(handle_iSystem_WinIdea_Python_Module,"ConnectionMgr"), NULL);

        //cmgr = PyObject_CallFunction(handle_iSystem_WinIdea_Python_Module,"ConnectionMgr", NULL);

        if(cmgr!=NULL)
        {

            PyObject_CallMethod(cmgr, "connectMRU", "s", "" );

            argList = Py_BuildValue("O", cmgr);
            debugger_Python_Object = PyObject_CallObject(PLAST_getDictionary(handle_iSystem_WinIdea_Python_Module,"CDebugFacade"), argList);
            //Py_DECREF(argList); TODO add this
        }
        else
        {
            debugger_Python_Object=NULL;
            iSystem_SimpleMessage("Debugger instantiation failed");
        }
        if(debugger_Python_Object != NULL)
        {
            retVal = 0;
            iSystem_SimpleMessage("Debugger instantiation success");
        }


    }
    //TODO remove the following ( debugging purposes only)
    //retVal=0;
    if(retVal==0){
        if(handle_Helper_Python_Module!=NULL){
            argList = Py_BuildValue("O", debugger_Python_Object);
            debugger_Helper_Python_Object=PyObject_CallObject(PLAST_getDictionary(handle_Helper_Python_Module,"debugger_helper"), argList);
        }
        if(debugger_Helper_Python_Object!=NULL){
            iSystem_SimpleMessage("Debugger helper instantiation success");
        }
        else{
            debugger_Helper_Python_Object=NULL;
            iSystem_SimpleMessage("Debugger helper instantiation failed");
            retVal=1;
        }

    }
    //TODO remove the following ( debugging purposes only)
    //retVal=0;
    return retVal;

}



static int iSystem_IsConnected(void)
{
    if (!iSystemDbg_Connected)
    {
        iSystem_SimpleMessage("Error: not yet connected to the debugger, call dbg.connect() first ");
        ZSWATT_DBG_ErrorHandlingBehavior(DBG_E_NOT_CONNECTED_SWATT);
        return DBG_E_NOT_CONNECTED_SWATT;
    }
    return DBG_E_OK_SWATT;
}

int iSystem_Connect(void)
{
    enum SWATT_DBG_ERROR_CODE retVal = DBG_E_OK_SWATT;
    if (PLAST_WinI_Connect()) // any error
    {
        iSystem_SimpleMessage("Error: cannot connect to the debugger");
        retVal = DBG_E_CANNOT_CONNECT_SWATT;
    }
    else
    {
        iSystem_SimpleMessage("Successfully connected to the debugger");
        iSystemDbg_Connected = 1;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_Configure(const char* param,const char*value)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    iSystem_SimpleMessage("Error: no such configuration parameter");
    // in case of success retVal=DBG_E_OK_SWATT;
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_Download(void)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_Download()) // any error
    {
        iSystem_SimpleMessage("Download failed ");
        retVal = DBG_E_FAILED_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_Reset(void)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_Reset())
    {
        iSystem_SimpleMessage("Cannot perform reset");
        retVal = DBG_E_FAILED_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_Run(void)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_Run())
    {
        iSystem_SimpleMessage("Cannot run");
        retVal = DBG_E_FAILED_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_Stop(void)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_Stop())
    {
        iSystem_SimpleMessage("Cannot stop");
        retVal = DBG_E_FAILED_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_StepInto(void)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_stepInto())
    {
        iSystem_SimpleMessage("Cannot step into");
        retVal = DBG_E_FAILED_SWATT;
    }
    retVal = DBG_E_FAILED_SWATT;
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_StepOver(void)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_stepOver())
    {
        iSystem_SimpleMessage("Cannot step over");
        retVal = DBG_E_FAILED_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_StepReturn(void)
{
    enum SWATT_DBG_ERROR_CODE retVal=DBG_E_FAILED_SWATT;
    if (WinI_stepReturn())
    {
        iSystem_SimpleMessage("Cannot step return");
        retVal = DBG_E_FAILED_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_BpSetOnFunction(const char* functionName)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_SetEnableBreakpoint(functionName))
    {
        iSystem_SimpleMessage("Cannot set breakpoint");
        retVal = DBG_E_CANNOT_SET_BREAKPOINT_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_BpClearOnFunction(const char* functionName)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_ClearSymbolBreakpoint(functionName))
    {
        iSystem_SimpleMessage("Cannot clear breakpoint");
        retVal = DBG_E_CANNOT_CLEAR_BREAKPOINT_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}


//#define WinI_SetLineBreakpoint(fileName, lineNr) ((PyObject_CallMethodObjArgs(debugger_Python_Object, "setBP", "O", Py_BuildValue("is", lineNr, fileName)) != NULL) ? OK : N_OK)

int iSystem_BpSetOnLineNumber(const char* fileName, unsigned int lineNr)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    //    if ((PyObject_CallMethod(debugger_Python_Object, "setBP", "O", Py_BuildValue("is", lineNr, fileName))) != NULL)
    WinI_SetLineBreakpoint(fileName,lineNr);
    //    if (WinI_SetLineBreakpoint(fileName,lineNr))
    //    {
    //        iSystem_SimpleMessage("Failure to set line breakpoint");
    //        retVal = DBG_E_CANNOT_SET_BREAKPOINT_SWATT;
    //    }
    //    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_BpClearAll(void)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_ClearAllBreakpoints())
    {
        iSystem_SimpleMessage("Failure to clear all breakpoints");
        retVal = DBG_E_CANNOT_CLEAR_BREAKPOINT_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_WaitUnitlStopped(unsigned int time)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_WaitForCpuStop(time))
    {
        iSystem_SimpleMessage("Execution did not stop in time");
        retVal = DBG_E_DID_NOT_STOPED_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_Modify(const char* accesType,const char* variableName,const char* variableValue)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_Modify(accesType,variableName,variableValue))
    {
        iSystem_SimpleMessage("Cannot modify Variable");
        retVal = DBG_E_FAILED_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_Evaluate(const char* accesType,const char* expressionName,const char* expressionType,...)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();

    PyObject* returnObj;
    uint8 winI_ErrCode = 0;
    returnObj=WinI_Evaluate(accesType,expressionName,expressionType);
    va_list ap;
    va_start (ap, expressionType);
    if(returnObj!=NULL){
        winI_ErrCode=PLAST_SaveAnyValue(returnObj,expressionType,ap);
        if (winI_ErrCode)
        {
            iSystem_SimpleMessage("Error evaluating");
            retVal = DBG_E_SYMBOL_NOT_FOUND_SWATT;
        }
    }
    else{
        iSystem_SimpleMessage("Did not manage to evaluate");
        retVal = DBG_E_SYMBOL_NOT_FOUND_SWATT;
    }

    va_end (ap);
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_ReadRegister(const char* accesType,const char* registerName,const char* registerType,...)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();

    PyObject* returnObj;
    uint8 winI_ErrCode = 0;
    returnObj=WinI_ReadRegister(accesType,registerName,registerType);
    va_list ap;
    va_start (ap, registerType);
    if(returnObj!=NULL){
        winI_ErrCode=PLAST_SaveAnyValue(returnObj,registerType,ap);
        if (winI_ErrCode)
        {
            iSystem_SimpleMessage("Error reading register ");
            retVal = DBG_E_SYMBOL_NOT_FOUND_SWATT;
        }
    }
    else{
        iSystem_SimpleMessage("Register  value not read");
        retVal = DBG_E_SYMBOL_NOT_FOUND_SWATT;
    }

    va_end (ap);
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_WriteRegister(const char* accesType,const char* registerName,const char* registerValue,const char* registerType)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    if (WinI_WriteRegister(accesType,registerName,registerValue,registerType))
    {
        iSystem_SimpleMessage("Cannot write Register");
        retVal = DBG_E_FAILED_SWATT;
    }
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int iSystem_Disconnect(void)
{
    enum SWATT_DBG_ERROR_CODE retVal = iSystem_IsConnected();
    iSystemDbg_Connected = 0;
    ZSWATT_DBG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PLAST_Debugger_SetErrorHandlingBehaviour( enum SWATT_DBG_ERROR_HANDLING_BEHAVIOR behaviour)
{
    enum SWATT_DBG_ERROR_CODE retVal;
#ifdef USE_DBG_SWATT_ERROR_HANDLER
    SWATT_Debugger_instance.errorHandlingBehaviorOption=behaviour;
    retVal = DBG_E_OK_SWATT;
    //iSystem_SimpleMessage("Error handling behaviour set");
#else
    retval=DBG_E_FAILED_SWATT;
#endif
    return retVal;
}

/* Exported functions */
/*============================================================================*/

void PLAST_Debugger_Init(void)
{
    
    handle_iSystem_WinIdea_Python_Module = PLAST_loadModule(ISYSTEM_MODULE);

    if (NULL == handle_iSystem_WinIdea_Python_Module)
    {
        SWATT_abort_executable("ERROR: Cannot load iSystem Interface.\n");
    }

    handle_Helper_Python_Module = PLAST_loadModule(HELPER_MODULE);

    if (NULL == handle_Helper_Python_Module)
    {
        SWATT_abort_executable("ERROR: Cannot load helper module.\n");
    }

    SWATT_Debugger_instance.dbg_api.connect = &iSystem_Connect;
    SWATT_Debugger_instance.dbg_api.configure = &iSystem_Configure;
    SWATT_Debugger_instance.dbg_api.download = &iSystem_Download;
    SWATT_Debugger_instance.dbg_api.reset = &iSystem_Reset;
    SWATT_Debugger_instance.dbg_api.run = &iSystem_Run;
    SWATT_Debugger_instance.dbg_api.stop = &iSystem_Stop;
    SWATT_Debugger_instance.dbg_api.stepInto = &iSystem_StepInto;
    SWATT_Debugger_instance.dbg_api.stepOver = &iSystem_StepOver;
    SWATT_Debugger_instance.dbg_api.stepReturn = &iSystem_StepReturn;
    SWATT_Debugger_instance.dbg_api.breakpint.setOnFunction = &iSystem_BpSetOnFunction;
    SWATT_Debugger_instance.dbg_api.breakpint.setOnLineNumber = &iSystem_BpSetOnLineNumber;
    SWATT_Debugger_instance.dbg_api.breakpint.clearOnFunction = &iSystem_BpClearOnFunction;
    SWATT_Debugger_instance.dbg_api.breakpint.clearAll = &iSystem_BpClearAll;
    SWATT_Debugger_instance.dbg_api.waitUnitlStopped = &iSystem_WaitUnitlStopped;
    SWATT_Debugger_instance.dbg_api.modify=&iSystem_Modify;
    SWATT_Debugger_instance.dbg_api.evaluate=&iSystem_Evaluate;
    SWATT_Debugger_instance.dbg_api.readRegister=&iSystem_ReadRegister;
    SWATT_Debugger_instance.dbg_api.writeRegister=&iSystem_WriteRegister;
    SWATT_Debugger_instance.dbg_api.disconnect = &iSystem_Disconnect;
    SWATT_Debugger_instance.dbg_api.setErrorHandlerBehaviour=&PLAST_Debugger_SetErrorHandlingBehaviour;
}

void PLAST_Debugger_DummyInit(void)
{
    
    handle_iSystem_WinIdea_Python_Module = NULL;
    handle_Helper_Python_Module=NULL;

    SWATT_Debugger_instance.dbg_api.connect = &iSystem_Connect;
    SWATT_Debugger_instance.dbg_api.configure = &iSystem_Configure;
    SWATT_Debugger_instance.dbg_api.download = &iSystem_Download;
    SWATT_Debugger_instance.dbg_api.reset = &iSystem_Reset;
    SWATT_Debugger_instance.dbg_api.run = &iSystem_Run;
    SWATT_Debugger_instance.dbg_api.stop = &iSystem_Stop;
    SWATT_Debugger_instance.dbg_api.stepInto = &iSystem_StepInto;
    SWATT_Debugger_instance.dbg_api.stepOver = &iSystem_StepOver;
    SWATT_Debugger_instance.dbg_api.stepReturn = &iSystem_StepReturn;
    SWATT_Debugger_instance.dbg_api.breakpint.setOnFunction = &iSystem_BpSetOnFunction;
    SWATT_Debugger_instance.dbg_api.breakpint.setOnLineNumber = &iSystem_BpSetOnLineNumber;
    SWATT_Debugger_instance.dbg_api.breakpint.clearOnFunction = &iSystem_BpClearOnFunction;
    SWATT_Debugger_instance.dbg_api.breakpint.clearAll = &iSystem_BpClearAll;
    SWATT_Debugger_instance.dbg_api.waitUnitlStopped = &iSystem_WaitUnitlStopped;
    SWATT_Debugger_instance.dbg_api.modify=&iSystem_Modify;
    SWATT_Debugger_instance.dbg_api.evaluate=&iSystem_Evaluate;
    SWATT_Debugger_instance.dbg_api.readRegister=&iSystem_ReadRegister;
    SWATT_Debugger_instance.dbg_api.writeRegister=&iSystem_WriteRegister;
    SWATT_Debugger_instance.dbg_api.disconnect = &iSystem_Disconnect;
    SWATT_Debugger_instance.dbg_api.setErrorHandlerBehaviour=&PLAST_Debugger_SetErrorHandlingBehaviour;
}

/* Notice: the file ends with a blank new line to avoid compiler warnings */

