def indirect(node_a, node_b, ip_address):
    if node_a.get_ip_address() == ip_address:
        return
    node_a.add_lookup_entry(ip_address, node_b)

def indirect_list(node_a, node_b, ip_addresses):
    for ip_address in ip_addresses:
        indirect(node_a, node_b, ip_address)

def one_way(node_a, node_b):
    if node_a.get_ip_address() == node_b.get_ip_address():
        return
    node_a.add_lookup_entry(node_b.get_ip_address(), node_b)

def both_ways(node_a, node_b):
    one_way(node_a, node_b)
    one_way(node_b, node_a)

def one_to_all(origin_node, node_list):
    for node in node_list:
        one_way(origin_node, node)

def one_to_all_both_ways(origin_node, node_list):
    for node in node_list:
        both_ways(origin_node, node)

def fully_connect(node_list):
    for node in node_list:
        copied_node_list = node_list.copy()
        copied_node_list.remove(node)
        one_to_all(node, copied_node_list)

def circle_connect(node_list):
    for i in range(len(node_list)):
        # if i == 0:
        #     one_way(node_list[-1], node_list[0])
        # else:
        one_way(node_list[i-1], node_list[i])

def routers_and_nodes(routers, list_of_list_of_nodes):
    # assumes nodes connected to a router has ip's as follows:
    # router ip i.e. "123.123"
    # nodes connected to that router has ip's "123.123.XXX.XXX"
    if not len(routers) == len(list_of_list_of_nodes):
        raise ValueError(
        "routers_and_nodes: length of routers list must be the same as length\
        of list of list of nodes.")

    router_ips = [router.get_ip_address() for router in routers]

    for i in range(len(list_of_list_of_nodes)):
        # router connected to all its nodes
        # one_to_all(routers[i], list_of_list_of_nodes[i])

        # a router is connected to one other router, and all router ips map to
        # that other router
        indirect_list(routers[i-1], routers[i], router_ips)



        local_nodes = list_of_list_of_nodes[i]
        for node in local_nodes:
            # nodes map all router ips to its router
            indirect_list(node, routers[i], router_ips)
        local_nodes.append(routers[i])
        # nodes fully connected to local nodes and router
        fully_connect(local_nodes)

def network_results(node_list):
    # function to print results after a simulation
    for node in node_list:
        node.write_results()
