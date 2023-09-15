import tkinter as tk
import requests
from bs4 import BeautifulSoup
import sys
import time
import re
import os


def submit():
    problem = problem_var.get()
    difficulty = difficulty_var.get()
    keywords = keywords_entry.get()

    # 在这里可以处理提交的数据，例如保存到文件或显示在界面上
    #首先编辑所属题库选项，分为洛谷、主题库、以及入门与面试
    if problem == "洛谷":
        problem_type = "B%7CP"
    elif problem == "主题库":
        problem_type = "P"
    elif problem == "入门与面试":
        problem_type = "B"

    #编辑所属难度，分为暂无评定，入门，普及-，普及/提高-，普及+/提高，提高+/省选-，省选/NOI-，NOI/NOI+/CTSC

    if difficulty == "暂无评定":
        difficulty_tpye = "0"
    elif difficulty == "入门":
        difficulty_tpye ="1"
    elif difficulty == "普及-":
        difficulty_tpye ="2"
    elif difficulty == "普及,提高-":
        difficulty_tpye ="3"
    elif difficulty == "普及+,提高":
        difficulty_tpye ="4"
    elif difficulty == "提高+,省选-":
        difficulty_tpye ="5"
    elif difficulty == "省选,NOI-":
        difficulty_tpye ="6"
    elif difficulty == "NOI and NOI+,CTSC":
        difficulty_tpye ="7"
        
    print("Difficulty_tpye:", difficulty_tpye)
    print("Keywords:", keywords)
    print("Problrm_tpye:",problem_type)

    return difficulty_tpye,keywords,problem_type

#查找主网页，显示全部页面
def scrape_website(difficulty_tpye,keywords,problem_type):
    p = problem_var.get()
    d = difficulty_var.get()
    k = keywords_entry.get()
    type = problem_type
    difficulty = difficulty_tpye
    keyword = keywords

    
    url = 'https://www.luogu.com.cn/problem/list?type='+ type +'&page=1&difficulty='+difficulty+'&keyword='+keyword 
    output_file = 'C:/Users/13986/Desktop/洛谷爬虫/爬出的总界面/'+p+'_'+d+'_'+k+'.md' 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 输出整个 HTML 内容
        with open(output_file, 'w') as file:
            file.write(soup.prettify())

        # 使用属性选择器查找带有 href 属性的标签
        a_tags = soup.find_all('a', href=True)
        choice = 0
        # 遍历找到的标签并获取 href 属性的值
        for a in a_tags:
            href_value = a['href']
            url_2 = 'https://www.luogu.com.cn/problem/'+ href_value
            url_solution = 'https://www.luogu.com.cn/problem/solution/'+ href_value
            
            response_2 = requests.get(url_2, headers=headers)
            response_solution = requests.get(url_solution, headers=headers)
            
            soup_2 = BeautifulSoup(response_2.text, 'html.parser')
            soup_solution = BeautifulSoup(response_solution.text, 'html.parser')

            html_content = response_2.text
            html_content_solution = response_solution.text

            
            # 定义文件夹路径和文件名
            folder_path = 'C:/Users/13986/Desktop/洛谷爬虫/'+p+'_'+d+'_'+k+'/'+'问题'+href_value

            # 定义问题名
            file_name = '问题'+str(choice)+'.md'

            # 定义答案名
            solution_name = '答案'+str(choice)+'.md'

            # 创建文件夹
            os.makedirs(folder_path, exist_ok=True)

            # 文件完整路径
            file_path = os.path.join(folder_path, file_name)
            solution_path = os.path.join(folder_path, solution_name)
            
            # 将 HTML 内容写入 Markdown 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(soup_2.prettify())
                
            with open(solution_path, 'w', encoding='utf-8') as file_1:
                file_1.write(soup_solution.prettify())
                
            choice +=1

            print(href_value)
        choice =0
        
        # 恢复标准输出
        
        print(f"输出已保存到文件：{output_file}")
    else:
        print('请求失败')


def main():
    difficulty_type,keywords,problem_type = submit()
    scrape_website(difficulty_type,keywords,problem_type)
    print("爬取页面成功")

def find(soup,brend):
    a = soup.find(brend)
    return a
# 创建一个窗口
window = tk.Tk()
window.title("前端界面")


# 创建所属题库标签和下拉菜单
problem_label = tk.Label(window, text="所属题库：")
problem_label.pack()

problem_var = tk.StringVar()
problem_choices = [
    "洛谷",
    "主题库",
    "入门与面试"
]
problem_dropdown = tk.OptionMenu(window, problem_var, *problem_choices)
problem_dropdown.pack()


# 创建题目难度标签和下拉菜单
difficulty_label = tk.Label(window, text="题目难度：")
difficulty_label.pack()

difficulty_var = tk.StringVar()
difficulty_choices = [
    "暂无评定",
    "入门",
    "普及-",
    "普及,提高-",
    "普及+,提高",
    "提高+,省选-",
    "省选,NOI-",
    "NOI and NOI+,CTSC"
]
difficulty_dropdown = tk.OptionMenu(window, difficulty_var, *difficulty_choices)
difficulty_dropdown.pack()

# 创建关键词标签和输入框
keywords_label = tk.Label(window, text="关键词：")
keywords_label.pack()

keywords_entry = tk.Entry(window)
keywords_entry.pack()

# 创建提交按钮
submit_button = tk.Button(window, text="提交", command=main)
submit_button.pack()

# 开始 Tkinter 事件循环
window.mainloop()
