*****************
Programmers Guide
*****************

Sample Scripts
**************

There are currently 2 scripts available:

:file:`EcMasterDemoPython.bat`
  Starts the console demo application

:file:`EcMasterDemoPythonInteractive.bat`
  Starts the interactive demo application

The scripts will start the demo application. The interactive demo application waits for user input where the user can enter the following commands:

.. code-block:: python

    # Write variable
    demo.processImage.variables.Slave_1005__EL2008_.Channel_1.Output.set(1)
    
    # Read variable
    demo.processImage.variables.Slave_1005__EL2008_.Channel_1.Output.get()
    
    # Print properties of variable
    demo.processImage.variables.Slave_1005__EL2008_.Channel_1.Output.dmp()
    
    # Stop the demo:
    demo.stopDemo()

Sample Code
***********

The Python demo application contains of 3 modules:

:file:`EcDemoApp.py`: 
  Console demo application 

:file:`EcDemoAppGui.py`:
  Gui demo application, based on Qt5 

:file:`EcDemoAppInteractive.py`: 
  Interactive demo application 


Wrapper
*******

Modules
=======

The Python Wrapper contains of 5 modules:

:file:`EcWrapperPython.py`
  .. class:: CEcWrapperPython

    EC-Wrapper base class
  
  .. class:: CEcMasterPython
  
    EC-Master
  
  .. class CEcMasterRasServerPython
  
    RAS Server for EC-Master
      
  .. class:: CEcMasterMbxGatewayClientPython
  
    Mailbox Gateway Client for EC-Master
  
  .. class:: CEcMasterMbxGatewayServerPython
  
    Mailbox Gateway Server for EC-Master
  
  .. class:: CEcSimulatorPython
  
    EC-Simulator
  
  .. class:: CEcSimulatorRasServerPython
  
    RAS Server for EC-Simulator
  
  .. class:: CEcRasClientPython
  
    RAS Client for EC-Master / EC-Simulator


:file:`EcMotionPython.py`
  .. class:: CEcMotionPython
  
    EC-Motion interface


:file:`EcWrapperPythonTypes.py`
  Python types
    
:file:`EcWrapper.py`
  CPython interface (internal)
    
:file:`EcWrapperTypes.py`
  CPython types (internal)

Return code vs. exception handling
==================================

The most of all API functions returns a return code for error handling. This behaviour can be changed to throw an exception in error case by simply setting:

.. code-block:: python

    CEcWrapperPython.EnableExceptionHandling = True # default is False

API with "out" or "ref" parameters
==================================

The Python Wrapper API is based on C# code. C# supports :code:`out` and :code:`ref` keywords for parameters. This is not supported in Python and is solved by simply submitting :code:`CEcWrapperPythonOutParam` or :code:`CEcWrapperPythonRefParam` to those functions:

.. code-block:: python

    # This function has an "out" parameter "out_oSbStatus"
    def GetScanBusStatus(self, out_oSbStatus):
        # ...
        return
    
    # Create "out" parameter
    out_oStatus = CEcWrapperPythonOutParam()
    # Call function
    pythonWrapper.GetScanBusStatus(out_oStatus)
    # Get the "out" parameter value
    oStatus = out_oStatus.value
    # Now, the "oStatus" object can be used
    print(oStatus.dwResultCode)

Supported IDEs
**************

Python Shell IDLE
=================

This is the default IDE. 

It can be started from Windows Start Menu or by calling :file:`C:/Python/Lib/idlelib/idle.py`:
  .. figure:: /Media/shell-idle.png
      :alt:

In this shell, the user can simply copy&paste the sample code from: :file:`Examples/EcMasterDemoPython/EcDemoAppInteractive.py`
  .. code-block:: python

      exec("""
      import os
      import sys
      INSTALLDIR = "C:/Program
      Files/acontis_technologies/EC-Master-Windows-x86_64Bit/"
      os.environ["PATH"] += os.pathsep + INSTALLDIR + "Bin/Windows/x64"
      sys.path.append(INSTALLDIR + "Sources/EcWrapperPython")
      sys.path.append(INSTALLDIR + "Examples/EcMasterDemoPython")
      from EcDemoApp import \*
      demo = EcMasterDemoPython()
      demo.pAppParms.tRunMode = RunMode.Master
      demo.pAppParms.dwBusCycleTimeUsec = 4000
      demo.pAppParms.szENIFilename = "ENI.xml"
      demo.pAppParms.szLinkLayer = "winpcap 127.0.0.0 1"
      demo.pAppParms.nVerbose = 3
      demo.startDemo()
      print("EcMasterDemoPython is running.")
      print("Type demo.help() for interactive help.")
      """)

... and the demo is running.
  .. figure:: /Media/shell-idle_ecmasterdemo.png
      :alt:


Visual Studio 2019
==================

Create a new project:
  .. figure:: /Media/vs2019_cerate-new-project.png
      :alt:

Configure the project:
  - Replace the generated file :file:`EcMasterDemoPython.py` with the existing :file:`EcDemoApp.py`.

  .. figure:: /Media/vs2019_configure-new-project.png
      :alt:

Configure project `General` settings:
  - Startup File: :file:`EcDemoApp.py`

  .. figure:: /Media/vs2019_configure-new-project-2.png
      :alt:

Configure project `Debug` settings:
  - Search Paths: 

  .. code-block::
    
    ../../Sources/EcWrapperPython;../EcMasterDemoPython

  - Script Arguments:

  .. code-block:: 

    --mode 1 -f ENI.xml --link "winpcap 127.0.0.0 1 1" -b 4000 -t 1000 -v 3

  - Environment Variables:

  .. code-block:: 
  
    PATH=../../Bin/Windows/x64;%PATH%

  .. figure:: /Media/vs2019_configure-new-project-3.png
      :alt:

Press `Start` and the demo is running:
  .. figure:: /Media/cmd_ecmasterdemo.png
      :alt:

Visual Studio Code
==================

Install python extension by open extension tab and enter `python`:
  .. figure:: /Media/vscode_install-phyton-extension.png
      :alt:
    
Open folder :file:`Examples/EcMasterDemoPython` and configure the :file:`launch.json`:
  .. code-block:: json

      {
          "version": "0.2.0",
          "configurations": [
              {
                  "name": "Python: Aktuelle Datei",
                  "type": "python",
                  "request": "launch",
                  "program": "${file}",
                  "console": "integratedTerminal",
                  "cwd": "",
                  "args" : [
                      "--mode", "1", 
                      "-f", "ENI.xml", 
                      "--link", "winpcap 127.0.0.1 1", 
                      "-b", "4000", 
                      "-t", "1000", 
                      "-v", "3",
                  ],
                  "env": {"PYTHONPATH": "${workspaceRoot}"} 
              }
          ]
      }

  .. figure:: /Media/vscode_install-phyton-extension-2.png
      :alt:

Configure linter in :file:`settings.json`:
  .. code-block:: json

      {
            "git.ignoreLimitWarning": true,
            "python.linting.pylintArgs": [
                "--init-hook='import sys; sys.path.append(\"C:/Temp/EC-Master-Windows-x86_64Bit/Sources/EcWrapperPython\")'"
            ]
      }

  .. figure:: /Media/vscode_install-phyton-extension-3.png
      :alt:

Open :file:`EcDemoApp.py` and the following lines to set environment:
  .. code-block:: python

      import os
      import sys
      INSTALLDIR = "C:/Temp/EC-Master-Windows-x86_64Bit/"
      os.environ["PATH"] += os.pathsep + INSTALLDIR + "Bin/Windows/x64"
      sys.path.append(INSTALLDIR + "Sources/EcWrapperPython")
      sys.path.append(INSTALLDIR + "Examples/EcMasterDemoPython")

  .. figure:: /Media/vscode_install-phyton-extension-4.png
      :alt:

Start debugging and the demo output will be written into the terminal:
  .. figure:: /Media/vscode_install-phyton-extension-5.png
      :alt: