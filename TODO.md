# TODOs
- implement alt routing
- implement timeout

# Notes
## Lookup
Network topology is important for how to implement.

(Ad-hoc all in range)
Easiest implementation is all nodes/users connected to all nodes/users.
However this is not useful.

(infrastructure network)
First realistic implementation is two levels, one router level and those are
never targets, other level is nodes that are connected to one router and
other nodes connected to the same router. Having the routers either all
connected to each other, connected as a circle or a chain.

(mesh)
More realistic is several levels of connectivity, some directly to routers,
but also pass on to APs

Lookup must also be altered based on alt routing

## Alt Routing
Easiest implementation is adding some connections and have a heuristic to chose,
or change nodes to check for duplicate packages and send package through both.
Check for duplicates can be done easily as a node/user will not create more than
one package at the same timestamp.

physical location simulation?


## Timeout
Check what is a reasonable timeout treshhold, this also require tick <-> time in
simulation.
