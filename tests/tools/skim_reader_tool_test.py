from unittest.mock import MagicMock

from crewai_tools.tools.skim_reader_tool.skim_reader_tool import SkimReaderTool


def _tool_with_fake_response(json_data, ok=True, status_code=200, text="", reason=""):
    tool = SkimReaderTool()
    fake_resp = MagicMock()
    fake_resp.ok = ok
    fake_resp.status_code = status_code
    fake_resp.text = text
    fake_resp.reason = reason
    fake_resp.json.return_value = json_data
    fake_session = MagicMock()
    fake_session.post.return_value = fake_resp
    # Inject the session so _get_session never imports x402 or hits the network.
    tool._session = fake_session
    return tool, fake_session


def test_tool_initialization():
    tool = SkimReaderTool()
    assert tool.name == "Skim reader tool"
    assert tool.base_url == "https://skim402.com"
    assert tool.max_price_usd == 0.01
    assert tool.include_metadata is True
    assert tool.timeout == 60.0


def test_run_returns_markdown_with_metadata_frontmatter():
    tool, session = _tool_with_fake_response(
        {
            "markdown": "# Hello\n\nBody text.",
            "metadata": {"title": "Hello", "language": "en", "byline": ""},
        }
    )
    result = tool._run(url="https://example.com")

    # Posts to the Skim read endpoint with the basic mode payload.
    args, kwargs = session.post.call_args
    assert args[0] == "https://skim402.com/api/v1/read"
    assert kwargs["json"] == {"url": "https://example.com", "mode": "basic"}

    # Non-empty metadata is rendered as YAML frontmatter; empty values dropped.
    assert result.startswith("---\n")
    assert "title: Hello" in result
    assert "language: en" in result
    assert "byline" not in result
    assert result.endswith("# Hello\n\nBody text.")


def test_run_without_metadata_when_disabled():
    tool, _ = _tool_with_fake_response(
        {"markdown": "# Hello", "metadata": {"title": "Hello"}}
    )
    tool.include_metadata = False
    result = tool._run(url="https://example.com")
    assert result == "# Hello"


def test_run_raises_on_error_status():
    tool, _ = _tool_with_fake_response(
        {}, ok=False, status_code=502, text="upstream boom", reason="Bad Gateway"
    )
    try:
        tool._run(url="https://example.com")
    except RuntimeError as exc:
        assert "502" in str(exc)
        assert "upstream boom" in str(exc)
    else:
        raise AssertionError("expected RuntimeError on error status")
