"""Admin configuration manifest."""

from collections.abc import Iterable

from free_claude_code.config.provider_catalog import PROVIDER_CATALOG
from free_claude_code.config.reasoning import (
    FALLBACK_REASONING_PREFERENCES,
    ROOT_REASONING_PREFERENCES,
    ROUTE_REASONING_PREFERENCES,
    ReasoningPreference,
)
from free_claude_code.config.settings import Settings

from .provider_manifest import provider_field_specs
from .specs import ConfigFieldSpec, ConfigOptionSpec, ConfigSectionSpec


def _reasoning_options(
    preferences: tuple[ReasoningPreference, ...],
) -> tuple[ConfigOptionSpec, ...]:
    labels = {
        ReasoningPreference.INHERIT: "继承",
        ReasoningPreference.OFF: "关闭",
        ReasoningPreference.CLIENT: "跟随客户端",
        ReasoningPreference.LOW: "低",
        ReasoningPreference.MEDIUM: "中",
        ReasoningPreference.HIGH: "高",
        ReasoningPreference.XHIGH: "极高",
        ReasoningPreference.MAX: "最大",
    }
    return tuple(
        ConfigOptionSpec(preference.value, labels[preference])
        for preference in preferences
    )


SECTIONS: tuple[ConfigSectionSpec, ...] = (
    ConfigSectionSpec(
        "providers",
        "供应商",
        "供应商密钥、本地端点与代理设置。",
    ),
    ConfigSectionSpec(
        "models",
        "模型路由",
        "为每个模型同时选择模型与推理强度。档位覆盖项可继承默认值。",
    ),
    ConfigSectionSpec(
        "runtime",
        "运行时",
        "服务端 API 令牌、限流、超时与进程设置。",
    ),
    ConfigSectionSpec(
        "messaging",
        "消息",
        "Discord、Telegram、CLI 工作区与会话相关设置。",
    ),
    ConfigSectionSpec(
        "voice",
        "语音",
        "语音消息转写设置。",
    ),
    ConfigSectionSpec(
        "web_tools",
        "网页工具",
        "本地 Anthropic web_search 与 web_fetch 的行为设置。",
    ),
    ConfigSectionSpec(
        "diagnostics",
        "诊断",
        "日志与调试相关开关。",
        advanced=True,
    ),
    ConfigSectionSpec(
        "smoke",
        "冒烟测试",
        "可选的在线冒烟测试模型覆盖项。",
        advanced=True,
    ),
)


_NON_PROVIDER_FIELDS: tuple[ConfigFieldSpec, ...] = (
    ConfigFieldSpec(
        "MODEL",
        "默认模型",
        "models",
        "model",
        settings_attr="model",
        description="未设置档位覆盖时使用的供应商/模型。",
    ),
    ConfigFieldSpec(
        "MODEL_FABLE",
        "Fable 档位覆盖",
        "models",
        "optional_model",
        settings_attr="model_fable",
        description="选择 None 表示 Fable 请求沿用默认模型。",
    ),
    ConfigFieldSpec(
        "MODEL_OPUS",
        "Opus 档位覆盖",
        "models",
        "optional_model",
        settings_attr="model_opus",
        description="选择 None 表示 Opus 请求沿用默认模型。",
    ),
    ConfigFieldSpec(
        "MODEL_SONNET",
        "Sonnet 档位覆盖",
        "models",
        "optional_model",
        settings_attr="model_sonnet",
        description="选择 None 表示 Sonnet 请求沿用默认模型。",
    ),
    ConfigFieldSpec(
        "MODEL_HAIKU",
        "Haiku 档位覆盖",
        "models",
        "optional_model",
        settings_attr="model_haiku",
        description="选择 None 表示 Haiku 请求沿用默认模型。",
    ),
    ConfigFieldSpec(
        "MODEL_FALLBACKS",
        "回退模型",
        "models",
        "model_list",
        settings_attr="model_fallbacks",
        options=_reasoning_options(FALLBACK_REASONING_PREFERENCES),
        description=(
            "当所选供应商/模型在输出开始前失败时，按顺序尝试这些回退项。对所有客户端生效。一次请求可能访问多个供应商，并在每一处消耗额度。原生 Anthropic Messages 请求只会用其他 Anthropic 模型作为回退。"
        ),
    ),
    ConfigFieldSpec(
        "REASONING_POLICY",
        "默认推理强度",
        "models",
        "select",
        settings_attr="reasoning_policy",
        options=_reasoning_options(ROOT_REASONING_PREFERENCES),
        description=(
            "用于继承档位的路由以及直连供应商/模型的请求。选择「跟随客户端」时保留 CLI 的推理强度。原生 Anthropic 主请求使用客户端自身的思考控制。"
        ),
    ),
    ConfigFieldSpec(
        "REASONING_FABLE",
        "Fable 推理强度",
        "models",
        "select",
        settings_attr="reasoning_fable",
        options=_reasoning_options(ROUTE_REASONING_PREFERENCES),
    ),
    ConfigFieldSpec(
        "REASONING_OPUS",
        "Opus 推理强度",
        "models",
        "select",
        settings_attr="reasoning_opus",
        options=_reasoning_options(ROUTE_REASONING_PREFERENCES),
    ),
    ConfigFieldSpec(
        "REASONING_SONNET",
        "Sonnet 推理强度",
        "models",
        "select",
        settings_attr="reasoning_sonnet",
        options=_reasoning_options(ROUTE_REASONING_PREFERENCES),
    ),
    ConfigFieldSpec(
        "REASONING_HAIKU",
        "Haiku 推理强度",
        "models",
        "select",
        settings_attr="reasoning_haiku",
        options=_reasoning_options(ROUTE_REASONING_PREFERENCES),
    ),
    ConfigFieldSpec(
        "PROXY_AUTH_ENABLED",
        "要求 API 认证",
        "runtime",
        "boolean",
        settings_attr="proxy_auth_enabled",
        restart_required=True,
        description="FCC 的 API 路由要求携带已保存的 API/CLI 令牌。",
    ),
    ConfigFieldSpec(
        "ANTHROPIC_AUTH_TOKEN",
        "API/CLI 认证令牌",
        "runtime",
        "secret",
        settings_attr="proxy_auth_token",
        secret=True,
        restart_required=True,
        description=(
            "下发给所有客户端的已保存非空令牌。可以关闭认证而保留该令牌值。"
        ),
    ),
    ConfigFieldSpec(
        "PROVIDER_RATE_LIMIT",
        "供应商请求速率上限",
        "runtime",
        "number",
        settings_attr="provider_rate_limit",
    ),
    ConfigFieldSpec(
        "PROVIDER_RATE_WINDOW",
        "供应商速率统计窗口",
        "runtime",
        "number",
        settings_attr="provider_rate_window",
    ),
    ConfigFieldSpec(
        "PROVIDER_MAX_CONCURRENCY",
        "供应商最大并发数",
        "runtime",
        "number",
        settings_attr="provider_max_concurrency",
    ),
    ConfigFieldSpec(
        "PROVIDER_MAX_ATTEMPTS",
        "供应商最大尝试次数",
        "runtime",
        "number",
        settings_attr="provider_max_attempts",
        description=(
            "单个请求对每个模型的总尝试次数（含首次）。重试、流中断续传与模型发现都计入其中。"
        ),
    ),
    ConfigFieldSpec(
        "HTTP_READ_TIMEOUT",
        "HTTP 读取超时",
        "runtime",
        "number",
        settings_attr="http_read_timeout",
    ),
    ConfigFieldSpec(
        "HTTP_WRITE_TIMEOUT",
        "HTTP 写入超时",
        "runtime",
        "number",
        settings_attr="http_write_timeout",
    ),
    ConfigFieldSpec(
        "HTTP_CONNECT_TIMEOUT",
        "HTTP 连接超时",
        "runtime",
        "number",
        settings_attr="http_connect_timeout",
    ),
    ConfigFieldSpec(
        "HOST",
        "服务监听地址",
        "runtime",
        settings_attr="host",
        restart_required=True,
    ),
    ConfigFieldSpec(
        "PORT",
        "服务端口",
        "runtime",
        "number",
        settings_attr="port",
        restart_required=True,
    ),
    ConfigFieldSpec(
        "FCC_OPEN_BROWSER",
        "启动时自动打开管理台",
        "runtime",
        "boolean",
        settings_attr="open_admin_browser",
        description="下次 fcc-server 启动并健康后自动打开管理台。",
    ),
    ConfigFieldSpec(
        "MESSAGING_PLATFORM",
        "消息平台",
        "messaging",
        "select",
        settings_attr="messaging_platform",
        options=("telegram", "discord", "none"),
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "MESSAGING_RATE_LIMIT",
        "消息请求速率上限",
        "messaging",
        "number",
        settings_attr="messaging_rate_limit",
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "MESSAGING_RATE_WINDOW",
        "消息速率统计窗口",
        "messaging",
        "number",
        settings_attr="messaging_rate_window",
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "TELEGRAM_BOT_TOKEN",
        "Telegram 机器人 Token",
        "messaging",
        "secret",
        settings_attr="telegram_bot_token",
        secret=True,
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "ALLOWED_TELEGRAM_USER_ID",
        "允许的 Telegram 用户 ID",
        "messaging",
        settings_attr="allowed_telegram_user_id",
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "TELEGRAM_PROXY_URL",
        "Telegram 代理地址",
        "messaging",
        "secret",
        settings_attr="telegram_proxy_url",
        secret=True,
        session_sensitive=True,
        description="可选的 Telegram 专用代理，例如 socks5://127.0.0.1:1080。",
    ),
    ConfigFieldSpec(
        "DISCORD_BOT_TOKEN",
        "Discord 机器人 Token",
        "messaging",
        "secret",
        settings_attr="discord_bot_token",
        secret=True,
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "ALLOWED_DISCORD_CHANNELS",
        "允许的 Discord 频道",
        "messaging",
        settings_attr="allowed_discord_channels",
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "ALLOWED_DIR",
        "允许访问的目录",
        "messaging",
        settings_attr="allowed_dir",
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "MAX_MESSAGE_LOG_ENTRIES_PER_CHAT",
        "每个会话最多跟踪的消息数",
        "messaging",
        "number",
        settings_attr="max_message_log_entries_per_chat",
        advanced=True,
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "VOICE_NOTE_ENABLED",
        "语音消息",
        "voice",
        "boolean",
        settings_attr="voice_note_enabled",
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "WHISPER_DEVICE",
        "Whisper 运行设备",
        "voice",
        "select",
        settings_attr="whisper_device",
        options=("cpu", "cuda", "nvidia_nim"),
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "WHISPER_MODEL",
        "Whisper 模型",
        "voice",
        settings_attr="whisper_model",
        session_sensitive=True,
    ),
    ConfigFieldSpec(
        "ENABLE_WEB_SERVER_TOOLS",
        "网页服务工具",
        "web_tools",
        "boolean",
        settings_attr="enable_web_server_tools",
        description=(
            "允许 Claude Code 通过 FCC 使用 WebSearch，并允许强制调用本地网页工具。关闭后将禁止本地网页访问。"
        ),
    ),
    ConfigFieldSpec(
        "WEB_FETCH_ALLOWED_SCHEMES",
        "允许的网页抓取协议",
        "web_tools",
        settings_attr="web_fetch_allowed_schemes",
    ),
    ConfigFieldSpec(
        "WEB_FETCH_ALLOW_PRIVATE_NETWORKS",
        "允许访问私有网络",
        "web_tools",
        "boolean",
        settings_attr="web_fetch_allow_private_networks",
    ),
    ConfigFieldSpec(
        "LOG_LEVEL",
        "日志级别",
        "diagnostics",
        "select",
        settings_attr="log_level",
        options=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        advanced=True,
        restart_required=True,
    ),
    ConfigFieldSpec(
        "DEBUG_PLATFORM_EDITS",
        "调试平台文件修改",
        "diagnostics",
        "boolean",
        settings_attr="debug_platform_edits",
        advanced=True,
        restart_required=True,
    ),
    ConfigFieldSpec(
        "DEBUG_SUBAGENT_STACK",
        "调试子代理调用栈",
        "diagnostics",
        "boolean",
        settings_attr="debug_subagent_stack",
        advanced=True,
        restart_required=True,
    ),
    ConfigFieldSpec(
        "LOG_RAW_API_PAYLOADS",
        "记录原始 API 请求体",
        "diagnostics",
        "boolean",
        settings_attr="log_raw_api_payloads",
        advanced=True,
        restart_required=True,
    ),
    ConfigFieldSpec(
        "LOG_RAW_SSE_EVENTS",
        "记录原始 SSE 事件",
        "diagnostics",
        "boolean",
        settings_attr="log_raw_sse_events",
        advanced=True,
    ),
    ConfigFieldSpec(
        "LOG_API_ERROR_TRACEBACKS",
        "记录 API 错误堆栈",
        "diagnostics",
        "boolean",
        settings_attr="log_api_error_tracebacks",
        advanced=True,
        restart_required=True,
    ),
    ConfigFieldSpec(
        "LOG_RAW_MESSAGING_CONTENT",
        "记录原始消息内容",
        "diagnostics",
        "boolean",
        settings_attr="log_raw_messaging_content",
        advanced=True,
        restart_required=True,
    ),
    ConfigFieldSpec(
        "LOG_RAW_CLI_DIAGNOSTICS",
        "记录原始 CLI 诊断信息",
        "diagnostics",
        "boolean",
        settings_attr="log_raw_cli_diagnostics",
        advanced=True,
        restart_required=True,
    ),
    ConfigFieldSpec(
        "LOG_MESSAGING_ERROR_DETAILS",
        "记录消息功能错误详情",
        "diagnostics",
        "boolean",
        settings_attr="log_messaging_error_details",
        advanced=True,
        restart_required=True,
    ),
    ConfigFieldSpec(
        "FCC_SMOKE_MODEL_MISTRAL_REASONING",
        "冒烟测试 Mistral 推理模型",
        "smoke",
        advanced=True,
    ),
    ConfigFieldSpec(
        "FCC_SMOKE_NIM_MODELS",
        "冒烟测试 NIM 模型",
        "smoke",
        advanced=True,
    ),
    ConfigFieldSpec(
        "FCC_SMOKE_NIM_EXTRA_MODELS",
        "冒烟测试 NIM 额外模型",
        "smoke",
        advanced=True,
    ),
    ConfigFieldSpec(
        "FCC_SMOKE_OPENROUTER_FREE_MODELS",
        "冒烟测试 OpenRouter 免费模型",
        "smoke",
        advanced=True,
    ),
    ConfigFieldSpec(
        "FCC_SMOKE_OPENROUTER_FREE_EXTRA_MODELS",
        "冒烟测试 OpenRouter 免费额外模型",
        "smoke",
        advanced=True,
    ),
)


def _catalog_smoke_fields() -> tuple[ConfigFieldSpec, ...]:
    return tuple(
        ConfigFieldSpec(
            key=f"FCC_SMOKE_MODEL_{provider_id.upper()}",
            label=f"冒烟测试 {descriptor.display_name} 模型",
            section_id="smoke",
            advanced=True,
        )
        for provider_id, descriptor in PROVIDER_CATALOG.items()
    )


FIELDS: tuple[ConfigFieldSpec, ...] = (
    *provider_field_specs(),
    *_NON_PROVIDER_FIELDS,
    *_catalog_smoke_fields(),
)
FIELD_BY_KEY = {field.key: field for field in FIELDS}


def field_input_key(field: ConfigFieldSpec) -> str | None:
    """Return the Settings input key used for a manifest field."""

    if field.settings_attr is None:
        return None
    model_field = Settings.model_fields[field.settings_attr]
    alias = model_field.validation_alias
    if alias is None:
        return field.settings_attr
    return str(alias)


def env_keys() -> frozenset[str]:
    """Return env keys owned by the admin manifest."""

    return frozenset(field.key for field in FIELDS)


def fields_with_attrs() -> Iterable[ConfigFieldSpec]:
    """Yield fields that validate through Settings."""

    return (field for field in FIELDS if field.settings_attr is not None)
