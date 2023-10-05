# recursor.py

import socket
from sys import argv

def main(args: list[str]) -> None:
    if len(args) != 1:
        print("Usage: python recursor.py <root_dns_server>")
        return

    root_dns_server = (args[0], 53)  # Ambil alamat server DNS root dari argumen command-line
    recursor = DNS_Recursor(root_dns_server)
    recursor.start()

class DNS_Recursor:
    def __init__(self, root_dns_server):
        self.root_dns_server = root_dns_server  # Alamat server DNS root
        self.cache = {}  # Cache DNS sederhana

    def start(self):
        while True:
            domain = input("Enter a domain (or 'exit' to quit): ")
            if domain == "exit":
                break

            response = self.resolve_dns(domain)
            print(response.decode('utf-8'))

    def resolve_dns(self, domain):
        # Cek cache terlebih dahulu
        if domain in self.cache:
            return self.cache[domain]

        # Tambahkan pernyataan print untuk debugging
        print(f"Mengirim permintaan DNS untuk domain: {domain}")

        # Jika tidak ada di cache, kirimkan permintaan ke root DNS server
        root_dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        root_dns_socket.connect(self.root_dns_server)
        
        # Kirim permintaan DNS ke root DNS server
        root_dns_socket.send(domain.encode('utf-8'))
        
        # Terima respons dari root DNS server
        response = root_dns_socket.recv(1024)
        
        # Simpan hasil ke cache sebelum mengembalikannya
        self.cache[domain] = response
        
        return response

if __name__ == "__main__":
    main(argv[1:])
