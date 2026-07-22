import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import build_parser, resolve_launch_config


def parse_config(*args: str):
    parser = build_parser()
    return resolve_launch_config(parser.parse_args(list(args)))


def test_default_launch_is_local() -> None:
    config = parse_config()

    assert config.mode == "local"
    assert config.host == "127.0.0.1"
    assert config.port == 7860
    assert config.share is False
    assert config.local_url == "http://127.0.0.1:7860"


def test_local_launch_accepts_custom_port() -> None:
    config = parse_config("--local", "--port", "7861")

    assert config.mode == "local"
    assert config.host == "127.0.0.1"
    assert config.port == 7861
    assert config.share is False


def test_share_launch_enables_public_link() -> None:
    config = parse_config("--share")

    assert config.mode == "share"
    assert config.host == "127.0.0.1"
    assert config.share is True


def test_colab_launch_uses_share_and_binds_all_interfaces() -> None:
    config = parse_config("--colab")

    assert config.mode == "colab"
    assert config.host == "0.0.0.0"
    assert config.port == 7860
    assert config.share is True
