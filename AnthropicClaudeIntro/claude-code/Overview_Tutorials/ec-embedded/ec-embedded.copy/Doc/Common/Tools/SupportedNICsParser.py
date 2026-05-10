import glob
import re
import copy
from pathlib import Path
from os.path import isfile
import json
import xml.etree.ElementTree as ET
import argparse
import logging

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("basepath", help="Base path, e.g. ec-embedded/")
    parser.add_argument("jsonfile", help="Output json file, SupportedNICs.json")
    parser.add_argument('--debug', action='store_true', help='Enable debug log messages')
    args = parser.parse_args()
    
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
except Exception as e:
    print(f"{e}")


linklayer_blackList = [
  "emllSimulator",
  "emlli8254x",
  "emlleg20t",
  "emllrin32",
  "emllrtl8139",
  "emlltap",
  "emlleom"
]
linklayer_rename = {
  "emllSnarfGpp" : "emllSnarf"
}
os_rename = {}

os_list = set()
os_fingerprint_list = set()
linkos_os_map = {}
arch_list = set()
arch_fingerprint_list = set()
linklayer_list = set()
os_ll_arch_matrix = {}
ll_fingerprint_list = set()

logging.debug("Read os, arch, link layer from PackagesFileList")
for pkg_file_list in glob.glob(args.basepath + "/Build/70_Tests/SetupOutputTests/**/PackagesFileList.txt"):
  with open(pkg_file_list, "r") as file:
    logging.debug("  File: %s", pkg_file_list)
    for line in file:
      # skip empty lines
      if not line.strip():
        continue
        
      # read os name
      os = re.split("ARM|PPC|RISCV|x86", line)[0].strip("-")
      # rename os if neccesary
      if os in os_rename:
        os = os_rename[os]

      os_list.add(os)

      # read arch name
      arch = re.findall("ARM_32|ARM_64|PPC|RISCV_64|x86_32|x86_64", line)[0]
      arch_list.add(arch)
      
      # read link layer name
      ll = re.findall("emll[a-zA-Z0-9]*", line)
      if ll and not re.findall("\.h|\.c|\.cpp", line):
        ll = ll[0]
        
        # skip blacklisted link layer
        if ll.lower() in [ll_b.lower() for ll_b in linklayer_blackList]:
          continue
        
        if ll in linklayer_rename:
          ll = linklayer_rename[ll]
        
        linklayer_list.add(ll)
            
        # create os linklayer arch os_ll_arch_matrix
        if os not in os_ll_arch_matrix:
          os_ll_arch_matrix[os] = {}
        if ll not in os_ll_arch_matrix[os]:
          os_ll_arch_matrix[os][ll] = set()   
        os_ll_arch_matrix[os][ll].add(arch)
      
      # linkos 
      linkos = re.findall(r"([A-Za-z0-9_-]+)\\LinkOsPlatform.h", line)
      if linkos:
        linkos = linkos[0]
        if linkos not in linkos_os_map:
          linkos_os_map[linkos] = set()
        linkos_os_map[linkos].add(os)
      
# find duplicates with different case
linklayer_list_sorted = sorted(linklayer_list)
for i in range(len(linklayer_list_sorted)):
  for ll in linklayer_list_sorted[i+1:]:
    if linklayer_list_sorted[i].lower() == ll.lower():
      linklayer_list.remove(ll)     

# clean map from duplicates
tmp = copy.deepcopy(os_ll_arch_matrix)
for os in tmp:
  for ll in tmp[os]:
    if ll not in linklayer_list:
      del os_ll_arch_matrix[os][ll]

# sort lists
os_list = sorted(os_list)
arch_list = sorted(arch_list)
linklayer_list = sorted(linklayer_list)
for os in os_ll_arch_matrix:
  for ll in os_ll_arch_matrix[os]:
    os_ll_arch_matrix[os][ll] = sorted(os_ll_arch_matrix[os][ll])

logging.debug("Parse linklayer source for IRQ and fingerprint")
ll_irq_list = set()
for srcFile in glob.glob(args.basepath + "/Sources/LinkLayer/*/*.cpp", recursive=True):
  with open(srcFile, "r") as f:
    logging.debug("  File: %s", srcFile)
    for line in f:
      ll = "emll" + Path(srcFile).parent.name
      # irq support
      if re.search("pfReceiveFrameCallback[\)]*\(", line):
        if ll.lower() in [ll_tmp.lower() for ll_tmp in linklayer_list]:
          ll_irq_list.add(ll)
      # fingerprint support
      if re.search("EcFingerprint.h", line):
        if ll.lower() in [ll_tmp.lower() for ll_tmp in linklayer_list]:
          ll_fingerprint_list.add(ll)
ll_irq_list = sorted(ll_irq_list)
ll_fingerprint_list = sorted(ll_fingerprint_list)
#logging.debug(f"ll_fingerprint_list: {ll_fingerprint_list}")

logging.debug("Parse linkos interrupt support")
os_irq_list = set()
for srcFile in glob.glob(args.basepath + "/Sources/LinkOsLayer/*/*.cpp", recursive=True):
  with open(srcFile, "r") as f:
    logging.debug("  File: %s", srcFile)
    for line in f:
      if re.search("pfIrqOpen[\)]*\(", line):
        os = Path(srcFile).parent.name
        if os in linkos_os_map:
          os_irq_list.update(linkos_os_map[os])
os_irq_list = sorted(os_irq_list)

logging.debug("Parse fingerprint arch support")
with open(args.basepath + "/Doc/EcSupportedNics/_build/doxygen/xml/combined.xml") as doxy_xml:
  doxy_xml_root = ET.parse(doxy_xml).getroot()
  for arch in arch_list:
    logging.debug("  Arch: %s", arch)
    if doxy_xml_root.find("./compounddef[@kind='page']/[compoundname='EC_FINGERPRINT_" + arch.upper() +"']") is not None:
      arch_fingerprint_list.add(arch)
  for os in os_list:
    logging.debug("  Os: %s", os)
    if doxy_xml_root.find("./compounddef[@kind='page']/[compoundname='EC_FINGERPRINT_" + os.upper() +"']") is not None:
      os_fingerprint_list.add(os)

arch_fingerprint_list = sorted(arch_fingerprint_list)
os_fingerprint_list = sorted(os_fingerprint_list)
#logging.debug(f"\narch_fingerprint_list: {arch_fingerprint_list} \nos_fingerprint_list: {os_fingerprint_list}")

# export as json
matrix_list = {os: {ll: list(os_ll_arch_matrix[os][ll]) for ll in os_ll_arch_matrix[os]} for os in list(os_ll_arch_matrix)}
with open(args.jsonfile, "w") as json_file:
  json_output = {
    "os" : os_list,
    "os_irq" : os_irq_list,
    "os_fingerprint" : os_fingerprint_list,
    "arch" : arch_list,
    "arch_fingerprint" : arch_fingerprint_list,
    "linklayer" : linklayer_list,
    "linklayer_irq" : ll_irq_list,
    "linklayer_fingerprint" : ll_fingerprint_list,
    "matrix" : matrix_list}
  json.dump(json_output, json_file, indent=4)
