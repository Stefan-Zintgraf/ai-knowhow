/*-----------------------------------------------------------------------------
 * Doc/EcSimulator/Snippets/api_mailbox.h
 * Copyright                acontis technologies GmbH, Ravensburg, Germany
 * Response                 Paul Bussmann
 * Description
 *---------------------------------------------------------------------------*/

#ifndef INC_DOC_ECSIMULATOR_SNIPPETS_API_MAILBOX
#define INC_DOC_ECSIMULATOR_SNIPPETS_API_MAILBOX

namespace EcSimulatorTests { namespace DocumentationSnippets {

/* include within namespace to prevent name clashes with EcTestCasesSimulator.cpp */
#include "../../../Examples/Common/EcSimulatorMbx.h"

TEST_GROUP(ApiMailbox)
{
};

/* ----------------- AoE ----------------- */
namespace AoE
{
namespace SimulatorSetSlaveAoeObjectTransferCallbacksExample
{
/** DocumentationSnippetsSimulatorSetSlaveAoeObjectTransferCallbacksExampleCallbacks */
/* EC_T_PF_AOE_READ_CB */
EC_T_DWORD EC_FNCALL myAppAoeReadObjectCallback(
    EC_T_VOID* /* pvContext */, EC_T_DWORD dwSimulatorId, EC_T_WORD wCfgFixedAddress,
    EC_T_AOE_NETID* /* poSenderNetId */, EC_T_WORD /* wSenderPort */, EC_T_AOE_NETID* /* poTargetNetId */, EC_T_WORD wTargetPort,
    EC_T_DWORD dwIndexGroup, EC_T_DWORD dwIndexOffset,
    EC_T_BYTE* pbyReadData, EC_T_DWORD* pdwReadDataLen,
    EC_T_DWORD* pdwErrorCode, EC_T_DWORD* pdwCmdResult)
{
    if (65535 != wTargetPort)
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_TARGET_PORT_NOT_FOUND);
        goto Exit;
    }

    if (0xF302 /* ADSIGRP_CANOPEN_SDO */ != dwIndexGroup)
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_INVALIDGRP);
        goto Exit;
    }

    /* check for object 0x2003, subindex 0, no complete access */
    if (0x20030000 != dwIndexOffset /* example value */)
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_NOTFOUND);
        goto Exit;
    }
    /* check for size of object 0x2003, subindex 0 */
    if (4 != EC_GETDWORD(pdwReadDataLen) /* UDINT: sizeof(EC_T_DWORD) */)
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_INVALIDSIZE);
        goto Exit;
    }

    /* all checks passed, return data and set success */
    EC_SET_FRM_DWORD(pbyReadData, 0x12345678);
    EC_SETDWORD(pdwErrorCode, EC_E_NOERROR);

Exit:
    EcLogMsg(EC_LOG_LEVEL_VERBOSE, (pEcLogContext, EC_LOG_LEVEL_VERBOSE, "myAppAoeReadObjectCallback(%d, %d, %d, 0x%04X, 0x%04X, %d bytes, 0x%08X, 0x%08X): %s (0x%08X)\n",
        dwSimulatorId, wCfgFixedAddress, wTargetPort,
        dwIndexGroup, dwIndexOffset, EC_GETDWORD(pdwReadDataLen), EC_GETDWORD(pdwErrorCode), EC_GETDWORD(pdwCmdResult),
        esGetText(dwSimulatorId, EC_GETDWORD(pdwErrorCode)), EC_GETDWORD(pdwErrorCode)));
    return EC_GETDWORD(pdwErrorCode);
}

/* EC_T_PF_AOE_WRITE_CB */
EC_T_DWORD EC_FNCALL myAppAoeWriteObjectCallback(
    EC_T_VOID* /* pvContext */, EC_T_DWORD dwSimulatorId, EC_T_WORD wCfgFixedAddress,
    EC_T_AOE_NETID* /* poSenderNetId */, EC_T_WORD /* wSenderPort */, EC_T_AOE_NETID* /* poTargetNetId */, EC_T_WORD wTargetPort,
    EC_T_DWORD dwIndexGroup, EC_T_DWORD dwIndexOffset,
    EC_T_BYTE* pbyWriteData, EC_T_DWORD dwWriteDataLen,
    EC_T_DWORD* pdwErrorCode, EC_T_DWORD* pdwCmdResult)
{
    EC_T_DWORD dwVal = 0;
    if (65535 != wTargetPort)
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_TARGET_PORT_NOT_FOUND);
        goto Exit;
    }

    if (0xF302 /* ADSIGRP_CANOPEN_SDO */ != dwIndexGroup)
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_INVALIDGRP);
        goto Exit;
    }

    /* check for object 0x2003, subindex 0, no complete access */
    if (0x20030000 != dwIndexOffset /* example value */)
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_NOTFOUND);
        goto Exit;
    }
    /* check for size of object 0x2003, subindex 0 */
    if (4 != dwWriteDataLen /* UDINT: sizeof(EC_T_DWORD) */)
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_INVALIDSIZE);
        goto Exit;
    }

    /* all checks passed, get data and set success */
    dwVal = EC_GET_FRM_DWORD(pbyWriteData);
    EC_SETDWORD(pdwErrorCode, EC_E_NOERROR);
Exit:
    EcLogMsg(EC_LOG_LEVEL_VERBOSE, (pEcLogContext, EC_LOG_LEVEL_VERBOSE, "myAppAoeWriteObjectCallback(%d, %d, %d, 0x%04X, 0x%04X, %d bytes, 0x%08X, 0x%08X) = %d (0x%08X): %s (0x%08X)\n",
        dwSimulatorId, wCfgFixedAddress, wTargetPort,
        dwIndexGroup, dwIndexOffset, dwWriteDataLen, EC_GETDWORD(pdwErrorCode), EC_GETDWORD(pdwCmdResult),
        dwVal, dwVal,
        esGetText(dwSimulatorId, EC_GETDWORD(pdwErrorCode)), EC_GETDWORD(pdwErrorCode)));
    return EC_GETDWORD(pdwErrorCode);
}

/* EC_T_PF_AOE_READWRITE_CB */
EC_T_DWORD EC_FNCALL myAppAoeReadWriteObjectCallback(
    EC_T_VOID* /* pvContext */, EC_T_DWORD dwSimulatorId, EC_T_WORD wCfgFixedAddress,
    EC_T_AOE_NETID* /* poSenderNetId */, EC_T_WORD /* wSenderPort */, EC_T_AOE_NETID* /* poTargetNetId */, EC_T_WORD wTargetPort,
    EC_T_DWORD dwIndexGroup, EC_T_DWORD dwIndexOffset,
    EC_T_BYTE* pbyReadData, EC_T_DWORD* pdwReadDataLen, EC_T_BYTE* pbyWriteData, EC_T_DWORD dwWriteDataLen,
    EC_T_DWORD* pdwErrorCode, EC_T_DWORD* pdwCmdResult)
{
    EC_T_DWORD dwVal = 0;
    if (65535 != wTargetPort)
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_TARGET_PORT_NOT_FOUND);
        goto Exit;
    }

    if (0xF302 /* ADSIGRP_CANOPEN_SDO */ != dwIndexGroup)
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_INVALIDGRP);
        goto Exit;
    }

    /* check for object 0x2003, subindex 0, no complete access */
    if (0x20030000 != dwIndexOffset /* example value */)
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_NOTFOUND);
        goto Exit;
    }
    /* check for size of object 0x2003, subindex 0 */
    if ((4 != EC_GETDWORD(pdwReadDataLen) /* UDINT: sizeof(EC_T_DWORD) */)
        || (4 != dwWriteDataLen /* UDINT: sizeof(EC_T_DWORD) */))
    {
        EC_SETDWORD(pdwErrorCode, EC_E_AOE_INVALIDSIZE);
        goto Exit;
    }

    /* all checks passed, set and get data and set success */
    EC_SET_FRM_DWORD(pbyReadData, 0x12345678);
    dwVal = EC_GET_FRM_DWORD(pbyWriteData);
    EC_SETDWORD(pdwErrorCode, EC_E_NOERROR);

Exit:

    EcLogMsg(EC_LOG_LEVEL_VERBOSE, (pEcLogContext, EC_LOG_LEVEL_VERBOSE, "myAppAoeReadWriteObjectCallback(%d, %d, %d, 0x%04X, 0x%04X, read %d bytes, write %d bytes, 0x%08X, 0x%08X) = %d (0x%08X): %s (0x%08X)\n",
        dwSimulatorId, wCfgFixedAddress, wTargetPort,
        dwIndexGroup, dwIndexOffset, EC_GETDWORD(pdwReadDataLen), dwWriteDataLen, EC_GETDWORD(pdwErrorCode), EC_GETDWORD(pdwCmdResult),
        dwVal, dwVal,
        esGetText(dwSimulatorId, EC_GETDWORD(pdwErrorCode)), EC_GETDWORD(pdwErrorCode)));
    return EC_GETDWORD(pdwErrorCode);
}
/** DocumentationSnippetsSimulatorSetSlaveAoeObjectTransferCallbacksExampleCallbacks */

static EC_T_VOID TestTransfers(T_EC_DEMO_APP_CONTEXT* pAppContext,
    EC_T_DWORD dwMasterId, EC_T_DWORD dwSimulatorId, EC_T_WORD wSlaveAddress)
{
    /** DocumentationSnippetsSimulatorSetSlaveAoeObjectTransferCallbacksExampleTransfer */
    EC_T_DWORD dwRes = EC_E_ERROR;
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    EC_T_BYTE  abyWriteData[sizeof(EC_T_DWORD)];
    EC_T_BYTE  abyReadData[sizeof(EC_T_DWORD)];
    EC_T_BYTE  abyReadWriteData[sizeof(EC_T_DWORD)];
    EC_T_DWORD dwDataOutLen = 0;
    EC_T_AOE_NETID oAoeNetId;
    EC_T_DWORD dwSlaveId = emGetSlaveId(dwMasterId, wSlaveAddress);
    EC_T_DWORD dwErrorCode = EC_E_ERROR;
    EC_T_DWORD dwCmdResult = EC_E_ERROR;

    OsMemset(abyWriteData, 0, sizeof(abyWriteData));
    OsMemset(abyReadData, 0, sizeof(abyReadData));
    OsMemset(abyReadWriteData, 0, sizeof(abyReadWriteData));

    /* EC-Master: get configured AoE net ID */
    dwRes = emAoeGetSlaveNetId(dwMasterId, dwSlaveId, &oAoeNetId);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emAoeGetSlaveNetId failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Simulator: register AoE handlers */
    dwRes = esSetSlaveAoeObjectTransferCallbacks(dwSimulatorId, wSlaveAddress,
        myAppAoeReadObjectCallback, myAppAoeWriteObjectCallback, myAppAoeReadWriteObjectCallback, pAppContext);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "esSetSlaveAoeObjectTransferCallbacks failed: %s (0x%lx))\n", esGetText(dwSimulatorId, dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Master: set PREOP state */
    dwRes = emSetMasterState(dwMasterId, 30000, eEcatState_PREOP);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emSetMasterState failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

#define AOE_TARGET_PORT     65535
#define AOE_INDEX_GROUP     0xF302  /* ADSIGRP_CANOPEN_SDO */

    /* CoE objects to access via AoE */
#define AOE_COE_OBJ_IDX            0x2003
#define AOE_COE_OBJ_SUBINDEX       0
#define AOE_COE_OBJ_COMPLETEACCESS EC_FALSE

    /* Bit 16-31: index, Bit 8: complete access, Bit 0-7: subindex */
#define AOE_INDEX_OFFSET ((AOE_COE_OBJ_IDX << 16) | (AOE_COE_OBJ_COMPLETEACCESS << 8) | AOE_COE_OBJ_SUBINDEX)

    /* EC-Master: write AoE to slave */
    EC_SET_FRM_DWORD(abyWriteData, 0x11223344 /* example value */);
    dwRes = emAoeWrite(dwMasterId, dwSlaveId, &oAoeNetId, AOE_TARGET_PORT, AOE_INDEX_GROUP, AOE_INDEX_OFFSET,
        sizeof(EC_T_DWORD), abyWriteData, &dwErrorCode, &dwCmdResult, MBX_TIMEOUT);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emAoeWrite failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Master: read AoE from slave */
    EC_SET_FRM_DWORD(abyReadData, 0);
    dwRes = emAoeRead(dwMasterId, dwSlaveId, &oAoeNetId, AOE_TARGET_PORT, AOE_INDEX_GROUP, AOE_INDEX_OFFSET,
        sizeof(EC_T_DWORD), abyReadData, &dwDataOutLen, &dwErrorCode, &dwCmdResult, MBX_TIMEOUT);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emAoeRead failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Master: read + write AoE from/to slave */
    EC_SET_FRM_DWORD(abyReadWriteData, 0x11223344 /* example value */);
    dwRes = emAoeReadWrite(dwMasterId, dwSlaveId, &oAoeNetId, AOE_TARGET_PORT, AOE_INDEX_GROUP, AOE_INDEX_OFFSET,
        sizeof(EC_T_DWORD), sizeof(EC_T_DWORD), abyReadWriteData, &dwDataOutLen, &dwErrorCode, &dwCmdResult, MBX_TIMEOUT);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emAoeReadWrite failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Simulator: write AoE to slave */
    EC_SET_FRM_DWORD(abyWriteData, 0x11223344 /* example value */);
    dwRes = esAoeWrite(dwSimulatorId, dwSlaveId, &oAoeNetId, AOE_TARGET_PORT, AOE_INDEX_GROUP, AOE_INDEX_OFFSET,
        sizeof(EC_T_DWORD), abyWriteData, &dwErrorCode, &dwCmdResult, MBX_TIMEOUT);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emAoeWrite failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Simulator: read AoE from slave */
    EC_SET_FRM_DWORD(abyReadData, 0);
    dwRes = esAoeRead(dwSimulatorId, dwSlaveId, &oAoeNetId, AOE_TARGET_PORT, AOE_INDEX_GROUP, AOE_INDEX_OFFSET,
        sizeof(EC_T_DWORD), abyReadData, &dwDataOutLen, &dwErrorCode, &dwCmdResult, MBX_TIMEOUT);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emAoeRead failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Simulator: read + write AoE from/to slave */
    EC_SET_FRM_DWORD(abyReadWriteData, 0x11223344 /* example value */);
    dwRes = esAoeReadWrite(dwSimulatorId, dwSlaveId, &oAoeNetId, AOE_TARGET_PORT, AOE_INDEX_GROUP, AOE_INDEX_OFFSET,
        sizeof(EC_T_DWORD), sizeof(EC_T_DWORD), abyReadWriteData, &dwDataOutLen, &dwErrorCode, &dwCmdResult, MBX_TIMEOUT);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emAoeReadWrite failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }
    /** DocumentationSnippetsSimulatorSetSlaveAoeObjectTransferCallbacksExampleTransfer */

    dwRetVal = EC_E_NOERROR;
Exit:
    CHECK_NOERROR(dwRetVal);
    CHECK_DWORD_EQUAL(0x12345678, EC_GET_FRM_DWORD(abyReadData));
    CHECK_DWORD_EQUAL(0x12345678, EC_GET_FRM_DWORD(abyReadWriteData));
}
} /* namespace SimulatorSetSlaveAoeObjectTransferCallbacksExample */

TEST(ApiMailbox, DOC_AoeTransfersExample)
{
    EC_T_WORD wSlaveAddress = EM_TEST_SLAVE;
    CEcSimulatorSilTestApplication oTestApplication;
    T_EC_DEMO_APP_CONTEXT* pAppContext = oTestApplication.GetAppContext();
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName());

    SimulatorSetSlaveAoeObjectTransferCallbacksExample::TestTransfers(pAppContext, oTestApplication.GetMasterId(), oTestApplication.GetSimulatorId(), wSlaveAddress);
}
} /* namespace AoE */

/* ----------------- CoE ----------------- */
namespace CoE
{
namespace SimulatorSetSlaveCoeObjectTransferCallbacksExample
{
/** DocumentationSnippetsSimulatorSetSlaveCoeObjectTransferCallbacksExampleCallbacks */
/* Length check in application if Object Dictionary unavailable at EC-Simulator */
static EC_T_DWORD myAppCoeObjectGetDataLen(
    EC_T_VOID* /* pvContext */, EC_T_WORD /* wCfgFixedAddress */,
    EC_T_WORD wObjectIndex, EC_T_BYTE bySubindex,
    EC_T_BOOL /* bCompleteAccess */, EC_T_DWORD* pdwDataLen)
{
    EC_T_DWORD dwRetVal = EC_E_SDO_ABORTCODE_INDEX;

    /* example for 0x1018 Identity Object, SubIndex 1 Vendor ID */
    if ((0x1018 == wObjectIndex) && (1 == bySubindex))
    {
        *pdwDataLen = 4;
        dwRetVal = EC_E_NOERROR;
    }

    return dwRetVal;
}

/* EC_T_PF_COE_READ_CB */
static EC_T_VOID EC_FNCALL myAppCoeReadObjectCallback(
    EC_T_VOID* pvContext, EC_T_DWORD /* dwSimulatorId */, EC_T_WORD wCfgFixedAddress,
    EC_T_WORD wObjectIndex, EC_T_BYTE bySubindex, 
    EC_T_DWORD dwBufSize, EC_T_BYTE* pbyData, EC_T_DWORD* pdwOutDataLen, 
    EC_T_BOOL bCompleteAccess, 
    EC_T_BOOL bCheckReadAccess /* EC_TRUE: Object Dictionary unavailable at EC-Simulator */,
    EC_T_DWORD* pdwErrorCode /* see EC_E_SDO_ABORTCODE_... */)
{
    EC_T_DWORD dwDataLen = *pdwOutDataLen;

    /* check transfer parameters in application if Object Dictionary unavailable at EC-Simulator */
    if (bCheckReadAccess)
    {
        *pdwErrorCode = myAppCoeObjectGetDataLen(pvContext, wCfgFixedAddress, wObjectIndex, bySubindex, bCompleteAccess, &dwDataLen);
        if ((EC_E_NOERROR == *pdwErrorCode) && (dwBufSize < dwDataLen))
        {
            *pdwErrorCode = EC_E_SDO_ABORTCODE_DATA_LENGTH_TOO_LOW;
        }
    }
    if (EC_E_NOERROR == *pdwErrorCode)
    {
        /* provide data. example for 0x1018 Identity Object, SubIndex 1 Vendor ID */
        if ((0x1018 == wObjectIndex) && (1 == bySubindex))
        {
            OsDbgAssert(4 == dwDataLen); EC_SET_FRM_DWORD((EC_T_DWORD*)pbyData, 0x12345678);
        }
    }
    else
    {
        dwDataLen = 0;
    }

    *pdwOutDataLen = dwDataLen;
    return;
}

/* EC_T_PF_COE_WRITE_CB */
static EC_T_VOID EC_FNCALL myAppCoeWriteObjectCallback(
    EC_T_VOID* /* pvContext */, EC_T_DWORD /* dwSimulatorId */, EC_T_WORD /* wCfgFixedAddress */,
    EC_T_WORD wObjectIndex, EC_T_BYTE bySubindex,
    EC_T_DWORD dwSize, EC_T_BYTE* pbyData,
    EC_T_BOOL /* bCompleteAccess */,
    EC_T_BOOL bCheckWriteAccess /* EC_TRUE if Object Dictionary unavailable at EC-Simulator */,
    EC_T_DWORD* pdwErrorCode)
{
    OsDbgAssert(!bCheckWriteAccess /* Object Dictionary available */
                || (EC_E_SDO_ABORTCODE_INDEX == *pdwErrorCode));

    if ((0x2000 == wObjectIndex) && (0 == bySubindex))
    {
        /* check write access if Object Dictionary unavailable at EC-Simulator */
        if (bCheckWriteAccess && (2 != dwSize))
        {
            if (dwSize > 2)
            {
                *pdwErrorCode = EC_E_SDO_ABORTCODE_DATA_LENGTH_TOO_HIGH;
            }
            else
            {
                *pdwErrorCode = EC_E_SDO_ABORTCODE_DATA_LENGTH_TOO_LOW;
            }
            return;
        }
        /* handle data, e.g. myCoeSdoWrite(wObjectIndex, bySubindex, pbyData); */
        EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, "myAppCoeWriteObjectCallback: 0x%04X, %d: 0x%04X)\n", wObjectIndex, bySubindex, EC_GET_FRM_WORD(pbyData)));

        *pdwErrorCode = EC_E_NOERROR;
        return;
    }
}
/** DocumentationSnippetsSimulatorSetSlaveCoeObjectTransferCallbacksExampleCallbacks */

static EC_T_VOID TestTransfers(T_EC_DEMO_APP_CONTEXT* pAppContext,
    EC_T_DWORD dwMasterId, EC_T_DWORD dwSimulatorId, EC_T_WORD wSlaveAddress)
{
/** DocumentationSnippetsSimulatorSetSlaveCoeObjectTransferCallbacksExampleTransfer */
    EC_T_DWORD dwRes = EC_E_ERROR;
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    EC_T_BYTE  abyWriteData[sizeof(EC_T_WORD)];
    EC_T_BYTE  abyReadData[sizeof(EC_T_DWORD)];
    EC_T_DWORD dwDataOutLen = 0;

    OsMemset(abyWriteData, 0, sizeof(abyWriteData));
    OsMemset(abyReadData, 0, sizeof(abyReadData));

    /* EC-Simulator: clear Object Dictionary */
    dwRes = esClearSlaveCoeObjectDictionary(dwSimulatorId, wSlaveAddress);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "esClearSlaveCoeObjectDictionary failed: %s (0x%lx))\n", esGetText(dwSimulatorId, dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Simulator: register CoE handlers */
    dwRes = esSetSlaveCoeObjectTransferCallbacks(dwSimulatorId, wSlaveAddress, 0xFFFF /* all objects */,
                                                 myAppCoeReadObjectCallback, myAppCoeWriteObjectCallback, pAppContext);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "esSetSlaveCoeObjectTransferCallbacks failed: %s (0x%lx))\n", esGetText(dwSimulatorId, dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Master: set PREOP state */
    dwRes = emSetMasterState(dwMasterId, 30000, eEcatState_PREOP);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emSetMasterState failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Master: write CoE to slave */
    EC_SET_FRM_WORD(abyWriteData, 0x1234 /* example value */);
    dwRes = emCoeSdoDownload(dwMasterId, emGetSlaveId(dwMasterId, wSlaveAddress), 0x2000, 0, abyWriteData, sizeof(EC_T_WORD), 5000 /* timeout */, 0);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emCoeSdoDownload failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Master: read CoE from slave */
    EC_SET_FRM_DWORD(abyReadData, 0);
    dwRes = emCoeSdoUpload(dwMasterId, emGetSlaveId(dwMasterId, wSlaveAddress), 0x1018, 1 /* vendor id */, abyReadData, sizeof(EC_T_DWORD), &dwDataOutLen, 5000 /* timeout */, 0);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emCoeSdoUpload failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Simulator: write CoE to slave */
    EC_SET_FRM_WORD(abyWriteData, 0x1234 /* example value */);
    dwRes = esCoeSdoDownload(dwSimulatorId, esGetSlaveId(dwSimulatorId, wSlaveAddress), 0x2000, 0, abyWriteData, sizeof(EC_T_WORD), 5000 /* timeout */, 0);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "esCoeSdoDownload failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Simulator: read CoE from slave */
    EC_SET_FRM_DWORD(abyReadData, 0);
    dwRes = esCoeSdoUpload(dwSimulatorId, esGetSlaveId(dwSimulatorId, wSlaveAddress), 0x1018, 1 /* vendor id */, abyReadData, sizeof(EC_T_DWORD), &dwDataOutLen, 5000 /* timeout */, 0);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emCoeSdoUpload failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }
/** DocumentationSnippetsSimulatorSetSlaveCoeObjectTransferCallbacksExampleTransfer */

    dwRetVal = EC_E_NOERROR;
Exit:
    CHECK_NOERROR(dwRetVal);
    CHECK_DWORD_EQUAL(0x12345678, EC_GET_FRM_DWORD(abyReadData));
}
} /* namespace SimulatorSetSlaveCoeObjectTransferCallbacksExample */

TEST(ApiMailbox, DOC_CoeTransfersExample)
{
    EC_T_WORD wSlaveAddress = EM_TEST_SLAVE;
    CEcSimulatorSilTestApplication oTestApplication;
    T_EC_DEMO_APP_CONTEXT* pAppContext = oTestApplication.GetAppContext();
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName());

    SimulatorSetSlaveCoeObjectTransferCallbacksExample::TestTransfers(pAppContext, oTestApplication.GetMasterId(), oTestApplication.GetSimulatorId(), wSlaveAddress);
}
} /* namespace CoE */

/* ----------------- EoE ----------------- */
namespace EoE
{
/** DocumentationSnippetsEoeExampleContext */
T_MY_EOE_CONTEXT G_oContext;
/** DocumentationSnippetsEoeExampleContext */

static EC_T_VOID EoeExampleRegisterCallbacks(T_EC_DEMO_APP_CONTEXT* pAppContext, EC_T_WORD wSlaveAddress)
{
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    EC_T_DWORD dwRes = EC_E_ERROR;

/** DocumentationSnippetsEoeExampleRegisterCallbacks */
    OsMemset(&G_oContext, 0, sizeof(G_oContext));
    dwRes = myAppEoeInit(pAppContext, &G_oContext, wSlaveAddress);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }
/** DocumentationSnippetsEoeExampleRegisterCallbacks */

    dwRetVal = EC_E_NOERROR;
Exit:
    CHECK_NOERROR(dwRetVal);
}

TEST(ApiMailbox, DOC_EoePingExample)
{
    EC_T_DWORD dwRes = EC_E_ERROR;

    CEcSimulatorSilTestApplication oTestApplication;
    T_EC_DEMO_APP_CONTEXT* pAppContext = oTestApplication.GetAppContext();
    EC_T_WORD wSlaveAddress = EM_TEST_SLAVE;

    oTestApplication.setup();
    oTestApplication.GetMasterInitParms()->dwAdditionalEoEEndpoints = 1;
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName());

    EoeExampleRegisterCallbacks(pAppContext, wSlaveAddress);

    oTestApplication.SetCheckMasterState(eEcatState_PREOP);

    dwRes = pingMockEndpointPing(&oTestApplication);
    CHECK_NOERROR(dwRes);
}

EC_T_VOID SimulatorGetCfgSlaveEoeInfoExample(T_EC_DEMO_APP_CONTEXT* pAppContext, EC_T_WORD wSlaveAddress)
{
    EC_T_DWORD dwRes = EC_E_ERROR;
    EC_T_DWORD dwRetVal = EC_E_ERROR;

#undef  pEcLogParms
#define pEcLogParms (&(pAppContext->LogParms))
#define T9293_LOG_MSG "esGetCfgSlaveEoeInfo(4104): MAC address: 02:00:00:00:10:08, IP address: 192.168.18.104, subnet mask: 255.255.255.0, default gateway: 192.168.18.1, DNS server: 192.168.18.0, DNS name: EmTestSlave"
/** DocumentationSnippetsSimulatorGetCfgSlaveEoeInfoExample */
    EC_T_CFG_SLAVE_EOE_INFO oInfo;
    OsMemset(&oInfo, 0, sizeof(EC_T_CFG_SLAVE_EOE_INFO));

    dwRes = esGetCfgSlaveEoeInfo(pAppContext->dwInstanceId, EC_TRUE, wSlaveAddress, &oInfo);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "esGetCfgSlaveEoeInfo failed: %s (0x%lx))\n", 
            esGetText(pAppContext->dwInstanceId, dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    EcLogMsg(EC_LOG_LEVEL_INFO, (pEcLogContext, EC_LOG_LEVEL_INFO, "esGetCfgSlaveEoeInfo(%d): "
        "MAC address: %02X:%02X:%02X:%02X:%02X:%02X, IP address: %d.%d.%d.%d, subnet mask: %d.%d.%d.%d, "
        "default gateway: %d.%d.%d.%d, DNS server: %d.%d.%d.%d, DNS name: %s\n", wSlaveAddress,
        oInfo.abyMacAddr[0], oInfo.abyMacAddr[1], oInfo.abyMacAddr[2],
        oInfo.abyMacAddr[3], oInfo.abyMacAddr[4], oInfo.abyMacAddr[5],

        oInfo.oIpAddr.sAddr.by[0], oInfo.oIpAddr.sAddr.by[1], oInfo.oIpAddr.sAddr.by[2], oInfo.oIpAddr.sAddr.by[3],
        oInfo.oSubnetMask.sAddr.by[0], oInfo.oSubnetMask.sAddr.by[1], oInfo.oSubnetMask.sAddr.by[2], oInfo.oSubnetMask.sAddr.by[3],

        oInfo.oDefaultGateway.sAddr.by[0], oInfo.oDefaultGateway.sAddr.by[1], oInfo.oDefaultGateway.sAddr.by[2], oInfo.oDefaultGateway.sAddr.by[3],
        oInfo.oDnsServer.sAddr.by[0], oInfo.oDnsServer.sAddr.by[1], oInfo.oDnsServer.sAddr.by[2], oInfo.oDnsServer.sAddr.by[3], oInfo.szDnsName));
/** DocumentationSnippetsSimulatorGetCfgSlaveEoeInfoExample */
#undef  pEcLogParms
#define pEcLogParms G_pEcLogParms

    dwRetVal = EC_E_NOERROR;
Exit:
    CHECK_NOERROR(dwRetVal);
}

TEST(ApiMailbox, DOC_GetCfgSlaveEoeInfoExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    T_EC_DEMO_APP_CONTEXT* pAppContext = oTestApplication.GetAppContext();
    oTestApplication.SetupMaster(oTestApplication.GetEniFileName());

    {
        CTraceTermLogMsgSpy oLogSpy(pAppContext->dwInstanceId, T9293_LOG_MSG);
        pAppContext->LogParms.dwLogLevel = EC_LOG_LEVEL_INFO;
        SimulatorGetCfgSlaveEoeInfoExample(pAppContext, EM_TEST_SLAVE);
        CHECK(oLogSpy.IsTraceTermMatched());
    }
}

} /* namespace EoE */

/* ----------------- FoE ----------------- */
namespace FoE
{
namespace SimulatorFoeTransferExample
{
/** DocumentationSnippetsFoeTransferExampleContextType */
#define MYAPP_FOE_BUFFER_SIZE (35264)
typedef struct
{
    EC_T_BYTE abyFileBuf[MYAPP_FOE_BUFFER_SIZE];
    EC_T_WORD wFileBufLen;

    /* ... */
} T_MY_CONTEXT;
/** DocumentationSnippetsFoeTransferExampleContextType */

T_MY_CONTEXT G_oSlaveApplContext;
EC_T_BYTE G_abyFileBuf[MYAPP_FOE_BUFFER_SIZE];

/** DocumentationSnippetsFoeDownloadExampleCallbacks */
extern "C" EC_T_WORD EC_FNCALL myAppFoeWrite(
    EC_T_VOID* pvContext, EC_T_DWORD /* dwSimulatorId */, EC_T_WORD /* wCfgFixedAddress */, 
    EC_T_WORD*, EC_T_WORD, EC_T_DWORD)
{
    T_MY_CONTEXT* poContext = (T_MY_CONTEXT*)pvContext;
    poContext->wFileBufLen = 0;

    return 0; /* accept file download (ECAT_FOE_ERRCODE_... denies download) */
}

extern "C" EC_T_WORD EC_FNCALL myAppFoeWriteData(
    EC_T_VOID* pvContext, EC_T_DWORD /* dwSimulatorId */, EC_T_WORD /* wCfgFixedAddress */,
    EC_T_WORD* pData, EC_T_WORD wSize, EC_T_BYTE bDataFollowing)
{
    T_MY_CONTEXT* poContext = (T_MY_CONTEXT*)pvContext;
    if (poContext->wFileBufLen + wSize > sizeof(poContext->abyFileBuf))
    {
        return ECAT_FOE_ERRCODE_DISKFULL; /* abort transfer */
    }

    OsMemcpy(&poContext->abyFileBuf[poContext->wFileBufLen], pData, wSize);
    poContext->wFileBufLen = poContext->wFileBufLen + wSize;

    /* FoE ACK segment at Master (more segments follow / download finished) */
    return bDataFollowing ? SSC_FOE_ACK : SSC_FOE_ACKFINISHED;
}
/** DocumentationSnippetsFoeDownloadExampleCallbacks */

/** DocumentationSnippetsFoeUploadExampleCallbacks */
extern "C" EC_T_WORD EC_FNCALL myAppFoeReadData(
    EC_T_VOID* pvContext, EC_T_DWORD /* dwSimulatorId */, EC_T_WORD /* wCfgFixedAddress */,
    EC_T_DWORD dwOffset, EC_T_WORD wMaxBlockSize, EC_T_WORD* pData)
{
    T_MY_CONTEXT* poContext = (T_MY_CONTEXT*)pvContext;
    if (dwOffset > poContext->wFileBufLen)
    {
        return 0;
    }

    if (dwOffset + wMaxBlockSize > poContext->wFileBufLen)
    {
        wMaxBlockSize = EC_LOWORD(poContext->wFileBufLen - dwOffset);
    }

    if (wMaxBlockSize > 0)
    {
        OsMemcpy(pData, &poContext->abyFileBuf[dwOffset], wMaxBlockSize);
    }

    return wMaxBlockSize; /* amount of data read */
}

extern "C" EC_T_WORD EC_FNCALL myAppFoeRead(
    EC_T_VOID* pvContext, EC_T_DWORD dwSimulatorId, EC_T_WORD wCfgFixedAddress,
    EC_T_WORD*, EC_T_WORD, EC_T_DWORD, EC_T_WORD wMaxBlockSize, EC_T_WORD* pData)
{
    /* APPL_FoeRead contains returning first data */
    return myAppFoeReadData(pvContext, dwSimulatorId, wCfgFixedAddress, 0, wMaxBlockSize, pData);
}
/** DocumentationSnippetsFoeUploadExampleCallbacks */

static EC_INLINESTART EC_T_DWORD SimulatorSnippetsFoeDownloadExample(EC_T_DWORD dwMasterId, EC_T_DWORD dwSimulatorId, EC_T_WORD wSlaveAddress)
{
    EC_T_DWORD dwRes = EC_E_ERROR;

    /** DocumentationSnippetsFoeDownloadExampleSimulatorMyAppPrepare */
    struct _EC_T_SLAVE_SSC_APPL_DESC oSlaveApp;
    OsMemset(&oSlaveApp, 0, sizeof(struct _EC_T_SLAVE_SSC_APPL_DESC));

    T_MY_CONTEXT* poSlaveApplContext = &G_oSlaveApplContext;
    OsMemset(poSlaveApplContext, 0, sizeof(G_oSlaveApplContext));

    oSlaveApp.dwSignature = SIMULATOR_SIGNATURE;
    oSlaveApp.dwSize = sizeof(struct _EC_T_SLAVE_SSC_APPL_DESC);
    oSlaveApp.szName = (EC_T_CHAR*)"mySlaveAppl";
    oSlaveApp.pvContext = poSlaveApplContext; /* pvContext of callbacks */
    oSlaveApp.pfnFoeWrite = myAppFoeWrite;
    oSlaveApp.pfnFoeWriteData = myAppFoeWriteData;

    /* register SlaveSscApplication call-backs (Master in INIT) */
    dwRes = esSetSlaveSscApplication(dwSimulatorId, wSlaveAddress, &oSlaveApp);
    if (dwRes != EC_E_NOERROR)
    {
        goto Exit;
    }
    /** DocumentationSnippetsFoeDownloadExampleSimulatorMyAppPrepare */

    /** DocumentationSnippetsFoeDownloadExampleMaster */
    /* set Master PREOP */
    dwRes = emSetMasterState(dwMasterId, 30000 /* dwTimeout */, eEcatState_PREOP);
    if (dwRes != EC_E_NOERROR)
    {
        goto Exit;
    }

    /* download file */
    dwRes = emFoeFileDownload(dwMasterId, emGetSlaveId(dwMasterId, wSlaveAddress),
        (EC_T_CHAR*)"foe.dat", (EC_T_DWORD)OsStrlen((EC_T_CHAR*)"foe.dat"),
        G_abyFileBuf, MYAPP_FOE_BUFFER_SIZE, 0 /* dwPassword */, 30000 /* dwTimeout */);
    if (dwRes != EC_E_NOERROR)
    {
        goto Exit;
    }
    /** DocumentationSnippetsFoeDownloadExampleMaster */
    
    return dwRes = EC_E_NOERROR;
Exit:
    return dwRes;
} EC_INLINESTOP

static EC_INLINESTART EC_T_DWORD SimulatorSnippetsFoeUploadExample(EC_T_DWORD dwMasterId, EC_T_DWORD dwSimulatorId, EC_T_WORD wSlaveAddress, EC_T_DWORD* pdwOutDataLen)
{
    EC_T_DWORD dwRes = EC_E_ERROR;
    EC_T_DWORD dwOutDataLen = 0;

    {
        /** DocumentationSnippetsFoeUploadExampleSimulatorMyAppPrepare */
        struct _EC_T_SLAVE_SSC_APPL_DESC oSlaveApp;
        OsMemset(&oSlaveApp, 0, sizeof(struct _EC_T_SLAVE_SSC_APPL_DESC));

        T_MY_CONTEXT* poSlaveApplContext = &G_oSlaveApplContext;
        OsMemset(poSlaveApplContext, 0, sizeof(G_oSlaveApplContext));

        /* pattern for file content */
        OsMemset(poSlaveApplContext->abyFileBuf, 0xAA, MYAPP_FOE_BUFFER_SIZE);
        poSlaveApplContext->wFileBufLen = MYAPP_FOE_BUFFER_SIZE;

        oSlaveApp.dwSignature = SIMULATOR_SIGNATURE;
        oSlaveApp.dwSize = sizeof(struct _EC_T_SLAVE_SSC_APPL_DESC);
        oSlaveApp.szName = (EC_T_CHAR*)"mySlaveAppl";
        oSlaveApp.pvContext = poSlaveApplContext; /* pvContext of callbacks */
        oSlaveApp.pfnFoeRead = myAppFoeRead;
        oSlaveApp.pfnFoeReadData = myAppFoeReadData;

        /* register SlaveSscApplication callbacks (Master in INIT) */
        dwRes = esSetSlaveSscApplication(dwSimulatorId, wSlaveAddress, &oSlaveApp);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }
        /** DocumentationSnippetsFoeUploadExampleSimulatorMyAppPrepare */

        /** DocumentationSnippetsFoeUploadExampleMaster */
        /* set Master PREOP */
        dwRes = emSetMasterState(dwMasterId, 30000 /* dwTimeout */, eEcatState_PREOP);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }

        /* upload file */
        dwRes = emFoeFileUpload(dwMasterId, emGetSlaveId(dwMasterId, wSlaveAddress),
            (EC_T_CHAR*)"foe.dat", (EC_T_DWORD)OsStrlen((EC_T_CHAR*)"foe.dat"),
            G_abyFileBuf, MYAPP_FOE_BUFFER_SIZE, &dwOutDataLen, 0 /* dwPassword */, 30000 /* dwTimeout */);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }
        /** DocumentationSnippetsFoeUploadExampleMaster */
    }

    *pdwOutDataLen = dwOutDataLen;
    dwRes = EC_E_NOERROR;
Exit:
    return dwRes;
} EC_INLINESTOP

EC_T_BOOL G_bFoeBusyAtEnd = EC_FALSE;
EC_T_BOOL G_bFoeBusyBeforeEnd = EC_FALSE;
EC_T_WORD G_wBusyVal = 0;

extern "C" EC_T_WORD myAppFoeWriteDataBusy(
    EC_T_VOID* pvContext, EC_T_DWORD /* dwSimulatorId */, EC_T_WORD /* wCfgFixedAddress */,
    EC_T_WORD* pData, EC_T_WORD wSize, EC_T_BYTE bDataFollowing)
{
    T_MY_CONTEXT* poContext = (T_MY_CONTEXT*)pvContext;
    if (poContext->wFileBufLen + wSize > sizeof(poContext->abyFileBuf))
    {
        return ECAT_FOE_ERRCODE_DISKFULL;
    }

    OsMemcpy(&poContext->abyFileBuf[poContext->wFileBufLen], pData, wSize);

    if (bDataFollowing)
    {
        /* FoE-Data services will follow */

        /* simulate flash delay during write -> send busy for files starting with "busySeg_" */
        if (G_bFoeBusyBeforeEnd && (0xFFFF == G_wBusyVal))
        {
            G_wBusyVal = 0;
        }
        if (0xFFFF != G_wBusyVal)
        {
            G_wBusyVal++;
            if (0 == (G_wBusyVal % 2))
            {
                /* return busy on every second write */
                return SSC_FOE_MAXBUSY_ZERO;
            }
        }
    }
    else
    {
        /* simulate flash delay -> send busy for files starting with "busy_" */
        if (G_bFoeBusyAtEnd && (0xFFFF == G_wBusyVal))
        {
            G_wBusyVal = 0;
        }

        if (G_wBusyVal < 10)
        {
            G_wBusyVal++;
            return (EC_T_WORD)(SSC_FOE_MAXBUSY_ZERO + (G_wBusyVal * 10));
        }
        G_wBusyVal = 0xFFFF;
    }

    poContext->wFileBufLen = poContext->wFileBufLen + wSize;
    if (bDataFollowing)
    {
        return SSC_FOE_ACK;
    }

    /* FoE download finished */
    return SSC_FOE_ACKFINISHED;
}
} /* namespace SimulatorFoeTransferExample */

/* s.a. TestWriteConfiguredStationAlias() */
TEST(ApiMailbox, DOC_FoeDownloadExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    EC_T_WORD wSlaveAddress = 1004; /* UnitTestsTiny EL4132 */

    OsMemset(SimulatorFoeTransferExample::G_abyFileBuf, 0xAB, MYAPP_FOE_BUFFER_SIZE);

    oTestApplication.setup();
    SetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms, eCnfType_Filename, oTestApplication.GetEniFileName("Tiny"));
    oTestApplication.SetupMaster(GetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms), eEcatState_INIT);

    CHECK_NOERROR(SimulatorFoeTransferExample::SimulatorSnippetsFoeDownloadExample(oTestApplication.GetMasterId(), oTestApplication.GetSimulatorId(), wSlaveAddress));

    MEMCMP_EQUAL(SimulatorFoeTransferExample::G_abyFileBuf, SimulatorFoeTransferExample::G_oSlaveApplContext.abyFileBuf, MYAPP_FOE_BUFFER_SIZE);
}

TEST(ApiMailbox, DOC_FoeUploadExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    EC_T_WORD wSlaveAddress = 1004; /* UnitTestsTiny EL4132 */
    EC_T_DWORD dwOutDataLen = 0;

    OsMemset(SimulatorFoeTransferExample::G_abyFileBuf, 0, MYAPP_FOE_BUFFER_SIZE);

    oTestApplication.setup();
    SetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms, eCnfType_Filename, oTestApplication.GetEniFileName("Tiny"));
    oTestApplication.SetupMaster(GetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms), eEcatState_INIT);

    CHECK_NOERROR(SimulatorFoeTransferExample::SimulatorSnippetsFoeUploadExample(oTestApplication.GetMasterId(), oTestApplication.GetSimulatorId(), wSlaveAddress, &dwOutDataLen));

    CHECK_DWORD_EQUAL(MYAPP_FOE_BUFFER_SIZE, dwOutDataLen);
    MEMCMP_EQUAL(SimulatorFoeTransferExample::G_oSlaveApplContext.abyFileBuf, SimulatorFoeTransferExample::G_abyFileBuf, MYAPP_FOE_BUFFER_SIZE);
}

TEST(ApiMailbox, DOC_FoeUploadDelayFoeReadExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    EC_T_DWORD dwRes = EC_E_ERROR;
    EC_T_WORD wSlaveAddress = 1004; /* UnitTestsTiny EL4132 */

    oTestApplication.setup();
    SetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms, eCnfType_Filename, oTestApplication.GetEniFileName("Tiny"));
    oTestApplication.SetupMaster(GetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms), eEcatState_PREOP);

    CNotifySpy oSpy(&oTestApplication);
    oSpy.StartTrace(EC_NOTIFY_MBOXRCV);

    EC_T_MBXTFER* pMbxTfer = EC_NULL;
    CEmMbxTfer oMbxTfer(oTestApplication.GetMasterId(), oSpy.GetClientId());
    oMbxTfer.SetApp(&oTestApplication);
    pMbxTfer = oMbxTfer.Create(512);
    CHECK(EC_NULL != pMbxTfer);
    OsMemset(pMbxTfer->pbyMbxTferData, 0xAB, pMbxTfer->dwDataLen);

    {
        /* disable ProcessMbx at slave */
        EC_T_SIMULATOR_MBX_PROCESS_CTL_DESC oMbxProcessCtrlDesc;
        oMbxProcessCtrlDesc.wCfgFixedAddress = wSlaveAddress;
        oMbxProcessCtrlDesc.bReadMbxOutEnabled = EC_TRUE; /* slave reads MAILBOXOUT (SM0) */
        oMbxProcessCtrlDesc.bProcessMbxEnabled = EC_FALSE; /* disable processing to simulate long processing time */
        dwRes = esIoCtl(oTestApplication.GetSimulatorId(), EC_IOCTL_SIMULATOR_SET_MBX_PROCESS_CTL,
            &oMbxProcessCtrlDesc, sizeof(EC_T_SIMULATOR_MBX_PROCESS_CTL_DESC), EC_NULL, 0, EC_NULL);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }

        dwRes = emFoeDownloadReq(oTestApplication.GetMasterId(), pMbxTfer, emGetSlaveId(oTestApplication.GetMasterId(), wSlaveAddress), (EC_T_CHAR*)"test.dat", (EC_T_DWORD)OsStrlen((EC_T_CHAR*)"test.dat"), 0, 30000);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }

        /* slave does not answer */
        CHECK_EC_ERROR_CODE_EQUAL(EC_E_TIMEOUT, oSpy.WaitForTracedNotification(EC_NOTIFY_MBOXRCV, 5000));

        /* enable ProcessMbx at slave */
        oMbxProcessCtrlDesc.bProcessMbxEnabled = EC_TRUE; /* enable processing to get response from slave */
        dwRes = esIoCtl(oTestApplication.GetSimulatorId(), EC_IOCTL_SIMULATOR_SET_MBX_PROCESS_CTL,
            &oMbxProcessCtrlDesc, sizeof(EC_T_SIMULATOR_MBX_PROCESS_CTL_DESC), EC_NULL, 0, EC_NULL);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }

        /* wait until transfer finished */
        CHECK_NOERROR(oMbxTfer.WaitForMbxTfer(eMbxTferStatus_TferDone, 5000));
        CHECK_NOERROR(pMbxTfer->dwErrorCode);
    }

Exit:
    CHECK_NOERROR(dwRes);
}

TEST(ApiMailbox, DOC_FoeUploadTimeoutFoeReadExampleProcessMbxDisabled)
{
    CEcSimulatorSilTestApplication oTestApplication;
    EC_T_DWORD dwRes = EC_E_ERROR;
    EC_T_WORD wSlaveAddress = 1004; /* UnitTestsTiny EL4132 */

    oTestApplication.setup();
    SetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms, eCnfType_Filename, oTestApplication.GetEniFileName("Tiny"));
    oTestApplication.SetupMaster(GetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms), eEcatState_PREOP);

    CNotifySpy oSpy(&oTestApplication);
    oSpy.StartTrace(EC_NOTIFY_MBOXRCV);

    EC_T_MBXTFER* pMbxTfer = EC_NULL;
    CEmMbxTfer oMbxTfer(oTestApplication.GetMasterId(), oSpy.GetClientId());
    oMbxTfer.SetApp(&oTestApplication);
    pMbxTfer = oMbxTfer.Create(512);
    CHECK(EC_NULL != pMbxTfer);
    OsMemset(pMbxTfer->pbyMbxTferData, 0xAB, pMbxTfer->dwDataLen);

    {
        /* disable ProcessMbx at slave */
        EC_T_SIMULATOR_MBX_PROCESS_CTL_DESC oMbxProcessCtrlDesc;
        oMbxProcessCtrlDesc.wCfgFixedAddress = wSlaveAddress;
        oMbxProcessCtrlDesc.bReadMbxOutEnabled = EC_TRUE; /* slave reads MAILBOXOUT (SM0) */
        oMbxProcessCtrlDesc.bProcessMbxEnabled = EC_FALSE; /* disable processing at slave for transfer timeout */
        dwRes = esIoCtl(oTestApplication.GetSimulatorId(), EC_IOCTL_SIMULATOR_SET_MBX_PROCESS_CTL,
            &oMbxProcessCtrlDesc, sizeof(EC_T_SIMULATOR_MBX_PROCESS_CTL_DESC), EC_NULL, 0, EC_NULL);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }

        dwRes = emFoeDownloadReq(oTestApplication.GetMasterId(), pMbxTfer, emGetSlaveId(oTestApplication.GetMasterId(), wSlaveAddress), (EC_T_CHAR*)"test.dat", (EC_T_DWORD)OsStrlen((EC_T_CHAR*)"test.dat"), 0, 1000);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }

        /* slave does not answer so transfer will timeout */
        oMbxTfer.WaitForMbxTfer(eMbxTferStatus_TferDone, 5000);
        CHECK_EC_ERROR_CODE_EQUAL(EC_E_TIMEOUT, pMbxTfer->dwErrorCode);
    }

Exit:
    CHECK_NOERROR(dwRes);
}

TEST(ApiMailbox, DOC_FoeUploadTimeoutFoeReadExampleReadMbxOutDisabled)
{
    CEcSimulatorSilTestApplication oTestApplication;
    EC_T_DWORD dwRes = EC_E_ERROR;
    EC_T_WORD wSlaveAddress = 1004; /* UnitTestsTiny EL4132 */

    oTestApplication.setup();
    SetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms, eCnfType_Filename, oTestApplication.GetEniFileName("Tiny"));
    oTestApplication.SetupMaster(GetEcLinkParmsSimulatorConfiguration(&oTestApplication.m_oLinkParms), eEcatState_PREOP);

    CNotifySpy oSpy(&oTestApplication);
    oSpy.StartTrace(EC_NOTIFY_MBOXRCV);

    EC_T_MBXTFER* pMbxTfer = EC_NULL;
    CEmMbxTfer oMbxTfer(oTestApplication.GetMasterId(), oSpy.GetClientId());
    oMbxTfer.SetApp(&oTestApplication);
    pMbxTfer = oMbxTfer.Create(512);
    CHECK(EC_NULL != pMbxTfer);
    OsMemset(pMbxTfer->pbyMbxTferData, 0xAB, pMbxTfer->dwDataLen);

    {
        /* disable ProcessMbx at slave */
        EC_T_SIMULATOR_MBX_PROCESS_CTL_DESC oMbxProcessCtrlDesc;
        oMbxProcessCtrlDesc.wCfgFixedAddress = wSlaveAddress;
        oMbxProcessCtrlDesc.bReadMbxOutEnabled = EC_FALSE; /* disable slave MAILBOXOUT (SM0) reading */
        oMbxProcessCtrlDesc.bProcessMbxEnabled = EC_TRUE;
        dwRes = esIoCtl(oTestApplication.GetSimulatorId(), EC_IOCTL_SIMULATOR_SET_MBX_PROCESS_CTL,
            &oMbxProcessCtrlDesc, sizeof(EC_T_SIMULATOR_MBX_PROCESS_CTL_DESC), EC_NULL, 0, EC_NULL);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }

        dwRes = emFoeDownloadReq(oTestApplication.GetMasterId(), pMbxTfer, emGetSlaveId(oTestApplication.GetMasterId(), wSlaveAddress), (EC_T_CHAR*)"test.dat", (EC_T_DWORD)OsStrlen((EC_T_CHAR*)"test.dat"), 0, 1000);
        if (dwRes != EC_E_NOERROR)
        {
            goto Exit;
        }

        /* slave does not answer so transfer will timeout */
        oMbxTfer.WaitForMbxTfer(eMbxTferStatus_TferDone, 5000);
        CHECK_EC_ERROR_CODE_EQUAL(EC_E_TIMEOUT, pMbxTfer->dwErrorCode);
    }

Exit:
    CHECK_NOERROR(dwRes);
}

} /* namespace FoE */

/* ----------------- VoE ----------------- */
namespace VoE
{

namespace SimulatorVoeReceiveCallbackExample
{
/** DocumentationSnippetsSimulatorVoeReceiveCallbackExampleContextType */
#define MYAPP_VOE_BUFFER_SIZE (512)
typedef struct
{
    EC_T_BYTE  abyVoeBuf[MYAPP_VOE_BUFFER_SIZE];
    EC_T_DWORD dwVoeBufLen;
    EC_T_VOID* pvEvent;

    /* ... */
} T_MY_CONTEXT;
/** DocumentationSnippetsSimulatorVoeReceiveCallbackExampleContextType */

/** DocumentationSnippetsSimulatorVoeReceiveCallbackExampleHandler */
EC_T_BYTE EC_FNCALL myAppVoeReceiveCallback(
    EC_T_VOID* pvContext, EC_T_DWORD /* dwSimulatorId */,
    EC_T_WORD /* wCfgFixedAddress VoE receiver address, e.g. 1001 */,
    EC_T_WORD /* wSrcFixedAddress VoE sender address, 0: Master */,
    EC_T_VOID* pvData, EC_T_DWORD dwDataLen)
{
    T_MY_CONTEXT* poContext = (T_MY_CONTEXT*)pvContext;

    OsMemcpy(poContext->abyVoeBuf, pvData, EC_AT_MOST(MYAPP_VOE_BUFFER_SIZE, dwDataLen));
    poContext->dwVoeBufLen = dwDataLen;

    /* No EC-Simulator APIs may be issued from within the callback context.
       Signalize VoE data received for deferred processing in other thread. */
    OsSetEvent(poContext->pvEvent);

    return 0;
}
/** DocumentationSnippetsSimulatorVoeReceiveCallbackExampleHandler */

static EC_INLINESTART EC_T_DWORD SimulatorSnippetsVoeReceiveCallbackExample(EC_T_DWORD dwMasterId, EC_T_DWORD dwSimulatorId)
{
    /** DocumentationSnippetsSimulatorVoeReceiveCallbackExampleTransfer */
    EC_T_DWORD dwRes = EC_E_ERROR;
    EC_T_DWORD dwRetVal = EC_E_ERROR;

#define MYAPP_VOE_SEND_BUF_LEN sizeof(EC_T_DWORD)
    EC_T_BYTE abyVoeSendBuf[MYAPP_VOE_SEND_BUF_LEN];
    OsMemset(abyVoeSendBuf, 0, MYAPP_VOE_SEND_BUF_LEN);

    T_MY_CONTEXT oContext;
    OsMemset(&oContext, 0, sizeof(T_MY_CONTEXT));
    oContext.pvEvent = OsCreateEvent();
    if (EC_NULL == oContext.pvEvent)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "OsCreateEvent failed\n"));
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }

    /* EC-Simulator: register VoE handler */
    dwRes = esSetVoeReceiveCallback(dwSimulatorId, 1001, myAppVoeReceiveCallback, &oContext);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "esSetVoeReceiveCallback failed: %s (0x%lx))\n", esGetText(dwSimulatorId, dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* EC-Master: set PREOP state */
    dwRes = emSetMasterState(dwMasterId, 30000, eEcatState_PREOP);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emSetMasterState failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* send VoE to slave */
    EC_SET_FRM_DWORD(abyVoeSendBuf, 0x12345678);
    dwRes = emVoeWrite(dwMasterId, emGetSlaveId(dwMasterId, 1001), abyVoeSendBuf, MYAPP_VOE_SEND_BUF_LEN, 5000);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emVoeWrite failed: %s (0x%lx))\n", ecatGetText(dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    /* wait for slave received data in callback */
    dwRes = OsWaitForEvent(oContext.pvEvent, 5000);
    if (dwRes != EC_E_NOERROR)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "OsWaitForEvent failed: %s (0x%lx))\n", esGetText(dwSimulatorId, dwRes), dwRes));
        dwRetVal = dwRes;
        goto Exit;
    }

    dwRetVal = EC_E_NOERROR;
Exit:
    SafeOsDeleteEvent(oContext.pvEvent);
    /** DocumentationSnippetsSimulatorVoeReceiveCallbackExampleTransfer */

    CHECK_DWORD_EQUAL(0x12345678, EC_GET_FRM_DWORD(oContext.abyVoeBuf));
    CHECK_DWORD_EQUAL(MYAPP_VOE_SEND_BUF_LEN, oContext.dwVoeBufLen);

    return dwRetVal;
} EC_INLINESTOP

} /* namespace SimulatorVoeReceiveCallbackExample */

TEST_GROUP(SimulatorVoeReceiveCallbackExample)
{
};
TEST(SimulatorVoeReceiveCallbackExample, DOC_VoeReceiveExample)
{
    CEcSimulatorSilTestApplication oTestApplication;
    SimpleString oExi = GetTestsDataFilepath("Tests/Data/EcSimulator/T9279EXI.xml");
    oTestApplication.SetupMaster((EC_T_CHAR*)oExi.asCharString());

    CHECK_NOERROR(SimulatorVoeReceiveCallbackExample::SimulatorSnippetsVoeReceiveCallbackExample(oTestApplication.GetMasterId(), oTestApplication.GetSimulatorId()));
    CHECK_DWORD_IN_RANGE(1, MYAPP_VOE_BUFFER_SIZE, EC_LODWORD(MYAPP_VOE_SEND_BUF_LEN));
    // CHECK_DWORD_EQUAL(0x12345678, EC_GET_FRM_DWORD(oContext.abyVoeBuf));
    // CHECK_DWORD_EQUAL(MYAPP_VOE_SEND_BUF_LEN, oContext.dwVoeBufLen);
}

} /* namespace VoE */

} } /* namespace EcSimulatorTests::DocumentationSnippets */

#endif /* INC_DOC_ECSIMULATOR_SNIPPETS_API_MAILBOX */
