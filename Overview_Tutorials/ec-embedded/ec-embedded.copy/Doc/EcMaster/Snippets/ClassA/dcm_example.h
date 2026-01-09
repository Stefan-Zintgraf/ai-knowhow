namespace EcMasterTests { namespace DocumentationSnippets {
TEST_GROUP(Dcm), CDocumentationSnippetsBase
{};

static EC_T_DWORD EcMasterNotifyCallback(EC_T_DWORD, EC_T_NOTIFYPARMS*) { return EC_E_NOERROR; }
IGNORE_TEST(Dcm, DOC_DcmConfiguration)
{
    EC_T_INIT_MASTER_PARMS oInitParms;
    T_EC_DEMO_APP_CONTEXT* pAppContext = EC_NULL;

    /* DocumentationSnippetsDcmConfigurationExample */
    /* initialize the master */
    dwRes = ecatInitMaster(&oInitParms);

    /* configure the master */
    dwRes = ecatConfigureNetwork(eCnfType_Filename, (EC_T_BYTE*)"ENI.xml", (EC_T_DWORD)OsStrlen("ENI.xml"));

    /* register client */
    EC_T_REGISTERRESULTS oRegisterClientResults;
    OsMemset(&oRegisterClientResults, 0, sizeof(EC_T_REGISTERRESULTS));
    dwRes = ecatRegisterClient(EcMasterNotifyCallback, pAppContext, &oRegisterClientResults);

    /* configure DC */
    EC_T_DC_CONFIGURE oDcConfigure;
    OsMemset(&oDcConfigure, 0, sizeof(EC_T_DC_CONFIGURE));
    oDcConfigure.dwTimeout = ETHERCAT_DC_TIMEOUT;
    dwRes = ecatDcConfigure(&oDcConfigure);

    /* configure DCM Bus Shift */
    EC_T_DCM_CONFIG oDcmConfig;
    OsMemset(&oDcmConfig, 0, sizeof(EC_T_DCM_CONFIG));
    oDcmConfig.eMode = eDcmMode_BusShift;
    oDcmConfig.u.BusShift.nCtlSetVal = DCM_CONTROLLER_SETVAL_NANOSEC;
    oDcmConfig.u.BusShift.bLogEnabled = EC_TRUE;
    dwRes = ecatDcmConfigure(&oDcmConfig, 0 /* dwInSyncTimeout */);

    /* set EtherCAT devices to OPERATIONAL state */
    dwRes = ecatSetMasterState(ETHERCAT_STATE_CHANGE_TIMEOUT, eEcatState_OP);
    /* DocumentationSnippetsDcmConfigurationExample */
}
IGNORE_TEST(Dcm, DOC_DcmLog)
{
    EC_T_USER_JOB_PARMS oJobParms;
    T_EC_DEMO_APP_CONTEXT oAppContext;
    T_EC_DEMO_APP_CONTEXT* pAppContext = &oAppContext;
    OsMemset(&oAppContext, 0, sizeof(T_EC_DEMO_APP_CONTEXT));

    /* DocumentationSnippetsDcmLogExample */
    do
    {
        /* wait for next cycle (event from scheduler task) */
        /* ... */

        /* process all received frames (read new input values) */
        dwRes = ecatExecJob(eUsrJob_ProcessAllRxFrames, &oJobParms);

        /* ... */

        EC_T_CHAR* szDcmLog = EC_NULL;
        ecatDcmGetLog(&szDcmLog);
        if (EC_NULL != szDcmLog)
        {
            ((CAtEmLogging*)pEcLogContext)->LogDcm(szDcmLog);
        }

        /* ... */
    } while (!pAppContext->bJobTaskShutdown);
    /* DocumentationSnippetsDcmLogExample */
}

} } /* namespace EcMasterTests::DocumentationSnippets */
