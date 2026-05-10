#include "EcMasterRasClientWrapper.h"

namespace EcMasterTests { namespace DocumentationSnippets {
TEST_GROUP(RasSoftwareIntegration), CDocumentationSnippetsBase
{
    EC_T_VOID* pvMyAppNotifyContext;

static EC_T_DWORD myAppRasNotifyCallback(
    EC_T_DWORD         dwCode,
    EC_T_NOTIFYPARMS*  pParms
)
{
    EC_T_DWORD dwRetVal = EC_E_NOERROR;
    CEmNotification* pNotificationHandler = EC_NULL;

    if ((EC_NULL == pParms) || (EC_NULL == pParms->pCallerData))
    {
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    pNotificationHandler = (CEmNotification*)pParms->pCallerData;
    dwRetVal = pNotificationHandler->emRasNotify(dwCode, pParms);

Exit:
    return dwRetVal;
}

EC_T_VOID InitRasClient()
{
    pvMyAppNotifyContext = this; // TODO: CEmNotification

    {
        /* DocumentationSnippetsEcMasterRasClientExampleInitRasClient */
        ECMASTERRAS_T_CLNTPARMS oRemoteApiParms;
        OsMemset(&oRemoteApiParms, 0, sizeof(ECMASTERRAS_T_CLNTPARMS));

        oRemoteApiParms.dwSignature = ECMASTERRASCLIENT_SIGNATURE;
        oRemoteApiParms.dwSize = sizeof(ECMASTERRAS_T_CLNTPARMS);

        OsMemcpy(&oRemoteApiParms.LogParms, pEcLogParms, sizeof(EC_T_LOG_PARMS));

        EC_CPUSET_ZERO(oRemoteApiParms.cpuAffinityMask);
        oRemoteApiParms.dwAdmStackSize = 8192; /* 8k */

        oRemoteApiParms.pvNotifCtxt = pvMyAppNotifyContext;
        oRemoteApiParms.pfNotification = myAppRasNotifyCallback;

        dwRes = emRasClntInit(&oRemoteApiParms);
        if (dwRes != EC_E_NOERROR)
        {
            dwRetVal = dwRes;
            goto Exit;
        }
        /* DocumentationSnippetsEcMasterRasClientExampleInitRasClient */
    }
Exit:
    return;
}
};

IGNORE_TEST(RasSoftwareIntegration, DOC_EcMasterRasClient)
{
    CEcSimulatorSilTestApplication oTestApplication;
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName(), eEcatState_OP);

    {
        /* DocumentationSnippetsEcMasterRasClientExampleAddConnection */
        /* Connect to Remote API Server */
        ECMASTERRAS_T_CLNTCONDESC oRasClientConDesc;
        OsMemset(&oRasClientConDesc, 0, sizeof(ECMASTERRAS_T_CLNTCONDESC));

        oRasClientConDesc.oAddr.dwAddr = OsInetAddr("127.0.0.1");
        oRasClientConDesc.wPort = ECMASTERRAS_DEFAULT_PORT;

        oRasClientConDesc.dwCycleTime = ECMASTERRAS_CYCLE_TIME;
        oRasClientConDesc.dwWDTOLimit = (ECMASTERRAS_MAX_WATCHDOG_TIMEOUT / ECMASTERRAS_CYCLE_TIME);
        oRasClientConDesc.dwRecvPrio = REMOTE_RECV_THREAD_PRIO;
        
        oRasClientConDesc.dwPktAdminSize = 20;
        oRasClientConDesc.dwWatchDog = 500;

        dwRes = emRasClntAddConnection(&oRasClientConDesc, &dwRasClientId);
        if (dwRes != EC_E_NOERROR)
        {
            dwRetVal = dwRes;
            goto Exit;
        }
        dwRasClientId = dwRasClientId | dwMasterId;
        /* DocumentationSnippetsEcMasterRasClientExampleAddConnection */
    }
    

    {
        /* DocumentationSnippetsEcMasterRasClientExampleGetMasterStateOverRAS */
        /* Get master state over RAS */
        EC_T_STATE eMasterState = emGetMasterState(dwRasClientId);
        EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, "Master state is %s\n", ecatStateToStr(eMasterState)));
        /* DocumentationSnippetsEcMasterRasClientExampleGetMasterStateOverRAS */
        CHECK_STATE_EQUAL(eEcatState_OP, eMasterState);
    }
Exit:
    CHECK_NOERROR(dwRetVal);
    CHECK_NOERROR(dwRes);
}

} } /* namespace EcMasterTests::DocumentationSnippets */
