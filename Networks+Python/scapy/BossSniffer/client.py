from scapy.all import *

SERVER_PORT = 5555
SERVER_IP = "127.0.0.1"

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp ipv4
my_socket.connect((SERVER_IP, SERVER_PORT)) # connecting to the server
print("Connected to server")

blacklisted_urls = (
    'www.facebook.com', 'www.youtube.com', 'www.walla.co.il', 'www.ynet.co.il', 'www.tiktok.com', 'www.instagram.com'
) # tuple the contains all the blacklisted sites
hosts_set = set()

def hostname_by_dns(packet):
    #this function is working on DNS queries. it finds DNS queries, takes the hostname out of the query
    # then checks if the hostname is in the blacklisted tuple, if so, it checks if it was already printed that the client
    # opened that website. if both conditions are true, it sends the server the msg about the site being open,
    # and then it stores the hostname in the set of hosts, in order to not spam the same host again and again
    if DNS in packet and DNSQR in packet[DNS]:
        hostname = packet[DNS][DNSQR].qname.decode("utf-8").rstrip('.')
        if hostname in blacklisted_urls and hostname not in hosts_set:
            msg = (f"Blacklisted site detected!! {hostname} is open")
            my_socket.send(msg.encode())
            hosts_set.add(hostname)

def hostname_by_http(packet):
    #works with http based sites. searches for http packets, extracts the hostname out of the GET request
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load.decode(errors="ignore")
        if payload.startswith("GET"):
            headers = payload.split('\r\n')
            for header in headers:
                if header.startswith("Host:"):
                    hostname = header.split()[1]
                    if hostname in blacklisted_urls and hostname not in hosts_set:
                        msg = (f"Blacklisted site detected!! {hostname} is open")
                        my_socket.send(msg.encode())
                        hosts_set.add(hostname)



def dns_and_http(packet):
    # In order to pass both DNS and HTTP filters to the sniff function, I created this function that runs them both
    # And then I pass it to the prn inside sniff
    hostname_by_http(packet)
    hostname_by_dns(packet)


sniff(prn=dns_and_http)