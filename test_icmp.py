import ICMP
import time
from LinkLayer import util
local_ip = util.get_local_ipv4_address()
remote_ip = '192.168.43.116'
ICMP.request(local_ip, remote_ip)

