*************************
Configuration with ET9000
*************************

Since version 2.11.0 of the EtherCAT Configurator from Beckhoff explicitly setup whether the DC time shall be controlled by the EtherCAT master or not.

To create a DCM capable configuration, please accomplish the following steps.

#. Scan the EtherCAT Bus

#. Select the EtherCAT device and press the button "Advanced Settings..."
    .. figure:: ../Media/EC_Configurator1.png
        :align:     center
        :alt:   

#. In the open dialog please select "Distributed Clocks" on the left column. Then de-select "Automatic DC Mode Selection" and select the option "DC Time controlled by TwinCAT Time (Slave Mode)". 
    .. figure:: ../Media/EC_Configurator2.png
        :align:     center
        :alt:   

#. Now the DC time can be controlled by the EtherCAT master. Don't forget to enable DC for the slaves.
    .. note:: Don't forget to enable DC for the slaves.

