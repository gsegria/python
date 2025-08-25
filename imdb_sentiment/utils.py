import re

def clean_text(text: str) -> str:
    """簡單清理文字內容"""
    text = text.lower()
    text = re.sub(r"<.*?>", "", text)  # 移除 HTML 標籤
    text = re.sub(r"[^a-z\s]", "", text)  # 僅保留英文字母
    return text.strip()
