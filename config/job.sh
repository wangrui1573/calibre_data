cd /docker/calibre/books
sh /docker/calibre/books/addbook.sh
sleep 3
/usr/bin/python3.6 /docker/calibre/books/pic.py
sleep 3 
/usr/bin/python3.6 /docker/calibre/books/set_pic.py 
