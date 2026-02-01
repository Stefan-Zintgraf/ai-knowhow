*************
Configuration
*************

This chapter explains how to configure Hot-Connect groups with group heads having rotary address switches in EC-Engineer.

#. Scan the network or create a network by hand.

   The EC-Engineer automatically scans the network and displays the connected slaves in case of online configuration or remote configuration.
   
   .. figure:: ../Media/Hot-Connect_Engineer_Scan.png
     :alt:

.. _createGroup:

#. Create a Group

   In order to create a Hot-Connect group, a head slave and all topologically following slaves of the stub must be marked. The group can be created via the context menu.

   .. figure:: ../Media/Hot-Connect_Engineer_CreateGroup.png
     :alt:

#. Configure Group Settings

   A Hot-Connect group configuration consists of a freely selectable name and an identification value. The identification value must be unique within the network. If the configuration was created by scanning the network, the identification value is automatically read from the slave and predefined in the field.

   .. figure:: ../Media/Hot-Connect_Engineer_Group-Settings.png

   After creating the Hot-Connect group, it is marked with a indicating icon in the slave tree:

   .. figure:: ../Media/Hot-Connect_Engineer_HC-Symbol-Tree.png

#. Group position restriction

   By default, when creating the Hot-Connect group, its location is restricted to the current position in the topology. The restriction can be removed by detaching the Hot-Connect group.

   .. figure:: ../Media/Hot-Connect_Engineer_Detach-Group.png
     :alt:

   After detaching the group, its floating in the network and positioned at the end of slave tree:

   .. figure:: ../Media/Hot-Connect_Engineer_Floating-Group.png
     :alt: