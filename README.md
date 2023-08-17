# p4-multiqueue
Virtual Machine with p4 and multiqueue (BMv2) using mininet.

In this github, we teach you how to get your own mininet running p4 code with multiple queues inside BMv2.
The easiest way is to download our Virtual Machine, available in **Option 1**, but you can follow our step-by-step tutorial to have your own machine running mininet with multiqueues in **Option 2**.

## Option 1
You can download our Virtual Machine in [this link](https://drive.google.com/file/d/1tb9hyiilT05lqAkQXTvaHiJtn9SA2tRs/view?usp=sharing). The base VM used is from mininet releases in [this link](https://github.com/mininet/mininet/releases/).

There are two users in this VM, you can choose to login on any.
P4 User has the lab for the priority-queues, including the p4 files and the python scripts, including the topology.
Vagrant User has BMv2, p4c and mininet files.


Login: p4

password: p4

Login: vagrant

password: vagrant

### Topology
<img src="https://github.com/dcomp-leris/p4-multiqueue/blob/main/Topology.png" alt="P4 Topology, including two switches and two hosts">

### How to run

```
cd /home/p4/labs/int/
```
```
sudo ./run_priority_queues.sh
```

This will get mininet to raise the topology specified above, with 2 hosts and 2 switches and with a simple IPv4 forwarding, with the priority-queues enabled on BMv2.

The p4 file for this lab consists on checking the IP destination on ```qid_table``` in the control plane to define the qid. On this example, if the destination is host 2 (IP = 10.0.1.10), then the priority is set to 1 by the action ```qid_change()```, else, if the destination is host 1 (IP = 10.0.0.10), then the priority is set to 0, changing the value of ```standard_metadata.priority```. The sender ```send_h1.py``` is responsible for creating packets to send to the destination and the switch appends the values of the qids for each node, couting each node value on ```nodeCount``` header and storing the switch ID and the values of priority and qid in the packets. You can change and test the qid value by changing it on ```command_s1.txt``` or ```command_s2.txt``` files.

With the mininet working, you can start to send packets using the sender file on host 1 and to receive packets using the receiver file on host 2. That can be done like this:


```
xterm h1 h2
```
On h2 terminal, run this:
```
sudo ./receive_h2.py
```

On h1 terminal, run this:
```
sudo ./send_h1.py 10.0.1.10
```

Congratulations! Now you have your own mininet running p4 programs that support multiple queues on BMv2!
Now you can use your own p4 files to use the priority-queues and change the qid.
You can change the topology by changing the topo.txt file, adding more hosts, more switches and new connections.

HINT: If you're having problems with packet forwarding you can see both switches log. It can be found on ```/tmp/p4s.s1.log``` for switch 1 and ```tmp/p4s.s2.log``` for switch 2.

## Option 2
By choosing this option you can follow this step-by-step to get your own machine to work with priority-queues inside BMv2.

Note: Your machine should have installed [BMv2](https://github.com/p4lang/behavioral-model), [mininet](https://github.com/mininet/mininet) and [p4c](https://github.com/p4lang/p4c).


We recommend you to download the same VM as we did. You can get this VM ready with BMv2, p4c and mininet [here](https://github.com/jafingerhut/p4-guide/blob/master/bin/README-install-troubleshooting.md). You can download the same version as ours directly from [this link](https://drive.google.com/file/d/1_1CCNnJeQRpAfhTpw-m2LZ2T97QWgKp8/view?pli=1). If you chose this VM, just proceed to Step 1 below.

To download and install BMv2, p4c and mininet inside your machine you should run these commands:
``` 
git clone https://github.com/p4lang/behavioral-model

sudo apt-get install -y automake cmake libgmp-dev \
    libpcap-dev libboost-dev libboost-test-dev libboost-program-options-dev \
    libboost-system-dev libboost-filesystem-dev libboost-thread-dev \
    libevent-dev libtool flex bison pkg-config g++ libssl-dev

cd behavioral-model
```

If you're on Ubuntu 22.04, run:
```
sudo ./install_deps_ubuntu_22.04.sh
```

If you're on Ubuntu 20.04, run:
```
sudo ./install_deps.sh
```

Now, you should install BMv2:
```
./autogen.sh
./configure
make
sudo make install
```

Now, for p4c, you should run:
```
cd .. #if you're on BMv2 folder

git clone --recursive https://github.com/p4lang/p4c.git

sudo apt-get install cmake g++ git automake libtool libgc-dev bison flex \
libfl-dev libboost-dev libboost-iostreams-dev \
libboost-graph-dev llvm pkg-config python3 python3-pip \
tcpdump

mkdir build
cd build
cmake .. <optional arguments>
make -j4
make -j4 check
sudo make install
```

Now with p4c you can compile your P4 programs.

Now, you must download and install mininet following the steps on [this link](https://github.com/mininet/mininet).

With BMv2, p4c and mininet in your machine you can proceed the following steps:

### Step 1
First of all, you need to follow [these steps](https://github.com/nsg-ethz/p4-learning/tree/master/examples/multiqueueing). This will allow your BMv2 and the compiler to be able to support multiqueueing inside BMv2.

### Step 2
You should now go to PATH_TO_BMV2/mininet and edit p4_mininet.py file. 

Look for this part of the code:
```
def start(self, controllers):
        "Start up a new P4 switch"
        info("Starting P4 switch {}.\n".format(self.name))
        args = [self.sw_path]
        for port, intf in self.intfs.items():
            if not intf.IP():
                args.extend(['-i', str(port) + "@" + intf.name])
        if self.pcap_dump:
            args.append("--pcap")
            # args.append("--useFiles")
        if self.thrift_port:
            args.extend(['--thrift-port', str(self.thrift_port)])
        if self.nanomsg:
            args.extend(['--nanolog', self.nanomsg])
        args.extend(['--device-id', str(self.device_id)])
        P4Switch.device_id += 1
        args.append(self.json_path)
        if self.enable_debugger:
            args.append("--debugger")
        if self.log_console:
            args.append("--log-console")
        print(args)
        logfile = "/tmp/p4s.{}.log".format(self.name)
        info(' '.join(args) + "\n")
```

Now, you have to add ``` args.append("-- --priority-queues 8")  ``` after the last if and get something like this:

```
def start(self, controllers):
        "Start up a new P4 switch"
        info("Starting P4 switch {}.\n".format(self.name))
        args = [self.sw_path]
        for port, intf in self.intfs.items():
            if not intf.IP():
                args.extend(['-i', str(port) + "@" + intf.name])
        if self.pcap_dump:
            args.append("--pcap")
            # args.append("--useFiles")
        if self.thrift_port:
            args.extend(['--thrift-port', str(self.thrift_port)])
        if self.nanomsg:
            args.extend(['--nanolog', self.nanomsg])
        args.extend(['--device-id', str(self.device_id)])
        P4Switch.device_id += 1
        args.append(self.json_path)
        if self.enable_debugger:
            args.append("--debugger")
        if self.log_console:
            args.append("--log-console")
        args.append("-- --priority-queues 8") #added here
        print(args)
        logfile = "/tmp/p4s.{}.log".format(self.name)
        info(' '.join(args) + "\n")
```

After following these steps your mininet is ready to allow your p4 codes with multiple queues in BMv2!
