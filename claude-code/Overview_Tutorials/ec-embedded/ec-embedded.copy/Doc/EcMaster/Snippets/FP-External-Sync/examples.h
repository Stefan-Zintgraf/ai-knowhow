namespace EcMasterTests { namespace DocumentationSnippets {

IGNORE_TEST(DocumentationSnippets, ExternalSync_Config)
{
    /* additional DC configuration */
    EC_T_DC_CONFIGURE oDcConfigure;
    OsMemset(&oDcConfigure, 0, sizeof(EC_T_DC_CONFIGURE));
    /* Enable acyclic distribution if cycle time is above 1000 usec to get DCX in sync */
    oDcConfigure.bAcycDistributionDisabled = EC_FALSE; 

    /* configure DCX external synchronization */
    EC_T_DWORD dwBusCycleTimeUsec = 1000;
    EC_T_DCM_CONFIG oDcmConfig;
    OsMemset(&oDcmConfig, 0, sizeof(EC_T_DCM_CONFIG));

    oDcmConfig.eMode = eDcmMode_Dcx;
    /* Mastershift */
    oDcmConfig.u.Dcx.MasterShift.nCtlSetVal = (dwBusCycleTimeUsec * 1000 * 2) / 3; /* 66% */
    /* 20 % limit in nsec for InSync monitoring */
    oDcmConfig.u.Dcx.MasterShift.dwInSyncLimit = (dwBusCycleTimeUsec * 1000) / 5;  /* 20% */
    oDcmConfig.u.Dcx.MasterShift.bLogEnabled = EC_FALSE;
    /* Dcx Busshift */
    oDcmConfig.u.Dcx.nCtlSetVal = (dwBusCycleTimeUsec * 1000 * 2) / 3; /* 66% */
    /* 20 % limit in nsec for InSync monitoring */
    oDcmConfig.u.Dcx.dwInSyncLimit = (dwBusCycleTimeUsec * 1000) / 5;    
    oDcmConfig.u.Dcx.bLogEnabled = EC_FALSE;
    oDcmConfig.u.Dcx.dwExtClockTimeout = 1000;
    oDcmConfig.u.Dcx.wExtClockFixedAddr = 0; /* 0 only when clock adjustment in external mode configured by EcEngineer */

    dwRes = emDcmConfigure(dwInstanceId, &oDcmConfig, 0);

    /* IGNORE_TEST(DocumentationSnippets, ExternalSync_Config) */
}

} } /* namespace EcMasterTests::DocumentationSnippets */

