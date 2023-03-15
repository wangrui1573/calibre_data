import csv
import os
import subprocess
from fuzzywuzzy import fuzz

# 读取lastaddgames.csv文件中的书籍名称
with open('lastaddgames.csv', 'r') as f:
    # 使用csv模块读取CSV文件
    reader = csv.reader(f)
    # 跳过标题行
    next(reader)
    for row in reader:
        # 忽略空白行或行中的列数不足的行
        if not row or len(row) < 1:
            continue
        book_name = row[0]

        # 列出所有图片文件
        files = os.listdir('/docker/calibre/books/temp')
        max_similarity = 0
        best_file = None

        # 找到最相似的图片文件
        for file in files:
            similarity = fuzz.token_set_ratio(book_name, file.split('.')[0])
            if similarity > max_similarity:
                max_similarity = similarity
                best_file = file
        print(best_file)

        # 使用calibredb搜索书籍ID并设置封面
        command_search = ['docker', 'exec', 'calibredb', 'calibredb', 'search', '--limit', ' 1', 'title:{}'.format(book_name), '--with-library=/books']
        result_search = subprocess.check_output(command_search).decode().strip()
        #print(command_search)
        print(result_search)

        # 如果没有找到匹配的书籍，跳过
        if not result_search:
            continue
        book_id = result_search.split('\t')[0]

        command_set_cover = ['docker', 'exec', 'calibredb', 'calibredb', 'set_metadata', '-f', 'cover:/books/temp/{}'.format(best_file), book_id, '--with-library=/books']
        subprocess.call(command_set_cover)

        # 删除CSV文件中的当前行
        with open('lastaddgames.csv', 'r') as f:
            lines = f.readlines()
        with open('lastaddgames.csv', 'w') as f:
            for line in lines:
                if line.strip().split(',')[0] != book_name:
                    f.write(line)

