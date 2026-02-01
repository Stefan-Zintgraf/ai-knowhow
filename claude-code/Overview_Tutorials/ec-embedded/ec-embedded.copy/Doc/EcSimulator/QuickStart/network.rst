*********************************************
EtherCAT\ |R| Network Configuration (ENI/EXI)
*********************************************

The |Product| needs knowledge about the network to be simulated which must be configured using a configuration file in the 
EtherCAT\ |R| Network Information Format (ENI) or the Extended Network Information Format (EXI).

**It is strongly recommended to use the same configuration file at Master and Simulator!**

The EtherCAT\ |R| Network can be configured using EC-Engineer, which can be obtained from https://www.acontis.com/en/ecdownloads.html\ .

The User Manuals of |Product| and EC-Engineer contain information that is more detailed. 
They are available at https://developer.acontis.com/manuals.html\ .

If you have questions, please contact us at https://www.acontis.com/en/contactform.html\ .


Use an Existing EtherCAT\ |R| Network Configuration
***************************************************

The configuration file is typically already available or can be exported from the configuration tool used to configure the EtherCAT\ |R| Master. 

In any other case, a new EtherCAT® Network must be configured, see below. 


Configure a New EtherCAT\ |R| Network (Offline Configuration)
*************************************************************

The new EtherCAT® Network to be simulated can be configured using EC-Engineer as described below.

#. Start EC-Engineer. Select "*Offline Configuration*" within the "*Start Page*" tab:

    .. figure:: ../Media/qsnetwork1crop.png
        :align: center
        :alt:
   
   .. raw:: latex

      \newpage
   
#. In the following dialog, select "EtherCAT Simulator Unit (HiL)" and press "*OK*":

    .. figure:: ../Media/qsnetwork2.png
        :align: center
        :alt:

#. Append desired slaves e.g., EK1100 + EL2004 + EL1008 + EL4132 and press "*OK*":

    .. figure:: ../Media/qsnetwork3.png
        :align: center
        :alt:

    Hint: The EC-Engineer needs to know about all slave types that are going to be configured. Slave descriptions (ESI files) can be added by "File > ESI Manager" from the menu bar.

   .. raw:: latex

      \newpage
   
#. Select Object Directories to be created from ESI files and click "*Apply changes to all slaves…*" (optional):

    .. figure:: ../Media/qsnetwork4crop.png
        :align: center
        :alt:

#. Finally click to "*Export EXI*" to store the configuration file e.g., "exi.xml":

    .. figure:: ../Media/qsnetwork5.png
        :align: center
        :alt:

.. only:: EcSimulatorHiL

    This configuration can now be loaded by the EcSimulatorHilDemo.

.. only:: EcSimulatorSiL

    This configuration can now be loaded by the EcSimulatorSilDemo.

