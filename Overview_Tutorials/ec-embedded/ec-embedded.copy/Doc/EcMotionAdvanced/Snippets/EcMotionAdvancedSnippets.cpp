/*------------------------------------------------------------------------------
 * EcMotionAdvancedSnippets.cpp
 * Copyright    acontis technologies GmbH, Franz-Beer-Strasse 98, 88250 Weingarten, Germany
 * Response     Frank Martin
 * Description  Example code for documentation
 * ---------------------------------------------------------------------------*/

#include "stdafx.h"

#define INSTANCE_DEFAULT                    0

TEST_GROUP(DocumentationSnippets)
{
    TEST_SETUP()
    {
    }
    TEST_TEARDOWN()
    {
    }
};

IGNORE_TEST(DocumentationSnippets, mcInit)
{
    MC_T_INIT_PARMS oMcInitParms;
    EC_T_DWORD dwRetVal;
    OsMemset(&oMcInitParms, 0, sizeof(MC_T_INIT_PARMS));
    oMcInitParms.dwSignature = MC_SIGNATURE;
    oMcInitParms.dwSize = sizeof(MC_T_INIT_PARMS);
    oMcInitParms.dwMaxMotionAxes = 4;
    dwRetVal = mcInit(INSTANCE_DEFAULT, oMcInitParms);
    /* IGNORE_TEST(DocumentationSnippets, mcInit) */
}

IGNORE_TEST(DocumentationSnippets, mcSetEthercatApiFunctions)
{
    MC_T_INIT_ECAT_PARMS oMcInitEcatParms;
    EC_T_DWORD dwRetVal;
    OsMemset(&oMcInitEcatParms, 0, sizeof(MC_T_INIT_ECAT_PARMS));
    oMcInitEcatParms.pfnGetSlaveState = emGetSlaveState;
    dwRetVal = mcSetEthercatApiFunctions(oMcInitEcatParms);
    /* IGNORE_TEST(DocumentationSnippets, mcSetEthercatApiFunctions) */
}

IGNORE_TEST(DocumentationSnippets, mcDeinit)
{
    EC_T_DWORD dwRetVal;
    dwRetVal = mcDeinit(INSTANCE_DEFAULT);
    /* IGNORE_TEST(DocumentationSnippets, mcDeinit) */
}

IGNORE_TEST(DocumentationSnippets, mcCreateVirtualAxis)
{
    AxisRef* S_pAxis = EC_NULL;
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    MC_T_AXIS_PARMS oAxisParms;
    OsMemset(&oAxisParms, 0, sizeof(MC_T_AXIS_PARMS));
    oAxisParms.dwCycleTime = 1000;
    oAxisParms.dwIncPerMM = 10000;
    oAxisParms.dwMaxMoveCmds = 8;
    dwRetVal = mcCreateVirtualAxis(oAxisParms, S_pAxis);
    /* IGNORE_TEST(DocumentationSnippets, mcCreateVirtualAxis) */
}

IGNORE_TEST(DocumentationSnippets, mcCreateDS402Axis)
{
    AxisRef* S_pAxis = EC_NULL;
    EC_T_DWORD dwRetVal = EC_E_ERROR;
    MC_T_AXIS_PARMS oAxisParms;
    MC_T_AXIS_IO_ENDPOINT oAxisIo;
    MC_T_AXIS_ECAT_PARMS oAxisEcatParms;
    OsMemset(&oAxisParms, 0, sizeof(MC_T_AXIS_PARMS));
    OsMemset(&oAxisIo, 0, sizeof(MC_T_AXIS_IO_ENDPOINT));
    OsMemset(&oAxisEcatParms, 0, sizeof(MC_T_AXIS_ECAT_PARMS));

    oAxisParms.dwCycleTime = 1000;
    oAxisParms.dwIncPerMM = 10000;
    oAxisParms.dwMaxMoveCmds = 8;

    oAxisIo.dwBitOffsStatusWord = 0; /* Determine offset by emGetSlaveInpVarByObjectEx for example */
    oAxisIo.dwBitSizeStatusWord = 8 * sizeof(EC_T_WORD);
    oAxisIo.dwBitOffsActualPosition = 16; /* Determine offset by emGetSlaveInpVarByObjectEx for example */
    oAxisIo.dwBitSizeActualPosition = 8 * sizeof(EC_T_SDWORD);
    oAxisIo.dwBitOffsControlWord = 0; /* Determine offset by emGetSlaveOutpVarByObjectEx for example */
    oAxisIo.dwBitSizeControlWord = 8 * sizeof(EC_T_WORD);
    oAxisIo.dwBitOffsTargetPosition = 16; /* Determine offset by emGetSlaveOutpVarByObjectEx for example */
    oAxisIo.dwBitSizeTargetPosition = 8 * sizeof(EC_T_SDWORD);
    
    oAxisEcatParms.dwSlaveId = 1; /* Determine value by emGetCfgSlaveInfo for example */
    oAxisEcatParms.wStationAddress = 1001;
    oAxisEcatParms.wCoeIdxOpMode = 0x6060;
    oAxisEcatParms.wCoeSubIdxOpMode = 0;
    oAxisEcatParms.eOpMode = DRV_MODE_OP_CSP;

    dwRetVal = mcCreateDS402Axis(oAxisParms, oAxisIo, oAxisEcatParms, S_pAxis);
    /* IGNORE_TEST(DocumentationSnippets, mcCreateDS402Axis) */
}

IGNORE_TEST(DocumentationSnippets, CyclicCalls)
{
    EC_T_DWORD dwRes = EC_E_ERROR;
    EC_T_BYTE* pbyPdIn = ecatGetProcessImageInputPtr();
    EC_T_BYTE* pbyPdOut = ecatGetProcessImageOutputPtr();

    dwRes = mcRefreshAxisInputs(INSTANCE_DEFAULT, 0, pbyPdIn);

    /*
     * Implementation of the application.
     * E.g. call of motion function blocks McPower and McMoveRelative
     */

    dwRes = mcCyclicTask(INSTANCE_DEFAULT, 0);

    dwRes = mcRefreshAxisOutputs(INSTANCE_DEFAULT, 0, pbyPdOut);
    /* IGNORE_TEST(DocumentationSnippets, CyclicCalls) */
}

IGNORE_TEST(DocumentationSnippets, CallMCFB)
{
    AxisRef* S_pAxis = EC_NULL;
    /* declaration of motion control function block */
    McPower S_oMcPower;

    /* cyclic call within the application */
    S_oMcPower.Axis = S_pAxis;
    S_oMcPower.Enable = EC_TRUE;
    S_oMcPower();
    if (S_oMcPower.Error)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, 
            "Error 0x%x during power on of axis!", (EC_T_DWORD)S_oMcPower.ErrorID));
    }
    /* IGNORE_TEST(DocumentationSnippets, CallMCFB) */
}