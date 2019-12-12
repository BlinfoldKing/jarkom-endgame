import argparse
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
import os

class Topologi:
    def __init__(self):
        setLogLevel('info')
        "Create custom topo."
	os.system("mn -c")
	self.net = Mininet(link=TCLink)
        # Add hosts and switches
        self.h1=self.net.addHost('h1',ip='192.168.1.2/24',mac = '00:00:00:00:00:01')
        self.h2=self.net.addHost('h2',ip='192.168.0.2/24',mac = '00:00:00:00:00:02')
        self.r1=self.net.addHost('r1')

        # Add links
        self.net.addLink(self.h1, self.r1,bw=2,max_queue_size=20)
        self.net.addLink(self.r1, self.h2,bw=1000,max_queue_size=20)
	self.net.build()

	#Server Config
	self.r1.cmd("ifconfig r1-eth0 0")
	self.r1.cmd("ifconfig r1-eth1 0")
	self.r1.cmd("ifconfig r1-eth0 hw ether 00:00:00:00:00:01")
	self.r1.cmd("ifconfig r1-eth1 hw ether 00:00:00:00:00:02")
	self.r1.cmd("ip addr add 192.168.1.1/24 brd + dev r1-eth0")
	self.r1.cmd("ip addr add 192.168.0.1/24 brd + dev r1-eth1")
	
	self.r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	
	self.h1.cmd("ip route add default via 192.168.1.1")
	self.h2.cmd("ip route add default via 192.168.0.1")

    def congestion(self, algo):
        self.h1.cmd("sysctl -w net.ipv4.tcp_congestion_control="+algo)
	self.h2.cmd("sysctl -w net.ipv4.tcp_congestion_control="+algo)
   
    def run(self):
        #Jalankan CLI
	CLI(self.net)
        self.net.stop()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", default="cubic")

    args = parser.parse_args()
    a = args.a
    print a
    t = Topologi()
    if a == "cubic" or a == "reno":
        print "set cubic as congestion"
        t.congestion(a)
    else:
        print "unknown congestion"
    t.run()


