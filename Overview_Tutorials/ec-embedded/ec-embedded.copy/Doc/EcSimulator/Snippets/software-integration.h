/*-----------------------------------------------------------------------------
 * Doc/EcSimulator/Snippets/software-integration.h
 * Copyright                acontis technologies GmbH, Ravensburg, Germany
 * Response                 Paul Bussmann
 * Description
 *---------------------------------------------------------------------------*/

#ifndef INC_DOC_ECSIMULATOR_SNIPPETS_SOFTWARE_INTEGRATION
#define INC_DOC_ECSIMULATOR_SNIPPETS_SOFTWARE_INTEGRATION

namespace EcSimulatorTests { namespace DocumentationSnippets {

TEST_GROUP(SoftwareIntegration)
{
};
IGNORE_TEST(SoftwareIntegration, DOC_SimulatorHilRtEthInit)
{
    EC_T_DWORD dwInstanceId = 1;
    EC_T_DWORD dwRes = EC_E_NOERROR;

    /** DocumentationSnippetsSimulatorHilRtEthInitExample */
    EC_T_SIMULATOR_INIT_PARMS oInitParms;
    OsMemset(&oInitParms, 0, sizeof(EC_T_SIMULATOR_INIT_PARMS));
    oInitParms.dwSignature = SIMULATOR_SIGNATURE;
    oInitParms.dwSize = sizeof(EC_T_SIMULATOR_INIT_PARMS);

    EC_T_LINK_PARMS_INTELGBE oLinkParmsIntelGbe;
    OsMemset(&oLinkParmsIntelGbe, 0, sizeof(EC_T_LINK_PARMS_INTELGBE));

    /* identify Link Layer in the common struture */
    oLinkParmsIntelGbe.linkParms.dwSignature = EC_LINK_PARMS_SIGNATURE_INTELGBE;
    oLinkParmsIntelGbe.linkParms.dwSize = sizeof(EC_T_LINK_PARMS_INTELGBE);
    OsStrncpy(oLinkParmsIntelGbe.linkParms.szDriverIdent, EC_LINK_PARMS_IDENT_INTELGBE, EC_DRIVER_IDENT_MAXLEN);
    oLinkParmsIntelGbe.linkParms.dwInstance = 1; /* instance ID of the adapter */
    oLinkParmsIntelGbe.linkParms.eLinkMode = EcLinkMode_INTERRUPT;
    oLinkParmsIntelGbe.linkParms.dwIstPriority = 0;
    
    /* specific Link Layer parameters should be set here */
    /* oLinkParmsIntelGbe.wRxBufferCnt = 128; */

    /* pass Link Layer parameters */
    oInitParms.apLinkParms[0] = &oLinkParmsIntelGbe.linkParms;
        
    /* initialize simulator */
    dwRes = esInitSimulator(dwInstanceId, &oInitParms);

    /** DocumentationSnippetsSimulatorHilRtEthInitExample */
    CHECK_NOERROR(dwRes);
}
IGNORE_TEST(SoftwareIntegration, DOC_SimulatorSilRtEthInit)
{
    EC_T_DWORD dwInstanceId = 0;
    EC_T_DWORD dwSimulatorId = 1;
    EC_T_DWORD dwRes = EC_E_NOERROR;

    /** DocumentationSnippetsSimulatorSilRtEthInitExample */
    /* master init parms */
    EC_T_INIT_MASTER_PARMS oInitMasterParms;
    OsMemset(&oInitMasterParms, 0, sizeof(EC_T_INIT_MASTER_PARMS));

    /* simulator parms */
    EC_T_LINK_PARMS_SIMULATOR oLinkParmsSimulator;
    OsMemset(&oLinkParmsSimulator, 0, sizeof(EC_T_LINK_PARMS_SIMULATOR));

    /* license Link Layer parms */
    EC_T_LINK_PARMS_INTELGBE oLinkParmsIntelGbe;
    OsMemset(&oLinkParmsIntelGbe, 0, sizeof(EC_T_LINK_PARMS_INTELGBE));

    /* identify simulator Link Layer in the common structure */
    oLinkParmsSimulator.linkParms.dwSignature = EC_LINK_PARMS_SIGNATURE_SIMULATOR;
    oLinkParmsSimulator.linkParms.dwSize = sizeof(EC_T_LINK_PARMS_SIMULATOR);
    OsStrncpy(oLinkParmsSimulator.linkParms.szDriverIdent, EC_LINK_PARMS_IDENT_SIMULATOR, EC_DRIVER_IDENT_MAXLEN);
    oLinkParmsSimulator.linkParms.dwInstance = dwSimulatorId;
    oLinkParmsSimulator.linkParms.eLinkMode = EcLinkMode_POLLING;

    /* specific simulator parameters should be set here */
    /* oLinkParmsSimulator.pbyCnfData = ENI/EXI; */

    /* identify license Link Layer in the common structure */
    oLinkParmsIntelGbe.linkParms.dwSignature = EC_LINK_PARMS_SIGNATURE_INTELGBE;
    oLinkParmsIntelGbe.linkParms.dwSize = sizeof(EC_T_LINK_PARMS_INTELGBE);
    OsStrncpy(oLinkParmsIntelGbe.linkParms.szDriverIdent, EC_LINK_PARMS_IDENT_INTELGBE, EC_DRIVER_IDENT_MAXLEN);
    oLinkParmsIntelGbe.linkParms.dwInstance = 1; /* instance ID of the adapter */
    oLinkParmsIntelGbe.linkParms.eLinkMode = EcLinkMode_POLLING;

    /* specific Link Layer parameters should be set here */
    /* oLinkParmsIntelGbe.wRxBufferCnt = 128; */

    /* pass license Link Layer parameters to simulator Link Layer */
    oLinkParmsSimulator.apLinkParms[0] = (EC_T_LINK_PARMS*)&oLinkParmsIntelGbe;

    /* more parameters should be set here */
    oInitMasterParms.dwSignature = ATECAT_SIGNATURE;
    oInitMasterParms.dwSize = sizeof(EC_T_INIT_MASTER_PARMS);

    /* pass simulator Link Layer to master init parms */
    oInitMasterParms.pLinkParms = (EC_T_LINK_PARMS*)&oLinkParmsSimulator;

    /* initialize master */
    dwRes = emInitMaster(dwInstanceId, &oInitMasterParms);

    /** DocumentationSnippetsSimulatorSilRtEthInitExample */
    CHECK_NOERROR(dwRes);
}

/* s.a. TestWriteConfiguredStationAlias() */
EC_T_DWORD ConfiguredStationAliasUpdateExample(EC_T_DWORD dwSimulatorId)
{
    EC_T_DWORD dwRes = EC_E_NOERROR;

    /** DocumentationSnippetsConfiguredStationAliasUpdateExample */
    EC_T_WORD wSlaveAddress = 1001;
    EC_T_WORD wAlias = 1234;
    EC_T_WORD wEepromVal = EC_GET_FRM_WORD(&wAlias);

    /* write new station alias to EEPROM */
    dwRes = esWriteSlaveEEPRom(dwSimulatorId, EC_TRUE, wSlaveAddress, ESC_SII_REG_ALIASADDRESS, &wEepromVal, 1, EEPROM_TIMEOUT);
    if (dwRes != EC_E_NOERROR)
    {
        goto Exit;
    }

    /* power cycle slave to apply station alias from ESC_SII_REG_ALIASADDRESS (EEPROM) to ECREG_STATION_ADDRESS_ALIAS (ESC register 0x0012) */
    dwRes = esPowerSlave(dwSimulatorId, wSlaveAddress, EC_FALSE);
    if (dwRes != EC_E_NOERROR)
    {
        goto Exit;
    }
    dwRes = esPowerSlave(dwSimulatorId, wSlaveAddress, EC_TRUE);
    if (dwRes != EC_E_NOERROR)
    {
        goto Exit;
    }
    /** DocumentationSnippetsConfiguredStationAliasUpdateExample */

Exit:
    return dwRes;
}
TEST(SoftwareIntegration, DOC_ConfiguredStationAliasUpdateExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    EC_T_WORD wAliasEscReg = 0;

    oTestApplication.SetupMaster(oTestApplication.GetEniFileName("Tiny"));

    /* write Configured Station Alias to EEPROM (ESC_SII_REG_ALIASADDRESS: word offset 4) and power-cycle slave */
    CHECK_NOERROR(ConfiguredStationAliasUpdateExample(oTestApplication.GetSimulatorId()));

    /* check Configured Station Alias loaded at ESC register 0x0012 */
    CHECK_NOERROR(oTestApplication.ScanBus());
    CHECK_NOERROR(oTestApplication.ReadSlaveRegister(EC_TRUE, 1001 /* wSlaveAddress */, 0x0012 /* ECREG_STATION_ADDRESS_ALIAS */,
        (EC_T_BYTE*)&wAliasEscReg, sizeof(EC_T_WORD), FW_BOOT_TIMEOUT));
    CHECK_WORD_EQUAL(1234 /* wAlias */, EC_GET_FRM_WORD(&wAliasEscReg));
}

} } /* namespace EcSimulatorTests::DocumentationSnippets */

#endif /* INC_DOC_ECSIMULATOR_SNIPPETS_SOFTWARE_INTEGRATION */
