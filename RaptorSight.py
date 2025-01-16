import socket
from concurrent.futures import ThreadPoolExecutor 
import os 
from tqdm import tqdm 


# RaptorSight port scanner by RogueElectron
# version 0.1

print("""
      
 ██▀███  ▒█████   ▄████ █    ██▓█████    ▓█████ ██▓   ▓█████ ▄████▄ ▄▄▄█████▓██▀███  ▒█████  ███▄    █ 
▓██ ▒ ██▒██▒  ██▒██▒ ▀█▒██  ▓██▓█   ▀    ▓█   ▀▓██▒   ▓█   ▀▒██▀ ▀█ ▓  ██▒ ▓▓██ ▒ ██▒██▒  ██▒██ ▀█   █ 
▓██ ░▄█ ▒██░  ██▒██░▄▄▄▓██  ▒██▒███      ▒███  ▒██░   ▒███  ▒▓█    ▄▒ ▓██░ ▒▓██ ░▄█ ▒██░  ██▓██  ▀█ ██▒
▒██▀▀█▄ ▒██   ██░▓█  ██▓▓█  ░██▒▓█  ▄    ▒▓█  ▄▒██░   ▒▓█  ▄▒▓▓▄ ▄██░ ▓██▓ ░▒██▀▀█▄ ▒██   ██▓██▒  ▐▌██▒
░██▓ ▒██░ ████▓▒░▒▓███▀▒▒█████▓░▒████▒   ░▒████░██████░▒████▒ ▓███▀ ░ ▒██▒ ░░██▓ ▒██░ ████▓▒▒██░   ▓██░
░ ▒▓ ░▒▓░ ▒░▒░▒░ ░▒   ▒░▒▓▒ ▒ ▒░░ ▒░ ░   ░░ ▒░ ░ ▒░▓  ░░ ▒░ ░ ░▒ ▒  ░ ▒ ░░  ░ ▒▓ ░▒▓░ ▒░▒░▒░░ ▒░   ▒ ▒ 
  ░▒ ░ ▒░ ░ ▒ ▒░  ░   ░░░▒░ ░ ░ ░ ░  ░    ░ ░  ░ ░ ▒  ░░ ░  ░ ░  ▒      ░     ░▒ ░ ▒░ ░ ▒ ▒░░ ░░   ░ ▒░
  ░░   ░░ ░ ░ ▒ ░ ░   ░ ░░░ ░ ░   ░         ░    ░ ░     ░  ░         ░       ░░   ░░ ░ ░ ▒    ░   ░ ░ 
   ░        ░ ░       ░   ░       ░  ░      ░  ░   ░  ░  ░  ░ ░                ░        ░ ░          ░ 
                                                            ░                                          
""")

def validate_int_input(user_input, default_value):
    try:
        return int(user_input or default_value)
    except ValueError:
        print("Invalid input, using default value")
        return default_value

class Raptor:
    def __init__(self):
        self.host = input("Enter the IP address or hostname to scan: ")
        self.port_start = validate_int_input(input("port start (default: 1): "), 1)
        self.port_end = validate_int_input(input("port end (default: 1666): "), 1666)
        self.threads = validate_int_input(input("how much threads? (default: no threading): "), False)
        self.open_ports = []
        self.errors = []
        
    
    def validate_target(self):
        ####----port validation----####
        if self.port_start > self.port_end:
            print("port start is greater than port end, using default values")
            self.port_start = 1
            self.port_end = 1666
        if self.port_end <= 0 or self.port_start <= 0:
            print("port can't be negative, using default values")
            self.port_start = 1
            self.port_end = 1666
        if self.port_end > 65535 or self.port_start > 65535:
            print("port can't be greater than 65535, using default values")
            self.port_start = 1
            self.port_end = 1666
        ####----hostname validation----####
        try:
            validhost = False
            socket.gethostbyname(self.host)
        except socket.gaierror as hostname_error:
            while not validhost:
                self.host = input("Enter a correct hostname to target: ")
                try:
                    socket.gethostbyname(self.host)
                    break
                except socket.gaierror:
                    print("Hostname is incorrect, try again")
                    

    def report(self):
        print(f"""
Target: {self.host}
Ports range: {self.port_start} - {self.port_end}

open ports: 
        """)

        for i in self.open_ports: 
            print(f"port: {i[0]}, service: {i[1]}")
        if self.errors:
            print("Errors faced:")
            for ERROR in self.errors:
                print(f"Faced error on port {ERROR[0]}, {ERROR[1]}")

    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((self.host, port))
        sock.close()
        if result == 0:
            service = socket.getservbyport(port)
            self.open_ports.append((port, service))
        if result != 0 and result != 10035:
            error_code = f"error {result}," + os.strerror(result) 
            self.errors.append((port, error_code))
    
    def scan(self):
        if self.threads == False:
            print("hold tight, scanning.")
            for port in tqdm(range(self.port_start, self.port_end + 1)):
                self.scan_port(port)

        elif self.threads != False:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                executor.map(self.scan_port, tqdm(range(self.port_start, self.port_end + 1)))

        self.report()
    
    def menu(self):
        while True:
            print("1: Start Scan")
            print("2: Exit")
            match input("Enter Option: "):
                case "1":
                    self.validate_target()
                    input("Press any button when ready")
                    print("Engaging target....")
                    self.scan()
                case "2": 
                    exit()
                case _:
                    print("Invalid input.")

        
        
if __name__ == "__main__":
    raptor = Raptor() 
    raptor.menu()
