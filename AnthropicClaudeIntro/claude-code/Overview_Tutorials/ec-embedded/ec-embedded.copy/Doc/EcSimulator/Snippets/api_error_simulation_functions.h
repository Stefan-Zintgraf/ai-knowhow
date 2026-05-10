/*-----------------------------------------------------------------------------
 * Doc/EcSimulator/Snippets/api_error_simulation_functions.h
 * Copyright                acontis technologies GmbH, Ravensburg, Germany
 * Response                 Paul Bussmann
 * Description
 *---------------------------------------------------------------------------*/

#ifndef INC_DOC_ECSIMULATOR_SNIPPETS_API_ERROR_SIMULATION_FUNCTIONS
#define INC_DOC_ECSIMULATOR_SNIPPETS_API_ERROR_SIMULATION_FUNCTIONS

namespace EcSimulatorTests { namespace DocumentationSnippets {

TEST_GROUP(ApiErrorSimulationFunctions)
{
};

EC_T_DWORD SendEmergencyExample(EC_T_DWORD dwSimulatorId, EC_T_WORD wSlaveAddress)
{
    EC_T_DWORD dwRes = EC_E_ERROR;

/** DocumentationSnippetsCoeEmergencyExample */
    /* send CoE Emergency */
    EC_T_BYTE abyEmergencyData[6] = { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06 };
    dwRes = esSendSlaveCoeEmergency(dwSimulatorId, wSlaveAddress, 0x1234 /* code */, abyEmergencyData, 6 /* data length */);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "esSendSlaveCoeEmergency failed: %s (0x%lx))\n", esGetText(dwSimulatorId, dwRes), dwRes));
        goto Exit;
    }
/** DocumentationSnippetsCoeEmergencyExample */

    return dwRes = EC_E_NOERROR;
Exit:
    return dwRes;
}
TEST(ApiErrorSimulationFunctions, DOC_CoeEmergencyExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName("Tiny"), eEcatState_PREOP);

    {
        CNotifySpy WaitForEmergency(0xFFFF);
        WaitForEmergency.Install(oTestApplication.GetMasterId());
        WaitForEmergency.StartTrace(EC_NOTIFY_MBOXRCV);

        CHECK_NOERROR(SendEmergencyExample(oTestApplication.GetSimulatorId(), 1004 /* UnitTestsTiny EL4132 */));

        CHECK_NOERROR(WaitForEmergency.WaitForTracedNotification(EC_NOTIFY_MBOXRCV, MBX_TIMEOUT));
    }
}

/* simulate sim slave error by application for WKC errors */
static EC_INLINESTART EC_T_DWORD SimulatorSnippetsSetSimSlaveStateError()
{
    EC_T_DWORD dwRes = EC_E_ERROR;
    EC_T_WORD  wSlaveAddr = 4104 /* 0x1008 EM_TEST_SLAVE */;
   
    struct _EC_T_SLAVE_SSC_APPL_DESC oSlaveApp;
    OsMemset(&oSlaveApp, 0, sizeof(struct _EC_T_SLAVE_SSC_APPL_DESC));

    oSlaveApp.dwSignature = SIMULATOR_SIGNATURE;
    oSlaveApp.dwSize = sizeof(struct _EC_T_SLAVE_SSC_APPL_DESC);
    oSlaveApp.szName = (EC_T_CHAR*)"mySlaveAppl";

    CEcSimulatorSilTestApplication oTestApplication;

    oTestApplication.setup();
    SetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms, eCnfType_Filename, oTestApplication.GetExiFileName());
    oTestApplication.SetupMaster(GetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms), eEcatState_INIT);

    EC_T_DWORD dwMasterId = oTestApplication.GetMasterId();
    EC_T_DWORD dwSimulatorId = oTestApplication.m_oLinkParms.linkParms.dwInstance;

    /* set master OP */
    dwRes = emSetMasterState(dwMasterId, 30000 /* dwTimeout */, eEcatState_OP);
    if (dwRes != EC_E_NOERROR)
    {
        goto Exit;
    }

    {
        CEcMasterNotifySpy oWkcErrorSpy(&oTestApplication);
        oWkcErrorSpy.DisableAllNotifications();
        oWkcErrorSpy.EnableNotification(EC_NOTIFY_CYCCMD_WKC_ERROR);
        oWkcErrorSpy.StartTrace(EC_NOTIFY_CYCCMD_WKC_ERROR);

/** DocumentationSnippetsSimulateSlaveErrorAlStatusCodeExample */
        /* start and immediately stop AL Status Error simulation (single shot) */
        dwRes = esSetSimSlaveState(dwSimulatorId, wSlaveAddr,
                    DEVICE_STATE_PREOP, DEVICE_STATUSCODE_ERROR);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }
        dwRes = esSetSimSlaveState(dwSimulatorId, wSlaveAddr,
                    0, DEVICE_STATUSCODE_NOERROR);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }
/** DocumentationSnippetsSimulateSlaveErrorAlStatusCodeExample */

        CHECK_NOERROR(oWkcErrorSpy.WaitForTracedNotification(EC_NOTIFY_CYCCMD_WKC_ERROR, 5000)); /* master reported WKC error */
    }

    dwRes = EC_E_NOERROR;
Exit:
    return dwRes;
} EC_INLINESTOP

TEST(ApiErrorSimulationFunctions, DOC_SetSimSlaveStateError)
{
    CHECK_NOERROR(SimulatorSnippetsSetSimSlaveStateError());
}

namespace SlaveSscAlStatusDelay
{
/** DocumentationSnippetsDelaySimSlaveAlStatusCallbacks */
    /* AL Status delay timer */
    static CEcTimer S_oAlStatusDelayTimer;
    
    /* EC_PF_SSC_APPL_START_MAILBOX_HANDLER */
    static EC_T_WORD EC_FNCALL APPL_StartMailboxHandlerCallback_DelayALStatus(
        EC_T_VOID* pvContext,
        EC_T_DWORD /* dwSimulatorId */,
        EC_T_WORD /* wCfgFixedAddress */)
    {
        T_EC_DEMO_APP_CONTEXT* pAppContext = (T_EC_DEMO_APP_CONTEXT*)pvContext;

        if (!S_oAlStatusDelayTimer.IsStarted())
        {
            EC_T_DWORD dwBusCycleTimeUsec = pAppContext->AppParms.dwBusCycleTimeUsec;

            /* simulate slave state delay (e.g 3 cycles) */
            S_oAlStatusDelayTimer.Start(EC_AT_LEAST(3 * dwBusCycleTimeUsec / 1000, 1));
        }

        /* return NOERROR_INWORK to delay the EtherCAT state transition */
        return 0xFF; /* NOERROR_INWORK, see also esSetSimSlaveState(..., 0, DEVICE_STATUSCODE_NOERROR) */
    }

    /* EC_PF_SSC_APPL_APPLICATION */
    static EC_T_VOID EC_FNCALL APPL_ApplicationCallback_DelayALStatus(
        EC_T_VOID* /* pvContext */,
        EC_T_DWORD dwInstanceId,
        EC_T_WORD wCfgFixedAddress)
    {
        /* application ready */
        if (S_oAlStatusDelayTimer.IsElapsed())
        {
            /* signal delayed EtherCAT state transition complete (see also NOERROR_INWORK) */
            esSetSimSlaveState(dwInstanceId, wCfgFixedAddress, 0, DEVICE_STATUSCODE_NOERROR);

            S_oAlStatusDelayTimer.Stop();
        }
    }
/** DocumentationSnippetsDelaySimSlaveAlStatusCallbacks */

    static EC_INLINESTART EC_T_DWORD SimulatorSnippetsDelaySlaveAlStatus(
        T_EC_DEMO_APP_CONTEXT* pAppContext, EC_T_DWORD dwMasterId, EC_T_DWORD dwSimulatorId, EC_T_WORD wSlaveAddress)
    {
        EC_T_DWORD dwRes = EC_E_ERROR;

        /* set Master INIT */
        dwRes = emSetMasterState(dwMasterId, 30000 /* dwTimeout */, eEcatState_INIT);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }

        {
/** DocumentationSnippetsDelaySimSlaveAlStatusMyAppPrepare */
            struct _EC_T_SLAVE_SSC_APPL_DESC oSlaveAppDesc;
            OsMemset(&oSlaveAppDesc, 0, sizeof(struct _EC_T_SLAVE_SSC_APPL_DESC));

            oSlaveAppDesc.dwSignature = SIMULATOR_SIGNATURE;
            oSlaveAppDesc.dwSize = sizeof(struct _EC_T_SLAVE_SSC_APPL_DESC);
            oSlaveAppDesc.szName = (EC_T_CHAR*)"mySlaveAppl";
            oSlaveAppDesc.pvContext = pAppContext;

            /* register callback APPL_Application, called after frame processing*/
            oSlaveAppDesc.pfnApplication = APPL_ApplicationCallback_DelayALStatus;
            /* register callback for master state transition request INIT to higher */
            oSlaveAppDesc.pfnStartMailboxHandler = APPL_StartMailboxHandlerCallback_DelayALStatus;
            /* register SlaveSscApplication callbacks (Master INIT) */
            dwRes = esSetSlaveSscApplication(dwSimulatorId, wSlaveAddress, &oSlaveAppDesc);
            if (dwRes != EC_E_NOERROR)
            {
                goto Exit;
            }
/** DocumentationSnippetsDelaySimSlaveAlStatusMyAppPrepare */

/** DocumentationSnippetsDelaySimSlaveAlStatusExample */
            dwRes = emSetMasterState(0, ETHERCAT_STATE_CHANGE_TIMEOUT, eEcatState_PREOP);
/** DocumentationSnippetsDelaySimSlaveAlStatusExample */
        }
Exit:
        return dwRes;
    } EC_INLINESTOP
}   /* namespace EcSimulatorTests/DocumentationSnippets/SlaveSscAlStatusDelay */

TEST(ApiErrorSimulationFunctions, DOC_SlaveSscAlStatusDelay)
{
    CEcSimulatorSilTestApplication oTestApplication;
    T_EC_DEMO_APP_CONTEXT* pAppContext = oTestApplication.GetAppContext();
    pAppContext->AppParms.dwBusCycleTimeUsec = oTestApplication.GetBusCycleTimeUsec();

    oTestApplication.setup();
    SetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms, eCnfType_Filename, oTestApplication.GetExiFileName());
    oTestApplication.SetupMaster(GetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms), eEcatState_INIT);
    /* simulate sim slave error by application for WKC errors */
    {
        CHECK_NOERROR(SlaveSscAlStatusDelay::SimulatorSnippetsDelaySlaveAlStatus(pAppContext, oTestApplication.GetMasterId(), oTestApplication.GetSimulatorId(), MBX_SLAVE_ADDRESS));
    }
}
} } /* namespace EcSimulatorTests/DocumentationSnippets */

#endif /* INC_DOC_ECSIMULATOR_SNIPPETS_API_ERROR_SIMULATION_FUNCTIONS */