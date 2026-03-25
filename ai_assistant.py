'''
目前这个 AI 助手已经具备了以下“硬核”特质：

1.持久化存储：对话流水账和每日总结分门别类，永不丢失。

2.自动化思维：自动计算时间、自动重试、退出是自动总结。

3.安全性：敏感的 API Key 藏在保险柜里。

4.鲁棒性（耐操性）：有计数器保护，不会死循环。


'''

import os  # 系统自带的，用来读取环境变量
from dotenv import load_dotenv  # 刚安装的工具
import openai
import time
from datetime import datetime

# 1. 加载 .env 文件
load_dotenv()

# 2. 从环境变量中获取 Key
# 这样代码里就不会出现明文的 sk-xxx 了
API_KEY = os.getenv("MOONSHOT_API_KEY")
BASE_URL = "https://api.moonshot.cn/v1"
MODEL_NAME = "kimi-k2.5"
# 如果 Key 没拿到，报错提醒
if not API_KEY:
    print("[错误]: 未找到 API_KEY，请检查 .env 文件！")
    exit()

client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 2. 状态初始化
messages = [{"role": "system", "content": "你是一个专业、高效且友好的人工智能助手。"}]
max_retries = 3  
retry_count = 0  

print(f"--- AI 助手已启动 (当前日期: {datetime.now().strftime('%Y-%m-%d')}) ---")

while True:
    try:
        user_input = input("\n[用户]: ").strip()
        
        if not user_input:
            print("[系统提示]: 内容不能为空。")
            continue
            
        if user_input.lower() in ['exit', 'quit', '退出']:
            print("\n[系统提示]: 正在生成对话总结...")
            summary_msg = messages + [{"role": "user", "content": "请用50字以内总结本次对话重点。"}]
            res = client.chat.completions.create(model=MODEL_NAME, messages=summary_msg)
            summary_result = res.choices[0].message.content
            
            with open("daily_notes.txt", "a", encoding="utf-8") as f_note:
                f_note.write(f"【{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 总结】\n{summary_result}\n{'-'*30}\n")
            
            print(f"今日总结: {summary_result}\n程序已安全退出。")
            break

        # 对话与记忆管理
        messages.append({"role": "user", "content": user_input})
        if len(messages) > 7:
            messages = [messages[0]] + messages[-6:]

        # 发送请求
        response = client.chat.completions.create(model=MODEL_NAME, messages=messages)
        
        # 只要成功，计数器立刻归零
        retry_count = 0 
        
        reply = response.choices[0].message.content
        print(f"[AI]: {reply}")

        # 数据保存
        messages.append({"role": "assistant", "content": reply})
        with open("chat_log.txt", "a", encoding="utf-8") as f_log:
            f_log.write(f"时间: {datetime.now().strftime('%H:%M:%S')}\n问: {user_input}\n答: {reply}\n\n")

    except Exception as e:
        # --- 这里的 IF 放到了最上面 ---
        retry_count += 1
        
        # 如果次数已经够了，直接打印最终判决并退出
        if retry_count >= max_retries:
            print(f"\n[运行异常]: {e}")
            print(f"已连续失败 {max_retries} 次，达到上限。程序终止，请检查配置。")
            break 
            
        # 如果还没到上限，再打印错误并提示正在重试
        print(f"\n[运行异常]: {e}")
        print(f"正在尝试第 {retry_count} 次重试（上限 {max_retries} 次）...")
        time.sleep(3)
        continue