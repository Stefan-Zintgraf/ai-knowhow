/*-----------------------------------------------------------------------------
 * Doc/EcMaster/Snippets/EcMasterSnippets.cpp
 * Copyright                acontis technologies GmbH, Ravensburg, Germany
 * Response     Holger Oelhaf
 * Description  Code snippets, examples for documentation
 *---------------------------------------------------------------------------*/

/*-INCLUDES------------------------------------------------------------------*/
#ifndef EC_TEST_COMMON_H
#include "EcTestCommon.h"
#endif

#ifndef INC_ECSIMULATORTESTAPPLICATION
#include "../../../Tests/EcSimulatorTests/CEcSimulatorSilTestApplication.h"
#endif

#ifndef ECTESTSIMULATOR_H
#include "../../../Tests/EcSimulatorTests/EcTestSimulator.h"
#endif

namespace EcMasterTests { namespace DocumentationSnippets {
class CDocumentationSnippetsBase
{
public:
    CDocumentationSnippetsBase()
    {
        dwRetVal = EC_E_NOERROR;
        dwRes = EC_E_NOERROR;
        dwInstanceId = INSTANCE_MASTER_DEFAULT;
        dwClientId = INVALID_CLIENT_ID;
        dwMasterId = INSTANCE_MASTER_DEFAULT;
        dwRasClientId = INSTANCE_MASTER_DEFAULT;
        dwSimulatorId = INSTANCE_MASTER_DEFAULT;
    }

    EC_T_DWORD dwRetVal;
    EC_T_DWORD dwRes;
    EC_T_DWORD dwInstanceId;
    EC_T_DWORD dwMasterId;
    EC_T_DWORD dwClientId;
    EC_T_DWORD dwRasClientId;
    EC_T_DWORD dwSimulatorId;
    EC_T_VOID* hDaq;
};

TEST_GROUP(DocumentationSnippets), CDocumentationSnippetsBase
{
    TEST_SETUP() { }
    TEST_TEARDOWN() {}

    EC_T_INIT_MASTER_PARMS oInitMasterParms;
    static EC_T_VOID CycFrameReceivedCallback(EC_T_DWORD dwTaskId, EC_T_VOID* pvContext)
    {
        EC_UNREFPARM(dwTaskId); EC_UNREFPARM(pvContext);
    }
};

} } /* namespace EcMasterTests::DocumentationSnippets */

/*-SNIPPETS--------------------------------------------------------------------*/
#include "ClassA/dcm_example.h"
#include "ClassB/api.h"
#include "ClassB/emll_init.h"
#include "ClassB/mbx_coe.h"
#include "ClassB/mbx_foe.h"
#include "ClassB/mbx_voe.h"
#include "ClassB/software-integration.h"
#include "FP-RAS/software-integration.h"
#include "FP-SuperSet-ENI/intro.h"
#include "FP-Split-Frame-Processing/examples.h"
#include "FP-External-Sync/examples.h"
#include "../../EcDaq/Snippets/examples.h"
