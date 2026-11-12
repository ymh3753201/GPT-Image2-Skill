# GPT-Image2-Skill v0.4.0 安装说明

本版由 ymh3753201 在 wuyoscar/GPT-Image2-Skill v0.3.0（提交 8a1e114）基础上维护，保留原项目 MIT 许可证、图库和署名。适用于 Codex 中制作海报、短剧角色与分镜关键帧、电商图，以及上传参考图后的生成和修改。

默认请求模型为 `gpt-image-2.6-sunburst`，默认画质为 `high`。用户可指定 `gpt-image-2.6-flare`、其他模型或第三方平台自己的模型名称。接口基础地址可以使用 OpenAI 或兼容 Images API 的第三方平台。

## 下载完整安装包

下载 Release 中的 `GPT-Image2-Skill-v0.4.0-full.zip`，或使用老师转发的同名完整包。解压后应包含 `pyproject.toml`、`src`、`skills`、`scripts`、`docs`、`tests` 和 `LICENSE`。

包内含两个 Skill、全部程序源码、参考资料、图库和测试。安装时无需从 GitHub 下载代码。首次安装仍需要 Python 3.11+、uv 和 Python 依赖；这些运行环境按 Windows/macOS/Linux 分别安装。API 生图需要访问用户选择的服务商。完整源码包不代表完全断网也能生图。

## 复制给 Codex 的安装提示词

```text
请帮我安装或更新这份 GPT-Image2-Skill 完整包。

完整包解压路径：【填写路径】
图片 API 基础地址：【填写服务商提供的地址，例如 https://api.openai.com/v1】
图片 API Key：【在本机安全提供，不要公开分享】
模型名称：【可不填；默认 gpt-image-2.6-sunburst；平台使用别名时填写其准确 ID】

先阅读包内 COURSE_INSTALL_ZH.md 和 docs/install.md，核对 pyproject.toml、src、skills、scripts 均存在。用这份本地包安装，避免访问 GitHub。检查现有 Python、uv、同名技能和 CLI。缺少运行环境或依赖时，使用这台电脑可访问的正规软件源补装，保留其他项目的环境。

在包根目录运行 uv tool install .，已有旧版时运行 uv tool install --force .。然后运行 python scripts/install_skills.py，更新这两个技能时加 --replace。默认安装到当前 CODEX_HOME 的 skills 目录，未设置时为用户目录下的 .codex/skills。安装程序会把本版 CLI 源码一起放进 gpt-image 技能，避免单独复制 SKILL.md 导致缺程序。

把我提供的图片 API 地址、Key 和可选模型保存到我指定的生图工作目录 .env，变量为 OPENAI_BASE_URL、OPENAI_API_KEY、OPENAI_IMAGE_MODEL。如果我没有指定工作目录，先让我指定。保留已有配置中无关的内容，已有同名配置先说明后再按我的选择处理。检查进程环境是否覆盖了文件设置。不要把 Key 打印在回复、命令参数、日志或公开文件中，不要修改 Codex 登录凭据。

完成不计费检查：gpt-image --version、gpt-image --help、安装后 scripts/generate.py --help。核对默认模型和第三方配置支持。安装成功后告诉我需要新开聊天或重启 Codex加载技能。只在我明确要求测试生图时发起真实图片请求，并先说明模型、画质、张数及可能计费；请求失败时停止，不自动换模型或重复提交。
```

## 手动安装

在解压根目录执行。Windows 可用 `python` 或 `py -3`，macOS/Linux 根据环境使用 `python3`。

```bash
uv tool install .
python scripts/install_skills.py
gpt-image --version
gpt-image --help
```

更新本版程序和两个 Skill：

```bash
uv tool install --force .
python scripts/install_skills.py --replace
```

选择项目级目录或其他 Agent 的 Skill 目录时，使用 `--skills-dir /path/to/skills`。程序不会修改 API 配置。已有符号链接会提示先处理，避免意外覆盖链接来源。

也可以直接在完整包目录运行，无需先全局安装 CLI：

```bash
uv run skills/gpt-image/scripts/generate.py --help
```

## 常用请求

先进入保存图片 API 配置的工作目录，或者使用已设置的进程环境。不要将带真实 Key 的 `.env` 放回分享包。

```bash
# 海报提示词可包含完整中文标题、副标题和信息模块
gpt-image --prompt-file poster.txt --size portrait -f poster.png

# 上传两张同一商品的参考图，保持商品身份
gpt-image --prompt-file product.txt -i front.png -i detail.png -f product.png

# 明确选用快速版本
gpt-image --model gpt-image-2.6-flare --quality low -p "白底橘猫" -f draft.png

# 临时指定第三方地址和准确模型别名
gpt-image --base-url https://images.example.com/v1 --model provider-model-id --prompt-file poster.txt -i reference.png -f poster.png
```

`--model` 优先于 `OPENAI_IMAGE_MODEL`，最后才使用内置默认模型。`--base-url` 优先于 `OPENAI_BASE_URL`，未配置地址时使用 OpenAI。进程环境优先于当前目录 `.env`，再优先于用户目录 `.env`。

这些命令中的 `-i` 会实际上传参考图片。服务商需要支持 `/images/edits`；只有聊天接口或自有异步任务接口的服务，需要额外适配。请根据服务商公开文档配置，避免猜测模型名或连续付费重试。

## 验证范围

`--help` 成功说明程序能启动。自动化测试使用模拟接口，检查请求内容和安装行为。服务商账户是否能使用 Sunburst、图片的实际质量和商品/角色一致性，需要用户授权的真实成图与看图检查。
