<b><h3># compass</h3></b>
A python based secure chat application
<p>
<b>Features:</b><br>
1.Encrypted Chat server</br>
2.Has dedicated relays that mimic onion routing
</p>
<div>
<b>Server-client connection command syntax:</b><br>
<code>server.py [port number]</code><br>
<code>client.py [port number]</code><br>
 </div>
<br>
<b>To connect to relay:</b><br>
<code>relay.py [port number]</code></br>
<br>
In client, type:<br>
                <code>_relay [hostname] [port]</code>
                <br>
  To chain the relay, connect the server to a relay and type the following commands in client<br>
      relay 2: <code>_relay_chain [hostname] [port]</code><br>
      relay 3: <code>_relay_control 0 _relay_chain [hostname] [port]</code><br>
      <br>
      for further relays, use the below command to add each relay<br>
       <code>_relay_control 0 {_relay_control 0} _relay_chain [hostname] [port]</code><br>
             <br>
             <em>*{} number of extra relays you wish to use</em>
