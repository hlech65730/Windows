/*============================================================================*/
/*                        I BS SOFTWARE GROUP                                 */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*/
/*!
 * $Source: PLAST_SignalGenerator.c $
 * $Author: Nitu, Laurentiu (uidv9994) $
 */
/*============================================================================*/
/* DESCRIPTION :                                                              */
/** \file
    Wrappers for PLAST signal generator module.
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

#include "PLAST_SignalGenerator.h"

/* Constants and types  */
/*============================================================================*/
#define SIGNALGENERATOR_PYTHON_MODULE "ControlledDevices.SignalGenerators.SG_HAMEG_HMF"

//#define NULL 0


/* Variables */
/*============================================================================*/

struct PLAST_SignalGenerator_class PLAST_SignalGenerator_instance ;

static PyObject* handle_SignalGenerator_Python_Module= NULL, *SignalGenerator_Python_Object = NULL;
static uint8 SignalGenerator_Connected = 0;


/* Private functions prototypes */
/*============================================================================*/
static void SignalGenerator_SimpleMessage(const char* message);
int SignalGenerator_Connect(void);
static int SignalGenerator_IsConnected(void);
int SignalGenerator_OpenPort(void);
int SignalGenerator_ClosePort(void);
int SignalGenerator_PrintPortConfiguration(void);
int SignalGenerator_SetOutputOn(unsigned int channel);
int SignalGenerator_SetOutputOff(void);
int SignalGenerator_SendCommand( char* data);
int SignalGenerator_SetAmplitude(double val);
int SignalGenerator_GetAmplitude(double *val);
int SignalGenerator_Reset(void);
int SignalGenerator_SetFrequency(double val);
int SignalGenerator_SetSinWaveform(void);
int SignalGenerator_SetSquareWaveform(double dutyCycle);
int SignalGenerator_SetPulseWaveform(double dutyCycle);
int SignalGenerator_SetRampWaveform(double symmetry);
int SignalGenerator_SetArbitraryWaveform(char* waveForm);
int SignalGenerator_GetWaveformType(char* waveForm);
int SignalGenerator_GetWaveformParameter(union PLAST_union_double_string* val);
int PLAST_SignalGenerator_SetErrorHandlingBehaviour( enum SWATT_SG_ERROR_HANDLING_BEHAVIOR behaviour);

/* Inline functions */
/*============================================================================*/

#define SignalGenerator_OpenPort_Python() ((PyObject_CallMethod(SignalGenerator_Python_Object, "OpenPort", NULL) != NULL) ? OK : N_OK)
#define SignalGenerator_ClosePort_Python() ((PyObject_CallMethod(SignalGenerator_Python_Object, "ClosePort", NULL) != NULL) ? OK : N_OK)
#define SignalGenerator_PrintPortConfiguration_Python() ((PyObject_CallMethod(SignalGenerator_Python_Object, "PrintPortConfiguration", NULL) != NULL) ? OK : N_OK)
#define SignalGenerator_SetOutputOn_Python(channel) ((PyObject_CallMethod(SignalGenerator_Python_Object, "SetOutputON","i",channel) != NULL) ? OK : N_OK)
#define SignalGenerator_SetOutputOff_Python() ((PyObject_CallMethod(SignalGenerator_Python_Object, "SetOutputOFF", NULL) != NULL) ? OK : N_OK)
#define SignalGenerator_SendCommand_Python(data) ((PyObject_CallMethod(SignalGenerator_Python_Object, "SendCommand","s",data) != NULL) ? OK : N_OK)
#define SignalGenerator_GetAmplitude_Python() (PyObject_CallMethod(SignalGenerator_Python_Object, "GetAmplitude", NULL))
#define SignalGenerator_SetAmplitude_Python(val) ((PyObject_CallMethod(SignalGenerator_Python_Object, "SetAmplitude","f",val) != NULL) ? OK : N_OK)
#define SignalGenerator_Reset_Python() ((PyObject_CallMethod(SignalGenerator_Python_Object, "Reset", NULL) != NULL) ? OK : N_OK)
#define SignalGenerator_SetFrequency_Python(frequency) ((PyObject_CallMethod(SignalGenerator_Python_Object, "SetFrequency","f",frequency) != NULL) ? OK : N_OK)
#define SignalGenerator_SetSinWaveForm_Python() ((PyObject_CallMethod(SignalGenerator_Python_Object, "SetSinWaveform", NULL) != NULL) ? OK : N_OK)
#define SignalGenerator_SetSquareWaveform_Python(dutyCycle) ((PyObject_CallMethod(SignalGenerator_Python_Object, "SetSquareWaveform","f",dutyCycle) != NULL) ? OK : N_OK)
#define SignalGenerator_SetPulseWaveform_Python(dutyCycle) ((PyObject_CallMethod(SignalGenerator_Python_Object, "SetPulseWaveform","f",dutyCycle) != NULL) ? OK : N_OK)
#define SignalGenerator_SetRampWaveform_Python(symmetry) ((PyObject_CallMethod(SignalGenerator_Python_Object, "SetRampWaveform","f",symmetry) != NULL) ? OK : N_OK)
#define SignalGenerator_SetArbitraryWaveform_Python(waveForm) ((PyObject_CallMethod(SignalGenerator_Python_Object, "SetArbitraryWaveform","s",waveForm) != NULL) ? OK : N_OK)
#define SignalGenerator_GetWaveformType_Python() (PyObject_CallMethod(SignalGenerator_Python_Object, "GetWaveformType", NULL))
#define SignalGenerator_GetWaveformParameter_Python() (PyObject_CallMethod(SignalGenerator_Python_Object, "GetWaveformParameter", NULL))

//(fi) = = = f is for float i is for integer () is for tuple



/* Private functions */
/*============================================================================*/


static void SignalGenerator_SimpleMessage(const char* message)
{
    printf("%s: %d: %s \n",PLAST_SignalGenerator_instance.file, PLAST_SignalGenerator_instance.line, message);
}


int SignalGenerator_Connect(void)
{
    enum SWATT_SG_ERROR_CODE retVal = SG_E_OK_SWATT;

    if(handle_SignalGenerator_Python_Module==NULL){
        SignalGenerator_SimpleMessage("Error: Power Source Module not enabled");
        retVal = SG_E_CANNOT_CONNECT_SWATT;
    }
    else{

        PyObject* SignalGeneratorClass=NULL;

        SignalGeneratorClass=PLAST_getDictionary(handle_SignalGenerator_Python_Module, "HamegHMF");

        if(SignalGeneratorClass!=NULL){
            SignalGenerator_Python_Object = PyInstance_New(SignalGeneratorClass, NULL, NULL);
        }else{
            SignalGenerator_Python_Object=NULL;
        }


        if ( (SignalGenerator_Python_Object==NULL))// any error
        {
            SignalGenerator_SimpleMessage("Error: Can not connect to the signal generator");
            retVal = SG_E_CANNOT_CONNECT_SWATT;
        }
        else
        {
            SignalGenerator_SimpleMessage("Successfully connected to the signal generator ");
            SignalGenerator_Connected = 1;
        }
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}


static int SignalGenerator_IsConnected(void)
{
    if (!SignalGenerator_Connected)
    {
        SignalGenerator_SimpleMessage("Error: not yet connected to the signal generator, call sg.connect() first ");
        ZSWATT_SG_ErrorHandlingBehavior(SG_E_NOT_CONNECTED_SWATT);
        return SG_E_NOT_CONNECTED_SWATT;
    }
    return SG_E_OK_SWATT;
}



int SignalGenerator_OpenPort(void)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_OpenPort_Python()) // any error
    {
        SignalGenerator_SimpleMessage("Can not open signal generator serial port ");
        retVal = SG_E_CANNOT_CONNECT_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SignalGenerator_ClosePort(void)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_ClosePort_Python()) // any error
    {
        SignalGenerator_SimpleMessage("Can not close signal generator serial port ");
        retVal = SG_E_NOT_CONNECTED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SignalGenerator_PrintPortConfiguration(void)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_PrintPortConfiguration_Python()) // any error
    {
        SignalGenerator_SimpleMessage("Can not print serial port configuration");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SignalGenerator_SetOutputOn(unsigned int channel)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_SetOutputOn_Python(channel)) // any error
    {
        SignalGenerator_SimpleMessage("Can not turn on signal generator output on");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SignalGenerator_SetOutputOff(void)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_SetOutputOff_Python()) // any error
    {
        SignalGenerator_SimpleMessage("Can not turn off signal generator output");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}
int SignalGenerator_SendCommand( char* data)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_SendCommand_Python(data)) // any error
    {
        SignalGenerator_SimpleMessage("Can not send command to signal generator ");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SignalGenerator_SetAmplitude(double val)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_SetAmplitude_Python(val)) // any error
    {
        SignalGenerator_SimpleMessage("Can not set signal generator amplitude ");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SignalGenerator_GetAmplitude(double *val)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();

    PyObject* outputVal=NULL;
    PyObject* outputDouble=NULL;

    outputVal=SignalGenerator_GetAmplitude_Python();

    if(PyString_Check(outputVal)){

        outputDouble=PyFloat_FromString(outputVal,NULL);

        if(outputDouble!=NULL){

            *val=PyFloat_AsDouble(outputDouble);

            if(PyErr_Occurred()){

                SignalGenerator_SimpleMessage("Signal generator amplitude value unknown ");
                retVal = SG_E_FAILED_SWATT;

            }
        }
        else{
            SignalGenerator_SimpleMessage("Signal generator amplitude value unknown ");
            retVal = SG_E_FAILED_SWATT;

        }
    }
    else
    {
        SignalGenerator_SimpleMessage("Signal generator amplitude value unknown ");
        retVal = SG_E_FAILED_SWATT;
    }


    if (outputVal==NULL) // any error
    {
        SignalGenerator_SimpleMessage("Can not read signal generator amplitude ");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SignalGenerator_Reset(void)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_Reset_Python()) // any error
    {
        SignalGenerator_SimpleMessage("Can not reset signal generator settings ");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}


int SignalGenerator_SetFrequency(double val)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_SetFrequency_Python(val)) // any error
    {
        SignalGenerator_SimpleMessage("Can not set signal generator frequency ");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SignalGenerator_SetSinWaveform(void)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_SetSinWaveForm_Python()) // any error
    {
        SignalGenerator_SimpleMessage("Can not set signal generator sin wave form ");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SignalGenerator_SetSquareWaveform(double dutyCycle)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_SetSquareWaveform_Python(dutyCycle)) // any error
    {
        SignalGenerator_SimpleMessage("Can not set signal generator square wave form ");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}
int SignalGenerator_SetPulseWaveform(double dutyCycle)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_SetPulseWaveform_Python(dutyCycle)) // any error
    {
        SignalGenerator_SimpleMessage("Can not set signal generator pulse wave form ");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}
int SignalGenerator_SetRampWaveform(double symmetry)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_SetRampWaveform_Python(symmetry)) // any error
    {
        SignalGenerator_SimpleMessage("Can not set signal generator ramp wave form ");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SignalGenerator_SetArbitraryWaveform(char* waveForm)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();
    if (SignalGenerator_SetArbitraryWaveform_Python(waveForm)) // any error
    {
        SignalGenerator_SimpleMessage("Can not set signal generator arbitrary wave form ");
        retVal = SG_E_FAILED_SWATT;
    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}
int SignalGenerator_GetWaveformType(char* waveForm)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();

    PyObject* outputVal=NULL;
    char * auxStringPointer;

    outputVal=SignalGenerator_GetWaveformType_Python();


    if ((outputVal!=NULL)&&(PyString_Check(outputVal))) // no error
    {
        auxStringPointer= PyString_AsString(outputVal);
        strcpy(waveForm,auxStringPointer);
    }
    else
    {
        SignalGenerator_SimpleMessage("Can not get wave form type");
        retVal = SG_E_FAILED_SWATT;

    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int SignalGenerator_GetWaveformParameter(union PLAST_union_double_string* val)
{
    enum SWATT_SG_ERROR_CODE retVal = SignalGenerator_IsConnected();

    PyObject* outputVal=NULL;
    char * auxStringPointer;

    outputVal=SignalGenerator_GetWaveformParameter_Python();


    if (outputVal!=NULL) // no error
    {
        if(PyString_Check(outputVal)){
            //returned value is a string
            auxStringPointer= PyString_AsString(outputVal);
            strcpy(val->stringVal,auxStringPointer);
            //SignalGenerator_SimpleMessage("Received a string");
        }
        else
        {
            if(PyFloat_Check(outputVal)){
                //returned value is a double
                val->doubleVal= PyFloat_AsDouble(outputVal);
               // SignalGenerator_SimpleMessage("Received a double");
            }
            else{
                SignalGenerator_SimpleMessage("Can not get wave form parameter");
                retVal = SG_E_FAILED_SWATT;
            }
        }

    }
    else
    {
        SignalGenerator_SimpleMessage("Can not get wave form parameter");
        retVal = SG_E_FAILED_SWATT;

    }
    ZSWATT_SG_ErrorHandlingBehavior(retVal);
    return retVal;
}

int PLAST_SignalGenerator_SetErrorHandlingBehaviour( enum SWATT_SG_ERROR_HANDLING_BEHAVIOR behaviour)
{
    enum SWATT_SG_ERROR_CODE retVal;
#ifdef USE_SG_SWATT_ERROR_HANDLER
    PLAST_SignalGenerator_instance.errorHandlingBehaviorOption=behaviour;
    retVal = SG_E_OK_SWATT;
    //iSystem_SimpleMessage("Error handling behaviour set");
#else
    retval=SG_E_FAILED_SWATT;
#endif
    return retVal;
}


/* Exported functions */
/*============================================================================*/

void PLAST_SignalGenerator_Init(void){

    handle_SignalGenerator_Python_Module = PLAST_loadModule(SIGNALGENERATOR_PYTHON_MODULE);

    if (NULL == handle_SignalGenerator_Python_Module)
    {
        SWATT_abort_executable("ERROR: Can not load signal generator module.\n");
    }

    PLAST_SignalGenerator_instance.sg_api.connect=&SignalGenerator_Connect;
    PLAST_SignalGenerator_instance.sg_api.openPort=&SignalGenerator_OpenPort;
    PLAST_SignalGenerator_instance.sg_api.closePort=&SignalGenerator_ClosePort;
    PLAST_SignalGenerator_instance.sg_api.printPortConfiguration=&SignalGenerator_PrintPortConfiguration;
    PLAST_SignalGenerator_instance.sg_api.setOutputON=&SignalGenerator_SetOutputOn;
    PLAST_SignalGenerator_instance.sg_api.setOutputOFF=&SignalGenerator_SetOutputOff;
    PLAST_SignalGenerator_instance.sg_api.sendCommand=&SignalGenerator_SendCommand;
    PLAST_SignalGenerator_instance.sg_api.getAmplitude=&SignalGenerator_GetAmplitude;
    PLAST_SignalGenerator_instance.sg_api.setAmplitude=&SignalGenerator_SetAmplitude;
    PLAST_SignalGenerator_instance.sg_api.reset=&SignalGenerator_Reset;
    PLAST_SignalGenerator_instance.sg_api.setFrequency=&SignalGenerator_SetFrequency;
    PLAST_SignalGenerator_instance.sg_api.setSinWaveform=&SignalGenerator_SetSinWaveform;
    PLAST_SignalGenerator_instance.sg_api.setSquareWaveform=&SignalGenerator_SetSquareWaveform;
    PLAST_SignalGenerator_instance.sg_api.setPulseWaveform=&SignalGenerator_SetPulseWaveform;
    PLAST_SignalGenerator_instance.sg_api.setRampWaveform=&SignalGenerator_SetRampWaveform;
    PLAST_SignalGenerator_instance.sg_api.setArbitraryWaveform=&SignalGenerator_SetArbitraryWaveform;
    PLAST_SignalGenerator_instance.sg_api.getWaveformType=&SignalGenerator_GetWaveformType;
    PLAST_SignalGenerator_instance.sg_api.getWaveformParameter=&SignalGenerator_GetWaveformParameter;
    PLAST_SignalGenerator_instance.sg_api.setErrorHandlerBehaviour=&PLAST_SignalGenerator_SetErrorHandlingBehaviour;

}

void PLAST_SignalGenerator_DummyInit(void){

    PLAST_SignalGenerator_instance.sg_api.connect=&SignalGenerator_Connect;
    PLAST_SignalGenerator_instance.sg_api.openPort=&SignalGenerator_OpenPort;
    PLAST_SignalGenerator_instance.sg_api.closePort=&SignalGenerator_ClosePort;
    PLAST_SignalGenerator_instance.sg_api.printPortConfiguration=&SignalGenerator_PrintPortConfiguration;
    PLAST_SignalGenerator_instance.sg_api.setOutputON=&SignalGenerator_SetOutputOn;
    PLAST_SignalGenerator_instance.sg_api.setOutputOFF=&SignalGenerator_SetOutputOff;
    PLAST_SignalGenerator_instance.sg_api.sendCommand=&SignalGenerator_SendCommand;
    PLAST_SignalGenerator_instance.sg_api.getAmplitude=&SignalGenerator_GetAmplitude;
    PLAST_SignalGenerator_instance.sg_api.setAmplitude=&SignalGenerator_SetAmplitude;
    PLAST_SignalGenerator_instance.sg_api.reset=&SignalGenerator_Reset;
    PLAST_SignalGenerator_instance.sg_api.setFrequency=&SignalGenerator_SetFrequency;
    PLAST_SignalGenerator_instance.sg_api.setSinWaveform=&SignalGenerator_SetSinWaveform;
    PLAST_SignalGenerator_instance.sg_api.setSquareWaveform=&SignalGenerator_SetSquareWaveform;
    PLAST_SignalGenerator_instance.sg_api.setPulseWaveform=&SignalGenerator_SetPulseWaveform;
    PLAST_SignalGenerator_instance.sg_api.setRampWaveform=&SignalGenerator_SetRampWaveform;
    PLAST_SignalGenerator_instance.sg_api.setArbitraryWaveform=&SignalGenerator_SetArbitraryWaveform;
    PLAST_SignalGenerator_instance.sg_api.getWaveformType=&SignalGenerator_GetWaveformType;
    PLAST_SignalGenerator_instance.sg_api.getWaveformParameter=&SignalGenerator_GetWaveformParameter;
    PLAST_SignalGenerator_instance.sg_api.setErrorHandlerBehaviour=&PLAST_SignalGenerator_SetErrorHandlingBehaviour;

}


/* Notice: the file ends with a blank new line to avoid compiler warnings */


