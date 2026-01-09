***********
Integration
***********

This section gives an overview of the possibilities and usage of Hot-Connect. It describes the sequence of the notification messages that the application receives in case a Hot-Connect group was connected or disconnected.

No special adjustment of the EtherCAT application is necessary at all. Hot-Connect is configured in the EtherCAT configurator such as the EC-Engineer or the Beckhoff ET9000. These tools can be used to define so-called Hot-Connect groups consisting of one or more EtherCAT slaves. 

.. seealso:: :ref:`config:Configuration`

Hot-Connect group connection sequence 
*************************************

The following sequence shows which notifications the application receives by connecting an EtherCAT slave that has been defined as a Hot-Connect group. 

It is assumed that the EtherCAT network configuration file (ENI) has been correctly created and exported with an EtherCAT configurator and a valid Hot-Connect group has been connected to the EtherCAT bus.

.. figure:: ../Media/hot-connect_group-connect.png
    :alt:

#. The EC-Master will be started. The validation of the EtherCAT network against the ENI is executed and the transition to operational is done for all slaves. The application receives :ref:`api:emNotify - EC_NOTIFY_SLAVE_PRESENCE` notification for each slave of the currently connected optional Hot-Connect groups. If the validation fails the application receives an :ref:`api:emNotify - EC_NOTIFY_SB_MISMATCH` and an :ref:`api:emNotify - EC_NOTIFY_SB_STATUS` notification.
#. Now the EtherCAT network is running and a new Hot-Connect group will be connected, either by plugging or power on.
#. The EC-Master recognizes the topology change and starts the internal Hot-Connect state machine.
#. The EC-Master check whether the new connected Hot-Connect group is valid and therefore scans the whole network to identify the connected Hot-Connect group. 
#. To identify the Hot-Connect group the vendor ID, product code and identification value of the Hot-Connect group must match to the ENI file.
#. If the EC-Master has identified the Hot-Connect group successfully, the application receives the :ref:`api:emNotify - EC_NOTIFY_SLAVE_PRESENCE` notification for each slave of the connected Hot-Connect group. If a slave could not successful validated, the application receives an :ref:`api:emNotify - EC_NOTIFY_SB_MISMATCH` and :ref:`api:emNotify - EC_NOTIFY_SB_STATUS` notification.
#. If the EC-Master could validate all the Hot-Connect groups successfully, the application receives the :ref:`api:emNotify - EC_NOTIFY_HC_DETECTADDGROUPS` notification which indicates that the detection of the all HotConnect group was successful finished.
#. The EC-Master now sets the connected slaves in operational state.
#. Finally the EC-Master signalizes with the :ref:`api:emNotify - EC_NOTIFY_HC_TOPOCHGDONE` notification, that the topology change was finished. The error code in the notification indicates whether the topology change was successful or not.

.. note::
    - :ref:`api:emNotify - EC_NOTIFY_SB_MISMATCH` and :ref:`api:emNotify - EC_NOTIFY_SB_STATUS` are common notifications that the application receives after a scan bus was performed. Please refer to the EC-Master manual for more information.
    - In case the application tries to access a slave by the EC-Master API that is currently not connected to the bus, :c:macro:`EC_E_SLAVE_NOT_PRESENT` will be returned.
     
Hot-Connect group disconnection sequence
****************************************

The disconnect case works analog to the connect case of a Hot-Connect group. The EC-Master of course does not need to validate new slaves, but must make sure that the network is valid after a Hot-Connect group was disconnected. If a mandatory slave, a slave that was not configured as a Hot-Connect group, was disconnected, the network validation will fail and the application receives :ref:`api:emNotify - EC_NOTIFY_SB_MISMATCH` and :ref:`api:emNotify - EC_NOTIFY_SB_STATUS` notifications. Finally the application will receive an :ref:`api:emNotify - EC_NOTIFY_HC_TOPOCHGDONE` with an error code.
If the network could be validated successfully the application receives an :ref:`api:emNotify - EC_NOTIFY_SLAVE_PRESENCE` and finally an :ref:`api:emNotify - EC_NOTIFY_HC_TOPOCHGDONE` notification with :c:macro:`EC_E_NOERROR`.

.. figure:: ../Media/hot-connect_group-connect-2.png
    :alt:


Modes of operation
******************

There are different modes how the EC-Master handles a Hot-Connect process and how the application can influence it.

Automatic mode
==============

:cpp:enumerator:`EC_T_EHOTCONNECTMODE::echm_automatic` is the default Hot-Connect mode. The detection, topology change handling and slave state transition is automatically handled by the EC-Master.


Manual mode
===========

In the modes :cpp:enumerator:`EC_T_EHOTCONNECTMODE::echm_manual_preop` and :cpp:enumerator:`EC_T_EHOTCONNECTMODE::echm_manual_noreset` the EC-Master detects and notifies a topology change. The application can accept the topology change and allow the EC-Master a slave transition to the master state. :cpp:enumerator:`EC_T_EHOTCONNECTMODE::echm_manual_noreset` does not perform a slave state change via DEVICE_STATE_INIT.

Border close
============

:cpp:enumerator:`EC_T_EHOTCONNECTMODE::echm_borderclose` is an option and can be combined with the other modes. If this option is set, the still open ports in the configuration and in the EtherCAT network, respectively are closed automatically.
