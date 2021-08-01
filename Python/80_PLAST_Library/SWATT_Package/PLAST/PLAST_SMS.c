/*============================================================================*/
/*                        I BS SOFTWARE GROUP                                 */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*/
/*!
 * $Source: PLAST_SMS.c $
 * $Author: Mancas, Andrei04 (uidv4966) $
 */
/*============================================================================*/
/* DESCRIPTION :                                                              */
/** \file
    Wrappers for PLAST SMS module.
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

#include "PLAST_SMS.h"

/* Constants and types  */
/*============================================================================*/
#define SMS_PYTHON_MODULE "PlatformFiles.DEVICE_Interface"

//#define NULL 0


/* Variables */
/*============================================================================*/

struct PLAST_SMS_class PLAST_SMS_instance ;

static PyObject* handle_SMS_Python_Module= NULL, *SMS_Python_Object = NULL;
static uint8 SMS_Connected = 0;


/* Private functions prototypes */
/*============================================================================*/
static void SMS_SimpleMessage(const char* message);
int SMS_Connect(void);
int SMS_SetPos(int serNum,int newPos);
int SMS_Reset(int serNum);
int SMS_Inc(int serNum);
int SMS_Dec(int serNum);
int SMS_ReadPos(int serNum,int* position);
int SMS_GetHallState(int serNum,char* a,char* b);
int SMS_SetHallErr(int serNum,char * string);
int SMS_SetBlock(int serNum,int blockPos, char * blockType);
int SMS_SetPinch(int serNum,int pinchPos, char * pinchType);
int PLAST_SMS_SetErrorHandlingBehaviour( enum SWATT_SMS_ERROR_HANDLING_BEHAVIOR behaviour);
/* Inline functions */
/*============================================================================*/

#define SMS_SetPos_Python(serNum,newPos) ((PyObject_CallMethod(SMS_Python_Object, "SetPos", "(ii)",serNum,newPos) != NULL) ? OK : N_OK)
#define SMS_Reset_Python(serNum) ((PyObject_CallMethod(SMS_Python_Object, "Reset","i",serNum) != NULL) ? OK : N_OK)
#define SMS_Inc_Python(serNum) ((PyObject_CallMethod(SMS_Python_Object, "Inc","i",serNum) != NULL) ? OK : N_OK)
#define SMS_Dec_Python(serNum) ((PyObject_CallMethod(SMS_Python_Object, "Dec","i",serNum) != NULL) ? OK : N_OK)
#define SMS_ReadPos_Python(serNum) (PyObject_CallMethod(SMS_Python_Object, "ReadPos","i",serNum))
#define SMS_GetHallState_Python(serNum) (PyObject_CallMethod(SMS_Python_Object, "GetHallState","i",serNum))
#define SMS_SetHallErr_Python(serNum,string) ((PyObject_CallMethod(SMS_Python_Object, "SetHallErr", "(is)",serNum,string) != NULL) ? OK : N_OK)
#define SMS_SetBlock_Python(serNum,blockPos,blockType) ((PyObject_CallMethod(SMS_Python_Object, "SetBlock", "(iis)",serNum,blockPos,blockType) != NULL) ? OK : N_OK)
#define SMS_SetPinch_Python(serNum,pinchPos,pinchType) ((PyObject_CallMethod(SMS_Python_Object, "SetPinch", "(iis)",serNum,pinchPos,pinchType) != NULL) ? OK : N_OK)




//(fi) = = = f is for float i is for integer () is for tuple



/* Private functions */
/*============================================================================*/


static void SMS_SimpleMessage(const char* message)
{
    printf("%s: %d: %s \n",PLAST_SMS_instance.file, PLAST_SMS_instance.line, message);
}


int SMS_Connect(void)
{
    enum SWATT_SMS_ERROR_CODE retVal = SMS_E_OK_SWATT;

    if(handle_SMS_Python_Module==NULL){
        SMS_SimpleMessage("Error: SMS Module not enabled");
        retVal = SMS_E_CANNOT_CONNECT_SWATT;
    }
    else{

        PyObject* SMSClass=NULL;

        SMSClass=PLAST_getDictionary(handle_SMS_Python_Module, "SMSInstance");

        if(SMSClass!=NULL){
            SMS_Python_Object = PyInstance_New(SMSClass, NULL, NULL);
        }else{
            SMS_Python_Object=NULL;
        }


        if ( (SMS_Python_Object==NULL))// any error
        {
            SMS_SimpleMessage("Error: Can not connect to SMS");
            retVal = SMS_E_CANNOT_CONNECT_SWATT;
        }
        else
        {
            SMS_SimpleMessage("Successfully connected to SMS ");
            SMS_Connected = 1;
        }
    }
    ZSWATT_SMS_ErrorHandlingBehavior(retVal);
    return retVal;
}


static int SMS_IsConnected(void)
{
    if (!SMS_Connected)
    {
        SMS_SimpleMessage("Error: not yet connected to SMS, call sg.connect() first ");
        ZSWATT_SMS_ErrorHandlingBehavior(SMS_E_NOT_CONNECTED_SWATT);
        return SMS_E_NOT_CONNECTED_SWATT;
    }
    return SMS_E_OK_SWATT;
}



int SMS_SetPos(int serNum,int newPos)
{
    enum SWATT_SMS_ERROR_CODE retVal = SMS_IsConnected();
    if (SMS_SetPos_Python(serNum,newPos)) // any error
    {
        SMS_SimpleMessage("Can not set SMS position ");
        retVal = SMS_E_CANNOT_CONNECT_SWATT;
    }
    ZSWATT_SMS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SMS_Reset(int serNum)
{
    enum SWATT_SMS_ERROR_CODE retVal = SMS_IsConnected();
    if (SMS_Reset_Python(serNum)) // any error
    {
        SMS_SimpleMessage("Can not reset SMS settings ");
        retVal = SMS_E_CANNOT_CONNECT_SWATT;
    }
    ZSWATT_SMS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SMS_Inc(int serNum)
{
    enum SWATT_SMS_ERROR_CODE retVal = SMS_IsConnected();
    if (SMS_Inc_Python(serNum)) // any error
    {
        SMS_SimpleMessage("Can not increment SMS");
        retVal = SMS_E_CANNOT_CONNECT_SWATT;
    }
    ZSWATT_SMS_ErrorHandlingBehavior(retVal);
    return retVal;
}


int SMS_Dec(int serNum)
{
    enum SWATT_SMS_ERROR_CODE retVal = SMS_IsConnected();
    if (SMS_Dec_Python(serNum)) // any error
    {
        SMS_SimpleMessage("Can not decrement SMS ");
        retVal = SMS_E_CANNOT_CONNECT_SWATT;
    }
    ZSWATT_SMS_ErrorHandlingBehavior(retVal);
    return retVal;
}


int SMS_ReadPos(int serNum,int* position)
{
    enum SWATT_SMS_ERROR_CODE retVal = SMS_IsConnected();

    PyObject* outputVal=NULL;
    long intVal;

    outputVal=SMS_ReadPos_Python(serNum);


    if ((outputVal!=NULL)&&(PyInt_Check(outputVal))) // no error
    {
        intVal= PyInt_AsLong(outputVal);
        if(!PyErr_Occurred()){
            *position=(int)intVal;
        }else
        {
            *position=-1;
            SMS_SimpleMessage("Can not read SMS position");
            retVal = SMS_E_FAILED_SWATT;
        }

    }
    else
    {
        SMS_SimpleMessage("Can read SMS position");
        retVal = SMS_E_FAILED_SWATT;

    }
    ZSWATT_SMS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SMS_GetHallState(int serNum,char* a,char* b)
{
    enum SWATT_SMS_ERROR_CODE retVal = SMS_IsConnected();

    PyObject* outputVal=NULL;
    PyObject* aVal=NULL;
    PyObject* bVal=NULL;

    outputVal=SMS_GetHallState_Python(serNum);


    if ((outputVal!=NULL)&&(PyTuple_Check(outputVal))) // no error
    {
        aVal=PyTuple_GetItem(outputVal,0);
        bVal=PyTuple_GetItem(outputVal,1);
        if((aVal!=NULL)&&(bVal!=NULL)&&(PyString_Check(aVal))&&(PyString_Check(bVal))){
            strcpy(a,PyString_AsString(aVal));
            strcpy(b,PyString_AsString(bVal));
        }
        else
        {
            SMS_SimpleMessage("Can not read SMS hall state");
            retVal = SMS_E_FAILED_SWATT;

        }

    }
    else
    {
        SMS_SimpleMessage("Can not read SMS hall state");
        retVal = SMS_E_FAILED_SWATT;

    }
    ZSWATT_SMS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SMS_SetHallErr(int serNum,char * string){
    enum SWATT_SMS_ERROR_CODE retVal = SMS_IsConnected();
    if (SMS_SetHallErr_Python(serNum,string)) // any error
    {
        SMS_SimpleMessage("Can not set  hall error for SMS");
        retVal = SMS_E_CANNOT_CONNECT_SWATT;
    }
    ZSWATT_SMS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SMS_SetBlock(int serNum,int blockPos, char * blockType){
    enum SWATT_SMS_ERROR_CODE retVal = SMS_IsConnected();
    if (SMS_SetBlock_Python(serNum,blockPos,blockType)) // any error
    {
        SMS_SimpleMessage("Can not set block in SMS");
        retVal = SMS_E_CANNOT_CONNECT_SWATT;
    }
    ZSWATT_SMS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SMS_SetPinch(int serNum,int pinchPos, char * pinchType){
    enum SWATT_SMS_ERROR_CODE retVal = SMS_IsConnected();
    if (SMS_SetPinch_Python(serNum,pinchPos,pinchType)) // any error
    {
        SMS_SimpleMessage("Can not set pinch in SMS");
        retVal = SMS_E_CANNOT_CONNECT_SWATT;
    }
    ZSWATT_SMS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PLAST_SMS_SetErrorHandlingBehaviour( enum SWATT_SMS_ERROR_HANDLING_BEHAVIOR behaviour)
{
    enum SWATT_SMS_ERROR_CODE retVal;
#ifdef USE_SMS_SWATT_ERROR_HANDLER
    PLAST_SMS_instance.errorHandlingBehaviorOption=behaviour;
    retVal = SMS_E_OK_SWATT;
    //iSystem_SimpleMessage("Error handling behavior set");
#else
    retval=SMS_E_FAILED_SWATT;
#endif
    return retVal;
}


/* Exported functions */
/*============================================================================*/

void PLAST_SMS_Init(void){

    handle_SMS_Python_Module = PLAST_loadModule(SMS_PYTHON_MODULE);

    if (NULL == handle_SMS_Python_Module)
    {
        SWATT_abort_executable("ERROR: Can not load SMS module.\n");
    }

    PLAST_SMS_instance.sms_api.connect=&SMS_Connect;
    PLAST_SMS_instance.sms_api.setPos=&SMS_SetPos;
    PLAST_SMS_instance.sms_api.reset=&SMS_Reset;
    PLAST_SMS_instance.sms_api.inc=&SMS_Inc;
    PLAST_SMS_instance.sms_api.dec=&SMS_Dec;
    PLAST_SMS_instance.sms_api.readPos=&SMS_ReadPos;
    PLAST_SMS_instance.sms_api.getHallState=&SMS_GetHallState;
    PLAST_SMS_instance.sms_api.setHallErr=&SMS_SetHallErr;
    PLAST_SMS_instance.sms_api.setBlock=&SMS_SetBlock;
    PLAST_SMS_instance.sms_api.setPinch=&SMS_SetPinch;
    PLAST_SMS_instance.sms_api.setErrorHandlerBehaviour=&PLAST_SMS_SetErrorHandlingBehaviour;

}

void PLAST_SMS_DummyInit(void){

    PLAST_SMS_instance.sms_api.connect=&SMS_Connect;
    PLAST_SMS_instance.sms_api.setPos=&SMS_SetPos;
    PLAST_SMS_instance.sms_api.reset=&SMS_Reset;
    PLAST_SMS_instance.sms_api.inc=&SMS_Inc;
    PLAST_SMS_instance.sms_api.dec=&SMS_Dec;
    PLAST_SMS_instance.sms_api.readPos=&SMS_ReadPos;
    PLAST_SMS_instance.sms_api.getHallState=&SMS_GetHallState;
    PLAST_SMS_instance.sms_api.setHallErr=&SMS_SetHallErr;
    PLAST_SMS_instance.sms_api.setBlock=&SMS_SetBlock;
    PLAST_SMS_instance.sms_api.setPinch=&SMS_SetPinch;
    PLAST_SMS_instance.sms_api.setErrorHandlerBehaviour=&PLAST_SMS_SetErrorHandlingBehaviour;

}


/* Notice: the file ends with a blank new line to avoid compiler warnings */


