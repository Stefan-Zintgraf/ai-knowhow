*****************************
Diagnosis and troubleshooting
*****************************

Logs
 The EcEoeGateway logs should be considered before any other diagnosis.

Network verification:
 Begin by pinging the EoE devices (e.g.192.168.2.2) with the -s 0 option to send raw packets. If it fails, verify that the TAP connection’s status is connected and the send/receive statistics reflect the requests using the ifconfig command. If not, check that the IP addresses are correct (see IPv4 configuration above) and that the connection to the RAS service is established (see below).

Service and software checks 
 Utilize the netstat command to confirm an established connection between the systems. If the connection is not established, check if the eceoegateway service is running. If the eceoegateway service is running, inspect log files for any error messages that might indicate the root cause of the issue.

EtherCAT specific checks 
 Check that the slave's EtherCAT state is PREOP, SAFEOP, or OP using e.g. EC-Engineer. If the state is correct, analyze the EtherCAT traffic to identify using filter “ecat_mailbox.eoe”.

Network setup review
 Finally, assess the need for routing and firewall configurations that might be interfering with the connection. Ensure these network components are configured to support the TAP adapter and the connection to the RAS server.
