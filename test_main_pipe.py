import time
import zmq

def getTransactionSummary(days):
    req = f"summary {days}"
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send(str.encode(req))
    
    summary = socket.recv()
    print(summary.decode())
    
def endTransactionSummary():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send(b"end 0")

if __name__ == "__main__":
    getTransactionSummary(7)
    time.sleep(5)
    getTransactionSummary(30)
    time.sleep(5)
    getTransactionSummary("all")
    time.sleep(5)
    
    endTransactionSummary()
