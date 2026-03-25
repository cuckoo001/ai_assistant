
'''
改造助手
API 是按字数 Token 扣钱的。如果你和它聊了 100 轮，第 101 轮发过去的消息会包含前面所有的 100 轮对话。
为了让程序既聪明又省钱，我们通常只给 AI 看最近几轮的对话。在 Python 里，这叫“列表切片"
切片 (Slicing) —— 只带最近的记忆
'''

import os  # 系统自带的，用来读取环境变量
from dotenv import load_dotenv  # 刚安装的工具
import openai

#  加载 .env 文件
load_dotenv()

#  从环境变量中获取 Key
# 这样代码里就不会出现明文的 sk-xxx 了
API_KEY = os.getenv("MOONSHOT_API_KEY")
BASE_URL = "https://api.moonshot.cn/v1"
MODEL_NAME = "kimi-k2.5"
# 如果 Key 没拿到，报错提醒
if not API_KEY:
    print("[错误]: 未找到 API_KEY,请检查 .env 文件！")
    exit()

# 创建一个 客户端实例,并连接到一个 AI 服务接口，拿到一个“操作入口
client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)

messages = [
        # 定义AI身份(这是给 AI 看的指令，用户看不到)
        {"role": "system", "content": "你是一个专业、高效且友好的人工智能助手"}
    ]

# --- 变化在这里：让用户输入---
# ---程序运行到这里会停住，等你打字并按回车---
# ---开启永动机模式---
print("--- 助手已上线，输入任意内容开始聊天,(具有记忆力模式) 退出系统请输入 'quit', 'exit', '退出'---")
while True:
    try:
        user_input = input("\n[有问题 尽管问]: ").strip() # <-- 重点：加个 strip() 杀掉空格,空内容
        # --- 检查是不是空话 ---
        if not user_input:
            print("[Assistant]: 您倒是说句话呀？(不能发空消息哦)")
            continue # 跳过这一轮，重新让你输入
        # 如果输入 exit 或 quit，程序就礼貌地拜拜
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("[Assistant]: 下次见。")
            break  # 这一行会直接跳出 while 循环，结束程序

        # 准备你的问题（这是一个列表，装着对话内容）
        # 把 user_input 这个变量塞进 messages 列表里
        # 使用 append 把用户的话“追加”到记事本末尾 ---
        messages.append({"role": "user", "content": user_input})
        # --- 核心优化：修剪记忆 (只保留 system + 最近 6 条记录) ---
        # 如果对话超过 7 条（1条系统 + 6条对话），我们就只取最新的
        if len(messages) > 7:
            # 删之前，我们先打印一下，看看现在记事本里有几样东西
            print(f"--- 警告：记忆太满(当前{len(messages)}条)，正在清理旧记忆... ---")
            # messages[0] 是系统设定，必须留着
            # messages[-6:] 是最后 6 条（3轮对话）
            messages = [messages[0]] + messages[-6:]
            # len(messages)用来数数。它会告诉你列表里现在有几行。
            # messages[-6:]：负号 - 代表从后面往前面数。[-6:] 就是“最后 6 个
        # 删完之后，再打印一下剩下的
            print(f"--- 清理完成，现在只记得{len(messages)} 条对话 ---") 

        # 发送请求，让 AI 开始计算
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )

        # 向大模型发送一次“对话请求”，让 AI 根据你的 messages 生成回复打印回复
        reply = response.choices[0].message.content
        print(f"[Assistant]: {reply}")

        # --- 重要：把 AI 回复的话也“追加”到记事本，这样下次它才知道自己说过啥 ---
        messages.append({"role": "assistant", "content": reply})
        # 在打印完 [Assistant] 的回复后，顺手存一下
        with open("chat_log.txt", "a", encoding="utf-8") as f:
            f.write(f"用户: {user_input}\n")
            f.write(f"Assistant: {reply}\n\n")
    except Exception as e:
        print(f"哎呀，出错了!(报错): {e}")
        break