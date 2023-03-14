  tail -n +2 gamelist.csv | while IFS=',' read -r title publisher; do
    # 添加书籍
    book_id=$(calibredb add --empty --title "$title" --with-library /books | grep -o 'Added book ids: [[:digit:]]*' | cut -d ' ' -f 4)

    # 设置元数据
    calibredb set_metadata -f "publisher:$publisher" "$book_id" --with-library /books
  done"
