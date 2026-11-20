<div align="center">

<h1>
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="assets/free-claude-code-wordmark-light.svg">
    <img src="assets/free-claude-code-wordmark-dark.svg" alt="Free Claude Code" width="610">
  </picture>
</h1>

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-2e7d32.svg?style=for-the-badge)](https://github.com/Alishahryar1/free-claude-code/blob/main/LICENSE)
[![Python 3.14](https://img.shields.io/badge/python-3.14-3776ab.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Package Manager: uv](assets/package-manager-uv.svg)](https://github.com/astral-sh/uv)
[![Testing: Pytest](https://img.shields.io/badge/Testing-Pytest-ad1457.svg?style=for-the-badge)](https://github.com/pytest-dev/pytest)
[![Type Checker: Ty](https://img.shields.io/badge/Type%20Checker-ty-fdd835.svg?style=for-the-badge)](https://github.com/astral-sh/ty)
[![Formatter: Ruff](https://img.shields.io/badge/Formatter-ruff-bf4b00.svg?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Logging: Loguru](https://img.shields.io/badge/logging-loguru-00695c.svg?style=for-the-badge)](https://github.com/Delgan/loguru)

[快速开始](#quick-start) · [选择供应商](#choose-a-provider) · [客户端集成](#integrations) · [API 直连](#use-the-api-directly) · [手机端使用](#use-from-your-phone) · [安装维护](#manage-your-installation)

</div>

<p align="center">
  <em>独立开源项目，与 Anthropic 无隶属关系，也未获得其背书。Claude 与 Claude Code 是 Anthropic 的商标。</em>
</p>

> **关于本仓库**：这是 [Alishahryar1/free-claude-code](https://github.com/Alishahryar1/free-claude-code) 的**中文汉化分支**（`zh-cn`）。代码功能与上游保持一致并持续跟随上游更新，汉化内容仅存在于本分支，不会回推到上游。英文原版 README 见[上游 main 分支](https://github.com/Alishahryar1/free-claude-code/blob/main/README.md)。

<a id="features"></a>

## 功能特性

- 可以把任意受支持的客户端（harness）路由到任意受支持的供应商（provider）提供的模型。
- 支持 12 种客户端：[Claude Code](https://code.claude.com/docs/en/overview)、[Codex](https://github.com/openai/codex)、[Pi](https://github.com/earendil-works/pi)、[OpenCode](https://github.com/anomalyco/opencode)、[Cline](https://github.com/cline/cline)、[Hermes](https://github.com/NousResearch/hermes-agent)、[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)、[Grok Build](https://github.com/xai-org/grok-build)、[Muse Code](https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2/)、[Aider](https://aider.chat/)、[Antigravity CLI](https://antigravity.google/docs/getting-started/)，以及 [VS Code Chat](https://code.visualstudio.com/)。
  - 完整保留原生流式输出、工具调用与交错思考，性能不打折。
  - 对 Claude Code，可把 [Fable](https://www.anthropic.com/claude/fable)、[Opus](https://www.anthropic.com/claude/opus)、[Sonnet](https://www.anthropic.com/claude/sonnet)、[Haiku](https://www.anthropic.com/claude/haiku) 四档分别路由到受支持的模型。
- 任意模型都可以通过四种 API 调用：[Anthropic Messages](https://platform.claude.com/docs/en/api/messages)（`/v1/messages`）、[OpenAI Chat Completions](https://platform.openai.com/docs/api-reference/chat/create)（`/v1/chat/completions`）、[OpenAI Responses](https://platform.openai.com/docs/api-reference/responses/create)（`/v1/responses`）或 [Gemini](https://ai.google.dev/api/generate-content)（`generateContent`）。参见 [API 直连](#use-the-api-directly)。
- 支持 61 家供应商，涵盖免费、付费、订阅制和本地供应商。
  - 每月 1.3B+ 免费 token 额度。
  - FCC 遵守各供应商的服务条款（TOS），一旦某项接入不再被允许，会移除该接入。
- 可在终端、桌面应用（[Codex App](https://learn.chatgpt.com/docs/app)、[Claude Desktop](https://claude.ai/download)、[DeepSeek Desktop](https://github.com/deepseek-ai/deepseek-harness)）、IDE 插件（[VS Code](https://code.visualstudio.com/) 与 [JetBrains](https://www.jetbrains.com/)）、[手机](#use-from-your-phone)（[Discord](https://discord.com/) 与 [Telegram](https://telegram.org/)），或者浏览器里的原生 Code 会话中使用。
  - Discord 与 Telegram 支持语音消息，可用本地 [Whisper](https://github.com/openai/whisper) 或 [NVIDIA NIM](https://docs.nvidia.com/nim/speech/latest/asr/deploy-asr-models/whisper.html) 转写。
- 借助 [RTK](https://github.com/rtk-ai/rtk) 与 [Headroom](https://github.com/headroomlabs-ai/headroom)，token 用量最高可降低 90%。
- 具备业界领先的可靠性特性，供应商故障时也能持续编码：
  - 自动重试。
  - 可配置的速率限制。
  - 可配置的并发控制。
  - 自动切换模型／供应商。
  - 多 API Key 自动顺延。

免费额度是否可用以及上限由各供应商自行控制，可能随时变化。

<div align="center">
  <img src="assets/pic.png" alt="Claude Code 通过 Free Claude Code 运行" width="700">
  <p><em>Claude Code 通过 FCC 运行。</em></p>
</div>

<div align="center">
  <img src="assets/browser-code-session.png" alt="FCC 中的原生 Codex 浏览器会话，展示模型控制与代码仓库探索" width="700">
  <p><em>FCC 浏览器界面中的原生 Codex 会话。</em></p>
</div>

<a id="quick-start"></a>

## 快速开始

<a id="install"></a>

### 1. 安装

macOS/Linux：

```bash
curl -fsSL "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.sh" | sh
```

Windows PowerShell：

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.ps1")))
```

按提示选择至少一个编码代理；对受支持的代理，还可选择启用 [RTK](https://github.com/rtk-ai/rtk) + [Headroom](https://github.com/headroomlabs-ai/headroom) 的 token 优化。

### 2. 启动 FCC

#### Windows

从桌面或开始菜单打开 **Free Claude Code**。

#### macOS

从桌面或「应用程序」文件夹打开 **Free Claude Code**。

#### Linux

运行：

```bash
fcc-server
```

FCC 启动后会自动打开 Admin 管理界面。在 Windows 和 macOS 上，可通过托盘或菜单栏图标打开 Admin、重启或退出。使用 `fcc-server` 时，请保持其终端窗口开启。

<a id="nvidia-nim-provider"></a>

### 3. 配置 NVIDIA NIM

1. 到 [build.nvidia.com/settings/api-keys](https://build.nvidia.com/settings/api-keys) 创建 API Key。
2. 从服务端日志中找到 Admin 界面地址并打开。
3. 在 **供应商** 中打开 NVIDIA NIM，点击 **添加密钥**，粘贴 Key，然后点击 **保存**。
4. `MODEL` 保持默认的 `nvidia_nim/nvidia/nemotron-3-ultra-550b-a55b`，或在模型下拉框中搜索并选择其他模型。
5. 点击 **应用** 保存模型选择。

如需用 Bearer Token 保护本地代理，请在 Admin 中启用 **要求 API 认证**。

<div align="center">
  <img src="assets/admin-page.png" alt="Free Claude Code Admin 管理界面" width="700">
</div>

### 4. 运行你的编码代理

Claude Code：

```bash
fcc-claude
```

Codex：

```bash
fcc-codex
```

Pi：

```bash
fcc-pi
```

OpenCode 2：

```bash
fcc-opencode
```

Cline：

```bash
fcc-cline
```

Hermes：

```bash
fcc-hermes
```

DeepSeek Harness Web：

```bash
fcc-dsh
```

Grok Build：

```bash
fcc-grok
```

Muse Code：

```bash
fcc-muse
```

Aider：

```bash
fcc-aider
```

Antigravity CLI：

```bash
fcc-agy
```

其他客户端与 SDK 也可以直接调用 FCC，参见 [API 直连](#use-the-api-directly)。

<a id="model-picker"></a>

<div align="center">
  <img src="assets/cc-model-picker.png" alt="Claude Code 模型选择器显示 FCC 模型" width="700">
  <p><em>在 Claude Code 原生 <code>/model</code> 选择器中选中 FCC 模型。</em></p>
</div>

<a id="choose-a-provider"></a>

## 选择供应商

1. 打开下方对应供应商的链接，查看其 Key、模型或配置说明。
2. 在 Admin 界面中配置表中列出的设置项。OpenAI / ChatGPT 订阅制接入请走 **供应商 → OAuth 供应商**。
3. 在 `MODEL` 下拉框中搜索并选择模型。如果供应商无法列出模型，请手动填写 `<provider-id>/<exact-provider-model-id>`。
4. 点击 **应用**。

可选：在 **模型配置** 下添加一个有序的 **回退模型**列表。它对所有已连接的客户端生效。一次失败的请求在成功之前，可能已经访问并消耗了多个供应商的额度。

供应商弹窗支持带编号的多 API Key。可用 **添加密钥** 新增、删除行，或拖动行手柄调整顺序。FCC 使用 1 号 Key。

如果要接入其他 API 端点，打开 **供应商 → 自定义供应商 → 添加供应商**，填写其 API Base URL、可选的 Key 和 API 格式。**模型 ID** 留空可自动发现模型，或每行填一个上游模型 ID。保存后到 **模型配置** 中选择模型。

<details>
<summary><strong>供应商目录</strong></strong></summary>

| 供应商 | Admin 界面配置项 | 示例 `MODEL` |
| --- | --- | --- |
| [NVIDIA NIM](https://build.nvidia.com/settings/api-keys) | `NVIDIA_NIM_API_KEY` | `nvidia_nim/nvidia/nemotron-3-ultra-550b-a55b` |
| [OpenRouter](https://openrouter.ai/keys) | `OPENROUTER_API_KEY` | `open_router/openrouter/free` |
| [Groq](https://console.groq.com/keys) | `GROQ_API_KEY` | `groq/llama-3.3-70b-versatile` |
| [ClinePass](https://docs.cline.bot/getting-started/clinepass) | `CLINE_API_KEY` | `cline_pass/cline-pass/kimi-k3` |
| [OpenAI / ChatGPT](https://learn.chatgpt.com/docs/auth) | 在 Admin 界面连接 ChatGPT | `openai/<model-id>` |
| [OpenAI API](https://platform.openai.com/api-keys) | `OPENAI_API_KEY` | `openai_api/gpt-5.6-sol` |
| [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-sdk/auth/authenticate) | 在 Admin 界面连接 GitHub Copilot | `github_copilot/<model-id>` |
| [xAI (Grok)](https://console.x.ai/team/default/api-keys) | `XAI_API_KEY` | `xai/grok-4.5` |
| [Alibaba Cloud](https://www.alibabacloud.com/help/en/model-studio/get-api-key) | `ALIBABA_CLOUD_API_KEY` | `alibaba_cloud/<model-id>` |
| [QwenCloud Token Plan](https://home.qwencloud.com/api-keys) | `QWENCLOUD_API_KEY` | `qwencloud/qwen3.7-plus` |
| [QwenCloud Coding Plan](https://home.qwencloud.com/api-keys) | `QWENCLOUD_CODING_API_KEY` | `qwencloud_coding/qwen3.7-plus` |
| [Together AI](https://api.together.ai/settings/api-keys) | `TOGETHER_API_KEY` | `together/zai-org/GLM-5.2` |
| [DeepInfra](https://deepinfra.com/dash/api_keys) | `DEEPINFRA_API_KEY` | `deepinfra/deepseek-ai/DeepSeek-V4-Flash` |
| [SiliconFlow](https://cloud.siliconflow.com/account/ak) | `SILICONFLOW_API_KEY` | `siliconflow/Qwen/Qwen3-32B` |
| [Nebius Token Factory](https://tokenfactory.nebius.com/project/api-keys) | `NEBIUS_API_KEY` | `nebius/Qwen/Qwen3-30B-A3B` |
| [Chutes](https://chutes.ai/docs/getting-started/authentication) | `CHUTES_API_KEY` | `chutes/Qwen/Qwen3-32B-TEE` |
| [Featherless AI](https://featherless.ai/account/api-keys) | `FEATHERLESS_API_KEY` | `featherless/Qwen/Qwen3-32B` |
| [Agnes AI](https://agnes-ai.com/) | `AGNES_API_KEY` | `agnes/agnes-2.0-flash` |
| [ZenMux](https://zenmux.ai/platform/pay-as-you-go) | `ZENMUX_API_KEY` | `zenmux/deepseek/deepseek-v4-flash-free` |
| [W&B Inference](https://wandb.ai/settings) | `WANDB_API_KEY` | `wandb/openai/gpt-oss-20b` |
| [Anthropic](https://platform.claude.com/settings/keys) | `ANTHROPIC_API_KEY` | `anthropic/<model-id>` |
| [Azure OpenAI](https://learn.microsoft.com/azure/foundry/openai/how-to/chatgpt) | `AZURE_OPENAI_API_KEY` 与 `AZURE_OPENAI_BASE_URL` | `azure_openai/<deployment-name>` |
| [Google AI Studio (Gemini)](https://aistudio.google.com/apikey) | `GEMINI_API_KEY` | `gemini/models/gemini-3.1-flash-lite` |
| [Google Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/start/openai) | `VERTEX_PROJECT_ID` + ADC | `vertex/google/gemini-3.5-flash` |
| [DeepSeek](https://platform.deepseek.com/api_keys) | `DEEPSEEK_API_KEY` | `deepseek/deepseek-chat` |
| [Mistral La Plateforme](https://console.mistral.ai/) | `MISTRAL_API_KEY` | `mistral/devstral-small-latest` |
| [Mistral Codestral](https://console.mistral.ai/) | `CODESTRAL_API_KEY` | `mistral_codestral/codestral-latest` |
| [OpenCode Zen](https://opencode.ai/auth) | `OPENCODE_API_KEY` | `opencode_zen/gpt-5.3-codex` |
| [OpenCode Go](https://opencode.ai/auth) | `OPENCODE_API_KEY` | `opencode_go/minimax-m2.7` |
| [Vercel AI Gateway](https://vercel.com/docs/ai-gateway/models-and-providers) | `AI_GATEWAY_API_KEY` | `vercel/openai/gpt-5.5` |
| [Amazon Bedrock](https://console.aws.amazon.com/bedrock/) | `AWS_BEARER_TOKEN_BEDROCK` | `bedrock/openai.gpt-oss-120b` |
| [Hugging Face Inference Providers](https://huggingface.co/settings/tokens) | `HUGGINGFACE_API_KEY` | `huggingface/Qwen/Qwen3-Coder-480B-A35B-Instruct:fastest` |
| [Cohere](https://dashboard.cohere.com/api-keys) | `COHERE_API_KEY` | `cohere/command-a-plus-05-2026` |
| [Wafer](https://wafer.ai/) | `WAFER_API_KEY` | `wafer/DeepSeek-V4-Pro` |
| [Kimi API](https://platform.moonshot.ai/console/api-keys) | `KIMI_API_KEY` | `kimi/kimi-k2.5` |
| [Kimi Code](https://www.kimi.com/code/console) | `KIMI_CODE_API_KEY` | `kimi_code/k3` |
| [MiniMax](https://platform.minimax.io/user-center/basic-information/interface-key) | `MINIMAX_API_KEY` | `minimax/MiniMax-M3` |
| [Cerebras Inference](https://cloud.cerebras.ai/) | `CEREBRAS_API_KEY` | `cerebras/gpt-oss-120b` |
| [SambaNova](https://cloud.sambanova.ai/apis) | `SAMBANOVA_API_KEY` | `sambanova/Meta-Llama-3.3-70B-Instruct` |
| [Kilo.ai](https://kilo.ai) | `KILO_API_KEY` | `kilo/kilo-auto/free` |
| [Fireworks AI](https://fireworks.ai/account/api-keys) | `FIREWORKS_API_KEY` | `fireworks/accounts/fireworks/models/llama-v3p3-70b-instruct` |
| [Novita AI](https://novita.ai/settings/key-management) | `NOVITA_API_KEY` | `novita/deepseek/deepseek-v4-flash-0731` |
| [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/) | `CLOUDFLARE_API_TOKEN` 与 `CLOUDFLARE_ACCOUNT_ID` | `cloudflare/@cf/moonshotai/kimi-k2.6` |
| [Z.ai Coding Plan](https://z.ai/manage-apikey/apikey-list) | `ZAI_API_KEY` | `zai/glm-5.2` |
| [Z.ai API (pay as you go)](https://z.ai/manage-apikey/apikey-list) | `ZAI_API_KEY` | `zai_api/glm-4.7-flash` |
| [TokenRouter](https://www.tokenrouter.com/) | `TOKENROUTER_API_KEY` | `tokenrouter/moonshotai/kimi-k3-free` |
| [NaraRoute](https://router.bynara.id/) | `NARAROUTE_API_KEY` | `nararoute/kimi-k3-free` |
| [Poolside AI](https://platform.poolside.ai/) | `POOLSIDE_API_KEY` | `poolside/poolside/laguna-s-2.1` |
| [LLM7.io](https://dash.llm7.io/) | `LLM7_API_KEY` | `llm7/default` |
| [Scaleway](https://console.scaleway.com/iam/api-keys) | `SCW_SECRET_KEY` | `scaleway/deepseek/deepseek-v4-flash` |
| [Lightning AI](https://lightning.ai/) | `LIGHTNING_API_KEY` | `lightning/lightning-ai/Qwen3.8-27B` |
| [Experiential Labs](https://platform.experientiallabs.ai/) | `EXPLABS_API_KEY` | `experiential/union-alpha` |
| [Cheaper Inference](https://cheaperinference.com/signup) | `CHEAPER_INFERENCE_API_KEY` | `cheaperinference/gpt-5.4-mini` |
| [OrcaRouter](https://www.orcarouter.ai/) | `ORCAROUTER_API_KEY` | `orcarouter/deepseek/deepseek-v4-flash-free` |
| [Atlas Cloud](https://console.atlascloud.ai/api-keys) | `ATLASCLOUD_API_KEY` | `atlascloud/deepseek-ai/deepseek-v4-flash` |
| [xKiro](https://xkiro.com/) | `XKIRO_API_KEY` | `xkiro/qwen/qwen3.7-flash:free` |
| [Opper](https://platform.opper.ai/) | `OPPER_API_KEY` | `opper/claude-sonnet-4-6` |
| [Ollama Cloud](https://ollama.com/settings/keys) | `OLLAMA_API_KEY` | `ollama_cloud/qwen3-coder:480b` |
| [LM Studio](https://lmstudio.ai/) | `LM_STUDIO_BASE_URL` | `lmstudio/<model-id>` |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | `LLAMACPP_BASE_URL` | `llamacpp/<model-id>` |
| [Ollama](https://ollama.com/) | `OLLAMA_BASE_URL` | `ollama/<model-tag>` |

</details>

<details>
<summary><strong>各供应商专项配置</strong></strong></summary>

- OpenAI / ChatGPT 用的是你的 ChatGPT 订阅，而非 API Key。在 Admin 界面依次打开
  **Providers → OAuth providers → OpenAI / ChatGPT → Connect**，
  然后在浏览器中完成登录。连接后请重启已在运行的代理。
- Anthropic 使用单独计费的 API Key。在
  **Providers → Cloud providers → Anthropic → Configure** 中添加，然后选择一个已发现的模型。
  多工作区的 Key 还需要设置 `ANTHROPIC_WORKSPACE_ID`。
- OpenAI API 使用的是独立的 Platform API Key。在
  **Providers → Cloud providers → OpenAI API → Configure** 中填写。模型列表中可能
  包含无法处理编码请求的 ID，请选择文本生成类模型。
- GitHub Copilot 使用你已登录的 GitHub 账号与订阅。请先把
  [Copilot CLI 1.0.83](https://github.com/github/copilot-cli/releases/tag/v1.0.83)
  安装到 PATH，然后选择 **Providers → OAuth providers → GitHub Copilot → Connect**，
  完成登录后从模型选择器中选择 `github_copilot/<model-id>`。
  可用模型与配额取决于你的订阅和组织策略。连接后请重启已在运行的代理。
- Azure OpenAI 使用你资源中的部署名（deployment name）。把
  `AZURE_OPENAI_BASE_URL` 设置为其完整的 v1 端点，例如
  `https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/`，并选择支持 Chat Completions 的部署。
  若该部署没有出现在模型下拉框中，请把部署名作为自定义模型 slug 手动填入。
- Mistral Codestral 使用与 Mistral La Plateforme 不同的 Key。
- Kimi Code 订阅 Key 使用 `kimi_code/` 前缀；Kimi API 额度 Key 使用
  `kimi/` 前缀。Kimi Code 套餐仅供个人交互式编码代理使用，需遵守
  [Kimi 社区准则](https://www.kimi.com/code/docs/en/kimi-code/community-guidelines.html)。
- Alibaba Cloud 使用 Model Studio 按量付费 Key，默认区域为新加坡。
  若使用其他区域或工作区，请把 `ALIBABA_CLOUD_BASE_URL` 设为其
  [OpenAI 兼容端点](https://www.alibabacloud.com/help/en/model-studio/base-url)
  （以 `/compatible-mode/v1` 结尾）。Key 与端点必须属于同一区域。
- QwenCloud Coding Plan 的 Key 使用 `qwencloud_coding/` 前缀；QwenCloud Token Plan 的
  Key 使用 `qwencloud/` 前缀。两者 Key 与端点不可互换。Coding Plan
  仅供本地、个人、交互式编码代理使用，需遵守
  [Coding Plan 条款](https://www.alibabacloud.com/help/en/model-studio/coding-plan)。
- OpenCode Zen 与 OpenCode Go 共用 `OPENCODE_API_KEY`，但模型前缀必须显式写
  `opencode_zen/` 或 `opencode_go/`。
- 使用 Amazon Bedrock 时，把 `BEDROCK_BASE_URL` 设为与 API Key 同一区域的 URL，
  并从列表中选一个模型。
- Vertex AI 使用 Google 应用默认凭据（ADC）而非 API Key。本地需先执行一次
  `gcloud auth application-default login`。也支持服务账号文件与附加服务账号。
  设置 `VERTEX_PROJECT_ID`，并可选择性修改默认值为 `global` 的 `VERTEX_LOCATION`。
- Cloudflare 需要同时提供 API Token 与 Account ID。
- Ollama Cloud 请使用模型选择器中显示的精确模型 ID。本地 Ollama 使用单独的
  `ollama/` 前缀。
- 编码代理优先选用支持工具调用的模型。本地模型还需要足够上下文来容纳代理的系统提示与工具定义。

</details>

<details>
<summary><strong>本地供应商配置</strong></strong></summary>

FCC 启动时会自动发现正在运行的本地服务中的模型。如果你之后才启动某个服务，在 Admin 中点击 **刷新模型**，即可把它的模型加入选择器。

### LM Studio

启动 LM Studio 的本地服务，加载一个支持工具调用的模型，然后使用 LM Studio 显示的模型标识并加上 `lmstudio/` 前缀。默认地址为 `http://localhost:1234/v1`。

### llama.cpp

以 OpenAI 兼容的 Chat Completions API 启动 `llama-server`，并给它足够的上下文。使用本地模型 ID 加 `llamacpp/` 前缀。`LLAMACPP_BASE_URL` 默认为 `http://localhost:8080/v1`。

### Ollama

```bash
ollama pull llama3.1
ollama serve
```

使用 `ollama list` 显示的 tag 加 `ollama/` 前缀。`OLLAMA_BASE_URL` 默认为 `http://localhost:11434`。

供应商卡片会显示检测到的端点与响应时间；本地服务不可用时会给出提示。启动服务或改正其配置后，点击 **测试** 刷新其模型列表。

</details>

<details>
<summary><strong>可选的模型档位路由</strong></summary>

`MODEL` 是所有请求的兜底。为 `MODEL_FABLE`、`MODEL_OPUS`、`MODEL_SONNET` 或 `MODEL_HAIKU` 选择模型，可单独覆盖 Claude Code 的某一档。选择 **None** 表示仍使用 `MODEL`。

在 **Admin UI → 模型配置** 中按 FCC 的重试顺序添加 **回退模型**。每个回退项都有各自的推理强度：**继承**、**关闭**、**跟随客户端**、**低**、**中**、**高**、**极高** 或 **最大**。

在底部一行选择模型、推理强度和 API Key 编号，然后点击 **+**。**密钥 1**、**密钥 2** 等指的是该供应商设置中当前带编号的 Key。可直接就地修改选择、拖动行手柄改变顺序，或点击红色垃圾桶按钮删除某个回退项。

**继承** 沿用原始请求已解析出的推理设置；**跟随客户端** 使用你的编码代理发来的推理强度或 token 预算，绕过全局或档位设置。同一个模型可以用不同的 Key 编号重复添加。

</details>

<details>
<summary><strong>推理强度控制</strong></strong></summary>

打开 **Admin UI → 模型配置 → 模型路由**，为每个模型选择推理强度。**默认推理强度** 初始为 **跟随客户端**；Fable、Opus、Sonnet、Haiku 初始为 **继承**。

| 选项 | 行为 |
| --- | --- |
| **跟随客户端** | 使用编码代理发来的推理强度；若客户端未发送，则保留供应商默认值。 |
| **关闭** | 请求关闭推理。 |
| **低**、**中**、**高**、**极高** 或 **最大** | 用所选强度覆盖客户端设置。 |
| **继承** | 档位覆盖项沿用默认推理强度；回退项沿用原始请求已解析的强度。 |

</details>

<a id="integrations"></a>
<a id="connect-your-client"></a>

## 客户端集成

FCC 的启动器会自动启动服务端。

对于编辑器与应用类集成：先安装对应客户端、启动 FCC，然后打开 **Admin UI → 集成**，在对应卡片上点击 **连接**。

- **VS Code 中的 Claude Code**：安装 [Claude Code 扩展](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)。
- **VS Code Chat**：安装最新版 [VS Code](https://code.visualstudio.com/)，连接后在自带 Chat 的模型选择器中选择 FCC 模型。
- **Claude Desktop**：安装 [Claude Desktop](https://claude.ai/download)。连接或断开前请先完全退出，之后再重新打开。断开后恢复为正常的 Claude 登录。
- **VS Code 与 App 中的 Codex**：安装 [Codex 扩展](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt) 或 Codex App。
- **DeepSeek Harness Desktop**：连接前先安装并打开一次该应用。新建会话即可使用 FCC 模型。
- **JetBrains ACP 中的 Claude Code**：在 JetBrains AI Assistant 中安装 Claude Agent 并启动一次，然后在 FCC 中点击 **连接**。重新打开 IDE，选择 **Claude Code (FCC)** 并新建对话。JetBrains 更新该代理后，需重启 FCC 再新建对话。要求 IDE 安装在标准安装位置。

连接后请重载 VS Code，或重启对应应用／IDE。在 Codex 与 Claude Desktop 中，从模型选择器中选择 FCC 模型。当 FCC 提示设置已更新时，重载或重启客户端。在相同卡片上点击 **断开** 可移除集成。

如需单独完成 Claude Code 的首次引导，打开 **Admin UI → 集成 → Claude Code 首次引导** 并点击 **完成引导**。在 VS Code 中连接 Claude Code 也会同时完成该引导。

请确保 FCC 与你要配置的客户端运行在同一台电脑、同一个用户环境下。

<a id="use-the-api-directly"></a>

## API 直连

任何支持这些 API 的客户端或 SDK 都可以直接调用 FCC。OpenAI 类客户端把 Base URL 设为
`http://127.0.0.1:8082/v1`；Anthropic 与 Gemini 类客户端设为 `http://127.0.0.1:8082`。
每个 FCC 模型在所有端点上都能用。若启用了**要求 API 认证**，
请把它的 token 作为客户端的 API Key，或在每个 `curl` 请求中加上
`-H "Authorization: Bearer <token>"`。
用 `curl "http://127.0.0.1:8082/v1/models?view=messages"` 列出可用模型。

[`POST /v1/messages`](https://platform.claude.com/docs/en/api/messages)：

```bash
curl http://127.0.0.1:8082/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia_nim/nvidia/nemotron-3-ultra-550b-a55b",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

[`POST /v1/chat/completions`](https://platform.openai.com/docs/api-reference/chat/create)：

```bash
curl http://127.0.0.1:8082/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia_nim/nvidia/nemotron-3-ultra-550b-a55b",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

[`POST /v1/responses`](https://platform.openai.com/docs/api-reference/responses/create)：

```bash
curl http://127.0.0.1:8082/v1/responses \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nvidia_nim/nvidia/nemotron-3-ultra-550b-a55b",
    "input": "Hello!"
  }'
```

[`POST /v1/models/{model}:generateContent`](https://ai.google.dev/api/generate-content)：

```bash
curl http://127.0.0.1:8082/v1/models/nvidia_nim/nvidia/nemotron-3-ultra-550b-a55b:generateContent \
  -H "Content-Type: application/json" \
  -d '{"contents": [{"role": "user", "parts": [{"text": "Hello!"}]}]}'
```

Responses 的回复始终为流式。要让 Messages 或 Chat Completions 也流式返回，请加上
`"stream": true`。Gemini 请调用 `:streamGenerateContent?alt=sse` 而不是 `:generateContent`。

<a id="use-from-your-phone"></a>
<a id="optional-integrations"></a>

## 手机端使用

在 Discord 或 Telegram 里跑编码任务，并可发送语音消息。在 **Admin UI → 消息** 中配置，然后点击 **应用**。

<details>
<summary><strong>Discord 机器人</strong></strong></summary>

1. 在 [Discord Developer Portal](https://discord.com/developers/applications) 创建机器人。
2. 开启 **Message Content Intent**，并以读取、发送、读取消息历史及
   **Manage Messages** 权限邀请它加入服务器，这样 `/clear` 才能删除
   用户消息。
3. 把 **消息平台** 设为 **discord**。
4. 填入 **Discord 机器人 Token**、**Allowed Discord Channels** 和一个绝对路径的 **Allowed Directory**。
5. 应用设置；如提示需要，重启服务端。

</details>

<details>
<summary><strong>Telegram 机器人</strong></strong></summary>

1. 通过 [@BotFather](https://t.me/BotFather) 创建机器人。
2. 从 [@userinfobot](https://t.me/userinfobot) 获取你的数字用户 ID。
   在群组中使用时，请授予机器人删除消息的权限。
3. 把 **消息平台** 设为 **telegram**。
4. 填入 **Telegram 机器人 Token**、**Allowed Telegram User ID** 和一个绝对路径的 **Allowed Directory**。
5. 应用设置；如提示需要，重启服务端。

</details>

### 消息命令

| 用法 | 行为 |
| --- | --- |
| `/stats` | 显示会话状态。 |
| 单独发送 `/stop` | 取消全部任务。 |
| 回复某条消息并带 `/stop` | 只取消被回复的那条请求，其他排队请求继续执行。 |
| 单独发送 `/clear` | 清空本聊天中所有 FCC 会话及其消息。 |
| 回复某条消息并带 `/clear` | 删除被回复的那条消息及其后续回复链，保留其他会话。 |

<details>
<summary><strong>语音消息</strong></summary>

所有安装方式都内置 NVIDIA NIM 转写支持。在 **Admin UI → 消息 → 语音** 中启用语音消息，
选择 `nvidia_nim` 并挑一个受支持的模型。**NVIDIA NIM API 密钥** 在 Providers 页面配置。

如需在 CPU 或 CUDA 上使用本地 Whisper，请带本地语音选项重跑安装脚本：

macOS/Linux：

CPU 或 CUDA 上的本地 Whisper：

```bash
curl -fsSL "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.sh" | sh -s -- --voice-local
```

CUDA 13.0 的本地 Whisper：

```bash
curl -fsSL "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.sh" | sh -s -- --voice-local --torch-backend cu130
```

Windows PowerShell：

CPU 或 CUDA 上的本地 Whisper：

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.ps1"))) -VoiceLocal
```

CUDA 13.0 的本地 Whisper：

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.ps1"))) -VoiceLocal -TorchBackend cu130
```

安装本地支持后，重启 `fcc-server`。在 **Admin UI → 消息 → 语音** 中启用语音消息，
选择 `cpu` 或 `cuda`，并选择 Whisper 模型。本地受限（gated）模型需要 `HUGGINGFACE_API_KEY`。

</details>

<a id="manage-your-installation"></a>

## 安装维护

运行 `fcc-server --version` 可在不启动 FCC 的情况下查看已安装版本。

### 更新

停止所有正在运行的 FCC 命令，然后执行：

```sh
fcc-update
```

`fcc-update` 会安装最新的 FCC 发行版（已是最新则跳过）。

如果 `fcc-update` 不可用或失败，可再执行一次[安装命令](#install)。

若已是最新版本，但仍想重装 FCC 或调整可选组件，请直接运行[安装脚本](#install)。

需要本地语音支持时，加上 `--voice-local`（macOS/Linux）或 `-VoiceLocal`（Windows），如使用还需带上 `--torch-backend` 或 `-TorchBackend` 选项。

### 原生 Windows 上的 Muse Code

仅安装或更新 Muse Code：

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install-muse.ps1")))
```

移除 FCC 安装的 Muse Code 副本但保留其数据：

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/uninstall-muse.ps1")))
```

卸载 FCC 时不会连带卸载 Muse Code。

### 卸载

卸载前请停止所有正在运行的 FCC 命令，并退出已连接的桌面／编辑器应用。

**会删除**

- Free Claude Code，包括其桌面启动器与命令
- `~/.fcc/`

**会保留**

- uv 与 Python
- 你的编码代理、RTK 与 Headroom

macOS/Linux：

```bash
curl -fsSL "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/uninstall.sh" | sh
```

Windows PowerShell：

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/uninstall.ps1")))
```

## 项目链接

安装后遇到问题，请运行下面的命令，并把输出粘贴到问题反馈中。

```bash
fcc-doctor
```

- [反馈 Bug 或提功能需求](https://github.com/Alishahryar1/free-claude-code/issues)
- [贡献指南](CONTRIBUTING.md)

## 维护者

项目维护者及其负责领域见 [MAINTAINERS.md](MAINTAINERS.md)。

## 许可证

GNU Affero General Public License version 3 only（`AGPL-3.0-only`）。详见 [LICENSE](LICENSE)。

本仓库是上游的修改版本（汉化 + 飞牛 fnOS 原生应用打包），依 AGPL-3.0 §5 在本仓库
[NOTICE](NOTICE) 中列明修改内容与日期，并保留上游版权声明。

- **源码就是本仓库**：`zh-cn` 分支的源码树即构建发布包所用的对应源码；每个 Release 同时附带
  `<包名>-source.tar.gz`（该版本完整源码归档）。
- **分发与网络使用**：按 AGPL-3.0，若你把本程序分发给他人，须同时提供对应源码；若把它作为
  网络服务提供给他人使用（§13），须向使用者提供源码获取方式。
- **商标**：Claude / Claude Code / Anthropic 等为各自权利人商标，本项目与上游作者及这些公司
  无隶属关系、未获背书，属社区非官方汉化分支。
