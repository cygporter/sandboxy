#!/usr/bin/env python3

from tempfile import NamedTemporaryFile
import xml.etree.ElementTree as ET
from typing import Optional, Union
import subprocess
import os

def mapped_folder_xml(host_folder: str,
                      sandbox_folder: Optional[str] = None,
                      read_only: Optional[bool] = None,
                      ) -> ET.Element:
    element = ET.Element('MappedFolder')
    ET.SubElement(element, 'HostFolder').text = host_folder
    if sandbox_folder is not None:
        ET.SubElement(element, 'SandboxFolder').text = sandbox_folder
    if read_only is not None:
        ET.SubElement(element, 'ReadOnly').text = str(read_only).lower()
    return element


if __name__ == "__main__":
    root = ET.Element('Configuration')
    mapped_folders = ET.SubElement(root, 'MappedFolders')
    mapped_folders.append(mapped_folder_xml(r'C:\Users\adinwoodie\Downloads', r'C:\Users\WDAGUtilityAccount\Downloads', False))
    mapped_folders.append(mapped_folder_xml(r'C:\cygwin64\home\adinwoodie\vcs\cygporter\python-pycurl', read_only=False))
    logon_commands = ET.SubElement(root, 'LogonCommand')
    command = ET.SubElement(logon_commands, 'Command')
    command.text = r'C:\Users\WDAGUtilityAccount\Downloads\setup-x86_64.exe -s https://www.mirrorservice.org/sites/sourceware.org/pub/cygwin/ -l C:\Users\WDAGUtilityAccount\Downloads\ -qP cygport,libcurl-devel,libssl-devel,python38-wheel,python38-devel,python38-exceptiongroup,python39-devel,python39-wheel,python39-exceptiongroup'
    tree = ET.ElementTree(root)
    with NamedTemporaryFile(suffix=".wsb", delete=False) as wsb_file:
        tree.write(wsb_file)
    print(wsb_file.name)
    subprocess.run(('cygstart', '-w', wsb_file.name))
    os.unlink(wsb_file.name)
