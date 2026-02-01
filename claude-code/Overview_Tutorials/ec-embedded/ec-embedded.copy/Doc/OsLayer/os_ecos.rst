..
    ****
    eCos
    ****

Setting up and running EcMasterDemo
***********************************

#. Build the eCos kernel with the parameters associated to the application
    As a starting point there is a eCos configuration file (.ecc) file located at :file:`SDK/LIB/eCos/x86/`.
    
    eCos is unable to get command line parameters for main().
    The parameters for the application are build in the kernel via the configuration tool ( Arguments to main ).
    
    .. figure:: ../../OsLayer/Media/eCos_demo.png
        :align:     center
        :alt:     
    
    To use an other example with different parameters, the kernel has to be rebuild.
    
    For the EcMasterDemo example following line has to be passed to the application via the configuration tool:
    
    .. code-block:: c
    
        {
            (char *)"name",(char *)"-f",(char *)"perf.xml",
            (char *)" -intelgbe",(char *)"1",(char *)"1",(char *)"-v",
            (char *)"3",(char *)"-t",(char *)"60000",(char *)"-perf",(char *)NULL
        }

#. Compile EcMasterDemo
    As a starting point there is the Eclipse project for EcMasterDemo for eCos located at :file:`Workspace/eCos/EcMasterDemo`. 
    The following macro in :file:`Sources/OsLayer/eCos/EcOs.cpp` loads the ENI file from disk: 
    
    .. code-block:: c
    
        "MTAB_ENTRY(fat, "/", "fatfs", "/dev/idedisk1/1",  0)" 

#. Copy the ENI file to target
    eCos supports only the 8.3 file format. Adjust the ENI file name and the command line in the configuration tool accordingly.
#. Configure Grub to load the application
    Adjust the Grub menu file:
    
    .. code-block::
    
        title eCos EcMasterDemo
        kernel (hd0,0)/EcMasterDemo
        boot  

#. Load and start the EcMasterDemo with Grub
#. Verify that the EcMasterDemo is running successfully
    The EcMasterDemo takes some seconds to start. The following message is sent to the serial port on startup finished:
    
    .. prompt:: bash
    
        [ 3593.654951] Master state changed from <SAFEOP> to <OP>

.. seealso:: :ref:`gettingstarted:Running EcMasterDemo`

OS Compiler settings
********************

Besides the general settings from :ref:`gettingstarted:Compiling the EcMasterDemo` the following settings are necessary to build the example application for eCos.

Extra include paths
    .. code-block::

        <InstallPath>/SDK/INC/eCos
        <InstallPath>/Examples/Common/eCos

Extra source paths
    .. code-block::

        <InstallPath>/Examples/Common/eCos
        <InstallPath>/Sources/OsLayer/eCos/EcOs.cpp

Extra library paths to the main EtherCAT components
    .. code-block::
    
        <InstallPath>/SDK/LIB/eCos

Extra libraries
    .. code-block::
    
        libEcMaster.a 
        libemllIntelGbe.a 
        libtarget.a
