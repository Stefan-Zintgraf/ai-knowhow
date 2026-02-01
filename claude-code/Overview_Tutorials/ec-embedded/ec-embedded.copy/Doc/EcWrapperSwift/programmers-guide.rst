*****************
Programmers Guide
*****************

Sample Code
***********

The Swift demo application contains of 1 module:

:file:`EcMasterDemoSwift.swift`: 
  Console demo application 


Wrapper
*******

Modules
=======

The Swift Wrapper contains of 5 modules:

:file:`CEcWrapperSwift.swift`
  .. class:: CEcWrapperSwift

    EC-Wrapper base class
  
  .. class:: CEcMasterSwift
  
    EC-Master
  
  .. class CEcMasterRasServerSwift
  
    RAS Server for EC-Master
      
  .. class:: CEcMasterMbxGatewayClientSwift
  
    Mailbox Gateway Client for EC-Master
  
  .. class:: CEcMasterMbxGatewayServerSwift
  
    Mailbox Gateway Server for EC-Master
  
  .. class:: CEcSimulatorSwift
  
    EC-Simulator
  
  .. class:: CEcSimulatorRasServerSwift
  
    RAS Server for EC-Simulator
  
  .. class:: CEcRasClientSwift
  
    RAS Client for EC-Master / EC-Simulator


:file:`EcMotionSwift.swift`
  .. class:: CEcMotionSwift
  
    EC-Motion interface


:file:`CEcWrapperSwiftTypes.swift`
  Swift types
    
:file:`CEcWrapper.swift`
  C Swift interface (internal)
    
:file:`CEcWrapperTypes.swift`
  C Swift types (internal)

Return code vs. exception handling
==================================

The most of all API functions returns a return code for error handling. This behaviour can be changed to throw an exception in error case by simply setting:

.. code-block:: Swift

    CEcWrapperSwift.EnableExceptionHandling = true // default is false

API with "out" or "ref" parameters
==================================

The Swift Wrapper API is based on C# code. C# supports :code:`out` and :code:`ref` keywords for parameters. This is not supported in Swift and is solved by simply submitting :code:`&myNullableObject` or :code:`&myObject` to those functions:

.. code-block:: Swift

    // This function has an "out" parameter "oSbStatus"
    func GetScanBusStatus(oSbStatus: inout DN_EC_T_SB_STATUS_NTFY_DESC?) -> ECError {
        // ...
        return
    }
    
    // Create "out" parameter
    var oStatus: DN_EC_T_SB_STATUS_NTFY_DESC?
    // Call function
    SwiftWrapper.GetScanBusStatus(oSbStatus: &oStatus)
    // Now, the "oStatus" object can be used
    print(oStatus!.dwResultCode)

Console Demo
************

Windows
=======

Open Windows Console Window, setup the environment and run the demo in the specific mode
  .. code-block:: console

      cd C:\Temp\EC-Master-Swift-V3.2.2.01-02-MacOS-ARM_64Bit-SDK_Source\Examples\EcMasterDemoSwift
      set PATH=C:\Temp\V3.2.2.01-Windows-x86_64Bit\EC-Master-Windows-x86_64Bit\Bin\Windows\x64;%PATH%
      set ECWRAPPERSWIFT_INSTALLDIR=C:\Temp\V3.2.2.01-Windows-x86_64Bit\EC-Master-Windows-x86_64Bit\Bin\Windows\x64\
      
      // Master 
      swift run EcMasterDemoSwift -mode 1 -file d:\project.xml -link "winpcap 172.20.143.181 1" -time 1
      // Master+NDIS 
      swift run EcMasterDemoSwift -mode 1 -file d:\project.xml -link "ndis 172.20.143.181 1" -time 1
      // Master+RAS
      swift run EcMasterDemoSwift -mode 1 -file d:\project.xml -link "winpcap 172.20.143.181 1" -port 6000 -time 0
      // Simulator
      swift run EcMasterDemoSwift -mode 1 -file d:\project.xml -link "simulator d:\project.xml 1 1" -time 1
      // RAS-Client
      swift run EcMasterDemoSwift -mode 2 -rem 127.0.0.1 -time 1
      // Motion+Sim
      swift run EcMasterDemoSwift -mode 1 -file d:\motion.xml -link "simulator d:\motion.xml 1 1" -motion 1001 -port 6000 -time 0

... and the demo is running.
  .. figure:: /Media/cmd_ecmasterdemo_windows.png
      :alt:


Linux
=====

Open Terminal, setup the environment and run the demo in the specific mode
  .. code-block:: console

      sudo -s // optional: required for sockraw link layer
      cd /home/testadmin/Downloads/EC-Master-Swift-V3.2.2.01-02-MacOS-ARM_64Bit-SDK_Source/Examples/EcMasterDemoSwift
      export PATH=/home/testadmin/Downloads/swift-5.10.1-RELEASE-ubuntu20.04/usr/bin:"${PATH}"
      export PATH=/home/testadmin/Downloads/V3.2.2.01-Linux-x86_64Bit/EC-Master-V3.2.2.01-Linux-x86_64Bit-Eval/Bin/Linux/x64:"${PATH}"
      export LD_LIBRARY_PATH=/home/testadmin/Downloads/V3.2.2.01-Linux-x86_64Bit/EC-Master-V3.2.2.01-Linux-x86_64Bit-Eval/Bin/Linux/x64:$LD_LIBRARY_PATH
      export ECWRAPPERSWIFT_INSTALLDIR=/home/testadmin/Downloads/V3.2.2.01-Linux-x86_64Bit/EC-Master-V3.2.2.01-Linux-x86_64Bit-Eval/Bin/Linux/x64/

      // Master 
      swift run EcMasterDemoSwift -mode 1 -file /tmp/project.xml -link "sockraw ens34 1" -time 1
      // Simulator
      swift run EcMasterDemoSwift -mode 1 -file /tmp/project.xml -link "simulator /tmp/project.xml 1 1" -time 1
      // RAS-Client
      swift run EcMasterDemoSwift -mode 2 -rem 172.17.5.112 -time 1

... and the demo is running.
  .. figure:: /Media/cmd_ecmasterdemo_linux.png
      :alt:


MacOS
=====

Open Terminal, setup the environment and run the demo in the specific mode
  .. code-block:: console

      sudo -s // optional: required for winpcap link layer, to avoid error message "(cannot open BPF device) /dev/bpf0: Permission denied"
      cd /Users/rte/Desktop/USERS/MGR/Test/EC-Master-Swift-V3.2.2.01-02-MacOS-ARM_64Bit-SDK_Source/Bin/MacOS/x64 // Run from here with --package-path, because otherwise link layers could not be found
      export PATH=/Users/rte/Desktop/USERS/MGR/Test/EC-Master-Swift-V3.2.2.01-02-MacOS-ARM_64Bit-SDK_Source/Bin/MacOS/x64:"${PATH}"
      export DYLD_LIBRARY_PATH=/Users/rte/Desktop/USERS/MGR/Test/EC-Master-Swift-V3.2.2.01-02-MacOS-ARM_64Bit-SDK_Source/Bin/MacOS/x64:$DYLD_LIBRARY_PATH
      export ECWRAPPERSWIFT_INSTALLDIR=/Users/rte/Desktop/USERS/MGR/Test/EC-Master-Swift-V3.2.2.01-02-MacOS-ARM_64Bit-SDK_Source/Bin/MacOS/x64/
      export ECWRAPPERSWIFT_WRAPPERDIR=/Users/rte/Desktop/USERS/MGR/Test/EC-Master-Swift-V3.2.2.01-02-MacOS-ARM_64Bit-SDK_Source/Bin/MacOS/x64/
      
      // Master 
      swift run --package-path ../../../Examples/EcMasterDemoSwift/Sources/ EcMasterDemoSwift -mode 1 -file /Users/rte/Desktop/USERS/MGR/project.xml -link "winpcap en7 1" -time 1
      // Master+IP
      swift run --package-path ../../../Examples/EcMasterDemoSwift/Sources/ EcMasterDemoSwift -mode 1 -file /Users/rte/Desktop/USERS/MGR/project.xml -link "winpcap 192.168.0.1 1" -time 1
      // Simulator
      swift run --package-path ../../../Examples/EcMasterDemoSwift/Sources/ EcMasterDemoSwift -mode 1 -file /Users/rte/Desktop/USERS/MGR/project.xml -link "simulator /Users/rte/Desktop/USERS/MGR/project.xml 1 1" -time 1
      // RAS-Client
      swift run --package-path ../../../Examples/EcMasterDemoSwift/Sources/ EcMasterDemoSwift -mode 2 -rem 172.17.5.112 -time 1

... and the demo is running.
  .. figure:: /Media/cmd_ecmasterdemo_macos.png
      :alt:
