"""Catalog-derived Admin provider fields."""

from dataclasses import replace
from typing import TypedDict

from free_claude_code.config.provider_catalog import PROVIDER_CATALOG
from free_claude_code.config.settings import ENV_KEY_BY_SETTING

from .specs import ConfigFieldSpec


class ProviderFieldOverride(TypedDict, total=False):
    """Optional catalog-field presentation overrides."""

    label: str
    description: str
    restart_required: bool


_PROVIDER_FIELD_OVERRIDES: dict[str, ProviderFieldOverride] = {
    "ANTHROPIC_API_KEY": {
        "description": "Anthropic API 访问，单独计费。Messages 请求使用 Anthropic 工具与客户端思考控制，原生回退仅使用其他 Anthropic 模型；FCC 的本地网页工具作用于兼容路由。",
    },
    "OPENAI_API_KEY": {
        "label": "OpenAI API 密钥",
        "description": "OpenAI Platform 的 API 密钥，与 ChatGPT 登录相互独立。",
    },
    "OPENAI_PROXY": {
        "description": (
            "可选的网络代理，不使用请留空。用于 OpenAI 登录与 ChatGPT Codex 请求；修改后会重启 FCC。"
        ),
        "restart_required": True,
    },
    "AZURE_OPENAI_API_KEY": {
        "description": "Azure OpenAI 资源的 API 密钥。",
    },
    "AZURE_OPENAI_BASE_URL": {
        "description": (
            "资源专属的 OpenAI v1 接口地址，例如 https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/。"
        ),
    },
    "NVIDIA_NIM_API_KEY": {
        "label": "NVIDIA NIM API 密钥",
        "description": "用于 NVIDIA NIM 对话，以及可选的 NIM 语音转写。",
    },
    "MISTRAL_API_KEY": {
        "label": "Mistral API 密钥",
        "description": (
            "Mistral La Plateforme（api.mistral.ai）；Experiment 套餐为免费档，但有速率限制。"
        ),
    },
    "CODESTRAL_API_KEY": {
        "label": "Codestral API 密钥",
        "description": (
            "Mistral Codestral 端点（codestral.mistral.ai），与 Mistral La Plateforme 的 ``MISTRAL_API_KEY`` 相互独立。编码与 FIM 领域说明见 Mistral 文档。"
        ),
    },
    "OPENCODE_API_KEY": {
        "label": "OpenCode API 密钥",
        "description": (
            "同时用于 OpenCode Zen 精选网关（opencode.ai/zen/v1）与 OpenCode Go 订阅网关（opencode.ai/zen/go/v1）；密钥在 opencode.ai/auth 获取。"
        ),
    },
    "AI_GATEWAY_API_KEY": {
        "label": "Vercel AI Gateway API 密钥",
        "description": (
            "Vercel AI Gateway 的 OpenAI 兼容端点密钥，端点 ai-gateway.vercel.sh/v1。"
        ),
    },
    "AWS_BEARER_TOKEN_BEDROCK": {
        "label": "Amazon Bedrock API 密钥",
        "description": (
            "Amazon Bedrock 的 Bearer API 密钥，用于对应区域的 Mantle OpenAI 兼容端点。"
        ),
    },
    "BEDROCK_BASE_URL": {
        "description": (
            "Amazon Bedrock Mantle 的 OpenAI 兼容接口地址，需与 API 密钥及所选模型同区域。"
        ),
    },
    "HUGGINGFACE_API_KEY": {
        "label": "Hugging Face API 密钥",
        "description": (
            "具备 Inference Providers 权限的 Hugging Face Token；当语音消息需要下载受限 Whisper 模型时也会使用。"
        ),
    },
    "COHERE_API_KEY": {
        "label": "Cohere API 密钥",
        "description": "Cohere 的 OpenAI 兼容 Compatibility API 密钥。",
    },
    "ZAI_API_KEY": {
        "label": "Z.ai API 密钥",
        "description": (
            "Z.ai Coding Plan（zai/...）与通用 API（zai_api/...）共用同一密钥；模型前缀决定使用 Coding Plan 额度还是按量付费余额。"
        ),
    },
    "FIREWORKS_API_KEY": {
        "label": "Fireworks API 密钥",
        "description": "Fireworks AI 推理 API 密钥。",
    },
    "NOVITA_API_KEY": {
        "label": "Novita AI API 密钥",
        "description": (
            "Novita AI 的 OpenAI 兼容 API 密钥（在 [novita.ai/settings/key-management](https://novita.ai/settings/key-management) 创建）。"
        ),
    },
    "MINIMAX_API_KEY": {
        "label": "MiniMax API 密钥",
        "description": (
            "MiniMax 的 OpenAI 兼容 Chat Completions API 密钥，端点位于 free_claude_code.api.minimax.io/v1。"
        ),
    },
    "KIMI_CODE_API_KEY": {
        "label": "Kimi Code API 密钥",
        "description": (
            "个人 Kimi Code 订阅密钥，来自 kimi.com/code/console；与 Kimi API 平台上的 KIMI_API_KEY 额度相互独立。"
        ),
    },
    "CLOUDFLARE_API_TOKEN": {
        "label": "Cloudflare API Token",
        "description": (
            "用于账号级 AI REST 请求的 Cloudflare API Token，需与 CLOUDFLARE_ACCOUNT_ID 一起使用。"
        ),
    },
    "GEMINI_API_KEY": {
        "label": "Gemini API 密钥",
        "description": (
            "Google AI Studio 的 Gemini API 密钥（Google AI Studio / Gemini API，[OpenAI 兼容](https://ai.google.dev/gemini-api/docs/openai)）；免费档按模型限流，且在英/瑞/欧洲经济区/欧盟以外地区数据可能被用于改进产品。"
        ),
    },
    "GROQ_API_KEY": {
        "label": "Groq API 密钥",
        "description": (
            "GroqCloud 的 OpenAI 兼容 API 密钥（[console.groq.com/keys](https://console.groq.com/keys)）；参见 Groq 的 [OpenAI 兼容文档](https://console.groq.com/docs/openai)。"
        ),
    },
    "CLINE_API_KEY": {
        "label": "Cline API 密钥",
        "description": (
            "先订阅 ClinePass，然后在 app.cline.bot 的 Settings > API Keys 下创建编程调用用 API 密钥。它不是 Cline CLI 的托管账号 Token。"
        ),
    },
    "XAI_API_KEY": {
        "label": "xAI API 密钥",
        "description": (
            "xAI 的 OpenAI 兼容 API 密钥，用于 Grok 对话与图像理解模型。"
        ),
    },
    "ALIBABA_CLOUD_API_KEY": {
        "description": (
            "阿里云百炼（Model Studio）按量付费 API 密钥，请使用与接口地址同区域的密钥。"
        ),
    },
    "ALIBABA_CLOUD_BASE_URL": {
        "description": (
            "可选的百炼 OpenAI 兼容接口地址，以 /compatible-mode/v1 结尾。默认新加坡区域；使用其他区域的密钥时，请填写对应区域或工作区的地址。"
        ),
    },
    "QWENCLOUD_API_KEY": {
        "label": "QwenCloud Token Plan API 密钥",
        "description": (
            "QwenCloud Token Plan 专用密钥（sk-sp-...）。Token Plan、Coding Plan 与按量付费的密钥走不同端点，不可混用。"
        ),
    },
    "QWENCLOUD_CODING_API_KEY": {
        "label": "QwenCloud Coding Plan API 密钥",
        "description": (
            "QwenCloud Coding Plan 专用密钥（sk-sp-...），供个人交互式编码代理使用。Token Plan、Coding Plan 与按量付费的密钥走不同端点，不可混用。"
        ),
    },
    "TOGETHER_API_KEY": {
        "label": "Together AI API 密钥",
        "description": (
            "Together AI 的 OpenAI 兼容 API 密钥，用于其无服务器与专属对话模型。"
        ),
    },
    "DEEPINFRA_API_KEY": {
        "label": "DeepInfra API 密钥",
        "description": (
            "DeepInfra API 密钥，用于其 OpenAI 兼容的对话与推理模型。"
        ),
    },
    "SILICONFLOW_API_KEY": {
        "label": "SiliconFlow API 密钥",
        "description": (
            "SiliconFlow API 密钥，用于其 OpenAI 兼容的对话、推理与视觉模型。"
        ),
    },
    "NEBIUS_API_KEY": {
        "label": "Nebius Token Factory API 密钥",
        "description": (
            "Nebius Token Factory API 密钥，用于其 OpenAI 兼容的对话、推理及支持工具调用的模型。"
        ),
    },
    "OPPER_API_KEY": {
        "label": "Opper API 密钥",
        "description": (
            "Opper 网关密钥，用于其托管在欧盟的模型池中 OpenAI 兼容的对话、推理及支持工具调用的模型。"
        ),
    },
    "SCW_SECRET_KEY": {
        "label": "Scaleway API 密钥",
        "description": (
            "Scaleway 生成式 API 的 Secret Key，用于其 OpenAI 兼容的对话及支持工具调用的模型。"
        ),
    },
    "CHUTES_API_KEY": {
        "label": "Chutes API 密钥",
        "description": (
            "Chutes API 密钥，用于其 OpenAI 兼容的对话、推理及支持工具调用的模型。"
        ),
    },
    "FEATHERLESS_API_KEY": {
        "label": "Featherless AI API 密钥",
        "description": (
            "Featherless AI API 密钥，用于套餐内可用的 OpenAI 兼容对话、推理及支持工具调用的模型。"
        ),
    },
    "SAMBANOVA_API_KEY": {
        "label": "SambaNova API 密钥",
        "description": (
            "SambaNova Cloud 的 OpenAI 兼容 API 密钥（在 [cloud.sambanova.ai/apis](https://cloud.sambanova.ai/apis) 创建）。"
        ),
    },
    "CEREBRAS_API_KEY": {
        "label": "Cerebras API 密钥",
        "description": (
            "Cerebras Inference API 密钥（在 [Cloud Console](https://cloud.cerebras.ai) 创建）；参考[快速开始](https://inference-docs.cerebras.ai/quickstart)与 [OpenAI 兼容说明](https://inference-docs.cerebras.ai/resources/openai)。"
        ),
    },
    "OLLAMA_API_KEY": {
        "description": (
            "Ollama API 密钥，用于直连 Ollama Cloud 的 OpenAI 兼容端点 ollama.com/v1。"
        ),
    },
    "TOKENROUTER_API_KEY": {
        "label": "TokenRouter API 密钥",
        "description": (
            "TokenRouter 的 OpenAI 兼容网关密钥，端点 api.tokenrouter.com/v1。"
        ),
    },
    "NARAROUTE_API_KEY": {
        "label": "NaraRoute API 密钥",
        "description": (
            "NaraRoute 的 OpenAI 兼容网关密钥，端点 router.bynara.id/v1。密钥以 sk-nry- 开头；可在 router.bynara.id/keys 创建。"
        ),
    },
    "LIGHTNING_API_KEY": {
        "label": "Lightning AI API 密钥",
        "description": (
            "Lightning AI Model APIs 密钥，端点 lightning.ai/api/v1。可在 lightning.ai 的 Model APIs 页面创建。"
        ),
    },
    "ORCAROUTER_API_KEY": {
        "label": "OrcaRouter API 密钥",
        "description": (
            "OrcaRouter 多供应商 OpenAI 兼容网关密钥，端点 api.orcarouter.ai/v1。密钥以 sk-orca- 开头；可在 www.orcarouter.ai/console 创建。"
        ),
    },
    "ATLASCLOUD_API_KEY": {
        "label": "Atlas Cloud API 密钥",
        "description": (
            "Atlas Cloud 多供应商 OpenAI 兼容网关密钥，端点 api.atlascloud.ai/v1；可在 console.atlascloud.ai/api-keys 创建。"
        ),
    },
    "XKIRO_API_KEY": {
        "label": "xKiro API 密钥",
        "description": (
            "xKiro API 密钥，端点 api.xkiro.com/v1。可在 xkiro.com/dashboard/api/keys 创建。"
        ),
    },
    "AGNES_API_KEY": {
        "label": "Agnes AI API 密钥",
        "description": (
            "Agnes AI 的 OpenAI 兼容 API 密钥，端点 apihub.agnes-ai.com/v1。"
        ),
    },
    "ZENMUX_API_KEY": {
        "label": "ZenMux API 密钥",
        "description": (
            "ZenMux 的 OpenAI 兼容网关密钥，端点 zenmux.ai/api/v1。可在 zenmux.ai/platform/pay-as-you-go 创建。"
        ),
    },
    "WANDB_API_KEY": {
        "label": "W&B Inference API 密钥",
        "description": (
            "W&B Serverless Inference 的 API 密钥，端点 api.inference.wandb.ai/v1。可在 [W&B 用户设置](https://wandb.ai/settings) 创建。"
        ),
    },
    "EXPLABS_API_KEY": {
        "label": "Experiential Labs API 密钥",
        "description": (
            "Experiential Labs 的 OpenAI 兼容网关密钥，端点 api.experientiallabs.ai/v1。密钥形如 xpl_ 加 40 位十六进制字符；可在 platform.experientiallabs.ai/settings/api-keys 创建。"
        ),
    },
    "CHEAPER_INFERENCE_API_KEY": {
        "label": "Cheaper Inference API 密钥",
        "description": (
            "Cheaper Inference 的 OpenAI 兼容网关密钥，端点 api.cheaperinference.com/v1。密钥以 ci_live_ 开头；可在 cheaperinference.com/signup 创建。"
        ),
    },
}


def provider_field_specs() -> tuple[ConfigFieldSpec, ...]:
    """Return provider fields generated from the provider catalog."""

    return (
        *_credential_field_specs(),
        ConfigFieldSpec(
            key="ANTHROPIC_WORKSPACE_ID",
            label="Anthropic 工作区 ID",
            section_id="providers",
            settings_attr="anthropic_workspace_id",
            provider_ids=("anthropic",),
            description="工作区级密钥可选；多工作区 API 密钥必填。",
        ),
        *_cloudflare_account_field_specs(),
        *_vertex_field_specs(),
        *_base_url_field_specs(),
        *_proxy_field_specs(),
    )


def _credential_field_specs() -> tuple[ConfigFieldSpec, ...]:
    specs: list[ConfigFieldSpec] = []
    seen_env_keys: set[str] = set()
    for descriptor in PROVIDER_CATALOG.values():
        if descriptor.credential_env is None:
            continue
        if descriptor.credential_env in seen_env_keys:
            continue
        seen_env_keys.add(descriptor.credential_env)
        specs.append(
            _with_override(
                ConfigFieldSpec(
                    key=descriptor.credential_env,
                    label=f"{descriptor.display_name} API 密钥",
                    section_id="providers",
                    field_type="api_key_list",
                    settings_attr=descriptor.credential_attr,
                    provider_ids=tuple(
                        provider.provider_id
                        for provider in PROVIDER_CATALOG.values()
                        if provider.credential_env == descriptor.credential_env
                    ),
                    secret=True,
                )
            )
        )
    return tuple(specs)


def _base_url_field_specs() -> tuple[ConfigFieldSpec, ...]:
    specs: list[ConfigFieldSpec] = []
    for descriptor in PROVIDER_CATALOG.values():
        if descriptor.base_url_attr is None:
            continue
        key = ENV_KEY_BY_SETTING[descriptor.base_url_attr]
        specs.append(
            _with_override(
                ConfigFieldSpec(
                    key=key,
                    label=f"{descriptor.display_name} 接口地址",
                    section_id="providers",
                    settings_attr=descriptor.base_url_attr,
                    provider_ids=(descriptor.provider_id,),
                )
            )
        )
    return tuple(specs)


def _cloudflare_account_field_specs() -> tuple[ConfigFieldSpec, ...]:
    return (
        ConfigFieldSpec(
            key="CLOUDFLARE_ACCOUNT_ID",
            label="Cloudflare 账号 ID",
            section_id="providers",
            settings_attr="cloudflare_account_id",
            provider_ids=("cloudflare",),
            description=(
                "用于拼接 /accounts/{id}/ai/v1 端点的 Cloudflare 账号 ID。"
            ),
        ),
    )


def _vertex_field_specs() -> tuple[ConfigFieldSpec, ...]:
    return (
        ConfigFieldSpec(
            key="VERTEX_PROJECT_ID",
            label="Google Cloud 项目 ID",
            section_id="providers",
            settings_attr="vertex_project_id",
            provider_ids=("vertex",),
            description=(
                "用于 Vertex AI 的 Google Cloud 项目。认证使用应用默认凭据（ADC）。"
            ),
        ),
        ConfigFieldSpec(
            key="VERTEX_LOCATION",
            label="Vertex AI 区域",
            section_id="providers",
            settings_attr="vertex_location",
            provider_ids=("vertex",),
            description=(
                "填 global 使用 Vertex AI 全球端点，或填写 us-central1 之类的区域。"
            ),
        ),
    )


def _proxy_field_specs() -> tuple[ConfigFieldSpec, ...]:
    specs: list[ConfigFieldSpec] = []
    for descriptor in PROVIDER_CATALOG.values():
        if descriptor.proxy_attr is None:
            continue
        specs.append(
            _with_override(
                ConfigFieldSpec(
                    key=ENV_KEY_BY_SETTING[descriptor.proxy_attr],
                    label=f"{descriptor.display_name} 代理",
                    description="可选的网络代理，不使用请留空",
                    section_id="providers",
                    field_type="secret",
                    settings_attr=descriptor.proxy_attr,
                    provider_ids=(descriptor.provider_id,),
                    secret=True,
                    advanced=True,
                )
            )
        )
    return tuple(specs)


def _with_override(spec: ConfigFieldSpec) -> ConfigFieldSpec:
    override = _PROVIDER_FIELD_OVERRIDES.get(spec.key)
    if override is None:
        return spec
    return replace(
        spec,
        label=override.get("label", spec.label),
        description=override.get("description", spec.description),
        restart_required=override.get("restart_required", spec.restart_required),
    )
