from ipaddress import ip_network

CACHE = {}

def get_network(cidr):
    cidr = unicode(cidr)
    try:
        return CACHE[cidr]
    except KeyError:
        network = ip_network(cidr)
        CACHE[cidr] = network
        return network

def get_cidr(network):
    # TODO: why are we accessing a protected attribute?
    #       does this work?
    # testing for IPv4?
    if network._prefixlen == 32:  # pylint: disable=protected-access
        return str(network.network_address)
    return str(network)

class NetworkDict(object):
    def __init__(self):
        self.networks = {}

    def read_list(self, values):
        # self["185.46.170.234"] = "Dj_Hazel_PL" + 
        for item in values:
            self[item[1]] = [item[0]] + item[2:]

    def make_list(self):
        values = []
        for network, value in self.iteritems():
            values.append([value[0]] + [network] + list(value[1:]))
        return values

    def remove(self, key):
        network = get_network(key)
        removed = self.networks[network]
        del self.networks[network]
        return removed

    def __setitem__(self, key, value):
        self.networks[get_network(key)] = value

    def __getitem__(self, key):
        return self.get_entry(key)

    def get_entry(self, key):
        return self.networks[get_network(key)]

    def __len__(self):
        return len(self.networks.keys())

    def __delitem__(self, key):
        del self.networks[get_network(key)]

    def pop(self, *arg, **kw):
        network, value = self.networks.pop(*arg, **kw)
        return get_cidr(network), value

    def iteritems(self):
        for network, value in self.networks.iteritems():
            yield get_cidr(network), value

    def __contains__(self, key):
        try:
            self.get_entry(key)
            return True
        except KeyError:
            return False
