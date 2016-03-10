# http-server
Authored by: Selena Flannery and Kevin Gifford

This is a simple HTTP server that accepts requests and returns full responses,
including status codes, headers, and a body. The server opens a persistent
socket for communication and can accept multiple connections while keeping the
socket open. The server is currently programmed to respond with either a
"200 OK" or "500 INTERNAL SERVER ERROR" code.
