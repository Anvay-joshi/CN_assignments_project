import random

def create_window(window_start, cwnd):
    window = [] * cwnd
    window_acks = [] * cwnd
    for i in range(0, cwnd):
        window.append(window_start + i)
        window_acks.append(False)
    return window, window_acks

def send_window(window, cwnd):
    print(f"send window: {window}, cwnd = {cwnd}")

def get_ack(window, window_acks, cwnd):
    for i in range(0, cwnd):
        if random.random() <= 0.9:
            window_acks[i] = True
            print(f"        ACK {window[i]} arrived")
    return window_acks

def main():
    n = int(input("Enter number of packets: "))
    cwnd = 1
    last_seq_acked = 0
    window_start = 1
    window = []
    window_acks = []

    i = 0
    while last_seq_acked != n:
        print("\n")
        if i == 10:
            #break
            pass

        if(window_start + cwnd - 1) > n:
            cwnd = n - window_start + 1
        window, window_acks = create_window(window_start, cwnd)

        send_window(window, cwnd)
        
        window_acks = get_ack(window, window_acks, cwnd)

        try:
            index = window_acks.index(False)
            lost_packet = window[index]
            last_seq_acked = lost_packet - 1
            window_start = lost_packet
            if(cwnd > 1):
                cwnd //= 2
                print(f"New congestion window = {cwnd}")
            print(f"New window start = {window_start}")
        except:
            window_start += cwnd
            cwnd += 1
            last_seq_acked = window_start - 1
            print(f"New congestion window = {cwnd}")
            print(f"New window start = {window_start}")

        i +=1
        




if __name__ == "__main__":
    main()
