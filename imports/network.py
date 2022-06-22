from numpy.random import randint

"""
File imports/network.py
Top-level functions: routers_and_nodes, routers_and_nodes_alt
and network_results

Routers_and_nodes:
Uses the line_connect function to connect the routers in a line, fully connects
the set of nodes for a router with themselves and their router, and forwards all
other ip addresses to their router. This esentially creates a network with
"""

def remove_connection(node, ip_address):
    node.remove_lookup_entry(ip_address)

def indirect(node_a, node_b, ip_address):
    if node_a.get_ip_address() == ip_address:
        return
    node_a.add_lookup_entry(ip_address, node_b)

def one_way(node_a, node_b):
    if node_a.get_ip_address() == node_b.get_ip_address():
        return
    node_a.add_lookup_entry(node_b.get_ip_address(), node_b)

def indirect_list(node_a, node_b, ip_addresses):
    for ip_address in ip_addresses:
        indirect(node_a, node_b, ip_address)

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

def line_connect(node_list):
    future_ips = [node.get_ip_address() for node in node_list]
    past_ips = []
    for i in range(len(node_list)):
        future_ips.remove(node_list[i].get_ip_address())
        if len(past_ips) > 0:
            indirect_list(node_list[i], node_list[i-1], past_ips)
        if len(future_ips) > 0:
            indirect_list(node_list[i], node_list[i+1], future_ips)
        past_ips.append(node_list[i].get_ip_address())

def routers_and_nodes(routers, list_of_list_of_nodes):
    # assumes nodes connected to a router has ip's as follows:
    # router ip i.e. "123"
    # nodes connected to that router has ip's "123.XXX"
    if not len(routers) == len(list_of_list_of_nodes):
        raise ValueError(
        "routers_and_nodes: length of routers list must be the same as length\
        of list of list of nodes.")

    router_ips = [router.get_ip_address() for router in routers]

    line_connect(routers)

    for i in range(len(list_of_list_of_nodes)):
        # router connected to all its nodes
        # one_to_all(routers[i], list_of_list_of_nodes[i])

        # a router is connected to one other router, and all router ips map to
        # that other router
        #indirect_list(routers[i-1], routers[i], router_ips)

        router = routers[i]

        local_nodes = list_of_list_of_nodes[i].copy()
        for node in local_nodes:
            # router connected to its nodes
            one_way(router, node)
            # nodes map all router ips to its router
            indirect_list(node, router, router_ips)

def routers_and_nodes_alt(routers, list_of_list_of_nodes, other_connections):
    routers_and_nodes(routers, list_of_list_of_nodes)
    for i in range(other_connections):
        random_router = randint(len(routers))
        random_node = randint(len(list_of_list_of_nodes[random_router]))
        random_router2 = randint(len(routers))
        while random_router == random_router2:
            random_router2 = randint(len(routers))
        random_node2 = randint(len(list_of_list_of_nodes[random_router2]))
        node1 = list_of_list_of_nodes[random_router][random_node]
        node2 = list_of_list_of_nodes[random_router2][random_node2]
        both_ways(node1, node2)

def network_results(node_list):
    # function to print results after a simulation
    result_string = "### Network Nodes Results ###\n"
    for node in node_list:
        result_string += node.write_results()

    return result_string
