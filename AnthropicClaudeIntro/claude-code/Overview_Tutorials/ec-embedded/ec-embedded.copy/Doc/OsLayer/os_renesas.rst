..
    *******
    Renesas
    *******

R-IN32M3
********

#. Prerequisites
    Hardware: 

    - R-IN32M3-EC Evaluation Board, 
    - adviceLUNA Emulator

    Software: 

    - microVIEW-PLUS debugger, 
    - GNU compiler (Sourcery G++ Lite for ARM EABI)

#. Verify TCP/IP evaluation sample from Renesas works fine. 
    
#. Download from official Renesas site following files: 
    - :file:`r-in32m3_tcpip_evaluation.zip`
    - :file:`r-in32m3_samplesoft.zip`.

#. Create ENI file for EtherCAT configuration.
    :file:`xxd.exe` is capable of converting ENI files to a C file as array, e.g. 
        .. prompt:: batch
        
            xxd.exe -i eni.xml ENI.c
    
    Replace ENI.c file with generated one. File should be manually modified to look like:
    
    .. code-block:: c
    
        unsigned char MasterENI_xml_data[] = {
        ...
        };
        unsigned int MasterENI_xml_data_size = ???;

#. Import project :file:`Workspace/RIN32M3/EcMasterDemo` into Eclipse IDE. 
    Hardcoded parameters for the demo can be changed using DEMO_PARAMETERS definition. 

#. Upload  :file:`Workspace/RIN32M3/EcMasterDemo/Release/EcMasterDemo.bin` with debugger and run

.. seealso:: :ref:`gettingstarted:Running EcMasterDemo`

R-IN32M4
********

#. Prerequisites
    Hardware:

    - SBEV-RIN32M4CL3 Evaluation Board

    Software: 

    - IAR Workbench 9.10.1, 
    - `"R-IN32M4 series R-IN32M4-CL3 Driver/Middleware Release Note - Sample Code" <https://www.renesas.com/us/en/document/scd/r-in32m4-series-r-in32m4-cl3-drivermiddleware-release-note-sample-code?language=en&r=1215996>`_ package 

#. Build EcMasterDemo

    #. Install "R-IN32M4 series R-IN32M4-CL3 Driver/Middleware Release Note - Sample Code" and set the path the environment variable *MIDDLEWARE_LOC* to the same folder.
    #. Start IAR Workbench and import EcMasterDemo project into workspace
    #. Create ENI file for EtherCAT configuration.
        :file:`xxd.exe` is capable of converting ENI files to a C file as array, e.g. 
            .. prompt:: batch
            
                xxd.exe -i eni.xml MasterENI.c
        
        Replace MasterENI.c file with generated one. File should be manually modified to look like:
        
        .. code-block:: c
        
            unsigned char MasterENI_xml_data[] = {
            ...
            };
            unsigned int MasterENI_xml_data_size = ???;

    #. Import project :file:`Workspace/RIN32M3/EcMasterDemo` into project. 
    #. Build the project and upload it to the board

.. seealso:: :ref:`gettingstarted:Running EcMasterDemo`

#. Troubleshouting

If after upload a program into serial FLASH the application has been trapped in HardFault_Handler_rom() reset the board with reset button.


