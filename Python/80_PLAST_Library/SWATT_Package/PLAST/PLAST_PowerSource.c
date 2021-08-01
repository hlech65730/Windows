/*============================================================================*/
/*                        I BS SOFTWARE GROUP                                 */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*/
/*!
 * $Source: PLAST_PowerSource.c $
 * $Author: Nitu, Laurentiu (uidv9994) $
 */
/*============================================================================*/
/* DESCRIPTION :                                                              */
/** \file
    Wrappers for PLAST power source module.
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

#include "PLAST_PowerSource.h"

/* Constants and types  */
/*============================================================================*/
#define POWERSOURCE_PYTHON_MODULE "PlatformFiles.DEVICE_Interface"

//#define NULL 0


/* Variables */
/*============================================================================*/

struct PLAST_PowerSource_class PLAST_PowerSource_instance ;

static PyObject* handle_PowerSource_Python_Module= NULL, *PowerSource_Python_Object = NULL;
static uint8 PowerSource_Connected = 0;


/* Private functions prototypes */
/*============================================================================*/
static void PowerSource_SimpleMessage(const char* message);
//static int PowerSource_Delay_Python(double delay);
int PowerSource_Connect(void);
static int PowerSource_IsConnected(void);
int PowerSource_OpenPort(void);
int PowerSource_ClosePort(void);
int PowerSource_PrintPortConfiguration(void);
int PowerSource_SetOutputOn(unsigned int channel);
int PowerSource_SetOutputOff(unsigned int channel);
int PowerSource_SetVoltage(double volts, unsigned int channel);
int PowerSource_SetCurrent(double amperes, unsigned int channel);
int PowerSource_Reset(void);
int PowerSource_GetVoltage(double *val,unsigned int channel);
int PowerSource_GetVoltageSetted(double *val,unsigned int channel);
int PowerSource_SetVoltageLimit(double volts);
int PowerSource_GetVoltageLimit(double *val);
int PowerSource_GetCurrent(double *val,unsigned int channel);
int PowerSource_GetCurrentSetted(double *val,unsigned int channel);
int PowerSource_SetCurrentLimit(double amperes);
int PowerSource_GetCurrentLimit(double *val);
int PLAST_PowerSource_SetErrorHandlingBehaviour( enum SWATT_PS_ERROR_HANDLING_BEHAVIOR behaviour);

/* Inline functions */
/*============================================================================*/

#define PowerSource_OpenPort_Python() ((PyObject_CallMethod(PowerSource_Python_Object, "OpenPort", NULL) != NULL) ? OK : N_OK)
#define PowerSource_ClosePort_Python() ((PyObject_CallMethod(PowerSource_Python_Object, "ClosePort", NULL) != NULL) ? OK : N_OK)
#define PowerSource_PrintPortConfiguration_Python() ((PyObject_CallMethod(PowerSource_Python_Object, "PrintPortConfiguration", NULL) != NULL) ? OK : N_OK)
#define PowerSource_SetOutputOn_Python(channel) ((PyObject_CallMethod(PowerSource_Python_Object, "SetOutputON","i",channel) != NULL) ? OK : N_OK)
#define PowerSource_SetOutputOff_Python(channel) ((PyObject_CallMethod(PowerSource_Python_Object, "SetOutputOFF","i",channel) != NULL) ? OK : N_OK)
#define PowerSource_SetVoltage_Python(volts,channel) ((PyObject_CallMethod(PowerSource_Python_Object, "SetVoltage","(fi)",volts,channel) != NULL) ? OK : N_OK)
#define PowerSource_SetCurrent_Python(amperes,channel) ((PyObject_CallMethod(PowerSource_Python_Object, "SetCurrent","(fi)",amperes,channel) != NULL) ? OK : N_OK)
#define PowerSource_Reset_Python() ((PyObject_CallMethod(PowerSource_Python_Object, "Reset", NULL) != NULL) ? OK : N_OK)
#define PowerSource_GetVoltage_Python(channel) (PyObject_CallMethod(PowerSource_Python_Object, "GetVoltage","i",channel))
#define PowerSource_GetVoltageSetted_Python(channel) (PyObject_CallMethod(PowerSource_Python_Object, "GetVoltageSetted","i",channel))
#define PowerSource_SetVoltageLimit_Python(volts) ((PyObject_CallMethod(PowerSource_Python_Object, "SetVoltageLimit","f",volts) != NULL) ? OK : N_OK)
#define PowerSource_GetVoltageLimit_Python() (PyObject_CallMethod(PowerSource_Python_Object, "GetVoltageLimit",NULL))
#define PowerSource_GetCurrent_Python(channel) (PyObject_CallMethod(PowerSource_Python_Object, "GetCurrent","i",channel))
#define PowerSource_GetCurrentSetted_Python(channel) (PyObject_CallMethod(PowerSource_Python_Object, "GetCurrentSetted","i",channel))
#define PowerSource_SetCurrentLimit_Python(amperes) ((PyObject_CallMethod(PowerSource_Python_Object, "SetCurrentLimit","f",amperes) != NULL) ? OK : N_OK)
#define PowerSource_GetCurrentLimit_Python() (PyObject_CallMethod(PowerSource_Python_Object, "GetCurrentLimit",NULL))

//#define PowerSource_Delay_Python(delay) ((PyObject_CallFunction(PowerSource_Delay_Function,"f",delay) != NULL) ? OK : N_OK)
//#define SLEEP(delay) (PyRun_SimpleString("import time; time.sleep( delay );"))

//(fi) = = = f is for float i is for integer () is for tuple



/* Private functions */
/*============================================================================*/
/*
static int PowerSource_Delay_Python(double delay){
	
	char command[100]=" ";
	
	sprintf(command,"import time; time.sleep(%f)",delay);
	//printf("%s",command);
	if(PyRun_SimpleString(command)!=-1){
			return OK;		
	}
	else{
			return N_OK;
	}

}
 */
static void PowerSource_SimpleMessage(const char* message)
{
    printf("%s: %d: %s \n",PLAST_PowerSource_instance.file, PLAST_PowerSource_instance.line, message);
}


int PowerSource_Connect(void)
{
    enum SWATT_PS_ERROR_CODE retVal = PS_E_OK_SWATT;

    if(handle_PowerSource_Python_Module==NULL){
        PowerSource_SimpleMessage("Error: Power Source Module not enabled");
        retVal = PS_E_CANNOT_CONNECT_SWATT;
    }
    else{

        PyObject* powerSourceClass=NULL;

        powerSourceClass=PLAST_getDictionary(handle_PowerSource_Python_Module, "PowerSourceInstance");

        if(powerSourceClass!=NULL){
            PowerSource_Python_Object = PyInstance_New(powerSourceClass, NULL, NULL);
        }else{
            PowerSource_Python_Object=NULL;
        }

        //PowerSource_Delay_Function = PLAST_getDictionary(handle_PowerSource_Python_Module,"timer");

        if ( (PowerSource_Python_Object==NULL) )// any error
        {
            PowerSource_SimpleMessage("Error: Can not connect to the power source");
            retVal = PS_E_CANNOT_CONNECT_SWATT;
        }
        else
        {
            PowerSource_SimpleMessage("Successfully connected to the power source ");
            PowerSource_Connected = 1;
        }
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}


static int PowerSource_IsConnected(void)
{
    if (!PowerSource_Connected)
    {
        PowerSource_SimpleMessage("Error: not yet connected to the power source, call ps.connect() first ");
        ZSWATT_PS_ErrorHandlingBehavior(PS_E_NOT_CONNECTED_SWATT);
        return PS_E_NOT_CONNECTED_SWATT;
    }
    return PS_E_OK_SWATT;
}



int PowerSource_OpenPort(void)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();
    if (PowerSource_OpenPort_Python()) // any error
    {
        PowerSource_SimpleMessage("Can not open power source serial port ");
        retVal = PS_E_CANNOT_CONNECT_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PowerSource_ClosePort(void)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();
    if (PowerSource_ClosePort_Python()) // any error
    {
        PowerSource_SimpleMessage("Can not close power source serial port ");
        retVal = PS_E_NOT_CONNECTED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PowerSource_PrintPortConfiguration(void)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();
    if (PowerSource_PrintPortConfiguration_Python()) // any error
    {
        PowerSource_SimpleMessage("Can not print serial port configuration");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PowerSource_SetOutputOn(unsigned int channel)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();
    if (PowerSource_SetOutputOn_Python(channel)) // any error
    {
        PowerSource_SimpleMessage("Can not turn on power supply output on");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PowerSource_SetOutputOff(unsigned int channel)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();
    if (PowerSource_SetOutputOff_Python(channel)) // any error
    {
        PowerSource_SimpleMessage("Can not turn off power supply output");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}
int PowerSource_SetVoltage(double volts, unsigned int channel)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();
    if (PowerSource_SetVoltage_Python(volts,channel)) // any error
    {
        PowerSource_SimpleMessage("Can not set power supply voltage ");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}


int PowerSource_SetCurrent(double amperes, unsigned int channel)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();
    if (PowerSource_SetCurrent_Python(amperes,channel)) // any error
    {
        PowerSource_SimpleMessage("Can not set power supply current ");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}
int PowerSource_Reset(void)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();
    if (PowerSource_Reset_Python()) // any error
    {
        PowerSource_SimpleMessage("Can reset power source");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PowerSource_GetVoltage(double *val,unsigned int channel)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();

    PyObject* outputVal=NULL;

    outputVal=PowerSource_GetVoltage_Python(channel);

    if((outputVal!=NULL)&&PyFloat_Check(outputVal)){

        *val=PyFloat_AsDouble(outputVal);
        if(PyErr_Occurred()){
            PowerSource_SimpleMessage("Power source voltage value unknown ");
            retVal = PS_E_FAILED_SWATT;
        }
       
    }
    else
    {
        PowerSource_SimpleMessage("Power source voltage value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    if (outputVal==NULL) // any error
    {
        PowerSource_SimpleMessage("Power source voltage value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PowerSource_GetVoltageSetted(double *val,unsigned int channel)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();

    PyObject* outputVal=NULL;

    outputVal=PowerSource_GetVoltageSetted_Python(channel);

    if((outputVal!=NULL)&&PyFloat_Check(outputVal)){

        *val=PyFloat_AsDouble(outputVal);
        if(PyErr_Occurred()){
            PowerSource_SimpleMessage("Power source voltage set value unknown ");
            retVal = PS_E_FAILED_SWATT;
        }
        
    }
    else
    {
        PowerSource_SimpleMessage("Power source voltage set value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    if (outputVal==NULL) // any error
    {
        PowerSource_SimpleMessage("Power source voltage set value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}
int PowerSource_SetVoltageLimit(double volts)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();
    if (PowerSource_SetVoltageLimit_Python(volts)) // any error
    {
        PowerSource_SimpleMessage("Can not set power supply voltage limit ");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PowerSource_GetVoltageLimit(double *val)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();

    PyObject* outputVal=NULL;

    outputVal=PowerSource_GetVoltageLimit_Python();

    if((outputVal!=NULL)&&PyFloat_Check(outputVal)){

        *val=PyFloat_AsDouble(outputVal);
        if(PyErr_Occurred()){
            PowerSource_SimpleMessage("Power source voltage limit value unknown ");
            retVal = PS_E_FAILED_SWATT;
        }
        
    }
    else
    {
        PowerSource_SimpleMessage("Power source voltage limit value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    if (outputVal==NULL) // any error
    {
        PowerSource_SimpleMessage("Power source voltage limit value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PowerSource_GetCurrent(double *val,unsigned int channel)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();

    PyObject* outputVal=NULL;

    outputVal=PowerSource_GetCurrent_Python(channel);


    if((outputVal!=NULL)&&PyFloat_Check(outputVal)){

        *val=PyFloat_AsDouble(outputVal);


        if(PyErr_Occurred()){
            PowerSource_SimpleMessage("Power source current value unknown ");
            retVal = PS_E_FAILED_SWATT;
        }
        
    }
    else
    {
        PowerSource_SimpleMessage("Power source current value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    if (outputVal==NULL) // any error1
    {
        PowerSource_SimpleMessage("Power source voltage value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PowerSource_GetCurrentSetted(double *val,unsigned int channel)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();

    PyObject* outputVal=NULL;

    outputVal=PowerSource_GetCurrentSetted_Python(channel);

    if((outputVal!=NULL)&&PyFloat_Check(outputVal)){

        *val=PyFloat_AsDouble(outputVal);

        if(PyErr_Occurred()){
            PowerSource_SimpleMessage("Power source current set value unknown ");
            retVal = PS_E_FAILED_SWATT;
        }
      
    }
    else
    {
        PowerSource_SimpleMessage("Power source Current set value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    if (outputVal==NULL) // any error
    {
        PowerSource_SimpleMessage("Power source Current set value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}
int PowerSource_SetCurrentLimit(double amperes)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();
    if (PowerSource_SetVoltageLimit_Python(amperes)) // any error
    {
        PowerSource_SimpleMessage("Can not set power supply Current limit ");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PowerSource_GetCurrentLimit(double *val)
{
    enum SWATT_PS_ERROR_CODE retVal = PowerSource_IsConnected();

    PyObject* outputVal=NULL;
    PyObject* outputDouble=NULL;

    outputVal=PowerSource_GetVoltageLimit_Python();

    if((outputVal!=NULL)&&PyFloat_Check(outputVal)){

        *val=PyFloat_AsDouble(outputDouble);

        if(PyErr_Occurred()){
            PowerSource_SimpleMessage("Power source current limit value unknown ");
            retVal = PS_E_FAILED_SWATT;
        }
       
    }
    else
    {
        PowerSource_SimpleMessage("Power source current limit value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    if (outputVal==NULL) // any error
    {
        PowerSource_SimpleMessage("Power source current limit value unknown ");
        retVal = PS_E_FAILED_SWATT;
    }
    ZSWATT_PS_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PLAST_PowerSource_SetErrorHandlingBehaviour( enum SWATT_PS_ERROR_HANDLING_BEHAVIOR behaviour)
{
    enum SWATT_PS_ERROR_CODE retVal;
#ifdef USE_PS_SWATT_ERROR_HANDLER
    PLAST_PowerSource_instance.errorHandlingBehaviorOption=behaviour;
    retVal = PS_E_OK_SWATT;
    //iSystem_SimpleMessage("Error handling behaviour set");
#else
    retval=PS_E_FAILED_SWATT;
#endif
    return retVal;
}
/* Exported functions */
/*============================================================================*/

void PLAST_PowerSource_Init(void){

    handle_PowerSource_Python_Module = PLAST_loadModule(POWERSOURCE_PYTHON_MODULE);

    if (NULL == handle_PowerSource_Python_Module)
    {
        SWATT_abort_executable("ERROR: Can not load Power source Interface.\n");
    }


    PLAST_PowerSource_instance.ps_api.connect=&PowerSource_Connect;
    PLAST_PowerSource_instance.ps_api.openPort=&PowerSource_OpenPort;
    PLAST_PowerSource_instance.ps_api.closePort=&PowerSource_ClosePort;
    PLAST_PowerSource_instance.ps_api.printPortConfiguration=&PowerSource_PrintPortConfiguration;
    PLAST_PowerSource_instance.ps_api.setOutputON=&PowerSource_SetOutputOn;
    PLAST_PowerSource_instance.ps_api.setOutputOFF=&PowerSource_SetOutputOff;
    PLAST_PowerSource_instance.ps_api.setVoltage=&PowerSource_SetVoltage;
    PLAST_PowerSource_instance.ps_api.setCurrent=&PowerSource_SetCurrent;
    PLAST_PowerSource_instance.ps_api.getVoltage=&PowerSource_GetVoltage;
    PLAST_PowerSource_instance.ps_api.reset=&PowerSource_Reset;
    PLAST_PowerSource_instance.ps_api.getVoltageSetted=&PowerSource_GetVoltageSetted;
    PLAST_PowerSource_instance.ps_api.setVoltageLimit=&PowerSource_SetVoltageLimit;
    PLAST_PowerSource_instance.ps_api.getVoltageLimit=&PowerSource_GetVoltageLimit;
	PLAST_PowerSource_instance.ps_api.getCurrent=&PowerSource_GetCurrent;
	PLAST_PowerSource_instance.ps_api.getCurrentSetted=&PowerSource_GetCurrentSetted;
    PLAST_PowerSource_instance.ps_api.setCurrentLimit=&PowerSource_SetCurrentLimit;
    PLAST_PowerSource_instance.ps_api.getCurrentLimit=&PowerSource_GetCurrentLimit;
    PLAST_PowerSource_instance.ps_api.setErrorHandlerBehaviour=&PLAST_PowerSource_SetErrorHandlingBehaviour;
    //PLAST_PowerSource_instance.ps_api.delay=&PowerSource_Delay;
}
void PLAST_PowerSource_DummyInit(void){

    handle_PowerSource_Python_Module=NULL;
    PLAST_PowerSource_instance.ps_api.connect=&PowerSource_Connect;
    PLAST_PowerSource_instance.ps_api.connect=&PowerSource_Connect;
    PLAST_PowerSource_instance.ps_api.openPort=&PowerSource_OpenPort;
    PLAST_PowerSource_instance.ps_api.closePort=&PowerSource_ClosePort;
    PLAST_PowerSource_instance.ps_api.printPortConfiguration=&PowerSource_PrintPortConfiguration;
    PLAST_PowerSource_instance.ps_api.setOutputON=&PowerSource_SetOutputOn;
    PLAST_PowerSource_instance.ps_api.setOutputOFF=&PowerSource_SetOutputOff;
    PLAST_PowerSource_instance.ps_api.setVoltage=&PowerSource_SetVoltage;
    PLAST_PowerSource_instance.ps_api.setCurrent=&PowerSource_SetCurrent;
    PLAST_PowerSource_instance.ps_api.getVoltage=&PowerSource_GetVoltage;
    PLAST_PowerSource_instance.ps_api.reset=&PowerSource_Reset;
    PLAST_PowerSource_instance.ps_api.getVoltageSetted=&PowerSource_GetVoltageSetted;
    PLAST_PowerSource_instance.ps_api.setVoltageLimit=&PowerSource_SetVoltageLimit;
    PLAST_PowerSource_instance.ps_api.getVoltageLimit=&PowerSource_GetVoltageLimit;
    PLAST_PowerSource_instance.ps_api.getCurrent=&PowerSource_GetCurrent;
    PLAST_PowerSource_instance.ps_api.getCurrentSetted=&PowerSource_GetCurrentSetted;
    PLAST_PowerSource_instance.ps_api.setCurrentLimit=&PowerSource_SetCurrentLimit;
    PLAST_PowerSource_instance.ps_api.getCurrentLimit=&PowerSource_GetCurrentLimit;
    PLAST_PowerSource_instance.ps_api.setErrorHandlerBehaviour=&PLAST_PowerSource_SetErrorHandlingBehaviour;
    //PLAST_PowerSource_instance.ps_api.delay=&PowerSource_Delay;
}



/* Notice: the file ends with a blank new line to avoid compiler warnings */


