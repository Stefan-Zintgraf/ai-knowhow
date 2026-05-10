The parameters to the CPSWG Real-time Ethernet Driver are setup-specific. 
The function :cpp:func:`CreateLinkParmsFromCmdLineCPSWG` in :file:`EcSelectLinkLayer.cpp` demonstrates how to initialize the Real-time Ethernet Driver instance.

.. doxygenstruct:: EC_T_LINK_PARMS_CPSWG
    :members:

.. doxygenenum:: EC_T_CPSWG_TYPE 

CPSWG usage under Linux
***********************

The unbind feature of the am65-cpsw-nuss Linux driver isn't supported and the atemsys kernel module must be assigned as driver for the platform device.
So the ``"ethernet/am654-cpsw-nuss"`` device tree node must be modified, by changing ``compatible = "atemsys";`` and adding ``atemsys-Ident = "CPSWG";`` and ``atemsys-Instance = <0x1>;``, also remove or comment out ``dma-coherent;``.

.. code-block:: dts

    ethernet@46000000 {
        compatible = "atemsys";
        atemsys-Ident = "CPSWG";
        atemsys-Instance = <0x1>;
        ...
        #dma-coherent;
        ...

So the ``"ethernet/am642-cpsw-nuss"`` device tree node must be modified likewise.
Second port of am642-cpsw-nuss is not supported.

.. code-block:: dts

    ethernet@8000000 {
        compatible = "atemsys";
        atemsys-Ident = "CPSWG";
        atemsys-Instance = <0x1>;
        ...
        #dma-coherent;
        ...

.. see also:: https://github.com/acontis/atemsys for more details.

Currently following Linux versions are supported:

- ti-processor-sdk-linux-rt-am65xx-evm-07_01_00_18 (tested on AM65 IDK)
- ti-processor-sdk-linux-rt-am65xx-evm-08.06.00.47 (tested on AM65 IDK)
- ti-processor-sdk-linux-rt-j7-evm-08_06_01_02 (tested on SK-TDA4VM)
- ti-processor-sdk-linux-rt-j7-evm-08_06_01_02 (tested on SK-TDA4VM)
- ti-processor-sdk-linux-edgeai-j721e-evm-09_01_00_06 (tested on SK-TDA4VM)
- ti-processor-sdk-linux-rt-am64xx-evm-08.02.00.14 (tested on TMDS64GPEVM)
- ti-processor-sdk-linux-rt-am64xx-evm-09.02.00.08 (tested on TMDS64GPEVM)
- SolidRun ti_am64x_build/20240221 microsd-debian-bookworm-sr1 (tested on AM64 HummingBoard-T)
- toradex_ti-linux-6.1.y Linux/arm64 6.1.46 Kernel (tested on Toradex Verdin AM62)

