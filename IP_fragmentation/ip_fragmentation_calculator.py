def calculate_ip_fragments(data_size, mtu, ip_header_size):
    if data_size <= 0 or mtu <= 0 or ip_header_size < 0:
        return "Invalid input values."

    max_payload_size = mtu - ip_header_size

    num_fragments = (data_size + max_payload_size - 1) // max_payload_size

    total_length = data_size
    fragments = []
    offset = 0

    for i in range(num_fragments):
        payload_size = max_payload_size - (max_payload_size % 8) if i < num_fragments - 1 else data_size - offset 
        
        #more flag: 0 for only last fragment
        mf_flag = 1 if i < num_fragments - 1 else 0

        temp_len = 0
        if i < num_fragments - 1:
            temp_len = payload_size + ip_header_size
        else:
            temp_len = payload_size - ip_header_size
        fragments.append({
            "Fragment": i + 1,
            "Total Length": temp_len,  # Including IP header size
            "MF Flag": mf_flag,
            "Offset": offset // 8  
        })
        
        offset += payload_size

    return num_fragments, fragments

def main():
    data_size = int(input("Enter data size: "))
    mtu = int(input("Enter maximum transmission unit MTU: "))
    ip_header_size = int(input("IP header size: "))

    num_fragments, fragments = calculate_ip_fragments(data_size, mtu, ip_header_size)

    # Display the results

    print(f"Number of fragments: {num_fragments}")
    print("\n")
    for fragment in fragments:
        print(f"Fragment {fragment['Fragment']}:")
        print(f"  Length: {fragment['Total Length']} bytes")
        print(f"  MF Flag: {fragment['MF Flag']}")
        print(f"  Offset: {fragment['Offset'] } bytes")
        print("\n")


if __name__ == "__main__":
    main()

