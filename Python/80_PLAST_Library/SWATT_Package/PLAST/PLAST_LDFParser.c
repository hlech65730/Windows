/*============================================================================*/
/*                        I BS SOFTWARE GROUP                                 */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*/
/*!
 * $Source: PLAST_LDFParser.c $
 * $Author: Mancas, Andrei04 (uidv4966) $
 */
/*============================================================================*/
/* DESCRIPTION :                                                              */
/** \file
    Wrappers for PLAST ldfParser.
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

#include "PLAST_LDFParser.h"

/* Constants and types  */
/*============================================================================*/
#define LDFPARSER_PYTHON_MODULE "PlatformFiles.ParserLDF_Interface"
#define LDFPARSER_VECTOR_PYTHON_MODULE "PlatformFiles.VECTOR_Interface"
#define LDFPARSER_THREADING_MODULE "threading"
//#define NULL 0


/* Variables */
/*============================================================================*/

struct PLAST_LDFParser_class PLAST_LDFParser_instance ;

static PyObject* handle_LDFParser_Python_Module= NULL;
static PyObject* handle_LDFParser_Vector_Python_Module= NULL;
static PyObject* handle_LDFParser_Threading_Python_Module=NULL;

/* Private functions prototypes */
/*============================================================================*/
static void LDFParser_SimpleMessage(const char* message);
static int LDFParser_getLDFParser(PLAST_LDFParser* ldfParser,char* ldfFile);
static int LDFParser_getLINFrame(PLAST_LDFParser ldfParser,char* frmName,PLAST_LINFrame* linFrame);
static int LDFParser_getLINNodeMaster(PLAST_LDFParser ldfParser,char* schedTable,PLAST_LINNode* linNode);
static int LDFParser_getLINNodeSlave(PLAST_LDFParser ldfParser,PLAST_LINNode* linNode);
static int LDFParser_getSignalValue(PLAST_LINFrame linFrame,char* signalName,char* signalValue);
static int LDFParser_setSignalValue(PLAST_LINFrame linFrame,char* signalName,char* signalValue);
static int LDFParser_AddFrame(PLAST_LINNode node,PLAST_LINFrame frame);
static int LDFParser_RemoveFrame(PLAST_LINNode node,PLAST_LINFrame frame);
static int LDFParser_GetFrames(PLAST_LINNode node,int maxNumberOfFrames,PLAST_LINFrame* returnedFrames,int* numberOfReturnedFrames);
static int LDFParser_startSending(PLAST_LINFrame linFrame);
static int LDFParser_stopSending(PLAST_LINFrame linFrame);
static int PLAST_LDFParser_SetErrorHandlingBehaviour( enum SWATT_LDF_ERROR_HANDLING_BEHAVIOR behaviour);

/* Inline functions */
/*============================================================================*/

#define CallPythonMethod(pythonObject,methodName,...) ((PyObject_CallMethod(pythonObject,methodName,__VA_ARGS__) != NULL) ? OK : N_OK)
#define CallPythonMethodReturn(pythonObject,methodName,...) (PyObject_CallMethod(pythonObject,methodName, __VA_ARGS__))

//(fi) = = = f is for float i is for integer () is for tuple



/* Private functions */
/*============================================================================*/


static void LDFParser_SimpleMessage(const char* message)
{
    printf("%s: %d: %s \n",PLAST_LDFParser_instance.file, PLAST_LDFParser_instance.line, message);
}


static int LDFParser_getLDFParser(PLAST_LDFParser* ldfParser,char* ldfFile)
{
    enum SWATT_LDF_ERROR_CODE retVal = LDF_E_OK_SWATT;

    PyObject *argList = NULL;


    if(handle_LDFParser_Python_Module==NULL||handle_LDFParser_Vector_Python_Module==NULL){
        LDFParser_SimpleMessage("Error: LDF Parser Module not enabled");
        retVal = LDF_E_NOT_INITIALIZED_SWATT;
    }
    else{


        argList = Py_BuildValue("(s)", ldfFile);
        (*ldfParser) = PyObject_CallObject(PLAST_getDictionary(handle_LDFParser_Python_Module,"LIN_Parser"), argList);

        Py_DECREF(argList);

        if ((*ldfParser)==NULL)// any error
        {
            LDFParser_SimpleMessage("Error: Can not instantiate a ldf parser");
            retVal = LDF_E_NOT_INITIALIZED_SWATT;
        }
        else
        {
           //LDFParser_SimpleMessage("Successfully instantiated ldf parser ");

        }
    }
    ZSWATT_LDF_ErrorHandlingBehavior(retVal);
    return retVal;
}

static int LDFParser_getLINFrame(PLAST_LDFParser ldfParser,char* frmName,PLAST_LINFrame* linFrame)
{
    enum SWATT_LDF_ERROR_CODE retVal = LDF_E_OK_SWATT;

    PyObject *argList = NULL;

    if(ldfParser==NULL){
        LDFParser_SimpleMessage("Error: ldf parser object not initialized");
        retVal = LDF_E_NOT_INITIALIZED_SWATT;
    }
    else{


        argList = Py_BuildValue("(Os)", ldfParser,frmName);
        (*linFrame) = PyObject_CallObject(PLAST_getDictionary(handle_LDFParser_Vector_Python_Module,"LINFrame"), argList);
        Py_DECREF(argList);

        if ((*linFrame)==NULL)// any error
        {
            LDFParser_SimpleMessage("Error: Can not instantiate a lin frame");
            retVal = LDF_E_NOT_INITIALIZED_SWATT;
        }
        else
        {
//            //LDFParser_SimpleMessage("Successfully instantiated a can  ");

        }
    }
    ZSWATT_LDF_ErrorHandlingBehavior(retVal);
    return retVal;
}
static int LDFParser_getLINNodeMaster(PLAST_LDFParser ldfParser,char* schedTable,PLAST_LINNode* linNode)
{
    enum SWATT_LDF_ERROR_CODE retVal = LDF_E_OK_SWATT;

    PyObject *argList = NULL;

    if(ldfParser==NULL){
        LDFParser_SimpleMessage("Error: ldf parser object not initialized");
        retVal = LDF_E_NOT_INITIALIZED_SWATT;
    }
    else{


        argList = Py_BuildValue("(Os)", ldfParser,schedTable);
        (*linNode) = PyObject_CallObject(PLAST_getDictionary(handle_LDFParser_Vector_Python_Module,"LINNode"), argList);
        Py_DECREF(argList);

        if ((*linNode)==NULL)// any error
        {
            LDFParser_SimpleMessage("Error: Can not instantiate a lin master node");
            retVal = LDF_E_NOT_INITIALIZED_SWATT;
        }
        else
        {
//            /LDFParser_SimpleMessage("Successfully instantiated a can  ");

        }
    }
    ZSWATT_LDF_ErrorHandlingBehavior(retVal);
    return retVal;
}

static int LDFParser_getLINNodeSlave(PLAST_LDFParser ldfParser,PLAST_LINNode* linNode)
{
    enum SWATT_LDF_ERROR_CODE retVal = LDF_E_OK_SWATT;

    PyObject *argList = NULL;

    if(ldfParser==NULL){
        LDFParser_SimpleMessage("Error: ldf parser object not initialized");
        retVal = LDF_E_NOT_INITIALIZED_SWATT;
    }
    else{


        argList = Py_BuildValue("(O)", ldfParser);
        (*linNode) = PyObject_CallObject(PLAST_getDictionary(handle_LDFParser_Vector_Python_Module,"LINNode"), argList);
        Py_DECREF(argList);

        if ((*linNode)==NULL)// any error
        {
            LDFParser_SimpleMessage("Error: Can not instantiate a lin slave node");
            retVal = LDF_E_NOT_INITIALIZED_SWATT;
        }
        else
        {
//            /LDFParser_SimpleMessage("Successfully instantiated a can  ");

        }
    }
    ZSWATT_LDF_ErrorHandlingBehavior(retVal);
    return retVal;
}


static int LDFParser_getSignalValue(PLAST_LINFrame linFrame,char* signalName,char* signalValue)
{
    enum SWATT_LDF_ERROR_CODE retVal = LDF_E_OK_SWATT;
    PyObject* outputVal;
    char* auxStringPointer;
    if (linFrame==NULL) // any error
    {
        LDFParser_SimpleMessage("LIN frame not initialized ");
        retVal = LDF_E_NOT_INITIALIZED_SWATT;
    }else{
        outputVal=CallPythonMethodReturn(linFrame,"GetSignalValue","s",signalName);
        if((outputVal!=NULL)&&PyString_Check(outputVal)){

            auxStringPointer= PyString_AsString(outputVal);
            strcpy(signalValue,auxStringPointer);
        }else
        {
            LDFParser_SimpleMessage("Signal value read failed ");
            retVal = LDF_E_FAILED_SWATT;
        }
    }
    ZSWATT_LDF_ErrorHandlingBehavior(retVal);
    return retVal;
}

static int LDFParser_setSignalValue(PLAST_LINFrame linFrame,char* signalName,char* signalValue)
{
    enum SWATT_LDF_ERROR_CODE retVal = LDF_E_OK_SWATT;
    if (linFrame==NULL) // any error
    {
        LDFParser_SimpleMessage("LIN frame not initialized ");
        retVal = LDF_E_NOT_INITIALIZED_SWATT;
    }
    else
    {
       if(CallPythonMethod(linFrame,"SetSignalValue","(ss)",signalName,signalValue))//any error
       {
           LDFParser_SimpleMessage("Signal value set failed ");
           retVal = LDF_E_FAILED_SWATT;
       }
    }
    ZSWATT_LDF_ErrorHandlingBehavior(retVal);
    return retVal;
}

static int LDFParser_AddFrame(PLAST_LINNode node,PLAST_LINFrame frame)
{
    enum SWATT_LDF_ERROR_CODE retVal = LDF_E_OK_SWATT;
    if (node==NULL) // any error
    {
        LDFParser_SimpleMessage("LIN node not initialized ");
        retVal = LDF_E_NOT_INITIALIZED_SWATT;
    }
    else
    {
       if(CallPythonMethod(node,"AddFrame","O",frame))//any error
       {
           LDFParser_SimpleMessage("Frame could not be added. ");
           retVal = LDF_E_FAILED_SWATT;
       }
    }
    ZSWATT_LDF_ErrorHandlingBehavior(retVal);

    return retVal;
}

static int LDFParser_RemoveFrame(PLAST_LINNode node,PLAST_LINFrame frame)
{
    enum SWATT_LDF_ERROR_CODE retVal = LDF_E_OK_SWATT;
    if (node==NULL) // any error
    {
        LDFParser_SimpleMessage("LIN node not initialized ");
        retVal = LDF_E_NOT_INITIALIZED_SWATT;
    }
    else
    {
       if(CallPythonMethod(node,"RemoveFrame","O",frame))//any error
       {
           LDFParser_SimpleMessage("Frame could not be removed. ");
           retVal = LDF_E_FAILED_SWATT;
       }
    }
    ZSWATT_LDF_ErrorHandlingBehavior(retVal);
    return retVal;
}

static int LDFParser_GetFrames(PLAST_LINNode node,int maxNumberOfFrames,PLAST_LINFrame* returnedFrames,int* numberOfReturnedFrames)
{
    PyObject* frameList;
    enum SWATT_LDF_ERROR_CODE retVal = LDF_E_OK_SWATT;
    if (node==NULL) // any error
    {
        LDFParser_SimpleMessage("LIN node not initialized ");
        retVal = LDF_E_NOT_INITIALIZED_SWATT;
    }
    else
    {
        frameList=CallPythonMethodReturn(node,"GetFrames",NULL);
       if((frameList!=NULL)&&(PyList_Check(frameList)))//
       {
          Py_ssize_t listSize=PyList_Size(frameList);
          if(listSize<=maxNumberOfFrames){
              *numberOfReturnedFrames=listSize;
          }
          else{
              *numberOfReturnedFrames=maxNumberOfFrames;
              LDFParser_SimpleMessage(" The number of frames in the node is larger than maxNumberOfFrames ");
          }
          Py_ssize_t i;
          for(i=0;i<(*numberOfReturnedFrames);i++){
              returnedFrames[i]=PyList_GetItem(frameList,i);
          }

       }else{
               LDFParser_SimpleMessage("Failed to get frames from node ");
               retVal = LDF_E_FAILED_SWATT;
       }
    }
    ZSWATT_LDF_ErrorHandlingBehavior(retVal);
    return retVal;
}

static int LDFParser_startSending(PLAST_LINNode node)
{
    enum SWATT_LDF_ERROR_CODE retVal = LDF_E_OK_SWATT;
    if (node==NULL) // any error
    {
        LDFParser_SimpleMessage("LIN node not initialized ");
        retVal = LDF_E_NOT_INITIALIZED_SWATT;
    }
    else
    {
       if(CallPythonMethod(node,"StartSending",NULL))//any error
       {
           LDFParser_SimpleMessage("start sending LIN node failed ");
           retVal = LDF_E_FAILED_SWATT;
       }
    }
    ZSWATT_LDF_ErrorHandlingBehavior(retVal);
    return retVal;
}

static int LDFParser_stopSending(PLAST_LINNode node)
{
    enum SWATT_LDF_ERROR_CODE retVal = LDF_E_OK_SWATT;
    if (node==NULL) // any error
    {
        LDFParser_SimpleMessage("LIN node not initialized ");
        retVal = LDF_E_NOT_INITIALIZED_SWATT;
    }
    else
    {
        if(CallPythonMethod(node,"StopSending",NULL))//any error
        {
            LDFParser_SimpleMessage("stop sending LIN node failed ");
            retVal = LDF_E_FAILED_SWATT;
        }
    }
    ZSWATT_LDF_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PLAST_LDFParser_SetErrorHandlingBehaviour( enum SWATT_LDF_ERROR_HANDLING_BEHAVIOR behaviour)
{
    enum SWATT_LDF_ERROR_CODE retVal;
#ifdef USE_LDF_SWATT_ERROR_HANDLER
    PLAST_LDFParser_instance.errorHandlingBehaviorOption=behaviour;
    retVal = LDF_E_OK_SWATT;
    //iSystem_SimpleMessage("Error handling behaviour set");
#else
    retval=LDF_E_FAILED_SWATT;
#endif
    return retVal;
}


/* Exported functions */
/*============================================================================*/

void PLAST_LDFParser_Init(void){

    handle_LDFParser_Python_Module = PLAST_loadModule(LDFPARSER_PYTHON_MODULE);

    if (NULL == handle_LDFParser_Python_Module)
    {
        SWATT_abort_executable("ERROR: Can not load ldf parser module.\n");
    }

    handle_LDFParser_Vector_Python_Module = PLAST_loadModule(LDFPARSER_VECTOR_PYTHON_MODULE);

    if (NULL == handle_LDFParser_Vector_Python_Module)
    {
        SWATT_abort_executable("ERROR: Can not load vector module.\n");
    }

//import threading
    handle_LDFParser_Threading_Python_Module = PLAST_loadModule(LDFPARSER_THREADING_MODULE);

    if (NULL == handle_LDFParser_Threading_Python_Module)
    {
        SWATT_abort_executable("ERROR: Can not load threading module.\n");
    }

    PLAST_LDFParser_instance.ldf_api.getLDFParser=&LDFParser_getLDFParser;
    PLAST_LDFParser_instance.ldf_api.getLINFrame=&LDFParser_getLINFrame;
    PLAST_LDFParser_instance.ldf_api.getLINNodeMaster=&LDFParser_getLINNodeMaster;
    PLAST_LDFParser_instance.ldf_api.getLINNodeSlave=&LDFParser_getLINNodeSlave;
    PLAST_LDFParser_instance.ldf_api.getSignalValue=&LDFParser_getSignalValue;
    PLAST_LDFParser_instance.ldf_api.setSignalValue=&LDFParser_setSignalValue;
    PLAST_LDFParser_instance.ldf_api.addFrame=&LDFParser_AddFrame;
    PLAST_LDFParser_instance.ldf_api.removeFrame=&LDFParser_RemoveFrame;
    PLAST_LDFParser_instance.ldf_api.getFrames=&LDFParser_GetFrames;
    PLAST_LDFParser_instance.ldf_api.startSending=&LDFParser_startSending;
    PLAST_LDFParser_instance.ldf_api.stopSending=&LDFParser_stopSending;
    PLAST_LDFParser_instance.ldf_api.setErrorHandlerBehaviour=&PLAST_LDFParser_SetErrorHandlingBehaviour;

}

void PLAST_LDFParser_DummyInit(void){

    PLAST_LDFParser_instance.ldf_api.getLDFParser=&LDFParser_getLDFParser;
    PLAST_LDFParser_instance.ldf_api.getLINFrame=&LDFParser_getLINFrame;
    PLAST_LDFParser_instance.ldf_api.getLINNodeMaster=&LDFParser_getLINNodeMaster;
    PLAST_LDFParser_instance.ldf_api.getLINNodeSlave=&LDFParser_getLINNodeSlave;
    PLAST_LDFParser_instance.ldf_api.getSignalValue=&LDFParser_getSignalValue;
    PLAST_LDFParser_instance.ldf_api.setSignalValue=&LDFParser_setSignalValue;
    PLAST_LDFParser_instance.ldf_api.addFrame=&LDFParser_AddFrame;
    PLAST_LDFParser_instance.ldf_api.removeFrame=&LDFParser_RemoveFrame;
    PLAST_LDFParser_instance.ldf_api.getFrames=&LDFParser_GetFrames;
    PLAST_LDFParser_instance.ldf_api.startSending=&LDFParser_startSending;
    PLAST_LDFParser_instance.ldf_api.stopSending=&LDFParser_stopSending;
    PLAST_LDFParser_instance.ldf_api.setErrorHandlerBehaviour=&PLAST_LDFParser_SetErrorHandlingBehaviour;

}


/* Notice: the file ends with a blank new line to avoid compiler warnings */


