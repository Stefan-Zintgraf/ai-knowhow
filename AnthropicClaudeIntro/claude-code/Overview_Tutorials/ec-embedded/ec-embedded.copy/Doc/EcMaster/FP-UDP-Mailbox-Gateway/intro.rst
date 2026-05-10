************
Introduction
************

The Mailbox Gateway is a functionality of the EtherCAT Master to access
EtherCAT devices within an EtherCAT network from an application outside
the EtherCAT network.

It is following the Function Guideline `ETG.8200 EtherCAT Mailbox
Gateway`.

All Mailbox protocols defined in the EtherCAT specification can be used
in general, i.e. CoE, FoE, VoE, SoE.

There is no error handling specified for the Mailbox Gateway
functionality. A request to a non-existing slave device can lead to no
response from the master.

Running the Mailbox Gateway Server on the top of EC-Master makes
possible to use for example the Beckhoff TwinSafe Loader to apply the
configuration to the safety devices.

To reduce development effort the Mailbox Gateway Server is provided by
RAS library, but has to be licensed separately.
