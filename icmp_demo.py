import ICMP
from LinkLayer import util
local_ip = util.get_local_ipv4_address()
remote_ip = '10.21.108.47'
ICMP.request(local_ip, remote_ip)

