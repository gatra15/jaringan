#!/usr/bin/python
 
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
 
def myNetwork():
 
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
    h1 = net.addHost('h1', cls=Host, ip='192.168.1.2/24', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='192.168.3.2/24', defaultRoute=None)
    
    info( '*** Add links\n')
    net.addLink(h1, r1)
    net.addLink(h1, r2)
    net.addLink(r1, r3)
    net.addLink(r1, r4)
    net.addLink(h2, r3)
    net.addLink(h2, r4)
    net.addLink(r2, r4)
    net.addLink(r2, r3)
    
    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()
 
    info( '*** Starting switches\n')
    h1.cmd('ifconfig h1-eth0 0')
    h1.cmd('ifconfig h1-eth1 0')
    h2.cmd('ifconfig h2-eth0 0')
    h2.cmd('ifconfig h2-eth1 0')
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
    h1.cmd('ifconfig h1-eth0 192.168.1.2/24')
    h1.cmd('ifconfig h1-eth1 192.168.2.2/24')
    h2.cmd('ifconfig h2-eth0 192.168.3.2/24')
    h2.cmd('ifconfig h2-eth0 192.168.4.2/24')
    r1.cmd('ifconfig r1-eth0 192.168.1.1/24')
    r1.cmd('ifconfig r1-eth1 10.10.10.1/30')
    r1.cmd('ifconfig r1-eth2 10.10.20.1/30')
    r2.cmd('ifconfig r2-eth0 192.168.2.1/24')
    r2.cmd('ifconfig r2-eth1 20.20.10.1/30')
    r2.cmd('ifconfig r2-eth2 20.20.20.1/30')
    r3.cmd('ifconfig r3-eth0 192.168.3.1/24')
    r3.cmd('ifconfig r3-eth1 10.10.10.2/30')
    r3.cmd('ifconfig r3-eth2 20.20.20.2/30')
    r4.cmd('ifconfig r4-eth0 192.168.4.1/24')
    r4.cmd('ifconfig r4-eth1 20.20.10.2/30')
    r4.cmd('ifconfig r4-eth2 10.10.20.2/30')
 
    r1.cmd('route add -net 192.168.3.0/24 gw 10.10.10.2')
    r1.cmd('route add -net 20.20.10.0/30 gw 10.10.20.2')
    r1.cmd('route add -net 20.20.20.0/30 gw 10.10.10.2')
    r1.cmd('route add -net 192.168.4.0/24 gw 10.10.20.2')
    r2.cmd('route add -net 192.168.3.0/24 gw 20.20.20.2')
    r2.cmd('route add -net 192.168.4.0/24 gw 20.20.10.2')
    r2.cmd('route add -net 10.10.20.0/30 gw 20.20.10.2')
    r2.cmd('route add -net 10.10.10.0/30 gw 20.20.20.2') 
    r3.cmd('route add -net 192.168.1.0/24 gw 10.10.10.1')
    r3.cmd('route add -net 192.168.2.0/24 gw 20.20.20.1')
    r3.cmd('route add -net 10.10.20.0/30 gw 10.10.10.1')
    r3.cmd('route add -net 20.20.10.0/30 gw 20.20.20.1')
    r4.cmd('route add -net 192.168.1.0/24 gw 10.10.20.1')
    r4.cmd('route add -net 192.168.2.0/24 gw 20.20.10.1')
    r4.cmd('route add -net 10.10.10.0/30 gw 10.10.20.1')
    r4.cmd('route add -net 20.20.10.0/30 gw 20.20.10.1')
    h1.cmd("ip rule add from 192.168.1.2 table 1")
    h1.cmd("ip rule add from 192.168.2.2 table 2")
    h1.cmd("ip route add 192.168.1.0/24 dev h1-eth0 scope link table 1")
    h1.cmd("ip route add default via 192.168.1.1 dev h1-eth0 table 1")
    h1.cmd("ip route add 192.168.2.0/24 dev h1-eth1 scope link table 2")
    h1.cmd("ip route add default via 192.168.2.1 dev h1-eth1 table 2")
    #h1.cmd("ip route add default scope global nexthop via 192.168.1.1 dev h1-eth0") 
    h2.cmd("ip rule add from 192.168.3.2 table 1")
    h2.cmd("ip rule add from 192.168.4.2 table 2")
    h2.cmd("ip route add 192.168.3.0/24 dev h2-eth0 scope link table 1")
    h2.cmd("ip route add default via 192.168.3.1 dev h2-eth0 table 1")
    h2.cmd("ip route add 192.168.4.0/24 dev h2-eth1 scope link table 1")
    h2.cmd("ip route add default via 192.168.4.1 dev h2-eth1 table 2")
    #h2.cmd("ip route add default scope global nexthop via 10.0.1.1 dev h2-eth0")
 
    CLI(net)
    net.stop()
 
if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
 