/*-----------------------------------------------------------------------------
* Doc/EcSimulator/Snippets/api_slave_control_and_status_functions.h
* Copyright                acontis technologies GmbH, Ravensburg, Germany
* Response                 Paul Bussmann
* Description
*---------------------------------------------------------------------------*/

#ifndef INC_DOC_ECSIMULATOR_SNIPPETS_API_SLAVE_CONTROL_AND_STATUS_FUNCTIONS
#define INC_DOC_ECSIMULATOR_SNIPPETS_API_SLAVE_CONTROL_AND_STATUS_FUNCTIONS

namespace EcSimulatorTests { namespace DocumentationSnippets {

TEST_GROUP(ApiSlaveControlAndStatusFunctions)
{
};

EC_T_DWORD GetBusSlaveInfoAndGetSlaveIdExamples(EC_T_DWORD dwSimulatorId)
{
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    EC_T_DWORD dwRes = EC_E_ERROR;
    {
        /** DocumentationSnippetsEsGetBusSlaveInfoWithStationAddress */
        EC_T_BUS_SLAVE_INFO oBusSlaveInfo;

        /* get bus slave info of slave with station address 1001 */
        dwRes = esGetBusSlaveInfo(dwSimulatorId, EC_TRUE, 1001, &oBusSlaveInfo);
        if (dwRes != EC_E_NOERROR)
        {
            dwRetVal = dwRes;
            goto Exit;
        }
        /** DocumentationSnippetsEsGetBusSlaveInfoWithStationAddress */

        {
            /** DocumentationSnippetsEsGetSlaveId */
            /* get slave id of slave with station address 1001 */
            EC_T_DWORD dwSlaveId = esGetSlaveId(dwSimulatorId, 1001);
            if (INVALID_SLAVE_ID == dwSlaveId)
            {
                dwRetVal = EC_E_NOTFOUND;
                goto Exit;
            }
            /** DocumentationSnippetsEsGetSlaveId */
        }
    }

    {
        /** DocumentationSnippetsEsGetBusSlaveInfoWithAutoIncAddress */
        EC_T_BUS_SLAVE_INFO oBusSlaveInfo;

        /* get bus slave info of third slave (auto inc address 0, -1, -2, ...) */
        dwRes = esGetBusSlaveInfo(dwSimulatorId, EC_FALSE, (EC_T_WORD)-2, &oBusSlaveInfo);
        if (dwRes != EC_E_NOERROR)
        {
            dwRetVal = dwRes;
            goto Exit;
        }
        /** DocumentationSnippetsEsGetBusSlaveInfoWithAutoIncAddress */

        {
            /** DocumentationSnippetsEsGetSlaveIdAtPosition */
            /* get slave id of third slave (auto inc address 0, -1, -2, ...) */
            EC_T_DWORD dwSlaveId = esGetSlaveIdAtPosition(dwSimulatorId, (EC_T_WORD)-2);
            if (INVALID_SLAVE_ID == dwSlaveId)
            {
                dwRetVal = EC_E_NOTFOUND;
                goto Exit;
            }
            /** DocumentationSnippetsEsGetSlaveIdAtPosition */
        }
    }
    dwRetVal = EC_E_NOERROR;
Exit:
    return dwRetVal;
}
TEST(ApiSlaveControlAndStatusFunctions, DOC_GetBusSlaveInfoAndGetSlaveIdExamples)
{
    CEcSimulatorSilTestApplication oTestApplication;
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName("Tiny"), eEcatState_INIT);
    CHECK_NOERROR(GetBusSlaveInfoAndGetSlaveIdExamples(oTestApplication.GetSimulatorId()));
}

#if 0
/* s.a. TestWriteConfiguredStationAlias() */
#define SLAVE_ADDRESS ((EC_T_WORD)1001)
TEST(ApiSlaveControlAndStatusFunctions, DOC_ConfiguredStationAliasByApp)
{
    CSimulatorLinkLayerTestApplication oTestApplication;
    EC_T_DWORD dwRes = EC_E_NOERROR;

    oTestApplication.setup();
    SetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms, eCnfType_Filename, oTestApplication.GetEniFileName("Tiny"));
    oTestApplication.SetupMaster(GetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms), eEcatState_INIT);

    CHECK_NOERROR(oTestApplication.ShutdownJobTask());

#define ALIAS_TEST_VAL 1234
    /* set Configured Station Alias, see docs "Configured Station Alias Update Example" */
    {
        /** DocumentationSnippetsConfiguredStationAliasUpdateExampleContextType */
        EC_T_WORD wAlias = 1234;
        EC_T_WORD wEepromVal = EC_GET_FRM_WORD(&wAlias);

        /* write new station alias to EEPROM */
        dwRes = esWriteSlaveEEPRom(dwSimulatorId, EC_TRUE, SLAVE_ADDRESS, ESC_SII_REG_ALIASADDRESS, &wEepromVal, 1, EEPROM_TIMEOUT);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }

        /* power cycle slave to apply station alias from ESC_SII_REG_ALIASADDRESS (EEPROM) to ECREG_STATION_ADDRESS_ALIAS (ESC register 0x0012) */
        dwRes = esPowerSlave(dwSimulatorId, SLAVE_ADDRESS, EC_FALSE);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }
        dwRes = esPowerSlave(dwSimulatorId, SLAVE_ADDRESS, EC_TRUE);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }
        /** DocumentationSnippetsConfiguredStationAliasUpdateExampleContextType */
        CHECK_WORD_EQUAL(ALIAS_TEST_VAL, wAlias);
    }

    /* check Configured Station Alias */
    {
        EC_T_WORD wAliasEscReg = 0;

        CHECK_NOERROR(oTestApplication.CreateJobTask());

        /* check ESC_SII_REG_ALIASADDRESS (EEPROM) to ECREG_STATION_ADDRESS_ALIAS (ESC register 0x0012) applied */
        CHECK_WORD_EQUAL(0x0012, ECREG_STATION_ADDRESS_ALIAS);
        CHECK_WORD_EQUAL(0x0004, ESC_SII_REG_ALIASADDRESS);
        CHECK_NOERROR(oTestApplication.ScanBus());
        CHECK_NOERROR(oTestApplication.ReadSlaveRegister(EC_TRUE, SLAVE_ADDRESS, ECREG_STATION_ADDRESS_ALIAS, (EC_T_BYTE*)&wAliasEscReg, sizeof(EC_T_WORD), FW_BOOT_TIMEOUT));
        CHECK_WORD_EQUAL(ALIAS_TEST_VAL, EC_GET_FRM_WORD(&wAliasEscReg));
    }

Exit:
    CHECK_NOERROR(dwRes);
}
#endif

} } /* namespace EcSimulatorTests::DocumentationSnippets */

#endif /* INC_DOC_ECSIMULATOR_SNIPPETS_API_SLAVE_CONTROL_AND_STATUS_FUNCTIONS */
