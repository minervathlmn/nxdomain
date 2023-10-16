#!/bin/bash

# Menjalankan server pada port 1024 di latar belakang
python server.py config.txt 1024 &

# Menunggu server untuk memulai
sleep 1

# Menjalankan beberapa perintah untuk menguji server
echo -e "!ADD host1 8080\n!ADD host2 9090\n!DEL host2\n!INVALID\n!EXIT" | nc localhost 1024

# Menunggu server untuk menyelesaikan perintah
sleep 1

# Menghentikan server
pkill -f "python server.py config.txt 1024"

# Menjalankan Coverage.py
coverage run -m unittest discover -s tests -p "*_test.py"

# Menghasilkan laporan cakupan
coverage report -m

# Membersihkan hasil pengujian
coverage erase
