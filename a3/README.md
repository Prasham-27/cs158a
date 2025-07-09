# CS158a - Assignment 3: Leader Election in a Ring

This project implements the O(n²) leader election algorithm for an asynchronous ring of processes. Each process (`myleprocess.py`) acts as both a client and a server, forming a node in a distributed ring. On startup, each process generates a unique ID (UUID) and participates in an election to designate a single leader. Communication is done via JSON-serialized messages over TCP sockets.

## How to Run the Local Demo

To demonstrate the leader election with three nodes on a single machine, you will need to open **three separate terminal windows**.

### 1. Prerequisite Files

Before running, ensure you have three configuration files in your project directory to form the ring.

**`config1.txt`**
```
127.0.0.1,5001
127.0.0.1,5002
```

**`config2.txt`**
```
127.0.0.1,5002
127.0.0.1,5003
```

**`config3.txt`**
```
127.0.0.1,5003
127.0.0.1,5001
```

### 2. Execution

Navigate to the project directory (`a3`) in each of the three terminals. Then, run the following commands, one in each terminal, in quick succession.

**Terminal 1:**
```bash
python3 myleprocess.py config1.txt log1.txt
```

**Terminal 2:**
```bash
python3 myleprocess.py config2.txt log2.txt
```

**Terminal 3:**
```bash
python3 myleprocess.py config3.txt log3.txt
```

The scripts will connect to each other, perform the election, print logs to the console and respective log files, and terminate after agreeing on a leader.

## Execution Example

Below is the sample output from a successful run across the three terminals.

### Terminal 1 Output (Process 1)
```
2025-07-09 09:36:19,779 - My Process UUID is a00ee5e2-ad2a-4e5c-bfce-0eddac0a408c
2025-07-09 09:36:19,779 - Server listening on 127.0.0.1:5001
2025-07-09 09:36:21,784 - Connected to client at 127.0.0.1:5002
2025-07-09 09:36:21,786 - Sent: uuid=a00ee5e2-ad2a-4e5c-bfce-0eddac0a408c, flag=0
2025-07-09 09:36:23,854 - Accepted connection from ('127.0.0.1', 55826)
2025-07-09 09:36:23,855 - Received: uuid=62eab4cd-917a-40ca-965e-350938343a20, flag=0, less, 0
2025-07-09 09:36:23,855 - Ignoring message, received UUID is smaller.
2025-07-09 09:36:23,856 - Received: uuid=dfb188e6-eb5e-4f8f-9531-9d315736e959, flag=0, greater, 0
2025-07-09 09:36:23,856 - Sent: uuid=dfb188e6-eb5e-4f8f-9531-9d315736e959, flag=0
2025-07-09 09:36:23,859 - Received: uuid=dfb188e6-eb5e-4f8f-9531-9d315736e959, flag=1, greater, 0
2025-07-09 09:36:23,859 - Leader is decided to dfb188e6-eb5e-4f8f-9531-9d315736e959
2025-07-09 09:36:23,859 - Sent: uuid=dfb188e6-eb5e-4f8f-9531-9d315736e959, flag=1
2025-07-09 09:36:23,859 - Server thread finished.
2025-07-09 09:36:25,955 - Process finished.
Leader is dfb188e6-eb5e-4f8f-9531-9d315736e959
```

### Terminal 2 Output (Process 2)
```
2025-07-09 09:36:20,542 - My Process UUID is dfb188e6-eb5e-4f8f-9531-9d315736e959
2025-07-09 09:36:20,543 - Server listening on 127.0.0.1:5002
2025-07-09 09:36:21,785 - Accepted connection from ('127.0.0.1', 55822)
2025-07-09 09:36:21,786 - Received: uuid=a00ee5e2-ad2a-4e5c-bfce-0eddac0a408c, flag=0, less, 0
2025-07-09 09:36:21,786 - Ignoring message, received UUID is smaller.
2025-07-09 09:36:22,549 - Connected to client at 127.0.0.1:5003
2025-07-09 09:36:22,550 - Sent: uuid=dfb188e6-eb5e-4f8f-9531-9d315736e959, flag=0
2025-07-09 09:36:23,858 - Received: uuid=dfb188e6-eb5e-4f8f-9531-9d315736e959, flag=0, same, 0
2025-07-09 09:36:23,859 - Leader is decided to dfb188e6-eb5e-4f8f-9531-9d315736e959
2025-07-09 09:36:23,859 - Sent: uuid=dfb188e6-eb5e-4f8f-9531-9d315736e959, flag=1
2025-07-09 09:36:23,859 - Server thread finished.
2025-07-09 09:36:25,881 - Process finished.
Leader is dfb188e6-eb5e-4f8f-9531-9d315736e959
```

### Terminal 3 Output (Process 3)
```
2025-07-09 09:36:21,848 - My Process UUID is 62eab4cd-917a-40ca-965e-350938343a20
2025-07-09 09:36:21,848 - Server listening on 127.0.0.1:5003
2025-07-09 09:36:22,549 - Accepted connection from ('127.0.0.1', 55824)
2025-07-09 09:36:22,550 - Received: uuid=dfb188e6-eb5e-4f8f-9531-9d315736e959, flag=0, greater, 0
2025-07-09 09:36:23,854 - Connected to client at 127.0.0.1:5001
2025-07-09 09:36:23,854 - Sent: uuid=62eab4cd-917a-40ca-965e-350938343a20, flag=0
2025-07-09 09:36:23,855 - Sent: uuid=dfb188e6-eb5e-4f8f-9531-9d315736e959, flag=0
2025-07-09 09:36:23,859 - Received: uuid=dfb188e6-eb5e-4f8f-9531-9d315736e959, flag=1, greater, 0
2025-07-09 09:36:23,859 - Leader is decided to dfb188e6-eb5e-4f8f-9531-9d315736e959
2025-07-09 09:36:23,859 - Sent: uuid=dfb188e6-eb5e-4f8f-9531-9d315736e959, flag=1
2025-07-09 09:36:23,859 - Server thread finished.
2025-07-09 09:36:25,964 - Process finished.
Leader is dfb188e6-eb5e-4f8f-9531-9d315736e959
```

**Result:** All three processes successfully and correctly elected the process with the highest UUID (`dfb188e6-eb5e-4f8f-9531-9d315736e959`) as the leader.
