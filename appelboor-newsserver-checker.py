import socket
import urllib2
import socket, ssl
import sys


def handle(conn):
    ### Get welcome text from newsserver, say QUIT, and return the welcome text
    welcometext = conn.recv().rstrip().split('\n')[0]
    conn.write(b'QUIT\r\n')
    return welcometext



def checkserver(HOST):
    PORT=563
    sock = socket.socket(socket.AF_INET)
    context = ssl.create_default_context()
    #context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    #context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
    conn = context.wrap_socket(sock, server_hostname=HOST)
    try:
        conn.connect((HOST, PORT))
        return "OK:" + handle(conn)
    except:
        return "*** no connection possible"
    finally:
        conn.close()
    return "Error"


#### MAIN

#checkserver('newszilla.xs4all.nl')

# timeout in seconds
timeout = 5
socket.setdefaulttimeout(timeout)

csv_url = 'https://www.appelboor.com/newsservers/newsservers-with-SSL.csv'
# Lines look like:
# "newszilla.xs4all.nl","IPv4-IPv6","TLSv1.2","OK","OK","OK","-","-"

req = urllib2.Request(csv_url)
response = urllib2.urlopen(req)

for line in response.read().split('\n'):
	try:
		host = line.split(',')[0].replace('"','')
		IPversion = line.split(',')[1].replace('"','')
		okornok = line.split(',')[5].replace('"','')

		if IPversion.find('IPv4') < 0:
			# For now, skip newsservers that don't speak IPv4
			continue

		if okornok == 'NOK':
			# Skip newsservers that have a faulty TLS/SSL setup
			continue

		print "Check:", host, "gives result:",
		print checkserver(host)
	except:
		continue


