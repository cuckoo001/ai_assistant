'''
改造助手
让它不停地等你提问
带“记忆力”的助手

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

# --- 变化在这里：让用户输入 ---
# 程序运行到这里会停住，等你打字并按回车
# # --- 开启永动机模式 ---
print("--- 助手已上线，输入任意内容开始聊天,(具有记忆力模式) (按 Ctrl+C 退出) ---")

while True:
    user_input = input("\n[有问题 尽管问]: ")

    # 准备你的问题（这是一个列表，装着对话内容）
    # 把 user_input 这个变量塞进 messages 列表里
    # 使用 append 把用户的话“追加”到记事本末尾 ---
    messages.append({"role": "user", "content": user_input})


    # 向大模型发送一次“对话请求”，让 AI 根据你的 messages 生成回复
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    # 从返回结果中，拿到第一个回答 → 取它的 message → 从模型返回结果中，提取“真正的回复内容
    reply = response.choices[0].message.content
    print(f"[Assistant]: {reply}")

    # --- 重要：把 AI 回复的话也“追加”到记事本，这样下次它才知道自己说过啥 ---
    messages.append({"role": "assistant", "content": reply})
