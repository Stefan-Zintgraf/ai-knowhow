/*-----------------------------------------------------------------------------
 * EcDeviceDummy.cpp
 * Copyright                acontis technologies GmbH, Weingarten, Germany
 * Description              Link Layer driver example
 *---------------------------------------------------------------------------*/

/*-INCLUDES------------------------------------------------------------------*/
#include "EcDeviceDummy.h"

/*-FUNCTION DECLARATIONS-----------------------------------------------------*/
static EC_T_LINKSTATUS EcLinkGetStatus(EC_T_VOID* pvInstance);
static EC_T_DWORD EcLinkClose(EC_T_VOID* pvInstance);
static EC_T_VOID  EcLinkFreeSendFrame(EC_T_VOID* pvInstance, EC_T_LINK_FRAMEDESC* pLinkFrameDesc);

/*-LOCAL VARIABLES-----------------------------------------------------------*/
static PT_DUMMY_INTERNAL    S_oOpenInstanceRoot  = EC_NULL;
static EC_T_INT             S_nOpenedInstances   = 0;

/*-HELPER FUNCTIONS----------------------------------------------------------*/

/*****************************************************************************/
/**
 * \brief Appends an adapter to the list of opened instances.
 *
 * \return #EC_TRUE
 */
static EC_T_BOOL ListAddOI(
    PT_DUMMY_INTERNAL poAdapter /**< [in] Instance handle */
)
{
    PT_DUMMY_INTERNAL oCur = S_oOpenInstanceRoot;
    if (EC_NULL == oCur)
    {
        S_oOpenInstanceRoot = poAdapter;
        S_oOpenInstanceRoot->pPrev = S_oOpenInstanceRoot->pNext = EC_NULL;
    }
    else
    {
        while (EC_NULL != oCur->pNext)
        {
            oCur = oCur->pNext;
        }

        oCur->pNext = poAdapter;
        poAdapter->pPrev = oCur;
        poAdapter->pNext = EC_NULL;
    }

    return EC_TRUE;
}

/*****************************************************************************/
/**
 * \brief Removes an adapter from the list of opened instances.
 *
 * \return #EC_TRUE
 */
static EC_T_BOOL ListRmOI(
    PT_DUMMY_INTERNAL poAdapter /**< [in] Instance handle */
)
{
    if (S_oOpenInstanceRoot == poAdapter)
    {
        S_oOpenInstanceRoot = poAdapter->pNext;
    }
    if (EC_NULL != poAdapter->pPrev)
    {
        poAdapter->pPrev->pNext = poAdapter->pNext;
    }
    if (EC_NULL != poAdapter->pNext)
    {
        poAdapter->pNext->pPrev = poAdapter->pPrev;
    }

    poAdapter->pPrev = EC_NULL;
    poAdapter->pNext = EC_NULL;

    return EC_TRUE;
}

/*****************************************************************************/
/**
 * \brief Search the adapter with given memory register base address in the list of opened instances.
 *
 * \return Pointer to the opened instance or #EC_NULL if not found
 */
static PT_DUMMY_INTERNAL ListSeekOI(EC_T_DWORD dwMemRegisterBase)
{
    PT_DUMMY_INTERNAL oCur = S_oOpenInstanceRoot;

    while ((EC_NULL != oCur) && (dwMemRegisterBase != oCur->dwMemRegisterBase))
    {
        oCur = oCur->pNext;
    }

    return oCur;
}

/*****************************************************************************/
/**
 * \brief Map BAR registers.
 *
 * \return #EC_TRUE on success, #EC_FALSE otherwise.
 */
static EC_T_BOOL MapMemory(
    PT_DUMMY_INTERNAL pAdapter /**< [in] Instance handle */
)
{
    EC_T_BOOL           bRet    = EC_TRUE;

    EC_UNREFPARM(pAdapter);

    /* map adapter memory here */
    /* <= change here */

    return bRet;
}

/*****************************************************************************/
/**
 * \brief Unmap and free BAR registers.
 *
 * \return #EC_TRUE on success, #EC_FALSE otherwise.
 */
static EC_T_BOOL UnmapMemory(
    PT_DUMMY_INTERNAL pAdapter /**< [in] Instance handle */
)
{
    EC_T_BOOL   bRet = EC_TRUE;

    EC_UNREFPARM(pAdapter);

    /* unmap adapter memory here */
    /* <= change here */

    return bRet;
}

/*****************************************************************************/
/**
 * \brief Open Link Layer instance.
 *
 * \return #EC_E_NOERROR or error code.
 */
static EC_T_DWORD EcLinkOpen(
    EC_T_VOID*                  pvLinkParms             /**< [in]  Link parameters */,
    EC_T_RECEIVEFRAMECALLBACK   pfReceiveFrameCallback  /**< [in]  Pointer to RX callback function */,
    EC_T_LINK_NOTIFY            pfLinkNotifyCallback    /**< [in]  Pointer to notification callback function */,
    EC_T_VOID*                  pvContext               /**< [in]  Caller context, to be used in callback functions */,
    EC_T_VOID**                 ppvInstance             /**< [out] Instance handle */
    )
{
#if (defined INCLUDE_LOG_MESSAGES)
#undef  pEcLogParmsLL
#define pEcLogParmsLL pEcLogParmsLLOpen
#endif
    EC_T_DWORD              dwRetVal = EC_E_ERROR;
    EC_T_LINK_PARMS_DUMMY*  pLinkParmsAdapter = (EC_T_LINK_PARMS_DUMMY*)pvLinkParms;
    EC_T_DWORD              dwMemRegisterBase = 0;

    PT_DUMMY_INTERNAL       pAdapter = EC_NULL;

    EC_UNREFPARM(pfLinkNotifyCallback);

    if (EC_NULL == pLinkParmsAdapter)
    {
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }
#if !(defined INSTRUMENT_LL)
#if EC_VERSION_BUILD != 99
    EcLogMsg(EC_LOG_LEVEL_ANY, (pEcLogContext, EC_LOG_LEVEL_ANY, "emllDummy(0x%08X): V%s for %s %s\n", pLinkParmsAdapter->linkParms.dwInstance, EC_FILEVERSIONSTR, EC_PLATFORMSTR, EC_COPYRIGHT));
#else
    EcLogMsg(EC_LOG_LEVEL_ANY, (pEcLogContext, EC_LOG_LEVEL_ANY, "emllDummy(0x%08X): V%s (%s %s) for %s %s\n", pLinkParmsAdapter->linkParms.dwInstance, EC_FILEVERSIONSTR, __DATE__, __TIME__, EC_PLATFORMSTR, EC_COPYRIGHT));
#endif
#endif
    /* EC_T_LINK_PARMS_... must start with EC_T_LINK_PARMS! */
    LinkOsDbgAssert((EC_T_BYTE*)&pLinkParmsAdapter->linkParms - (EC_T_BYTE*)pLinkParmsAdapter == 0);

    if (EC_NULL == ppvInstance)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "EcLinkOpen(): Instance handle NULL-pointer!\n"));
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }
    *ppvInstance = EC_NULL;

    /* check signature */
    if (pLinkParmsAdapter->linkParms.dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Dummy-EcLinkOpen(): Invalid Configuration for Dummy Link Layer\n"));
        *ppvInstance = EC_NULL;
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    if (EC_NULL == ppvInstance)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Dummy-EcLinkOpen(): No Space for Driver Instance handle provided\n"));
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    /* initialize PCI here (if needed) */
    /* <= change here */

    /* check whether the instance is alraedy in use */
    if (EC_NULL != ListSeekOI(dwMemRegisterBase))
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Dummy-EcLinkOpen(): Instance already in use!\n"));
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    /* register receive callback function if needed */
    if ((EC_NULL == pfReceiveFrameCallback) && (EcLinkMode_INTERRUPT == pLinkParmsAdapter->linkParms.eLinkMode))
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Dummy-EcLinkOpen(): Missing receive frame callback\n"));
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    /* create new instance */
    pAdapter = (PT_DUMMY_INTERNAL)LinkOsMalloc(sizeof(T_DUMMY_INTERNAL));
    if (EC_NULL == pAdapter)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Dummy-EcLinkOpen(): Error allocating memory\n"));
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }
    LinkOsMemset(pAdapter, 0, sizeof(T_DUMMY_INTERNAL));
    LinkOsMemcpy(&(pAdapter->oInitParms), pLinkParmsAdapter, sizeof(EC_T_LINK_PARMS_DUMMY));
    pAdapter->dwSignature = EC_LINK_PARMS_SIGNATURE_DUMMY;

    /* create context */
    dwRetVal = LinkOsCreateContext((EC_T_VOID*)&pLinkParmsAdapter->linkParms, &pAdapter->pvLinkOsContext);
    if (EC_E_NOERROR != dwRetVal)
    {
        goto Exit;
    }

    /* do initialization here */
    if (!MapMemory(pAdapter))
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Dummy-EcLinkOpen(): Error Mapping memory\n"));
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }

    /* Example, allocate internal memory */
    pAdapter->pbyIntBuffer = (EC_T_BYTE*)LinkOsMalloc(1536);
    pAdapter->dwFrameLen = 0;
    pAdapter->bNewData = EC_FALSE;
    if (EC_NULL == pAdapter->pbyIntBuffer)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "Dummy-EcLinkOpen(): Error allocating memory\n"));
        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }

    /* configure new instance */
    pAdapter->pfReceiveFrameCallback = pfReceiveFrameCallback;
    pAdapter->pvCallbackContext = pvContext;

    /* Interrupt handling */
    /* <= change here */

    /* set up Device Control registers (incl. Device reset) */
    /* <= change here */

    /* initialize DMA control */
    /* <= change here */

    /* now configure DMA space */

    /* STOP NIC RX & TX */
    /* <= change here */
    /*
    dwRes = XXXX_StopReceiver(pAdapter);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }
    dwRes = XXXX_StopTransceiver(pAdapter);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }
    */

    /* initialize DMA Memory */
    /* <= change here */
    /*
    dwRes = XXXX_InitDmaMemory(pAdapter);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }
    */

    /* startup the receiver */
    /* <= change here */
    /*
    dwRes = XXXX_StartReceiver(pAdapter);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }
    */

    /* startup the transceiver */
    /* <= change here */
    /*
    dwRes = XXXX_StartTransceiver(pAdapter);
    if (EC_E_NOERROR != dwRes)
    {
        dwRetVal = dwRes;
        goto Exit;
    }
    */

    /* enqueue Adapter */
    ListAddOI(pAdapter);

    /* no errors */
    dwRetVal = EC_E_NOERROR;

    /* increment instance counter */
    S_nOpenedInstances++;

    /* return Instance handle */
    *ppvInstance = pAdapter;

Exit:
    if ((EC_E_NOERROR != dwRetVal) && (EC_E_INVALIDSTATE != dwRetVal))
    {
        *ppvInstance = EC_NULL;

        if (EC_NULL != pAdapter)
        {
            EcLinkClose(pAdapter);
            pAdapter = EC_NULL;
        }
    }

    return dwRetVal;
}

/*****************************************************************************/
/**
 * \brief Close Link Layer instance.
 *
 * \return #EC_E_NOERROR or error code.
 */
static EC_T_DWORD EcLinkClose(
    EC_T_VOID* pvInstance /**< [in] Instance handle */
)
{
    PT_DUMMY_INTERNAL pAdapter = (PT_DUMMY_INTERNAL)pvInstance;

    /* check for Type Signature */
    if ((EC_NULL == pAdapter) || (pAdapter->dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY))
    {
        return EC_E_INVALIDPARM;
    }

    if (EcLinkMode_INTERRUPT == pAdapter->oInitParms.linkParms.eLinkMode)
    {
        /* <= change here */
        /* i.e. Disable and remove interrupt handler */
    }

    /* stop adapter */
    /* <= change here */
    /*
    XXXX_StopReceiver(pAdapter);
    XXXX_StopTransceiver(pAdapter);
    */

    /* reset adapter */
    /* <= change here */
    /*
    XXXX_Reset(pAdapter);
    */

    /* Free memory used for all descriptors */
    /* <= change here */

    /* unmap memory */
    /* <= change here */
    /* Example */
    UnmapMemory(pAdapter);

    /* example */
    /* free internal memory allocated in EcLinkOpen() */
    LinkOsFree(pAdapter->pbyIntBuffer);

    /* release context */
    LinkOsReleaseContext(pAdapter->pvLinkOsContext);

    /* remove adapter from the list */
    ListRmOI(pAdapter);

    /* decrease counter */
    S_nOpenedInstances--;

    /* Free memory */
    LinkOsFree(pAdapter);

    return EC_E_NOERROR;
}

/*****************************************************************************/
/**
 * \brief Determine link speed.
 *
 * \return #EC_E_NOERROR on success or #EC_E_INVALIDDATA if speed cannot be determined.
 */
static EC_T_DWORD EcLinkGetSpeed(
    EC_T_VOID*  pvInstance /**< [in]  Instance handle */,
    EC_T_DWORD* pdwSpeed   /**< [out] Current link speed */
)
{
    PT_DUMMY_INTERNAL       pAdapter    = (PT_DUMMY_INTERNAL)pvInstance;
    EC_T_DWORD              dwRetVal    = EC_E_ERROR;
    EC_T_DWORD              dwSpeed     = 0;
    EC_T_BYTE               byPhySpeed  = 0;

    /* check for Type Signature */
    if ((EC_NULL == pAdapter) || (pAdapter->dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY))
    {
        return EC_E_INVALIDPARM;
    }

    /* check parameters */
    if (EC_NULL == pdwSpeed)
    {
        return EC_E_INVALIDPARM;
    }

    /* get speed from HW */
    /* <= change here */
    /* Example
    dwRes = XXXX_GetPhySpeed(pAdapter, &byPhySpeed);
    if (EC_E_NOERROR != dwRes)
    {
        dwSpeed = dwRes;
        goto Exit;
    }
    */

    /* mask out unnecessary */
    switch (byPhySpeed)
    {
    case 0:     dwRetVal = EC_E_INVALIDDATA; goto Exit; /* no break */
    case 1:     dwSpeed = 10;               break;
    case 2:     dwSpeed = 100;              break;
    case 3:     dwSpeed = 1000;             break;
    default:    dwRetVal = EC_E_INVALIDDATA; goto Exit; /* no break */
    }

    /* no error */
    dwRetVal = EC_E_NOERROR;
Exit:
    *pdwSpeed = dwSpeed;
    return dwRetVal;
}

/*****************************************************************************/
/**
 * \brief Determine link mode
 *
 * \return #EcLinkMode_POLLING or EcLinkMode_INTERRUPT
 */
static EC_T_LINKMODE EcLinkGetMode(
    EC_T_VOID* pvInstance /**< [in] Instance handle */
)
{
    PT_DUMMY_INTERNAL pAdapter = (PT_DUMMY_INTERNAL)pvInstance;

    /* check for Type Signature */
    if ((EC_NULL == pAdapter) || (pAdapter->dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY))
    {
        return EcLinkMode_UNDEFINED;
    }

    return pAdapter->oInitParms.linkParms.eLinkMode;
}

/*****************************************************************************/
/**
 * \brief Determine current link status.
*
* \return Current link status.
*/
static EC_T_LINKSTATUS EcLinkGetStatus(
    EC_T_VOID* pvInstance /**< [in] Instance handle */
)
{
    PT_DUMMY_INTERNAL   pAdapter    = (PT_DUMMY_INTERNAL)pvInstance;
    EC_T_LINKSTATUS     oStatus     = eLinkStatus_UNDEFINED;

    /* check for Type Signature */
    if ((EC_NULL == pAdapter) || (pAdapter->dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY))
    {
        return eLinkStatus_UNDEFINED;
    }

    /* get link status from Hardware */
    /* <= change here */
    /*
    if (EC_E_NOERROR != XXXX_GetStatusReg(pAdapter, &statusreg))
    {
        goto Exit;
    }
    */

    /* <= change here */
    /*
    oStatus = eLinkStatus_HALFDUPLEX;
    oStatus = eLinkStatus_DISCONNECTED;
    */
    oStatus = eLinkStatus_OK;

    return oStatus;
}

/*****************************************************************************/
/**
 * \brief Determine link layer MAC address
 *
 * \return #EC_E_NOERROR or error code.
 */
static EC_T_DWORD EcLinkGetEthernetAddress(
    EC_T_VOID* pvInstance               /**< [in]  Instance handle */,
    EC_T_BYTE* pbyEthernetMacAddress    /**< [out] Ethernet MAC address */
)
{
    PT_DUMMY_INTERNAL   pAdapter    = (PT_DUMMY_INTERNAL)pvInstance;
    EC_T_DWORD          dwRetVal    = EC_E_ERROR;
    EC_T_BYTE           abyMac[6]   = {0x00,0x01,0x02,0x03,0x04,0x05};

    /* check Type Signature */
    if ((EC_NULL == pAdapter) || (pAdapter->dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY))
    {
        return EC_E_INVALIDPARM;
    }

    /* check parameters */
    if (EC_NULL == pbyEthernetMacAddress)
    {
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    /* evaluate MAC address and return it */
    /* <= change here */

    LinkOsMemcpy(pbyEthernetMacAddress, abyMac, 6);

    /* no error */
    dwRetVal = EC_E_NOERROR;

Exit:
    return dwRetVal;
}

/*****************************************************************************/
/**
 * \brief Allocate a frame buffer used for send
 *
 *    If the link layer doesn't support frame allocation, this function must return
 *    EC_E_NOTSUPPORTED
 *
 * \return #EC_E_NOERROR or error code.
 */
static EC_T_DWORD EcLinkAllocSendFrame(
    EC_T_VOID*           pvInstance     /**< [in]     Instance handle */,
    EC_T_LINK_FRAMEDESC* pLinkFrameDesc /**< [in/out] Link frame descriptor */,
    EC_T_DWORD           dwSize         /**< [in]     Frame size to allocate */
)
{
    EC_T_DWORD          dwRetVal    = EC_E_ERROR;
    PT_DUMMY_INTERNAL   pAdapter    = (PT_DUMMY_INTERNAL)pvInstance;

#if (defined INCLUDE_LICENSE_SUPPORT)
/* PREPROCESSOR MACRO BLOCK NEEDED FOR BUILD PROCESS */
#endif /* INCLUDE_LICENSE_SUPPORT */

    /* check for Type Signature */
    if ((EC_NULL == pAdapter) || (pAdapter->dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY))
    {
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    if (eLinkStatus_DISCONNECTED == EcLinkGetStatus(pvInstance))
    {
        dwRetVal = EC_E_INVALIDSTATE;
        goto Exit;
    }

    /* estimate how much DMA memory to allocate, reserve and return it */
    /* <= change here */

    /* Example */
    pLinkFrameDesc->pbyFrame = (EC_T_BYTE*)LinkOsMalloc(dwSize);
    pLinkFrameDesc->dwSize = dwSize;

    if (EC_NULL == pLinkFrameDesc->pbyFrame)
    {
        pLinkFrameDesc->dwSize = 0;

        dwRetVal = EC_E_NOMEMORY;
        goto Exit;
    }

    dwRetVal = EC_E_NOERROR;
Exit:
    return dwRetVal;
}

/*****************************************************************************/
/**
 * \brief Send frame.
 *
 * Queue frame for sending and set frame send timestamp (pLinkFrameDesc->pfnTimeStamp). 
 * 
 * \return #EC_E_NOERROR or error code.
 */
static EC_T_DWORD EcLinkSendFrame(
    EC_T_VOID*           pvInstance     /**< [in] Instance handle */,
    EC_T_LINK_FRAMEDESC* pLinkFrameDesc /**< [in] Link frame descriptor */
)
{
    EC_T_DWORD              dwRetVal    = EC_E_ERROR;
    PT_DUMMY_INTERNAL       pAdapter    = (PT_DUMMY_INTERNAL)pvInstance;

    if ((EC_NULL == pAdapter) || (pAdapter->dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY))
    {
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    /* transmit Buffer. If alloc supported, check if give descriptor was allocated previously */
    /* <= change here */

    /* now really send */
    /* <= change here */

    /* Example */
    LinkOsMemcpy(pAdapter->pbyIntBuffer, pLinkFrameDesc->pbyFrame, pLinkFrameDesc->dwSize);
    pAdapter->dwFrameLen = pLinkFrameDesc->dwSize;
    pAdapter->bNewData = EC_TRUE;

    /* set frame send timestamp */
    if (EC_NULL != pLinkFrameDesc->pfnTimeStamp)
    {
        *pLinkFrameDesc->pdwLastTSResult    =  pLinkFrameDesc->pfnTimeStamp(pLinkFrameDesc->pvTimeStampCtxt, pLinkFrameDesc->pdwTimeStampLo);
        *pLinkFrameDesc->pdwTimeStampPostLo = *pLinkFrameDesc->pdwTimeStampLo;
    }

    /* no error */
    dwRetVal = EC_E_NOERROR;
Exit:
    return dwRetVal;
}

/*****************************************************************************/
/**
 * \brief Send data frame and free the frame buffer. This function must be
 *        supported if EcLinkAllocSendFrame() is supported.
 *
 * \return #EC_E_NOERROR or error code.
 */
static EC_T_DWORD EcLinkSendAndFreeFrame(
    EC_T_VOID*           pvInstance      /**< [in] Instance handle */,
    EC_T_LINK_FRAMEDESC* pLinkFrameDesc  /**< [in] Link frame descriptor */
)
{
    EC_T_DWORD dwRetVal = EC_E_ERROR;

    /* <= change here */

    /* example */
    /* send frame */
    dwRetVal = EcLinkSendFrame(pvInstance, pLinkFrameDesc);
    /* Free frame memory, no error check in this case */
    EcLinkFreeSendFrame(pvInstance, pLinkFrameDesc);

    /* nothing to do */
    return dwRetVal;
}

/*****************************************************************************/
/**
 * \brief Poll for received frame. This function is called by the ethercat Master
 *        if the function EcLinkGetMode() returns EcLinkMode_POLLING
 *
 * \return #EC_E_NOERROR or error code.
 */
static EC_T_DWORD EcLinkRecvFrame(
    EC_T_VOID*           pvInstance      /**< [in] Instance handle */,
    EC_T_LINK_FRAMEDESC* pLinkFrameDesc  /**< [in] Link frame descriptor */
)
{
    EC_T_DWORD              dwRetVal    = EC_E_ERROR;
    PT_DUMMY_INTERNAL       pAdapter    = (PT_DUMMY_INTERNAL)pvInstance;

    /* check for Type Signature */
    if ((EC_NULL == pAdapter) || (pAdapter->dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY))
    {
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    if (EcLinkMode_INTERRUPT == pAdapter->oInitParms.linkParms.eLinkMode)
    {
        dwRetVal = EC_E_NOTSUPPORTED;
        goto Exit;
    }

    if (EC_NULL == pLinkFrameDesc)
    {
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    /* now rx single frame */
    /* <= change here */

    /* Example */
    /* Just an echo of the last frame sent */
    pLinkFrameDesc->dwSize = 0;
    if (pAdapter->bNewData)
    {
        pLinkFrameDesc->pbyFrame = pAdapter->pbyIntBuffer;
        pLinkFrameDesc->pbyFrame[17]++;
        pLinkFrameDesc->dwSize = pAdapter->dwFrameLen;
        pAdapter->bNewData = EC_FALSE;
    }

    dwRetVal = EC_E_NOERROR;

Exit:
    return dwRetVal;
}

/*****************************************************************************/
/**
 * \brief Release a frame buffer previously allocated with EcLinkAllocFrame().
 *
 * \return #EC_E_NOERROR or error code.
 */
static EC_T_VOID  EcLinkFreeSendFrame(
    EC_T_VOID*           pvInstance      /**< [in] Instance handle */,
    EC_T_LINK_FRAMEDESC* pLinkFrameDesc  /**< [in] Link frame descriptor */
)
{
    PT_DUMMY_INTERNAL pAdapter = (PT_DUMMY_INTERNAL)pvInstance;

    if ((EC_NULL == pAdapter) || (pAdapter->dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY))
    {
        goto Exit;
    }

    /* if given descriptor was allocated correctly and is not in use by Hardware free it */
    /* <= change here */

    /* Example */
    LinkOsFree(pLinkFrameDesc->pbyFrame);
    pLinkFrameDesc->pbyFrame = EC_NULL;
    pLinkFrameDesc->dwSize = 0;

    EC_UNREFPARM(pLinkFrameDesc);
Exit:
    return;
}

/*****************************************************************************/
/**
 * \brief Release a frame buffer given to the ethercat master through the receive
 *          callback function
 *
 * \return #EC_E_NOERROR or error code.
 */
static EC_T_VOID  EcLinkFreeRecvFrame(
    EC_T_VOID*           pvInstance      /**< [in] Instance handle */,
    EC_T_LINK_FRAMEDESC* pLinkFrameDesc  /**< [in] Link frame descriptor */
)
{
    PT_DUMMY_INTERNAL   pAdapter = (PT_DUMMY_INTERNAL)pvInstance;

    /* check for Type Signature */
    if ((EC_NULL == pAdapter) || (pAdapter->dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY))
    {
        goto Exit;
    }

    if (EC_NULL == pLinkFrameDesc)
    {
        goto Exit;
    }

    /* Free previously received Frame Descriptor */
    /* <= change here */
    /*XXXX_FreeRecvFrame(pAdapter, pLinkFrameDesc);*/

    /* Example */
    LinkOsDbgAssert(pLinkFrameDesc->pbyFrame == pAdapter->pbyIntBuffer);

Exit:
    return;
}

/*****************************************************************************/
/**
 * \brief Multi Purpose LinkLayer IOCTL
 *
 * \return #EC_E_NOERROR or error code.
 */
static EC_T_DWORD EcLinkIoCtl(
    EC_T_VOID*              pvInstance      /**< [in]  Instance handle */,
    EC_T_DWORD              dwCode          /**< [in]  Control code (EC_LINKIOCTL...) */,
    const EC_T_VOID* const  pbyInBuf,       /**< [in]  IOCTL input parameters */
    EC_T_DWORD              dwInBufSize,    /**< [in]  Size of IOCTL input parameters in bytes */
    EC_T_VOID* const        pbyOutBuf,      /**< [out] Buffer for IOCTL output */
    EC_T_DWORD              dwOutBufSize,   /**< [in]  Size of buffer at pbyOutBuf in bytes */
    EC_T_DWORD* const       pdwNumOutData   /**< [out] Amount of bytes written to pbyOutBuf by IOCTL. EC_NULL: amount not set by IOCTL. */
)
{
    EC_T_DWORD                  dwRetVal     = EC_E_ERROR;
    EC_T_DWORD                  dwRes        = EC_E_ERROR;
    EC_T_DWORD                  dwNumOutData = 0;
    PT_DUMMY_INTERNAL           pAdapter = (PT_DUMMY_INTERNAL)pvInstance;

    EC_UNREFPARM(pbyInBuf);
    EC_UNREFPARM(dwInBufSize);
    if ((EC_NULL == pAdapter) || (pAdapter->dwSignature != EC_LINK_PARMS_SIGNATURE_DUMMY))
    {
        dwRetVal = EC_E_INVALIDPARM;
        goto Exit;
    }

    /* fan out IOCTL functions */

    switch (dwCode)
    {
    case EC_LINKIOCTL_GET_ETHERNET_ADDRESS:
    {
        if ((EC_NULL == pbyOutBuf) || (dwOutBufSize < ETHERNET_ADDRESS_LEN))
        {
            dwRetVal = EC_E_INVALIDPARM;
            goto Exit;
        }

        dwRes = EcLinkGetEthernetAddress(pAdapter, (EC_T_BYTE*)pbyOutBuf);
        if (EC_E_NOERROR != dwRes)
        {
            dwRetVal = dwRes;
            goto Exit;
        }
        dwNumOutData = ETHERNET_ADDRESS_LEN;
    } break;

    default:
    {
        dwRetVal = EC_E_NOTSUPPORTED;
        goto Exit;
    } /* no break */
    }

    /* no error */
    if (EC_NULL != pdwNumOutData)
    {
        *pdwNumOutData = dwNumOutData;
    }
    dwRetVal = EC_E_NOERROR;
Exit:
    return dwRetVal;
}

/*****************************************************************************/
/**
 * \brief Register link layer driver.
 *
 * \return #EC_E_NOERROR or error code.
 */
ATEMLL_API EC_T_DWORD EC_API_FNCALL emllRegisterDummy(
    EC_T_LINK_DRV_DESC* pLinkDrvDesc        /**< [in,out] link layer driver descriptor */,
    EC_T_DWORD          dwLinkDrvDescSize   /**< [in]     size in bytes of link layer driver descriptor */
)
{
#if (defined INCLUDE_LOG_MESSAGES)
#undef  pEcLogParmsLL
#define pEcLogParmsLL pEcLogParmsLLRegister
#endif
    EC_T_DWORD  dwResult = EC_E_NOERROR;

    if (pLinkDrvDesc == EC_NULL)
    {
        dwResult = EC_E_INVALIDPARM;
        goto Exit;
    }
    if (pLinkDrvDesc->dwValidationPattern != LINK_LAYER_DRV_DESC_PATTERN)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emllRegisterDummy: invalid link layer driver descriptor pattern: 0x%x instead of 0x%x\n",
                  pLinkDrvDesc->dwValidationPattern, LINK_LAYER_DRV_DESC_PATTERN));
        dwResult = EC_E_INVALIDPARM;
        goto Exit;
    }

    /* check the size of the given link layer driver descriptor */
    if (dwLinkDrvDescSize != sizeof(EC_T_LINK_DRV_DESC))
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emllRegisterDummy: invalid link layer driver descriptor size: %d bytes instead of %d\n",
            dwLinkDrvDescSize, sizeof(EC_T_LINK_DRV_DESC)));
        dwResult = EC_E_INVALIDPARM;
        goto Exit;
    }

    /* check if the version of the interface is supported  */
    if (pLinkDrvDesc->dwInterfaceVersion != LINK_LAYER_DRV_DESC_VERSION)
    {
        EcLogMsg(EC_LOG_LEVEL_ERROR, (pEcLogContext, EC_LOG_LEVEL_ERROR, "emllRegisterDummy: invalid link layer driver descriptor version: 0x%x instead of 0x%x\n",
            pLinkDrvDesc->dwInterfaceVersion, LINK_LAYER_DRV_DESC_VERSION));
        dwResult = EC_E_INVALIDPARM;
        goto Exit;
    }

    pLinkDrvDesc->pfEcLinkOpen = EcLinkOpen;
    pLinkDrvDesc->pfEcLinkClose = EcLinkClose;
    pLinkDrvDesc->pfEcLinkSendFrame = EcLinkSendFrame;
    pLinkDrvDesc->pfEcLinkSendAndFreeFrame = EcLinkSendAndFreeFrame;
    pLinkDrvDesc->pfEcLinkRecvFrame = EcLinkRecvFrame;
    pLinkDrvDesc->pfEcLinkAllocSendFrame = EcLinkAllocSendFrame;
    pLinkDrvDesc->pfEcLinkFreeSendFrame  = EcLinkFreeSendFrame ;
    pLinkDrvDesc->pfEcLinkFreeRecvFrame  = EcLinkFreeRecvFrame ;
    pLinkDrvDesc->pfEcLinkGetEthernetAddress = EcLinkGetEthernetAddress;
    pLinkDrvDesc->pfEcLinkGetStatus = EcLinkGetStatus;
    pLinkDrvDesc->pfEcLinkGetSpeed = EcLinkGetSpeed;
    pLinkDrvDesc->pfEcLinkGetMode = EcLinkGetMode;
    pLinkDrvDesc->pfEcLinkIoCtl = EcLinkIoCtl;

Exit:
    return dwResult;

#if (defined INCLUDE_LOG_MESSAGES)
#undef  pEcLogParmsLL
#define pEcLogParmsLL pEcLogParmsLLDefault
#endif
}

/*-END OF SOURCE FILE--------------------------------------------------------*/
