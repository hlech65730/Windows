/*============================================================================*/
/*                        I BS SOFTWARE GROUP                                 */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*/
/*!
 * $Source: PLAST_SignalGenerator.h $
 * $Author: Nitu, Laurentiu (uidv9994) $
 */
/*============================================================================*/
/* DESCRIPTION :                                                              */
/** \file
    PLAST signal generator module header.
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

#ifndef PLAST_SIGNALGENERATOR_H
#define PLAST_SIGNALGENERATOR_H

/* Includes */
/*============================================================================*/

#define USE_SG_SWATT_ERROR_HANDLER


#include "PLAST_Common.h"

/* Constants and types */
/*============================================================================*/
union PLAST_union_double_string {
	
	double doubleVal;
	char stringVal[8];
};

enum SWATT_SG_ERROR_HANDLING_BEHAVIOR
{

    /** generate fatal error and stop execution */
    SG_SWATT_HALT_IF_ANY_ERROR,

    /** generate fatal error and stop execution if can not connect to signal generator */
    SG_SWATT_HALT_IF_CONNECT,

    /** do not generate fatal error, allow test skip instead of failure */
    SG_SWATT_HALT_NONE
};

enum SWATT_SG_ERROR_CODE
{
    /** success */
    SG_E_OK_SWATT,

    /** Not connected to the signal generator */
    SG_E_NOT_CONNECTED_SWATT,

    /** cannot connect to the signal generator */
    SG_E_CANNOT_CONNECT_SWATT,

    /** general failure  */
    SG_E_FAILED_SWATT
};

/* Type definitions for interface functions */
typedef int (*Type_SWATT_SG_FNC_simple)(void);
typedef int (*Type_SWATT_SG_FNC_uint)(unsigned int);
typedef int (*Type_SWATT_SG_FNC_double)(double);
typedef int (*Type_SWATT_SG_FNC_string)(char*);
typedef int (*Type_SWATT_SG_FNC_outputdouble)(double*);
typedef int (*Type_SWATT_SG_FNC_outputdouble_or_string)(union PLAST_union_double_string*);
typedef int (*Type_SWATT_SG_FNC_enum)(enum SWATT_SG_ERROR_HANDLING_BEHAVIOR);
//TODO wtf do I do with get WaveFormParameter

struct SignalGenerator_api
{
	/**
	 * Connects to the power source (instantiates the python object)
	 * \param void
	 * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_CANNOT_CONNECT_SWATT)
	 */
        Type_SWATT_SG_FNC_simple connect;

	/**
	 * Open the serial port to the signal generator
	 * \param void
	 * \return int, value SG_E_OK_SWATT in case of success, otherwise error (PS_E_CANNOT_CONNECT_SWATT)
	 */
        Type_SWATT_SG_FNC_simple openPort;

	/**
	 * Close the serial port to the signal generator
	 * \param void
	 * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_simple closePort;

	/**
	 * Prints the serial port configuration
	 * \param void
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */

        Type_SWATT_SG_FNC_simple printPortConfiguration;

	/**
	 * Send user command to power source. More information about compatible commands is found in the power source manual
	 * \param char* command - command to be sent
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_string sendCommand;

	/**
	 * Turns signal generator output on
	 * \param int channel - channel ( if the signal generator does not have multiple channels then you should send channel=1)
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_uint setOutputON;

	/**
	 * Turns power source output off
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_simple setOutputOFF;
	/**
	 * Returns the output voltage value
	 * \param double* amplitude -pointer to received amplitude
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_outputdouble getAmplitude;

	/**
	 * Sets the output voltage
	 * \param double amplitude
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_double setAmplitude;

	/**
	 * Resets the device parameters
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_simple reset;

	/**
	 * Sets the signal frequency
	 * \param double frequency
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_double setFrequency;

	/**
	 * Sets a sinusoidal waveform
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_simple setSinWaveform;

	/**
	 * Sets a square waveform
	 * \param double dutyCycle
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_double setSquareWaveform;
	/**
	 * Sets a pulse waveform
	 * \param double dutyCycle
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_double setPulseWaveform;

	/**
	 * Sets a ramp waveform
	 * \param double symmetry
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_double setRampWaveform;

	/**
	 * Sets a ramp waveform
	 * \param string waveformType
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_string setArbitraryWaveform;
	/**
	 * Returns the waveform type
	 * \param string waveformType
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_string getWaveformType;
	/**
	 * Returns the waveform parameter(dutycycle / symmetry / arbitrary selected)
	 * \param union PLAST_union_double_string* val
     * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
	 */
        Type_SWATT_SG_FNC_outputdouble_or_string getWaveformParameter;
       /**
        * set the signal generator error handling behavior
        * \param SWATT_SG_ERROR_HANDLING_BEHAVIOR behavior - error handling behavior
        * \return int, value SG_E_OK_SWATT in case of success, otherwise error (SG_E_FAILED_SWATT)
        */
        Type_SWATT_SG_FNC_enum setErrorHandlerBehaviour;


};


/**
    Structure for the power source interface instance
*/
struct PLAST_SignalGenerator_class
{
        const char* file;
        unsigned int line;
        enum SWATT_SG_ERROR_HANDLING_BEHAVIOR errorHandlingBehaviorOption;
        struct SignalGenerator_api sg_api;
};


/* Exported Variables */
/*============================================================================*/
extern struct PLAST_SignalGenerator_class PLAST_SignalGenerator_instance ;

#define sg (PLAST_SignalGenerator_instance.file=__FILE__, PLAST_SignalGenerator_instance.line=__LINE__,&PLAST_SignalGenerator_instance)->sg_api

/* Exported functions prototypes */
/*============================================================================*/
#ifdef __CDT_PARSER__
#define SWATT_SG_INLINE inline
#else
#define SWATT_SG_INLINE static __attribute__((always_inline))
#endif




SWATT_SG_INLINE void ZSWATT_SG_ErrorHandlingBehavior(enum SWATT_SG_ERROR_CODE err_code);
SWATT_SG_INLINE void ZSWATT_SG_ErrorHandlingBehavior(enum SWATT_SG_ERROR_CODE err_code)
{
#ifdef USE_SG_SWATT_ERROR_HANDLER
    SWATT_number_of_assertions_executed++;
    if (SG_E_OK_SWATT == err_code)
    {
        return;
    }
    SWATT_number_of_assertions_failed++;
    switch (PLAST_SignalGenerator_instance.errorHandlingBehaviorOption)
    {
        case SG_SWATT_HALT_NONE:
            break;
        case SG_SWATT_HALT_IF_CONNECT:
            if ((err_code == SG_E_CANNOT_CONNECT_SWATT) || (err_code == SG_E_NOT_CONNECTED_SWATT) )
            {
                SWATT_abort_executable("ERROR: Fatal signal generator error");
            }
            break;
        case SG_SWATT_HALT_IF_ANY_ERROR:
            SWATT_abort_executable("ERROR: Fatal signal generator error");
            break;
        default:
            break;
    }
#endif
}

extern void PLAST_SignalGenerator_Init(void);
extern void PLAST_SignalGenerator_DummyInit(void);

#endif  /* Notice: the file ends with a blank new line to avoid compiler warnings */

