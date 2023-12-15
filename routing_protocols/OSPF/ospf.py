import heapq

def add_routers(network_topology, r1, r2, dist):
    if r1 not in network_topology:
        network_topology[r1] = []
    if r2 not in network_topology:
        network_topology[r2] = []
    network_topology[r1].append((r2, dist))
    network_topology[r2].append((r1, dist))

network_topology = {}

add_routers(network_topology, 'A', 'B', 6)
add_routers(network_topology, 'A', 'C', 3)
add_routers(network_topology, 'B', 'C', 2)
add_routers(network_topology, 'B', 'D', 7)
add_routers(network_topology, 'C', 'E', 9)
add_routers(network_topology, 'D', 'E', 1)
add_routers(network_topology, 'D', 'F', 8)
add_routers(network_topology, 'E', 'F', 4)

# Initialize the initial routing tables for all routers
initial_routing_tables = {}

for router, neighbors in network_topology.items():
    initial_routing_tables[router] = {neighbor: distance for neighbor, distance in neighbors}

# Print the initial routing tables
print("Initial Routing Tables:")
for router, neighbors in initial_routing_tables.items():
    print(f"Router {router}:")
    for neighbor, distance in neighbors.items():  # Changed this line
        print(f"  {neighbor} -> Distance: {distance}")

# Dijkstra's algorithm to calculate the final routing table for Router R1
def dijkstra(start_router, network_topology):
    distances = {router: float('inf') for router in network_topology}
    distances[start_router] = 0
    via = {router: [] for router in network_topology}

    # Priority queue to keep track of the routers to visit
    priority_queue = [(0, start_router)]

    while priority_queue:
        current_distance, current_router = heapq.heappop(priority_queue)

        if current_distance > distances[current_router]:
            continue

        for neighbor, neighbor_distance in network_topology[current_router]:
            total_distance = current_distance + neighbor_distance

            if total_distance < distances[neighbor]:
                distances[neighbor] = total_distance
                via[neighbor] = via[current_router] + [current_router]
                heapq.heappush(priority_queue, (total_distance, neighbor))

    return distances, via

# Calculate the final routing table for Router R1
final_routing_table, via = dijkstra("A", network_topology)

# Print the final routing table for Router R1
print("\nFinal Routing Table for Router R1:")
print("Router\tDistance\tVia")
for router, distance in final_routing_table.items():
    path = " -> ".join(via[router] + [router])
    print(f"{router}\t{distance}\t{path}")
