from xml.dom import minidom
from xml.dom import Node
import re

# Filter for functions in header files
filterListHeaderFiles = [
  "EcMaster.h",
  "EcMonitor.h",
  "EcSimulator.h",
  "EcRasServer.h",
  "EcMqttServer.h",
  "EcMotionAdvanced.h"
]
whiteListFunctionsHeader = [
  "emSetOemKey",
  "emBadConnectionsReset",  
  "esSetOemKey",
  "ecat"
]
filterListSourceFiles = [
  "EcPerfMeas.cpp",
  "EcMasterApi.cpp",
]
blackListFunctionSource = [
  "ecat",
]

# Filter for doxygengroups
filterListGroups = [
  "_SZTXT_E_",
  "_SZTXT_EVT_"
]

filterListEnumValues = [ 
  "BCppDummy",
  "eEthTap_Hilscher_netANALYZER",
]

# Helper to get string from text node
def getTextNodeData(p):
  for n in p.childNodes:
    if n.nodeType == Node.TEXT_NODE:
      return n.data
      
  return ""

def filterFunction(compound, whiteList=None, blackList=None):
  for member in compound.getElementsByTagName("member"):
    if member.getAttribute("kind") == "function":
      memberName = getTextNodeData(member.getElementsByTagName("name")[0])

      removeMember = False
      if whiteList:
        removeMember |= not any(regex.match(memberName) for regex in map(re.compile, whiteList))
      if blackList:
        removeMember |= any(regex.match(memberName) for regex in map(re.compile, blackList))

      if removeMember:
        parent = member.parentNode
        parent.removeChild(member)

      
xmldoc = minidom.parse("index.xml")

# backup
with open("index.xml.org","w") as fs:
  fs.write(xmldoc.toxml())
  fs.close()

# filter functions from header files
for compound in xmldoc.getElementsByTagName("compound"):
  compoundName = getTextNodeData(compound.getElementsByTagName("name")[0])
  if compoundName in filterListHeaderFiles:
    filterFunction(compound, whiteList=whiteListFunctionsHeader)
  if compoundName in filterListSourceFiles:
    filterFunction(compound, blackList=blackListFunctionSource)

# filter defines from doxygen groups
for compound in xmldoc.getElementsByTagName("compound"):
  if compound.getAttribute("kind") == "group":
    subXmlDoc = None
    compoundRefId = compound.getAttribute("refid")
    for member in compound.getElementsByTagName("member"):
      memberName = getTextNodeData(member.getElementsByTagName("name")[0])
      if any(s in memberName for s in filterListGroups):
        # open group specific xml and backup
        if subXmlDoc == None:
          subXmlDoc = minidom.parse(compoundRefId + ".xml")
          with open(compoundRefId + ".xml.org","w") as fs:
            fs.write(subXmlDoc.toxml())
            fs.close()
        # remove member definitions from group xml
        for memberdef in subXmlDoc.getElementsByTagName("memberdef"):
          memberdefName = getTextNodeData(memberdef.getElementsByTagName("name")[0])
          if memberdefName == memberName:
            parent = memberdef.parentNode
            parent.removeChild(memberdef)
    # save changes to group xml
    if subXmlDoc != None:
      with open(compoundRefId + ".xml","w") as fs:
        fs.write(subXmlDoc.toxml())
        fs.close()

# filter enum values
for compound in xmldoc.getElementsByTagName("compound"):
  if compound.getAttribute("kind") == "file":
    subXmlDoc = None
    compoundRefId = compound.getAttribute("refid")
    for member in compound.getElementsByTagName("member"):
      if member.getAttribute("kind") == "enumvalue":
        memberName = getTextNodeData(member.getElementsByTagName("name")[0])
        enumRefId = member.getAttribute("refid")
        if any(s in memberName for s in filterListEnumValues):
          # open specific xml and backup
          if subXmlDoc == None:
            subXmlDoc = minidom.parse(compoundRefId + ".xml")
            with open(compoundRefId + ".xml.org","w") as fs:
              fs.write(subXmlDoc.toxml())
              fs.close()
          # remove enum value from xml
          for enumvalue in subXmlDoc.getElementsByTagName("enumvalue"):
            if enumRefId == enumvalue.getAttribute("id"):
              parent = enumvalue.parentNode
              parent.removeChild(enumvalue)
    # save changes
    if subXmlDoc != None:
      with open(compoundRefId + ".xml","w") as fs:
        fs.write(subXmlDoc.toxml())
        fs.close()

# clean pages
for compound in xmldoc.getElementsByTagName("compound"):
  if compound.getAttribute("kind") == "page":
    compoundRefId = compound.getAttribute("refid")
    # open specific xml and backup
    subXmlDoc = minidom.parse(compoundRefId + ".xml")
    with open(compoundRefId + ".xml.org","w") as fs:
      fs.write(subXmlDoc.toxml())
      fs.close()
    # clean varlistentry/term
    for varlistentry in subXmlDoc.getElementsByTagName("varlistentry"):
      term = varlistentry.getElementsByTagName("term")[0]
      varlistentry.removeChild(term)
      varlistentry.appendChild(xmldoc.createElement("term"))
    # save changes
    with open(compoundRefId + ".xml","w") as fs:
      fs.write(subXmlDoc.toxml())
      fs.close()

# save changes
with open("index.xml","w") as fs:
  fs.write(xmldoc.toxml())
  fs.close()