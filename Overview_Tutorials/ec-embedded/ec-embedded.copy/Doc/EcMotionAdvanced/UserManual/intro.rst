************
Introduction
************

General
*******

The goal of a motion control library is the hardware independent implementation of movement
commands. It should be easy to use in terms of installation, maintenance and application
programming. Furthermore an efficient design increases the understanding and consistency
of the code. Future extensions are possible without any problems and the scope of the
library is not mandatory but sufficiently complete.

EC-Motion-Advanced is a motion control solution supporting EtherCAT. The main component is
an abstractation of an axis object which could be a drive controlled over EtherCAT or a
virtual drive. With the help of motion control function blocks designed as C++ classes
orders are commanded to an axis. One distinguishes between motion and administrative
function blocks. All internal tasks such as trajectory generation, interpolation
and state machines are hidden from the user in this way.

EC-Motion-Advanced is targeted to work in conjunction with the acontis EC-Master
(EtherCAT Master library) but the library is not mandatory.

For optimal use of EC-Motion-Advanced, it is highly recommended to familiarize
yourself with the `EC-Master user manual <https://developer.acontis.com/ec-master>`_
and the User Manual of your drive.

The EC-Motion-Advanced - Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

EC-Motion-Advanced supports the CANopen device profile CiA® 402 for drives and motion
control. The physical communication channel is EtherCAT and the CiA 402 protocol is mapped
to EtherCAT according to IEC 61800-7-300 as “drive profiles”.

.. kroki::
    :type: tikz
    :align: center
    :filename: ../Media/Overview.tex
    :caption: EtherCAT servo drive profiles

In addition EC-Motion-Advanced provides virtual axes with no hardware or protocol in the
background.

Open Source Software
********************

EC-Motion-Advanced contains no free open source software.

Versioning
**********

EC-Motion-Advanced follows the same versioning scheme as the
`EC-Master <https://public.acontis.com/manuals/EC-Master/3.2/html/ec-master-class-b/intro.html#versioning>`_:
**V**\ *MAJOR*\ **.** \ *MINOR*\ **.** \ *SERVICEPACK*\ **.** \ *BUILD* (e.g. V3.2.1.04).

The libraries are binary compatible by unchanged *MAJOR* and *MINOR* digits. If *SERVICEPACK* increments, *BUILD* restarts with 01.
*BUILD* 99 is reserved for test builds that have not been officially released for productive usage.
