/*-----------------------------------------------------------------------------
 * EcDemoApp.h
 * Copyright                acontis technologies GmbH, Ravensburg, Germany
 * Response                 Paul Bussmann
 * Description              Application specific settings for EC-Master demo
 *---------------------------------------------------------------------------*/

#ifndef INC_ECDEMOAPP_H
#define INC_ECDEMOAPP_H 1

/*-LOGGING-------------------------------------------------------------------*/
#ifndef pEcLogParms
#define pEcLogParms (&(pAppContext->LogParms))
#endif

#ifndef EC_SIMULATOR_DS402
#define EC_SIMULATOR_DS402
#endif

#define INCLUDE_EC_SIMULATOR
#define INCLUDE_EC_SIMULATOR_HIL
#define INCLUDE_EC_LOGGING

/* obsolete */
#ifndef EC_SIMULATOR
#define EC_SIMULATOR
#endif

/*-INCLUDES------------------------------------------------------------------*/
#include "EcSimulator.h"
#include "EcDemoPlatform.h"
#include "EcDemoParms.h"
#include "EcLogging.h"
#include "EcNotification.h"
#include "EcSelectLinkLayer.h"
#include "EcSlaveInfo.h"
#include "EcDemoTimingTaskPlatform.h"

/*-DEFINES-------------------------------------------------------------------*/
#define EC_DEMO_APP_NAME (EC_T_CHAR*)"EcSimulatorHilDemoMotion"

/* the RAS server is necessary to support the EC-Engineer or other remote applications */
#if (!defined INCLUDE_RAS_SERVER) && (defined EC_SOCKET_SUPPORTED)
#define INCLUDE_RAS_SERVER
#endif

#if (defined INCLUDE_RAS_SERVER)
#include "EcRasServer.h"
#define ECMASTERRAS_MAX_WATCHDOG_TIMEOUT    10000
#define ECMASTERRAS_CYCLE_TIME              2
#endif

#ifndef ecatGetText
#define ecatGetText(dwTextId)       esGetText(0, (dwTextId))
#define ecatGetNotifyText(dwTextId) esGetNotifyText(0, (dwTextId))
#endif

#define PRINT_PERF_MEAS() ((EC_NULL != pEcLogContext)?((CAtEmLogging*)pEcLogContext)->PrintPerfMeas(0, pAppContext->dwInstanceId, pEcLogContext) : 0)

/*-FUNCTION DECLARATIONS-----------------------------------------------------*/
EC_T_VOID  ShowSyntaxAppUsage(T_EC_DEMO_APP_CONTEXT* pAppContext);
EC_T_VOID  ShowSyntaxApp(T_EC_DEMO_APP_CONTEXT* pAppContext);
EC_T_VOID  ShowSyntaxLinkLayer(EC_T_VOID);
EC_T_DWORD EcDemoApp(T_EC_DEMO_APP_CONTEXT* pAppContext);

#endif /* INC_ECDEMOAPP_H */

/*-END OF SOURCE FILE--------------------------------------------------------*/
