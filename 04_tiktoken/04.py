from message import Message
from count_tokens import count_tokens
from tiktoken import get_encoding

messages = [Message(role="system", content="Hey, you!")]

num = count_tokens(messages, 'gpt-4')  # 11
print("Token Count: ", num)
encoding = get_encoding("cl100k_base")
print("Token IDs: ", encoding.encode(messages[0].content))
