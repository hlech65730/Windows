/*============================================================================*/
/*                        I BS SOFTWARE GROUP                                 */
/*============================================================================*/
/*                        OBJECT SPECIFICATION                                */
/*============================================================================*/
/*!
 * $Source: PLAST_PowerSource.h $
 * $Author: Nitu, Laurentiu (uidv9994) $
 */
/*============================================================================*/
/* DESCRIPTION :                                                              */
/** \file
    PLAST power source module header.
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

#ifndef PLAST_POWERSOURCE_H
#define PLAST_POWERSOURCE_H

/* Includes */
/*============================================================================*/
//#define ENABLE_PLAST_POWERSOURCE

#define USE_PS_SWATT_ERROR_HANDLER


#include "PLAST_Common.h"

/* Constants and types */
/*============================================================================*/

enum SWATT_PS_ERROR_HANDLING_BEHAVIOR
{

    /** generate fatal error and stop execution */
    PS_SWATT_HALT_IF_ANY_ERROR,

    /** generate fatal error and stop execution if can not connect to power supply */
    PS_SWATT_HALT_IF_CONNECT,

    /** do not generate fatal error, allow test skip instead of failure */
    PS_SWATT_HALT_NONE
};

enum SWATT_PS_ERROR_CODE
{
    /** success */
    PS_E_OK_SWATT,

    /** Not connected to the power source */
    PS_E_NOT_CONNECTED_SWATT,

    /** cannot connect to the power source */
    PS_E_CANNOT_CONNECT_SWATT,

    /** general failure  */
    PS_E_FAILED_SWATT
};

/* Type definitions for interface functions */
typedef int (*Type_SWATT_PS_FNC_simple)(void);
typedef int (*Type_SWATT_PS_FNC_uint)(unsigned int);
typedef int (*Type_SWATT_PS_FNC_double_uint)(double,unsigned int);
typedef int (*Type_SWATT_PS_FNC_double)(double);
typedef int (*Type_SWATT_PS_FNC_outputdouble)(double*);
typedef int (*Type_SWATT_PS_FNC_outputdouble_uint)(double*,unsigned int);
typedef int (*Type_SWATT_PS_FNC_enum)(enum SWATT_PS_ERROR_HANDLING_BEHAVIOR);

struct PowerSource_api
{
	/**
	 * Connects to the power source (instantiates the python object)
	 * \param void
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_CANNOT_CONNECT_SWATT)
	 */
	Type_SWATT_PS_FNC_simple connect;

	/**
	 * Open the serial port to the power source
	 * \param void
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_CANNOT_CONNECT_SWATT)
	 */
	Type_SWATT_PS_FNC_simple openPort;

	/**
	 * Close the serial port to the power source
	 * \param void
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_simple closePort;

	/**
	 * Prints the serial port configuration
	 * \param void
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */

	Type_SWATT_PS_FNC_simple printPortConfiguration;

	/**
	 * Sets the voltage
	 * \param double volts - voltage
	 * \param int channel - channel ( if the power source does not have multiple channels this parameter is ignored)
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_double_uint setVoltage;

	/**
	 * Sets the current
	 * \param double amperes - current
	 * \param int channel - channel ( if the power source does not have multiple channels this parameter is ignored)
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_double_uint setCurrent;

	/**
	 * Turns power source output on
	 * \param int channel - channel ( if the power source does not have multiple channels this parameter is ignored)
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_uint setOutputON;

	/**
	 * Turns power source output off
	 * \param int channel - channel ( if the power source does not have multiple channels this parameter is ignored)
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_uint setOutputOFF;
	
	/**
	 * Reset power source device parameter
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_simple reset;
	
	/**
	 * Returns measured voltage
	 * \param int channel - channel ( if the power source does not have multiple channels this parameter is ignored)
	 * \param double* voltage - returned voltage
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_outputdouble_uint getVoltage;
	
	/**
	 * Returns set voltage value
	 * \param int channel - channel ( if the power source does not have multiple channels this parameter is ignored)
	 * \param double* voltage - returned voltage
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_outputdouble_uint getVoltageSetted;
	
	/**
	 * Sets the voltage limit
	 * \param double volts - voltage
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_double setVoltageLimit;

	/**
	 * Gets the voltage limit
	 * \param double* volts - returned voltage
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_outputdouble getVoltageLimit;

	/**
	 * Returns measured current
	 * \param int channel - channel ( if the power source does not have multiple channels this parameter is ignored)
	 * \param double* amperes - returned current
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_outputdouble_uint getCurrent;
	
	/**
	 * Returns set current value
	 * \param int channel - channel ( if the power source does not have multiple channels this parameter is ignored)
	 * \param double* amperes - returned current
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_outputdouble_uint getCurrentSetted;
	
	/**
	 * Sets the current limit
	 * \param double amperes - current
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_double setCurrentLimit;

	/**
	 * Gets the current limit
	 * \param double* amperes - returned current
	 * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
	 */
	Type_SWATT_PS_FNC_outputdouble getCurrentLimit;

	/**
     * set the power source error handling behavior
     * \param SWATT_PS_ERROR_HANDLING_BEHAVIOR behavior - error handling behavior
     * \return int, value PS_E_OK_SWATT in case of success, otherwise error (PS_E_FAILED_SWATT)
     */
    Type_SWATT_PS_FNC_enum setErrorHandlerBehaviour;



};


/**
    Structure for the power source interface instance
*/
struct PLAST_PowerSource_class
{
        const char* file;
        unsigned int line;
        enum SWATT_PS_ERROR_HANDLING_BEHAVIOR errorHandlingBehaviorOption;
        struct PowerSource_api ps_api;
};




/* Exported Variables */
/*============================================================================*/
extern struct PLAST_PowerSource_class PLAST_PowerSource_instance ;

#define ps (PLAST_PowerSource_instance.file=__FILE__, PLAST_PowerSource_instance.line=__LINE__,&PLAST_PowerSource_instance)->ps_api

/* Exported functions prototypes */
/*============================================================================*/
#ifdef __CDT_PARSER__
#define SWATT_PS_INLINE inline
#else
#define SWATT_PS_INLINE static __attribute__((always_inline))
#endif




SWATT_PS_INLINE void ZSWATT_PS_ErrorHandlingBehavior(enum SWATT_PS_ERROR_CODE err_code);
SWATT_PS_INLINE void ZSWATT_PS_ErrorHandlingBehavior(enum SWATT_PS_ERROR_CODE err_code)
{
#ifdef USE_PS_SWATT_ERROR_HANDLER
    SWATT_number_of_assertions_executed++;
    if (PS_E_OK_SWATT == err_code)
    {
        return;
    }
//TODO make this work
    SWATT_number_of_assertions_failed++;
    switch (PLAST_PowerSource_instance.errorHandlingBehaviorOption)
    {
        case PS_SWATT_HALT_NONE:
            break;
        case PS_SWATT_HALT_IF_CONNECT:
            if ((err_code == PS_E_CANNOT_CONNECT_SWATT) || (err_code == PS_E_NOT_CONNECTED_SWATT) )
            {
                SWATT_abort_executable("ERROR: Fatal power supply error");
            }
            break;
        case PS_SWATT_HALT_IF_ANY_ERROR:
            SWATT_abort_executable("ERROR: Fatal power supply error");
            break;
        default:
            break;
    }
#endif
}

extern void PLAST_PowerSource_Init(void);
extern void PLAST_PowerSource_DummyInit(void);

#endif  /* Notice: the file ends with a blank new line to avoid compiler warnings */

