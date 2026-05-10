#include "EcMbxGatewaySrv.h"
#include "EcMbxGatewayClnt.h"

namespace EcMasterTests {    namespace DocumentationSnippets {
IGNORE_TEST(DocumentationSnippets, UdpMailboxGatewaySrv)
{
    /* emInitMaster(..) */
    /* emConfigureMaster(..) */

    EC_T_VOID* pvMbxGatewaySrvHandle = EC_NULL;
    EC_T_MBX_GATEWAY_SRV_PARMS MbxGatewaySrvParms;
    OsMemset(&MbxGatewaySrvParms, 0, sizeof(EC_T_MBX_GATEWAY_SRV_PARMS));
    MbxGatewaySrvParms.dwSignature = EC_MBX_GATEWAY_SRV_SIGNATURE;
    MbxGatewaySrvParms.dwSize = sizeof(EC_T_MBX_GATEWAY_SRV_PARMS);
    MbxGatewaySrvParms.oAddr.dwAddr = 0; /* bind to every available network*/
    MbxGatewaySrvParms.wPort = EC_MBX_GATEWAY_DEFAULT_PORT;
    MbxGatewaySrvParms.dwInstanceID = INSTANCE_MASTER_DEFAULT;
    MbxGatewaySrvParms.dwMaxQueuedFrames = 10;
    EC_CPUSET_ZERO(MbxGatewaySrvParms.cpuAffinityMask);
    MbxGatewaySrvParms.dwThreadPriority = MAIN_THREAD_PRIO;

    dwRes = emMbxGatewaySrvStart(&MbxGatewaySrvParms, &pvMbxGatewaySrvHandle);
    
    /* main loop */
    
    dwRes = emMbxGatewaySrvStop(pvMbxGatewaySrvHandle,2000);
    
    /* emDeInitMaster(..) */

    /* IGNORE_TEST(DocumentationSnippets, UdpMailboxGatewaySrv) */
}

IGNORE_TEST(DocumentationSnippets, UdpMailboxGatewayClient)
{
    EC_T_DWORD dwMbxGatewayConId = 0;

    /* initialize mailbox gateway */
    {
        EC_T_MBX_GATEWAY_CLNT_PARMS MbxGatewayClientParms;
        OsMemset(&MbxGatewayClientParms, 0, sizeof(EC_T_MBX_GATEWAY_CLNT_PARMS));
        MbxGatewayClientParms.dwSignature = EC_MBX_GATEWAY_CLNT_SIGNATURE;
        MbxGatewayClientParms.dwSize = sizeof(EC_T_MBX_GATEWAY_CLNT_PARMS);
        OsMemcpy(&MbxGatewayClientParms.LogParms, G_pEcLogParms, sizeof(EC_T_LOG_PARMS));
        dwRes = emMbxGatewayClntInit(&MbxGatewayClientParms);
    }
    
    /* add a connection to mailbox gateway */
    {
        EC_T_MBX_GATEWAY_CLNT_CONDESC MbxGatewayClientConnection;
        OsMemset(&MbxGatewayClientConnection, 0, sizeof(MbxGatewayClientConnection));
        MbxGatewayClientConnection.oAddr.sAddr = { 127, 0, 0, 1 }; /* localhost */
        MbxGatewayClientConnection.wPort = EC_MBX_GATEWAY_DEFAULT_PORT;
        dwRes = emMbxGatewayClntAddConnection(&MbxGatewayClientConnection, &dwMbxGatewayConId);
        
        if (dwRes != EC_E_NOERROR)
        {
            EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emMbxGatewayClntAddConnection failed! %s (Result = 0x%x)\\n", ecatGetText(dwRes), dwRes));
            goto Exit;
        }
    }

    /* read vendorId from CoE object dictionary (index 0x1018, sub index 1) of slave 1001 */
    {
        EC_T_BYTE abyData[] = { 0,0,0,0 };
        EC_T_DWORD dwOutDataLen = 0;
        dwRes = emMbxGatewayClntCoeSdoUpload(dwMbxGatewayConId, 1001, 0x1018, 1, abyData, sizeof(abyData), &dwOutDataLen, 5000, 0);
        
        if (dwRes != EC_E_NOERROR)
        {
            EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emMbxGatewayClntInit failed! %s (Result = 0x%x)\\n", ecatGetText(dwRes), dwRes));
            goto Exit;
        }
        EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, "Vendor ID: 0x%x\\n", EC_GETDWORD(abyData)));
    }

    Exit:
    /* remove connection from mailbox gateway */

    dwRes = emMbxGatewayClntRemoveConnection(dwMbxGatewayConId);
    
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emMbxGatewayClntRemoveConnection failed! %s (Result = 0x%x)\\n", ecatGetText(dwRes), dwRes));
    }

    /* terminate mailbox gateway*/

    dwRes = emMbxGatewayClntDeinit();

    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emMbxGatewayClntDeinit failed! %s (Result = 0x%x)\\n", ecatGetText(dwRes), dwRes));
    }
    /* IGNORE_TEST(DocumentationSnippets, UdpMailboxGatewayClient) */
}
}} /* namespace EcMasterTests::DocumentationSnippets */