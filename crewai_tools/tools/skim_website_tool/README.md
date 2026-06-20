# SkimWebsiteTool

## Description

[Skim](https://skim402.com) is an x402-native clean reader API for AI agents.
Give it any URL and it returns clean, agent-ready Markdown plus structured
metadata (title, byline, published date, language, excerpt) -- stripping nav,
ads, and boilerplate.

Skim has no API keys and no signup. Each read is paid automatically over the
[x402 protocol](https://x402.org): $0.002 per call in USDC on Base, signed
locally by a wallet you control. The private key never leaves your machine -- it
only signs an EIP-3009 USDC authorization.

## Installation

Install the x402 client with EVM support alongside `crewai[tools]`:

```
pip install 'x402[evm]' requests eth-account 'crewai[tools]'
```

## Setup

Set `SKIM_WALLET_PRIVATE_KEY` to the hex private key of a Base wallet funded
with a little USDC. Use a dedicated wallet, never your personal one.

```
export SKIM_WALLET_PRIVATE_KEY=0x...
```

## Example

```python
from crewai_tools import SkimWebsiteTool

tool = SkimWebsiteTool()  # reads SKIM_WALLET_PRIVATE_KEY from the env
markdown = tool.run(url="https://en.wikipedia.org/wiki/HTTP_402")
print(markdown)
```

## Arguments

- `url` (str): The fully-qualified URL to fetch and clean.

## Configuration

`SkimWebsiteTool` accepts these optional constructor parameters:

- `private_key` (str): Base wallet hex private key. Falls back to the
  `SKIM_WALLET_PRIVATE_KEY` environment variable.
- `base_url` (str): Skim API base URL. Defaults to `https://skim402.com`.
- `max_price_usd` (float): Hard per-call price cap in USD. The wallet refuses to
  sign for anything above this. Defaults to `0.01` (Skim is `$0.002`).
- `include_metadata` (bool): When `True` (default), prepend a YAML frontmatter
  block of the page metadata to the returned Markdown.
- `timeout` (float): Per-request timeout in seconds. Defaults to `60`.
