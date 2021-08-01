/*============================================================================*/
/*                        I BS SOFTWARE GROUP                                 */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*/
/*!
 * $Source: PLAST_DBCParser.c $
 * $Author: Mancas, Andrei04 (uidv4966) $
 */
/*============================================================================*/
/* DESCRIPTION :                                                              */
/** \file
    Wrappers for PLAST dbcParser.
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

#include "PLAST_DBCParser.h"

/* Constants and types  */
/*============================================================================*/
#define DBCPARSER_PYTHON_MODULE "PlatformFiles.ParserDBC_Interface"
#define DBCPARSER_VECTOR_PYTHON_MODULE "PlatformFiles.VECTOR_Interface"
#define DBCPARSER_THREADING_MODULE "threading"
//#define NULL 0


/* Variables */
/*============================================================================*/

struct PLAST_DBCParser_class PLAST_DBCParser_instance ;

static PyObject* handle_DBCParser_Python_Module= NULL;
static PyObject* handle_DBCParser_Vector_Python_Module= NULL;
static PyObject* handle_DBCParser_Threading_Python_Module=NULL;

/* Private functions prototypes */
/*============================================================================*/
static void DBCParser_SimpleMessage(const char* message);
static int DBCParser_getDBCParser(PLAST_DBCParser* dbcParser,char* dbcFile);
static int DBCParser_getCANMessage(PLAST_DBCParser dbcParser,char* msgName,PLAST_CANMessage* canMessage);
static int DBCParser_getSignalValue(PLAST_CANMessage canMessage,char* signalName,char* signalValue);
static int DBCParser_setSignalValue(PLAST_CANMessage canMessage,char* signalName,char* signalValue);
static int DBCParser_startSending(PLAST_CANMessage canMessage);
static int DBCParser_stopSending(PLAST_CANMessage canMessage);
static int PLAST_DBCParser_SetErrorHandlingBehaviour( enum SWATT_DBC_ERROR_HANDLING_BEHAVIOR behaviour);

/* Inline functions */
/*============================================================================*/

#define CallPythonMethod(pythonObject,methodName,...) ((PyObject_CallMethod(pythonObject,methodName,__VA_ARGS__) != NULL) ? OK : N_OK)
#define CallPythonMethodReturn(pythonObject,methodName,...) (PyObject_CallMethod(pythonObject,methodName, __VA_ARGS__))

//(fi) = = = f is for float i is for integer () is for tuple



/* Private functions */
/*============================================================================*/


static void DBCParser_SimpleMessage(const char* message)
{
    printf("%s: %d: %s \n",PLAST_DBCParser_instance.file, PLAST_DBCParser_instance.line, message);
}


int DBCParser_getDBCParser(PLAST_DBCParser* dbcParser,char* dbcFile)
{
    enum SWATT_DBC_ERROR_CODE retVal = DBC_E_OK_SWATT;

    PyObject *argList = NULL;

    if(handle_DBCParser_Python_Module==NULL||handle_DBCParser_Vector_Python_Module==NULL){
        DBCParser_SimpleMessage("Error: DBC Parser Module not enabled");
        retVal = DBC_E_NOT_INITIALIZED_SWATT;
    }
    else{


        argList = Py_BuildValue("(s)", dbcFile);
        (*dbcParser) = PyObject_CallObject(PLAST_getDictionary(handle_DBCParser_Python_Module,"DBC_Parser"), argList);

        Py_DECREF(argList);

        if ((*dbcParser)==NULL)// any error
        {
            DBCParser_SimpleMessage("Error: Can not instantiate a dbc parser");
            retVal = DBC_E_NOT_INITIALIZED_SWATT;
        }
        else
        {
           // DBCParser_SimpleMessage("Successfully instantiated dbc parser ");

        }
    }
    ZSWATT_DBC_ErrorHandlingBehavior(retVal);
    return retVal;
}

int DBCParser_getCANMessage(PLAST_DBCParser dbcParser,char* msgName,PLAST_CANMessage* canMessage)
{
    enum SWATT_DBC_ERROR_CODE retVal = DBC_E_OK_SWATT;

    PyObject *argList = NULL;

    if(dbcParser==NULL){
        DBCParser_SimpleMessage("Error: dbc parser object not initialized");
        retVal = DBC_E_NOT_INITIALIZED_SWATT;
    }
    else{


        argList = Py_BuildValue("(Os)", dbcParser,msgName);
        (*canMessage) = PyObject_CallObject(PLAST_getDictionary(handle_DBCParser_Vector_Python_Module,"CANMessage"), argList);
        Py_DECREF(argList);

        if ((*canMessage)==NULL)// any error
        {
            DBCParser_SimpleMessage("Error: Can not instantiate a can message");
            retVal = DBC_E_NOT_INITIALIZED_SWATT;
        }
        else
        {
//            /DBCParser_SimpleMessage("Successfully instantiated a can  ");

        }
    }
    ZSWATT_DBC_ErrorHandlingBehavior(retVal);
    return retVal;
}


int DBCParser_getSignalValue(PLAST_CANMessage canMessage,char* signalName,char* signalValue)
{
    enum SWATT_DBC_ERROR_CODE retVal = DBC_E_OK_SWATT;
    PyObject* outputVal;
    char* auxStringPointer;
    if (canMessage==NULL) // any error
    {
        DBCParser_SimpleMessage("Can message not initialized ");
        retVal = DBC_E_NOT_INITIALIZED_SWATT;
    }else{
        outputVal=CallPythonMethodReturn(canMessage,"GetSignalValue","s",signalName);
        if((outputVal!=NULL)&&PyString_Check(outputVal)){

            auxStringPointer= PyString_AsString(outputVal);
            strcpy(signalValue,auxStringPointer);
        }else
        {
            DBCParser_SimpleMessage("Signal value read failed ");
            retVal = DBC_E_FAILED_SWATT;
        }
    }
    ZSWATT_DBC_ErrorHandlingBehavior(retVal);
    return retVal;
}

int DBCParser_setSignalValue(PLAST_CANMessage canMessage,char* signalName,char* signalValue)
{
    enum SWATT_DBC_ERROR_CODE retVal = DBC_E_OK_SWATT;
    if (canMessage==NULL) // any error
    {
        DBCParser_SimpleMessage("Can message not initialized ");
        retVal = DBC_E_NOT_INITIALIZED_SWATT;
    }
    else
    {
       if(CallPythonMethod(canMessage,"SetSignalValue","(ss)",signalName,signalValue))//any error
       {
           DBCParser_SimpleMessage("Signal value set failed ");
           retVal = DBC_E_FAILED_SWATT;
       }
    }
    ZSWATT_DBC_ErrorHandlingBehavior(retVal);
    return retVal;
}

int DBCParser_startSending(PLAST_CANMessage canMessage)
{
    enum SWATT_DBC_ERROR_CODE retVal = DBC_E_OK_SWATT;
    if (canMessage==NULL) // any error
    {
        DBCParser_SimpleMessage("Can message not initialized ");
        retVal = DBC_E_NOT_INITIALIZED_SWATT;
    }
    else
    {
       if(CallPythonMethod(canMessage,"StartSending",NULL))//any error
       {
           DBCParser_SimpleMessage("start sending CAN message failed ");
           retVal = DBC_E_FAILED_SWATT;
       }
    }
    ZSWATT_DBC_ErrorHandlingBehavior(retVal);
    return retVal;
}

int DBCParser_stopSending(PLAST_CANMessage canMessage)
{
    enum SWATT_DBC_ERROR_CODE retVal = DBC_E_OK_SWATT;
    if (canMessage==NULL) // any error
    {
        DBCParser_SimpleMessage("Can message not initialized ");
        retVal = DBC_E_NOT_INITIALIZED_SWATT;
    }
    else
    {
        if(CallPythonMethod(canMessage,"StopSending",NULL))//any error
        {
            DBCParser_SimpleMessage("stop sending CAN message failed ");
            retVal = DBC_E_FAILED_SWATT;
        }
    }
    ZSWATT_DBC_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PLAST_DBCParser_SetErrorHandlingBehaviour( enum SWATT_DBC_ERROR_HANDLING_BEHAVIOR behaviour)
{
    enum SWATT_DBC_ERROR_CODE retVal;
#ifdef USE_DBC_SWATT_ERROR_HANDLER
    PLAST_DBCParser_instance.errorHandlingBehaviorOption=behaviour;
    retVal = DBC_E_OK_SWATT;
    //iSystem_SimpleMessage("Error handling behaviour set");
#else
    retval=DBC_E_FAILED_SWATT;
#endif
    return retVal;
}


/* Exported functions */
/*============================================================================*/

void PLAST_DBCParser_Init(void){

    handle_DBCParser_Python_Module = PLAST_loadModule(DBCPARSER_PYTHON_MODULE);

    if (NULL == handle_DBCParser_Python_Module)
    {
        SWATT_abort_executable("ERROR: Can not load dbc parser module.\n");
    }

    handle_DBCParser_Vector_Python_Module = PLAST_loadModule(DBCPARSER_VECTOR_PYTHON_MODULE);

    if (NULL == handle_DBCParser_Vector_Python_Module)
    {
        SWATT_abort_executable("ERROR: Can not load vector module.\n");
    }

//import threading
    handle_DBCParser_Threading_Python_Module = PLAST_loadModule(DBCPARSER_THREADING_MODULE);

    if (NULL == handle_DBCParser_Threading_Python_Module)
    {
        SWATT_abort_executable("ERROR: Can not load threading module.\n");
    }

    PLAST_DBCParser_instance.dbc_api.getDBCParser=&DBCParser_getDBCParser;
    PLAST_DBCParser_instance.dbc_api.getCANMessage=&DBCParser_getCANMessage;
    PLAST_DBCParser_instance.dbc_api.getSignalValue=&DBCParser_getSignalValue;
    PLAST_DBCParser_instance.dbc_api.setSignalValue=&DBCParser_setSignalValue;
    PLAST_DBCParser_instance.dbc_api.startSending=&DBCParser_startSending;
    PLAST_DBCParser_instance.dbc_api.stopSending=&DBCParser_stopSending;
    PLAST_DBCParser_instance.dbc_api.setErrorHandlerBehaviour=&PLAST_DBCParser_SetErrorHandlingBehaviour;

}

void PLAST_DBCParser_DummyInit(void){

    PLAST_DBCParser_instance.dbc_api.getDBCParser=&DBCParser_getDBCParser;
    PLAST_DBCParser_instance.dbc_api.getCANMessage=&DBCParser_getCANMessage;
    PLAST_DBCParser_instance.dbc_api.getSignalValue=&DBCParser_getSignalValue;
    PLAST_DBCParser_instance.dbc_api.setSignalValue=&DBCParser_setSignalValue;
    PLAST_DBCParser_instance.dbc_api.startSending=&DBCParser_startSending;
    PLAST_DBCParser_instance.dbc_api.stopSending=&DBCParser_stopSending;
    PLAST_DBCParser_instance.dbc_api.setErrorHandlerBehaviour=&PLAST_DBCParser_SetErrorHandlingBehaviour;

}


/* Notice: the file ends with a blank new line to avoid compiler warnings */


