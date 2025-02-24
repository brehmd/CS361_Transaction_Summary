# CS361_Transaction_Summary

## REQUEST data
1. From your main program, initialize a zmq socket which will connect with the microservice for Transaction_Summary.
   ```
   context = zmq.Context()
   socket = context.socket(zmq.REQ)
   socket.connect("tcp://localhost:5555")
   ```
2. Use the socket to SEND a request to the microservice in the form of "summary {number of days}" or "end 0". The string must be encoded to be passed through the socket so either use 'b"summary 7"' or use `str.encode(stringVar)` within the send() function
   ```
   days = 30
   req = f"summary {days}"
   socket.send(str.encode(req))
   ```

In full, your code may look like the following for a request:
   ```
   days = 30
   req = f"summary {days}"
   context = zmq.Context()
   socket = context.socket(zmq.REQ)
   socket.connect("tcp://localhost:5555")
   socket.send(str.encode(req))
   ```

## RECEIVE data
From your main program use the built-in socket `.receive()` function to return an encoded string from the microservice. All that is left is to decode it and then likely print the string that was returned.
```
summary = socket.recv()
print(summary.decode())
```

## UML Sequence Diagram

