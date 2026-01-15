# app/services/input_sanitization.py
import re
from typing import Dict, List, Tuple


class InputSanitizationService:
    """敏感信息脱敏与输入清洗服务"""

    # 敏感信息正则模式
    PATTERNS = {
        "name": r"[\u4e00-\u9fa5]{2,4}(?:先生|女士)",
        "id_card": r"\d{15}|\d{17}[\dXx]",
        "phone": r"1[3-9]\d{9}",
        "email": r"\w+@\w+\.\w+",
    }

    # 危险模式（注入攻击）
    DANGEROUS_PATTERNS = [
        r"<script>",
        r"javascript:",
        r"onerror=",
        r"ignore instructions",
        r"print.*length",
    ]

    def sanitize(self, text: str) -> Tuple[str, Dict[str, List[str]]]:
        """
        清洗输入文本中的敏感信息

        Args:
            text: 原始文本

        Returns:
            (清洗后文本, 检测到的敏感信息字典)
        """
        detected = {}
        cleaned_text = text

        for key, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, cleaned_text)
            if matches:
                detected[key] = matches
                cleaned_text = re.sub(
                    pattern,
                    f"[{key}_已脱敏]",
                    cleaned_text
                )

        return cleaned_text, detected

    def validate_input(self, text: str) -> bool:
        """
        检测输入是否包含注入攻击

        Args:
            text: 输入文本

        Returns:
            True 表示安全，False 表示检测到攻击
        """
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return False
        return True
