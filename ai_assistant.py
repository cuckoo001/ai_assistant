'''
对话一轮游
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
    print("[错误]: 未找到 API_KEY，请检查 .env 文件！")
    exit()

# 创建一个 客户端实例,并连接到一个 AI 服务接口，拿到一个“操作入口
client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)

# --- 变化在这里：让用户输入 ---
# 程序运行到这里会停住，等你打字并按回车
user_input = input("[用户]有问题 尽管问: ")

# 第三步：准备你的问题（这是一个列表，装着对话内容）
# 把 user_input 这个变量塞进 messages 列表里
messages = [
    {"role": "user", "content": user_input}
]


# 第四步：发送请求，让 AI 开始计算
response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=messages
)

# 第五步：把结果拿出来
print(f"[小龙虾]: {response.choices[0].message.content}")

