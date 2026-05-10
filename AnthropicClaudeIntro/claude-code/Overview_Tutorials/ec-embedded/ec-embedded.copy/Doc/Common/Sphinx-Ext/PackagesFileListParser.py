import glob
import re
import copy
import pathlib

linklayer_blackList = [
  "emllSimulator",
  "emlli8254x",
  "emlleom"
]
linklayer_rename = {
  "emllSnarfGpp" : "emllSnarf"
}
os_rename = {}

os_list = set()
arch_list = set()
linklayer_list = set()

def parseOsArchLinkLayerMapping(pathname):
  global os_list
  global arch_list
  global linklayer_list
  os_list = set()
  arch_list = set()
  linklayer_list = set()
  mapping = {}

  # read os, arch, link layer from PackagesFileList and store them in a map
  for pkgFileList in glob.glob(pathname):
    with open(pkgFileList, "r") as file:
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
              
          # create os linklayer arch mapping
          if os not in mapping:
            mapping[os] = {}
          if ll not in mapping[os]:
            mapping[os][ll] = set()   
          mapping[os][ll].add(arch)

  # find duplicates with different case
  linklayer_list_sorted = sorted(linklayer_list)
  for i in range(len(linklayer_list_sorted)):
    for ll in linklayer_list_sorted[i+1:]:
      if linklayer_list_sorted[i].lower() == ll.lower():
        linklayer_list.remove(ll)     
  # clean map from duplicates
  tmp = copy.deepcopy(mapping)
  for os in tmp:
    for ll in tmp[os]:
      if ll not in linklayer_list:
        del mapping[os][ll]

  os_list = sorted(os_list)
  arch_list = sorted(arch_list)
  linklayer_list = sorted(linklayer_list)

  return mapping