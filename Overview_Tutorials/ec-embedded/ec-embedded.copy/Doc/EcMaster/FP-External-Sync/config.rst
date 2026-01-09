******************************
Configuration with EC-Engineer
******************************
Since version 2.5.0 of the EC-Engineer the configuration of the reference clock adjustment by external synchronization device is supported. 

Primary Segment
***************

The following steps are required to create a DCX-capable configuration in the primary segment.

#. Scan the EtherCAT bus.
#. Select the Bridge Device (e.g. EL6692) and enable DC-Synchron mode.
    
   .. figure:: ../Media/external-sync_prim-config-dc.png
       :align: center
       :alt:

#. Activate PDO 0x1A02 to display the time stamps.
    
   .. figure:: ../Media/external-sync_prim-config-pdo.png
       :align: center
       :alt:

#. Export ENI

Secondary Segment
*****************

The following steps are required to create a DCX-capable configuration in the secondary segment.

#. Scan the EtherCAT bus.
#. Select the Bridge Device (e.g. EL6692) and enable DC-Synchron mode.
#. Enable External Mode in the Distribute Clocks tab of the Master.

   .. figure:: ../Media/external-sync_sec-config-dc-mode.png
       :align: center
       :alt:

#. Export ENI