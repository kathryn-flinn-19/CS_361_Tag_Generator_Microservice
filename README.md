# CS_361_Tag_Generator_Microservice

# Requesting data from the microservice:
1. Download ZMQ
2. Import zmq and json to your program
3. Set up a socket and connect to tcp://localhost:8932
4. Set up your photo data as an _object_, then use json.dumps() to convert it to a string

   Example photo data format:

   ```
    photo_data = {
                    "title": "My Photo Title",              # REQUIRED FIELD
                    "date": "Photo date (any format)",      # optional field; may be excluded
                    "location": "txt",                      # optional field; may be excluded
                    "notes": "txt"                          # optional field; may be excluded
                 }
   ```
   
5. Use socket.send_string() to send the photo data to the microservice

    Python example:

    ```
      import zmq
      import json

      context = zmq.Context()
      socket = context.socket(zmq.REQ)
      socket.connect("tcp://localhost:8932")

      photo_data = {
                    "title": "Penguins",               
                    "date": "December 30, 2024",      
                    "location": "Monterey Bay Aquarium",                      
                    "notes": "Feeding time for the penguins!!"                          
                 }

      str_to_send = json.dumps(photo_data)
      socket.send_string(str_to_send)
    ```

# Receiving data from the microservice:
1. Follow the instructions in [Requesting data from the microservice](#requesting-data-from-the-microservice)
2. Call socket.recv() to receive the microservice's response.
3. Use .decode() on the recv'd message to make it usable. Note that the microservice sends a _string_ as a response.

   Python example:

   ```
    import zmq
    import json

    # code to send data to microservice --- see above

    response = socket.recv()
    decoded = response.decode()      # decoded now holds a string!
   ```

   Note that the microservice sends the data as a _string_ where distinct tags are separated by semicolons. Each tag may be multiple words.

     Example format:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tag1;tag2;tag3;tag4
   
# UML Sequence Diagram:
<img width="1539" height="1151" alt="image" src="https://github.com/user-attachments/assets/b06592a2-180b-4b23-885f-ff772332a6ec" />
