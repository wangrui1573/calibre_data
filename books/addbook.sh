#!/bin/bash


#这段脚本的主要作用是下载一个CSV文件并读取文件内容，
#然后使用Calibre将CSV中的书籍信息添加到书库中。脚本首先下载CSV文件，
#然后使用sed在文件头插入“title，publisher”行。然后，使用awk将CSV文件与历史文件进行比对，
#如果发现文件中有已存在的书籍，则从CSV文件中删除这些书籍。接下来，脚本使用while循环逐行读取CSV文件并执行命令，
#使用Calibre添加书籍信息，设置元数据并将已添加的书籍信息写入历史文件。

# 下载csv文件
cd /docker/calibre/books
wget -O gamelist.csv "https://gist.githubusercontent.com/wangrui1573/50d3b32c4cbbd0e04966a0f9676d50b0/raw/gamelist.csv"
sed -i '1i title,publisher' gamelist.csv

# 比对history.csv，删除已存在的title
if [ -f history.csv ]; then
  awk -F ',' 'NR==FNR{a[$1];next} !($1 in a)' history.csv gamelist.csv > tmp.csv
  mv tmp.csv lastaddgames.csv
fi


#推送lastgamelist到github
curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/gists/e9a3f2e83125a90297d42be7bea5cd6c \
  -d '{"files":{"lastaddgames.csv":{"content":"'$(sed -z 's/\n/\\n/g' lastaddgames.csv)'","filename":"lastaddgames.csv"}}}'




#批量删除书籍
#for i in {889..909}; do calibredb remove --with-library /books "$i"; done

# 进入容器并执行命令
docker exec -it calibredb /bin/bash -c "export PATH=/opt/calibre/bin:\$PATH && cd /books && \
  # 逐行读取csv文件并执行命令
  tail -n +2 lastaddgames.csv | while IFS=',' read -r title publisher; do
    # 添加书籍
    book_id=\$(calibredb add --empty --title \"\$title\" --with-library /books | grep -o 'Added book ids: [[:digit:]]*' | cut -d ' ' -f 4

)

    # 设置元数据
    calibredb set_metadata -f \"publisher:\$publisher\" \"\$book_id\" --with-library /books
    echo "\$title,\$publisher" >> "history.csv"

  done"

