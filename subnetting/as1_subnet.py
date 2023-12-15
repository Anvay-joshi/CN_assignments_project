def int_to_address(ip_int):
    binary_ip = format(ip_int, '032b')

    octets = [binary_ip[i:i + 8] for i in range(0, len(binary_ip), 8)]

    decimal_ip = '.'.join([str(int(octet, 2)) for octet in octets])

    return decimal_ip

def find_network_id(ip_address, subnet_mask):
    return (ip_address & subnet_mask)

def find_broadcast_address(ip_address, subnet_mask):
    return ip_address | (~ subnet_mask & 0xFFFFFFFF)

def address_to_int(ip_address):
    
    octets = ip_address.split('.')
    
    binary_ip = ''.join([format(int(octet), '08b') for octet in octets])
    
    decimal_number = int(binary_ip, 2)
    
#    print(f"Binary representation: {binary_ip}")
#    print(f"Decimal representation: {decimal_number}")
    return decimal_number



def main():
    subnet_class = input("Select the class for IPv4 subnet mask (A, B, C): ").upper()
    if subnet_class not in ["A", "B", "C"]:
        print("Invalid subnet class. Please choose A, B, or C.")
        return

    valid_subnet_masks = {
        "A": list(range(8, 31)),  # Class A subnet mask range: /8 to /15
        "B": list(range(16, 31)),  # Class B subnet mask range: /16 to /23
        "C": list(range(24, 31))
    }

    subnet_class_base = {
        "A": 4278190080,
        "B": 4294901760,
        "C": 4294967040
    }

    subnet_mask_length = 0
    while True:
        try:
            subnet_mask_length = int(input(f"Enter the subnet mask length for class {subnet_class} (/{min(valid_subnet_masks[subnet_class])} to /{max(valid_subnet_masks[subnet_class])}): /"))
            if subnet_mask_length not in valid_subnet_masks[subnet_class]:
                print(f"Invalid subnet mask length for class {subnet_class}.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid subnet mask length.")

    borrowed_bits = subnet_mask_length - min(valid_subnet_masks[subnet_class])
    subnetworks = 2 ** borrowed_bits

    subnet_mask = subnet_class_base[subnet_class] 
    subnet_mask_updated = subnet_mask 
    for i in range(borrowed_bits):
        subnet_mask_updated += (1 << (32 - min(valid_subnet_masks[subnet_class]) - i - 1))
    print(f"subnet mask is: {int_to_address(subnet_mask_updated)}")

    print(f"\nTotal subnets = {subnetworks}\n")

    ip_address_string = input("Enter an IP address in the subnet: ")
    ip_address_decimal = address_to_int(ip_address_string)
    
    netword_id = find_network_id(ip_address_decimal, subnet_mask)
    broadcast_address = find_broadcast_address(ip_address_decimal, subnet_mask)
#    print(f"network address: {int_to_address(netword_id)}")
#    print(f"broadcast address: {int_to_address(broadcast_address)}")

    subnetwork_size = (broadcast_address - netword_id) // subnetworks
    print("")
    for i in range(subnetworks):
        subnetwork_id = netword_id + i * (subnetwork_size + 1)
        subnetwork_broadcast_address = subnetwork_id + subnetwork_size
        host_start = subnetwork_id + 1
        host_end = subnetwork_broadcast_address - 1

        print(f"Network id: {int_to_address(subnetwork_id)}")
        print(f"Usable host range: {int_to_address(host_start)} to {int_to_address(host_end)}")
        print(f"Broadcast address: {int_to_address(subnetwork_broadcast_address)}")
        print("\n")

        
if __name__ == "__main__":
    main()

    
