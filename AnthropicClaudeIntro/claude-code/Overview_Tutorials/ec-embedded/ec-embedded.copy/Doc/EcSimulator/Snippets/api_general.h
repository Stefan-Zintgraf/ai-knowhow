/*-----------------------------------------------------------------------------
 * Doc/EcSimulator/Snippets/api_general.h
 * Copyright                acontis technologies GmbH, Ravensburg, Germany
 * Response                 Paul Bussmann
 * Description
 *---------------------------------------------------------------------------*/

#ifndef INC_DOC_ECSIMULATOR_SNIPPETS_API_GENERAL
#define INC_DOC_ECSIMULATOR_SNIPPETS_API_GENERAL

namespace EcSimulatorTests { namespace DocumentationSnippets {
class CDocumentationSnippetsBase
{
public:
    CDocumentationSnippetsBase()
    {
        dwRetVal = EC_E_NOERROR;
        dwRes = EC_E_NOERROR;
        dwInstanceId = 0;
        dwClientId = INVALID_CLIENT_ID;
        dwMasterId = INSTANCE_MASTER_DEFAULT;
        dwRasClientId = 0;
        dwSimulatorId = 0;
    }

    EC_T_DWORD dwRetVal;
    EC_T_DWORD dwRes;
    EC_T_DWORD dwInstanceId;
    EC_T_DWORD dwMasterId;
    EC_T_DWORD dwClientId;
    EC_T_DWORD dwRasClientId;
    EC_T_DWORD dwSimulatorId;
};

TEST_GROUP(ApiGeneral), CDocumentationSnippetsBase
{
};

IGNORE_TEST(ApiGeneral, DOC_GetCfgSlaveInfo)
{
    /** DocumentationSnippetsGetCfgSlaveInfoExample */
    /* get information about slave configured in ENI file */
    EC_T_CFG_SLAVE_INFO oSlaveInfo;
    OsMemset(&oSlaveInfo, 0, sizeof(EC_T_CFG_SLAVE_INFO));
    dwRes = esGetCfgSlaveInfo(dwInstanceId, EC_TRUE, 1001, &oSlaveInfo);
    /** DocumentationSnippetsGetCfgSlaveInfoExample */
    CHECK_NOERROR(dwRes);
}

IGNORE_TEST(ApiGeneral, DOC_GetCfgSlaveSmInfo)
{
    /** DocumentationSnippetsGetCfgSlaveSmInfoExample */
    /* get information about slave's sync managers configured in ENI file */
    EC_T_CFG_SLAVE_SM_INFO oSlaveSmInfo;
    OsMemset(&oSlaveSmInfo, 0, sizeof(EC_T_CFG_SLAVE_SM_INFO));
    dwRes = esGetCfgSlaveSmInfo(dwInstanceId, EC_TRUE, 1001, &oSlaveSmInfo);
    /** DocumentationSnippetsGetCfgSlaveSmInfoExample */
    CHECK_NOERROR(dwRes);
}

} } /* namespace EcSimulatorTests::DocumentationSnippets */

#endif /* INC_DOC_ECSIMULATOR_SNIPPETS_API_GENERAL */
