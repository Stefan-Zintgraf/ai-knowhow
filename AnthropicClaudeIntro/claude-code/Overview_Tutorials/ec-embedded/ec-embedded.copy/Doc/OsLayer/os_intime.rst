..
    **************
    tenAsys INtime
    **************

Real-time Ethernet Driver are available for INtime.
If using INtime with Windows running in parallel on the same host the network adapter card has to be assigned to INtime
The network adapters should be passed to INtime using the ``INtime Device Manager``. Please refer to the INtime user manual for this.

Search locations for Real-time Ethernet Driver can be adjusted using the ``PATH`` environment variable

.. only:: not EcSimulatorSiL

    Setting up and running |EcDemo|
    *******************************
    
    The file |EcDemo|.rta has to be executed. The full path and file name of the configuration file has to be given as a command line parameter as well as the appropriate Real-time Ethernet Driver.
    To start the application from the command prompt, enter following commands:
        
    .. prompt:: text >
        :substitutions:
        
        nodemgr start NodeA
        sleep 5
        piperta.exe -node NodeA -stderr |EcDemo|.rta -intelgbe 1 1 -f eni.xml
    
    .. seealso:: :ref:`running-ecdemo`

OS Compiler settings
********************

Besides the general settings from :ref:`compile-ecdemo` the following settings are necessary to build the example application for INtime.

Extra include paths
    .. code-block::
        
        <InstallPath>\SDK\INC\INtime
        <InstallPath>\Examples\Common\INtime

Extra source paths
    .. code-block::

        <InstallPath>\Examples\Common\INtime
        <InstallPath>\Sources\OsLayer\INtime

Extra library paths to the main EtherCAT components
    .. code-block::

        <InstallPath>\SDK\LIB\INtime
