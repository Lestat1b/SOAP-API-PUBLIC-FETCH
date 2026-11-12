# SOAP-API-PUBLIC-FETCH
Module 5 Assignment 1
What I learned from this assignment is that public SOAP web service can be hard to fing a working URL. I also looked at WSDL files that described the operations of available through a SOAP service and using a Zeep
to create a client. Like I said it eariler it was a challenge to find a working public SOAP service that was still available to use. Some of the first services I tried either would time out or refused to connect.
Which I thought a first it was the way the code was writen. I eventually found the one I called Soccer Rankings, which successfully returned the team information.

The code was a simple local SOAP that added validation to make sure the team entered by the user exists in the list of valid teams and created custom error messages for invalid imputs. Finally I wrapped the client
in Flask and add GET and POST endpoints for testing.

I believe I'm getting a better understanding of how WSDL, SOAP, Zeep, and XML response and validation and Flask can work together. I like learn about larger and more complex SAOP responses.
