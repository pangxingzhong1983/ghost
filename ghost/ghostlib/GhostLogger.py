# -*- coding: utf-8 -*-
"""
Ghost 日志系统，包含敏感数据自动过滤功能
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import re
from typing import Pattern, Optional


class SensitiveDataFilter(logging.Filter):
    """敏感数据过滤器，自动脱敏日志中的密钥、密码等"""

    # 敏感信息正则模式
    PATTERNS: list[Pattern[str]] = [
        # RSA 私钥
        re.compile(
            r'(-----BEGIN (?:RSA )?PRIVATE KEY-----.*?-----END (?:RSA )?PRIVATE KEY-----)',
            re.DOTALL | re.IGNORECASE
        ),
        # SSL 私钥
        re.compile(
            r'(-----BEGIN PRIVATE KEY-----.*?-----END PRIVATE KEY-----)',
            re.DOTALL
        ),
        # 证书（可能包含敏感信息）
        re.compile(
            r'(-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----)',
            re.DOTALL
        ),
        # 密码模式
        re.compile(r'(?i)(password|pwd|pass)\s*[=:]\s*[\'"]([^\'\"]{8,})[\'"]'),
        # 高熵字符串（可能是密钥）
        re.compile(r'([A-Za-z0-9+/]{40,}={0,2})'),
        # JWT Token
        re.compile(r'(eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})'),
        # API Key 模式
        re.compile(r'(?i)(api[_-]?key|apikey|secret|token)\s*[=:]\s*[\'"]?([A-Za-z0-9]{20,})[\'"]?'),
    ]

    def __init__(
        self,
        name: str = '',
        mask_char: str = '***',
        enabled: bool = True
    ) -> None:
        super().__init__(name)
        self.mask_char = mask_char
        self.enabled = enabled

    def filter(self, record: logging.LogRecord) -> bool:
        """过滤日志记录"""
        if not self.enabled:
            return True

        # 脱敏消息内容
        if hasattr(record, 'getMessage'):
            msg = str(record.msg)
            if isinstance(record.args, tuple):
                try:
                    msg = msg % record.args
                except Exception:
                    pass

            sanitized = self._sanitize(msg)
            if sanitized != msg:
                record.msg = sanitized
                record.args = ()

        return True

    def _sanitize(self, text: str) -> str:
        """脱敏文本"""
        result = text
        for pattern in self.PATTERNS:
            if 'PRIVATE KEY' in pattern.pattern or 'CERTIFICATE' in pattern.pattern:
                result = pattern.sub('[REDACTED - Sensitive Key/Cert]', result)
            else:
                def replace_match(match: re.Match) -> str:
                    if match.lastindex and match.lastindex >= 2:
                        return match.group(1).split('=')[0] + f'= {self.mask_char}'
                    return self.mask_char
                result = pattern.sub(replace_match, result)
        return result


# 配置 logger
logger = logging.getLogger('ghost')
_sensitive_filter = SensitiveDataFilter(enabled=True)
logger.addFilter(_sensitive_filter)


def getLogger(name: str) -> logging.Logger:
    """获取子 logger，自动继承敏感数据过滤器"""
    child_logger = logger.getChild(name)
    # 确保子 logger 也应用过滤器
    if not any(isinstance(f, SensitiveDataFilter) for f in child_logger.filters):
        child_logger.addFilter(_sensitive_filter)
    return child_logger


def setup_logging(
    level: int = logging.INFO,
    format_str: Optional[str] = None,
    filename: Optional[str] = None
) -> None:
    """配置日志系统"""
    if format_str is None:
        format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    handlers: list[logging.Handler] = []

    # 控制台处理器
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(logging.Formatter(format_str))
    console.addFilter(SensitiveDataFilter())
    handlers.append(console)

    if filename:
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(format_str))
        file_handler.addFilter(SensitiveDataFilter())
        handlers.append(file_handler)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    for h in list(root_logger.handlers):
        root_logger.removeHandler(h)
        h.close()
    for h in handlers:
        root_logger.addHandler(h)

