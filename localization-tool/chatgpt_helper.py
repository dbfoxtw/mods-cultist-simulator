import os
from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError, AuthenticationError, APIConnectionError

class ChatGPTHelper:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def review(self, source_text, translated_text, matched_nouns):
        system_prompt = self.get_system_prompt()
        user_prompt = self.get_user_prompt(source_text, translated_text, matched_nouns)

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

    def get_system_prompt(self):
        return """
你是神祕學卡牌遊戲翻譯審稿員，我會貼兩個文本，分別是英文原文、中文翻譯，請針對翻譯檢查以下問題：
1. 漏譯或誤譯（與英文原文不符）
2. 語病或句法錯誤
3. 不符合台灣慣用語的人名、地名、表達（如直翻、陸式用語）

此外，請遵守以下規定：
1. 半引號內部只允許“”，禁止使用「」。
2. 如果有提供，則保留專有詞。
3. 除了建議與理由，也需提供修正後的全文。
4. 為節省時間，若全部都不用改，簡潔說「無需修改」即可。"""

    def get_user_prompt(self, original, translated, matched_nouns):
        if matched_nouns:
            proper_noun_text = "\n".join(f"{pn.english} {pn.chinese}" for pn in matched_nouns)
        else:
            proper_noun_text = "無"

        return f"""英文：
{original}

中文：
{translated}

專有詞：
{proper_noun_text}"""