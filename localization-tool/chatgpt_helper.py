import os
from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError, AuthenticationError, APIConnectionError

class ChatGPTHelper:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def review(self, source_text, translated_text):
        system_prompt = """
你是卡牌遊戲翻譯審稿員，請審查繁體中文翻譯內容，指出以下問題：
1. 漏譯或誤譯（與英文原文不符）
2. 語病或句法錯誤
3. 不符合台灣慣用語的人名、地名、表達（如直翻、陸式用語）

只需提供建議與理由，不需要修正後的全文。若無問題請回覆「無需修改」。"""

        user_prompt = f"""英文原文：{source_text}\n翻譯：{translated_text}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content

        except RateLimitError:
            return "⚠️ API 使用量已達上限，請稍後再試。"
        except AuthenticationError:
            return "❌ API 金鑰錯誤，請確認是否正確。"
        except APIConnectionError:
            return "🌐 無法連線到 OpenAI，請檢查網路。"
        except APIError as e:
            return f"🔥 OpenAI API 錯誤：{e.message}"
        except Exception as e:
            return f"🐱‍👤 未知錯誤：{e}"


