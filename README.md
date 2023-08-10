# p4-multiqueue
Virtual Machine with p4 and multiqueue (bmv2) using mininet

In this github we teach you how to get your own mininet running p4 code with multiple queues inside bmv2.
The easiest way is to download our Virtual Machine, avaiable in **Option 1**, but you can follow our step by step tutorial to have your own machine running mininet with multiqueue in **Option 2**

## Option 1
You can download our Virtual Machine in [this link](https://drive.google.com/file/d/1k-QrubUFgCbdEahJZdQ0aoEi4tixcrm9/view?usp=sharing) this link. The base VM used is from mininet releases in [this link](https://github.com/mininet/mininet/releases/).

### Topology
<img src="https://github.com/dcomp-leris/p4-multiqueue/blob/main/Topology.png" alt="P4 Topology, including two switches and two hosts">

### How to run

```
cd /home/p4/labs/int/
```
```
sudo ./run_int.sh
```

This will get mininet to raise the topology specified above, with 2 hosts and 2 switches and with a simple INT based on [this link](https://github.com/dcomp-leris/InbandNetworkTelemetry-P4). 

With the mininet working, you can start to send packets using the send.py file on host 1 and to receive packets using the receive.py file on host 2. That can be done like this:


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

Congratulations! Now you have your own mininet running p4 programs that support multiple queues on bmv2!
Now you can use your own p4 files to use the priority-queues and change the qid.
You can change the topology by changing the topo.txt file, adding more hosts, more switches and new connections.

HINT: If you're having problems with packet forwarding you can see both switches log. It can be found on /tmp/p4s.s1.log for switch 1 and tmp/p4s.s2.log for switch 2.

## Option 2
By choosing this option you can follow this step by step to get your own machine to work with priority-queues inside bmv2.
Note: Your machine should have installed [bmv2](https://github.com/p4lang/behavioral-model), [mininet](https://github.com/mininet/mininet) and [p4c](https://github.com/p4lang/p4c).

### Step 1
First off all, you need to follow [these steps](https://github.com/nsg-ethz/p4-learning/tree/master/examples/multiqueueing). This will allow your bmv2 and the compiler to be able to support multiqueueing inside bmv2

### Step 2
You should now go to PATH_TO_BMV2/mininet and edit p4_mininet.py file. You can get a VM ready with all of that [these steps](https://github.com/mininet/mininet/releases/).

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

After following these steps your mininet is ready to allow your p4 codes with multiple queues in bmv2!
