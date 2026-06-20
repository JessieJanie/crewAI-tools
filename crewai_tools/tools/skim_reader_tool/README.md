# SkimReaderTool

## Description

[Skim](https://skim402.com) is the x402-native clean reader API for AI agents.
Give it a URL and it returns agent-ready Markdown (the article body with nav,
ads, and boilerplate stripped) plus structured metadata (title, byline,
published date, language, excerpt).

Skim has no accounts and no API keys. Each read costs $0.002 in USDC on
[Base](https://base.org), paid automatically over the [x402](https://x402.org)
protocol from a wallet you control. The wallet's private key never leaves your
machine; it only signs an EIP-3009 USDC authorization locally.

## Installation

Skim is paid per call over x402, so instead of an API key you need a Base wallet
funded with a little USDC (a dollar covers roughly 500 reads). Install the x402
client with EVM support along with the `crewai[tools]` package:

```
pip install 'crewai-tools[x402]' 'crewai[tools]'
```

Set the paying wallet's private key in the `SKIM_WALLET_PRIVATE_KEY` environment
variable. Use a dedicated wallet, not your personal one. Step-by-step wallet
setup for non-crypto-native developers: [skim402.com/wallet](https://skim402.com/wallet).

## Example

```python
from crewai_tools import SkimReaderTool

tool = SkimReaderTool()  # reads SKIM_WALLET_PRIVATE_KEY from the environment
markdown = tool.run(url="https://en.wikipedia.org/wiki/HTTP_402")
```

## Arguments

- `private_key`: Optional. Base wallet private key that signs USDC payment
  authorizations locally. Defaults to the `SKIM_WALLET_PRIVATE_KEY` environment
  variable.
- `base_url`: Optional. Skim API base URL. Defaults to `https://skim402.com`.
- `max_price_usd`: Optional. Hard per-call price cap in USD. The wallet refuses
  to sign for anything above this. Defaults to `0.01` (Skim is `$0.002`).
- `include_metadata`: Optional. When `True` (default), prepend a YAML frontmatter
  block of the page metadata to the returned Markdown.
- `timeout`: Optional. Per-request timeout in seconds. Defaults to `60`.

## How payment works

Skim uses the x402 protocol. The first request returns `402 Payment Required`
with a payment challenge; the x402 client signs an EIP-3009 USDC transfer
authorization locally and retries with an `X-PAYMENT` header. Skim verifies and
settles the payment on Base, then returns the content. The `max_price_usd` cap
bounds what the wallet will sign for, so a misconfigured price can never drain
the wallet.
