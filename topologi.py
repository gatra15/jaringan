#!/usr/bin/python
 
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
 
def myTopologi():
 
    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')
 
    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    r4 = net.addHost('r4', cls=Node, ip='0.0.0.0')
    info( '*** Add hosts\n')
    hA = net.addHost('hA', cls=Host, ip='0.0.0.0', defaultRouter=None)
    hB = net.addHost('hB', cls=Host, ip='0.0.0.0', defaultRoute=None)
    
    info( '*** Add links\n')
    net.addLink(hA, r1, cls=TCLink, bw=1)
    net.addLink(hA, r2, cls=TCLink, bw=1)
    net.addLink(hB, r3, cls=TCLink, bw=1)
    net.addLink(hB, r4, cls=TCLink, bw=1)
    net.addLink(r1, r3, cls=TCLink, bw=0.5)
    net.addLink(r2, r4, cls=TCLink, bw=0.5)
    net.addLink(r1, r4, cls=TCLink, bw=1)
    net.addLink(r2, r3, cls=TCLink, bw=1)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    hA.cmd('ifconfig hA-eth0 0')
    hA.cmd('ifconfig hA-eth1 0')
    hB.cmd('ifconfig hB-eth0 0')
    hB.cmd('ifconfig hB-eth1 0')
    r1.cmd('ifconfig r1-eth0 0')
    r1.cmd('ifconfig r1-eth1 0')
    r1.cmd('ifconfig r1-eth2 0')
    r2.cmd('ifconfig r2-eth0 0')
    r2.cmd('ifconfig r2-eth1 0')
    r2.cmd('ifconfig r2-eth2 0')
    r3.cmd('ifconfig r3-eth0 0')
    r3.cmd('ifconfig r3-eth1 0')
    r3.cmd('ifconfig r3-eth2 0')
    r4.cmd('ifconfig r4-eth0 0')
    r4.cmd('ifconfig r4-eth1 0')
    r4.cmd('ifconfig r4-eth2 0')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    info( '*** Post configure switches and hosts\n')
    hA.cmd('ifconfig hA-eth0 172.16.5.2/24')
    hA.cmd('ifconfig hA-eth1 172.16.10.2/24')
    hB.cmd('ifconfig hB-eth0 172.16.15.2/24')
    hB.cmd('ifconfig hB-eth1 172.16.20.2/24')
    r1.cmd('ifconfig r1-eth0 172.16.5.1/24')
    r1.cmd('ifconfig r1-eth1 50.50.10.1/30')
    r1.cmd('ifconfig r1-eth2 50.50.30.1/30')
    r2.cmd('ifconfig r2-eth0 172.16.10.1/24')
    r2.cmd('ifconfig r2-eth1 50.50.20.1/30')
    r2.cmd('ifconfig r2-eth2 50.50.40.1/30')
    r3.cmd('ifconfig r3-eth0 172.16.15.1/24')
    r3.cmd('ifconfig r3-eth1 50.50.10.2/30')
    r3.cmd('ifconfig r3-eth2 50.50.30.2/30')
    r4.cmd('ifconfig r4-eth0 172.16.20.1/24')
    r4.cmd('ifconfig r4-eth1 50.50.20.2/30')
    r4.cmd('ifconfig r4-eth2 50.50.40.2/30')

    r1.cmd('route add -net 172.16.15.0/24 gw 50.50.10.2')
    r1.cmd('route add -net 172.16.20.0/24 gw 50.50.30.2')
    r1.cmd('route add -net 50.50.20.0/30 gw 50.50.30.2')
    r1.cmd('route add -net 50.50.40.0/30 gw 50.50.10.2')
    r2.cmd('route add -net 172.16.15.0/24 gw 50.50.40.2')
    r2.cmd('route add -net 172.16.20.0/24 gw 50.50.20.2')
    r2.cmd('route add -net 50.50.10.0/30 gw 50.50.40.2')
    r2.cmd('route add -net 50.50.30.0/30 gw 50.50.20.2') 
    r3.cmd('route add -net 172.16.5.0/24 gw 50.50.10.1')
    r3.cmd('route add -net 172.16.10.0/24 gw 50.50.40.1')
    r3.cmd('route add -net 50.50.20.0/30 gw 50.50.40.1')
    r3.cmd('route add -net 50.50.30.0/30 gw 50.50.10.1')
    r4.cmd('route add -net 172.16.5.0/24 gw 50.50.30.1')
    r4.cmd('route add -net 172.16.10.0/24 gw 50.50.20.1')
    r4.cmd('route add -net 50.50.10.0/30 gw 50.50.30.1')
    r4.cmd('route add -net 50.50.40.0/30 gw 50.50.20.1')
    hA.cmd("ip rule add from 172.16.5.2 table 1")
    hA.cmd("ip rule add from 172.16.10.2 table 2")
    hA.cmd("ip route add 172.16.5.0/24 dev hA-eth0 scope link table 1")
    hA.cmd("ip route add default via 172.16.5.1 dev hA-eth0 table 1")
    hA.cmd("ip route add 172.16.10.0/24 dev hA-eth1 scope link table 2")
    hA.cmd("ip route add default via 172.16.10.1 dev hA-eth1 table 2")
    hA.cmd("ip route add default scope global nexthop via 172.16.5.1 dev hA-eth0") 
    hA.cmd("ip route add default scope global nexthop via 172.16.10.1 dev hA-eth1")
    hB.cmd("ip rule add from 172.16.15.2 table 1")
    hB.cmd("ip rule add from 172.16.20.2 table 2")
    hB.cmd("ip route add 172.16.15.0/24 dev hB-eth0 scope link table 1")
    hB.cmd("ip route add default via 172.16.15.1 dev hB-eth0 table 1")
    hB.cmd("ip route add 172.16.20.0/24 dev hB-eth1 scope link table 1")
    hB.cmd("ip route add default via 172.16.20.1 dev hB-eth1 table 2")
    hB.cmd("ip route add default scope global nexthop via 172.16.15.1 dev hB-eth0")
    hB.cmd("ip route add default scope global nexthop via 172.16.20.1 dev hB-eth1")

    CLI(net)
    net.stop()
 
if __name__ == '__main__':
    setLogLevel( 'info' )
    myTopologi()
 
