# Python port scanning script

import serial.tools.list_ports
import json

def scan_usb_ports():
    usb_devices = []
    ports = list(serial.tools.list_ports.comports())
    
    for port in ports:
        device_info = {
            "device_name": port.device,
            "device_description": port.description,
            "device_hwid": port.hwid,
            "device_vid": port.vid,
            "device_pid": port.pid,
            "device_serial_number": port.serial_number,
        }
        usb_devices.append(device_info)

        num_devices = len(ports)
        
    return usb_devices, num_devices

def print_usb_devices(usb_devices):
    for device in usb_devices:
        print("Device Name:", device["device_name"])
        print("Description:", device["device_description"])
        print("HWID:", device["device_hwid"])
        print("VID:", device["device_vid"])
        print("PID:", device["device_pid"])
        print("Serial Number:", device["device_serial_number"])
        print()

def getDevicePorts(usb_devices):
    with open('devices.json') as json_file:
        data = json.load(json_file)

    for device in usb_devices:
        if "USB-SERIAL CH340" in device["device_description"]:
            MFC_PORT = device["device_name"]
        elif "Prolific PL2303GT USB Serial COM Port" in device["device_description"]:
            THERMOTRON_PORT = device["device_name"]

    return MFC_PORT,THERMOTRON_PORT

# end of script