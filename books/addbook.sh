#!/bin/bash

# 下载csv文件
cd /docker/calibre/books
wget -O gamelist.csv "https://gist.githubusercontent.com/wangrui1573/50d3b32c4cbbd0e04966a0f9676d50b0/raw/gamelist.csv"
sed -i '1i title,publisher' gamelist.csv

# 进入容器并执行命令
docker exec -it calibredb /bin/bash -c "export PATH=/opt/calibre/bin:\$PATH && cd /books && \
  # 逐行读取csv文件并执行命令
  tail -n +2 gamelist.csv | while IFS=',' read -r title publisher; do
    # 添加书籍
    book_id=\$(calibredb add --empty --title \"\$title\" --with-library /books | grep -o 'Added book ids: [[:digit:]]*' | cut -d ' ' -f 4)

    # 设置元数据
    calibredb set_metadata -f \"publisher:\$publisher\" \"\$book_id\" --with-library /books
    echo "\$title,\$publisher" >> "history_file.csv"

  done"

#剩余比对历史任务了
