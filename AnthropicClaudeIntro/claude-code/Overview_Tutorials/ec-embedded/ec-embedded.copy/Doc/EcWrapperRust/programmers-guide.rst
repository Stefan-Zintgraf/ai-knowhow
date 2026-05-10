*****************
Programmers Guide
*****************

Sample Application
******************

There is currently 1 script available:

:file:`EcMasterDemoRust.bat`
  Starts the console demo application

Sample Code
***********

The Rust demo application contains of 3 modules:

:file:`EcDemoApp.rs`: 
  Console demo application 

:file:`EcLogging.rs`:
  Logging module, which writes asynchronous messages to console, file, ...

:file:`EcUtil.rs`: 
  Utility module, which contains some helper functions


Wrapper
*******

Modules
=======

The Rust Wrapper contains of 5 modules:

:file:`EcWrapperRust.rs`
  .. class:: CEcWrapperRust

    EC-Wrapper base class
  
  .. class:: CEcMasterRust
  
    EC-Master
  
  .. class CEcMasterRasServerRust
  
    RAS Server for EC-Master
      
  .. class:: CEcMasterMbxGatewayClientRust
  
    Mailbox Gateway Client for EC-Master
  
  .. class:: CEcMasterMbxGatewayServerRust
  
    Mailbox Gateway Server for EC-Master
  
  .. class:: CEcSimulatorRust
  
    EC-Simulator
  
  .. class:: CEcSimulatorRasServerRust
  
    RAS Server for EC-Simulator
  
  .. class:: CEcRasClientRust
  
    RAS Client for EC-Master / EC-Simulator


:file:`EcMotionRust.rs`
  .. class:: CEcMotionRust
  
    EC-Motion interface


:file:`EcWrapperRustTypes.rs`
  Rust types
    
:file:`EcWrapper.rs`
  C Rust interface (internal)
    
:file:`EcWrapperTypes.rs`
  C Rust types (internal)

Return code vs. exception handling
==================================

The most of all API functions returns a return code for error handling. This behaviour can be changed to throw an exception in error case by simply setting:

.. code-block:: rust

    CEcWrapperRust_EnableExceptionHandling = true // default is false

Supported IDEs
**************

Visual Studio Code
==================

Install rust extension by open extension tab and enter `rust`:
  .. figure:: /Media/vscode_install-rust-extension.png
      :alt:
    
Open package folder e.g. :file:`EC-Master-V3.2.2.04-Windows-x86_64Bit-SDK_Source` and configure the :file:`launch.json`:
  .. code-block:: json

      {
          "version": "0.2.0",
          "configurations": [       
              {
                  "type": "lldb",
                  "request": "launch",
                  "name": "Debug executable 'ecmasterdemorust'",
                  "cargo": {
                      "args": [
                          "build",
                          "--bin=ecmasterdemorust",
                          "--package=ecmasterdemorust"
                      ],
                      "filter": {
                          "name": "ecmasterdemorust",
                          "kind": "bin"
                      }
                  },
                  "args": [ "-mode", "1", "-file", "ENI.xml", "-link", "winpcap 127.0.0.1 1", "-cycleTime", "4000", "-time", "1000", "-lvl", "3" ],
                  "env": {
                      "PATH": "C:/Temp/EC-Master-V3.2.2.04-Windows-x86_64Bit-SDK_Source/Windows/x64/",
                      "ECWRAPPERRUST_INSTALLDIR": "C:/Temp/EC-Master-V3.2.2.04-Windows-x86_64Bit-SDK_Source/Windows/x64/"
                  },      
                  "cwd": "${workspaceFolder}"
              },
          ]
      }

  .. figure:: /Media/vscode_install-rust-launch.png
      :alt:

Start debugging and the demo output will be written into the terminal:
  .. figure:: /Media/vscode_install-rust-terminal.png
      :alt: