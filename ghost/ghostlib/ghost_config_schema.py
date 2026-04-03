# -*- coding: utf-8 -*-
"""
Ghost 配置验证模型

使用 Pydantic 验证 Ghost 配置文件，确保配置项的类型和安全约束
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
import re


class ServerConfig(BaseModel):
    """服务器配置"""
    host: str = Field("0.0.0.0", description="监听地址")
    port: int = Field(443, ge=1, le=65535, description="监听端口")
    ssl: bool = Field(True, description="是否启用 SSL")
    client_cert_required: bool = Field(True, description="是否要求客户端证书")

    @validator('port')
    def validate_port(cls, v: int) -> int:
        if v < 1 or v > 65535:
            raise ValueError('端口必须在 1-65535 范围内')
        return v


class SecurityConfig(BaseModel):
    """安全配置"""
    bind_password_min_length: int = Field(16, ge=8, description="Bind 密码最小长度")
    allow_default_credentials: bool = Field(False, description="是否允许使用默认凭据（生产环境应设为 False）")
    enable_gnome_keyring: bool = Field(False, description="是否启用 Gnome Keyring 存储密码")

    @validator('bind_password_min_length')
    def validate_password_length(cls, v: int) -> int:
        if v < 8:
            raise ValueError('密码最小长度不能小于 8')
        return v


class LoggingConfig(BaseModel):
    """日志配置"""
    level: str = Field("INFO", description="日志级别: DEBUG, INFO, WARNING, ERROR")
    file: Optional[str] = Field(None, description="日志文件路径")
    max_size_mb: int = Field(10, ge=1, description="日志文件最大大小(MB)")
    backup_count: int = Field(5, ge=0, description="保留的日志文件数")
    sanitize_sensitive: bool = Field(True, description="自动脱敏敏感数据")

    @validator('level')
    def validate_level(cls, v: str) -> str:
        allowed = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        v_upper = v.upper()
        if v_upper not in allowed:
            raise ValueError(f'日志级别必须是: {", ".join(allowed)}')
        return v_upper


class NetworkConfig(BaseModel):
    """网络配置"""
    timeout: int = Field(10, ge=1, description="连接超时时间(秒)")
    keepalive: bool = Field(True, description="是否启用 Keep-Alive")
    retry_count: int = Field(3, ge=0, description="重试次数")
    dns_enabled: bool = Field(True, description="是否启用 DNS 解析")

    @validator('timeout')
    def validate_timeout(cls, v: int) -> int:
        if v < 1:
            raise ValueError('超时时间必须大于 0')
        return v


class GhostConfigSchema(BaseModel):
    """完整的 Ghost 配置架构"""
    server: ServerConfig = Field(default_factory=ServerConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    network: NetworkConfig = Field(default_factory=NetworkConfig)

    # 自定义配置节（允许扩展）
    custom: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic 配置"""
        extra = 'allow'  # 允许额外字段
        validate_assignment = True


def validate_config_dict(config_data: Dict[str, Any]) -> GhostConfigSchema:
    """从字典验证配置并返回模型实例

    Args:
        config_data: 配置字典（通常从 ConfigParser 转换而来）

    Returns:
        GhostConfigSchema: 验证后的配置模型

    Raises:
        pydantic.ValidationError: 如果配置无效
    """
    return GhostConfigSchema(**config_data)


def config_to_dict(config_parser) -> Dict[str, Dict[str, Any]]:
    """将 ConfigParser 对象转换为字典"""
    result: Dict[str, Dict[str, Any]] = {}
    for section in config_parser.sections():
        result[section] = {}
        for key, value in config_parser.items(section):
            # 尝试转换类型
            result[section][key] = _convert_value(value)
    return result


def _convert_value(value: str) -> Any:
    """将字符串转换为适当的类型"""
    # 布尔值
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'
    # 整数
    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
        try:
            return int(value)
        except ValueError:
            pass
    # 浮点数
    try:
        float_val = float(value)
        if '.' in value:
            return float_val
    except ValueError:
        pass
    # 保持原样（字符串）
    return value
