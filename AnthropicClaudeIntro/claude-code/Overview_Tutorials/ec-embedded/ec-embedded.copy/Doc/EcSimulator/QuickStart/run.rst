**************************************
Running EcSimulator\ |LcEdition|\ Demo
**************************************

.. only:: EcSimulatorHiL

    The :file:`EcSimulatorHilDemo` is an |Product| example application that initializes the |Product| |Edition| to listen on a specific network adapter for EtherCAT® frames sent 
    by the Master, simulate the network and send them back to the Master. At least the **network adapter** and the **configuration file** (ENI/EXI) for the network 
    to be simulated must be known to run the :file:`EcSimulatorHilDemo`:

    .. image:: ../Media/qsrun1.png
      :scale: 75
      :align: center

    While :file:`EcSimulatorHilDemo` runs, the Master System can scan and operate the simulated EtherCAT\ |R| network.

    Most EtherCAT\ |R| systems require modifications to the |Edition| System if real-time constraints must be kept, else the Master may fail switching to the EtherCAT\ |R|
    PREOP or SAFE-OP state.

    The |Product| |Edition| license key can be given to the :file:`EcSimulatorHilDemo` as parameter "-lic ...". 

.. only:: EcSimulatorSiL

    The EcSimulatorSilDemo is an example application that integrates EC-Master with |Product| |Edition|\ :

    .. image:: ../Media/qssilrun1.png

    At least the **network adapter** for license check and the **configuration file** (ENI/EXI) for the network to be simulated must be known to run the EcSimulatorSilDemo:

    .. image:: ../Media/qssilrun2.png

    The |Product| |Edition| license key can be given to the EcSimulatorSilDemo as parameter:

    .. code-block::
    
    EcSimulatorSilDemo -simulator 1 1 eni.xml --lic ... 


Setting Up and Running EcSimulator\ |Edition|\ Demo (Windows)
*************************************************************

.. only:: EcSimulatorHiL

    Copy all of the example application files into one directory, i.e. the application :file:`EcSimulatorHilDemo.exe` and all DLLs from within :file:`Bin\\Windows\\x64`, 
    as well as the EtherCAT\ |R| network configuration file (ENI/EXI) EXI file.

    The following command starts :file:`EcSimulatorHilDemo`:

    .. prompt:: bash

        EcSimulatorHilDemo.exe -ndis 192.168.99.1 0 -f exi.xml -t 0 -v 3 -sp

.. only:: EcSimulatorSiL

    Copy all of the example application files into one directory, i.e. the application EcSimulatorSilDemo.exe and all DLLs from within :file:`Bin\\Windows\\x64`, 
    as well as the EtherCAT\ |R| network configuration file (ENI/EXI) EXI file.

    The following command starts :file:`EcSimulatorSilDemo`:

    .. prompt:: bash

        EcSimulatorSilDemo.exe -simulator 1 1 exi.xml --lic … --link -ndis 192.168.99.1 0 --sp -f exi.xml -t 0 -v 3 -sp
  
  
Setting Up and Running EcSimulator\ |Edition|\ Demo (Linux)
***********************************************************

.. only:: EcSimulatorHiL

    The following command starts EcSimulatorHilDemo after preparing the system as described above::

    .. prompt:: bash

        root@myLinuxTarget: # cd Bin/Linux/x64

        … # export LD_LIBRARY_PATH=.

        … # ./EcSimulatorHilDemo -f exi.xml -intelgbe 0x01010000 1 -t 0 -v 3 -sp

.. only:: EcSimulatorSiL

 The following command starts EcSimulatorSilDemo after preparing the system as described above::

    .. prompt:: bash

        root@myLinuxTarget: # cd Bin/Linux/x64

        … # export LD_LIBRARY_PATH=.
   
        … # ./EcSimulatorSilDemo -simulator 1 1 exi.xml --lic … --link -intelgbe 0x01010000 1 --sp -f exi.xml -t 0 -v 3 -sp

Online Diagnosis (EC-Engineer Diagnosis Mode)
*********************************************

1. Start EC-Engineer. Enter "*Remote Diagnosis*" within the "*Start Page*" tab and select "EtherCAT Simulator Unit (HiL)":
   
   .. image:: ../Media/qsrun2crop.png

.. only:: EcSimulatorHiL

   2. Enter the LAN IP address of the system running the EcSimulatorHilDemo and press "Select"

   .. image:: ../Media/qsrun3crop.png
     :scale: 82
     :align: right
   
.. only:: EcSimulatorSiL
   
   2. Enter the LAN IP address of the system running the EcSimulatorSilDemo, **set Instance 1 (!)** and press "*Select*"
   
   .. image:: ../Media/qssilrun3.png
     :scale: 82
     :align: right
   
.. raw:: latex

    \newpage   
   
3. Process Data OUTPUTs from the Master can be inspected and Process Data INPUTs to the Master can be forced at the "*Process Data Image*" tab of the
   EC-Simulator Device:

   .. image:: ../Media/qsrun4crop.png
   
   
**********
Next Steps
**********

The |Product|'s User Manual is located in the "Doc" folder of the SDK installation and available online at https://developer.acontis.com/manuals.html .

It contains information that is more detailed and helps with the next steps i.e.:

- Check-out the "-flash" parameter of EcSimulator\ |Edition|\ Demo and inspect the values in EC-Engineer as an example for setting Process Data INPUTs programmatically
- Learn about |Product|'s features 
- Learn using the API: See "EC-Simulator Software Development Kit (SDK)" in the User Manual.

Define your application:

- Check what is required by the EtherCAT\ |R| Master application
- Create the system design of EtherCAT\ |R| Master and EtherCAT\ |R| Simulator
- Define your use cases of |Product|'s and design your own |Product|'s application.
- Create the EtherCAT\ |R| Network Configurations for your Use Cases
- Implement your own |Product|'s application in C / C++ / Python / .NET

If you have questions, please contact us at https://www.acontis.com/en/contactform.html .
