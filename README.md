# Bearer Token Image Skills

Reusable image-generation skills for Trae, Hermes, and other agent frameworks that can execute Python CLI commands.

面向 Trae、Hermes 以及其他可执行 Python CLI 的 Agent 框架的可复用图片生成技能仓库。

## Overview | 项目概览

This repository contains two deliverables:

- a production-ready Agnes Image 2.1 Flash skill bundle
- a reusable bearer-token image skill template for other providers

本仓库包含两部分内容：

- 一个可直接使用的 Agnes Image 2.1 Flash 生产级 skill
- 一个可复用的 Bearer Token 图片 skill 模板，方便适配其他提供方

## Why This Repo | 为什么做这个仓库

Image-generation skills that rely on bearer tokens often break in agent environments because of:

- inconsistent env-file locations
- masked secrets such as `***`
- Hermes-specific runtime behavior
- split configuration between primary and secondary env keys

这类依赖 Bearer Token 的图片 skill 在 Agent 环境里常见问题包括：

- 环境文件位置不一致
- 密钥被脱敏成 `***`
- Hermes 特有的运行时行为
- 主次环境变量分裂导致读取到错误 token

This repository packages a verified solution and a reusable template so the same problems do not need to be solved again.

这个仓库把已经验证过的解决方案和模板整理在一起，避免后续重复踩坑。

## Repository Layout | 仓库结构

- `skills/agnes-image-generator-hermes-refresh/`
  - production bundle for `agnes-image-2.1-flash`
  - includes Trae skill definition, CLI generator, and one-time token setup helper
- `templates/bearer-token-image-skill-template/`
  - reusable template for other bearer-token image APIs
  - includes placeholder constants for provider name, model, endpoint, and env key names

## Production Bundle | 成品技能

### Agnes Image Generator Hermes Refresh

Path: `skills/agnes-image-generator-hermes-refresh/`

Highlights:

- model: `agnes-image-2.1-flash`
- endpoint: `https://apihub.agnes-ai.com/v1/images/generations`
- supports text-to-image and image-to-image by URL
- supports one-time bearer-token setup
- handles Hermes-specific env resolution
- skips masked placeholder secrets such as `***`

主要特性：

- 模型固定为 `agnes-image-2.1-flash`
- 支持文生图和基于 URL 的图生图
- 支持一次性保存 Bearer Token 并后续复用
- 自动兼容 Hermes 环境变量加载
- 自动跳过 `***` 这类脱敏占位值

Quick start:

```bash
cd skills/agnes-image-generator-hermes-refresh
python3 ./scripts/setup_agnes_env.py --api-key "Bearer YOUR_TOKEN"
python3 ./scripts/agnes_image_generate.py \
  --prompt "Ink wash painting of Shanghai Bund skyline, misty morning" \
  --size 1024x768 \
  --output /tmp/agnes-bund.png
```

## Template Bundle | 通用模板

### Bearer Token Image Skill Template

Path: `templates/bearer-token-image-skill-template/`

Use this template when you want to adapt the same structure to another provider.

当你要接入其他图片服务商时，可以直接复用这个模板结构。

Customize these constants:

- `PROVIDER_NAME`
- `MODEL_NAME`
- `API_URL`
- `PRIMARY_ENV_KEY`
- `SECONDARY_ENV_KEY`

Then rename the skill directory and the `name` field in `SKILL.md`.

## Compatibility | 兼容性

- Trae
- Hermes-compatible agents
- Any agent framework that can execute Python CLI commands

## Hermes Notes | Hermes 使用说明

- Do not use agent-side `write_file` to modify `~/.hermes/.env`
- Prefer running setup helpers in a real shell
- Some Hermes flows may surface masked placeholder secrets such as `***`
- The included scripts treat masked placeholders as invalid and prefer real file-based keys

- 不要通过 Agent 侧 `write_file` 直接改 `~/.hermes/.env`
- 优先在真实 shell 中执行初始化脚本
- Hermes 某些路径会把密钥脱敏成 `***`
- 仓库内脚本会把这类占位值视为无效并优先使用真实文件中的 token

## Suggested GitHub Topics | 建议的 GitHub Topics

```text
agent-skill, trae, hermes-agent, image-generation, bearer-token, python-cli, ai-tools, prompt-engineering
```

## Suggested Repository Description | 建议仓库简介

```text
Reusable image-generation skills for Trae and Hermes, including a production Agnes Image 2.1 Flash bundle and a bearer-token skill template.
```

## Screenshot Copy | 示例截图文案

You can use the following captions on the GitHub page or release page:

你可以把下面这些文案直接配到仓库截图或 Release 截图里：

- Screenshot 1: `Agnes image generator running inside Hermes with persisted bearer token support`
- Screenshot 2: `Trae-ready skill bundle structure with setup helper and generator CLI`
- Screenshot 3: `Reusable bearer-token image skill template for adapting other providers`
- 截图 1：`Hermes 中成功复用已保存 Bearer Token 的 Agnes 图片生成技能`
- 截图 2：`可直接导入 Trae 的 skill 目录结构与初始化脚本`
- 截图 3：`适配其他图片服务商的通用 Bearer Token skill 模板`

## Versioning | 版本信息

- Repository release tag: `v1.0.1`
- Agnes bundle version: `1.1.1`
- Template bundle version: `1.0.0`

## License | 许可证

See [LICENSE](./LICENSE).
