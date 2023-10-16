#!/bin/bash
coverage erase
# Menjalankan server pada port 1024 di latar belakang
coverage run --append server.py config.txt &

# Menunggu server untuk memulai
sleep 2
echo fake recursor sends ADD
echo fake recursor sends ADD
echo fake recursor sends DEL
echo fake recursor sends EXIT
# Menjalankan beberapa perintah untuk menguji server
echo -e '!ADD host1 8080\n!ADD host2 9090\n!DEL host2\n!EXIT' | nc localhost 1024
#printf '!ADD twitter.com 8070\n!ADD host2\n!DEL host2\n!EXIT\n' | nc localhost 1024

# Menunggu server untuk menyelesaikan perintah
sleep 0.1

# Menghentikan server
pkill -f "coverage run --append server.py config.txt"

# Menjalankan Coverage.py
#coverage run -m unittest discover -s tests -p "*_test.py"

# Menghasilkan laporan cakupan
coverage report -m --omit /usr/lib/python3/dist-packages/_distutils_hack/__init__.py

# Membersihkan hasil pengujian
coverage erase
