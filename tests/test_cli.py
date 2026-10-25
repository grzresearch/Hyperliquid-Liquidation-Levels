import subprocess
import sys
from pathlib import Path

from hyperliquid_liquidation.main import LiquidationHeatmapGenerator

ROOT = Path(__file__).resolve().parents[1]


def test_main_script_help():
    result = subprocess.run(
        [sys.executable, str(ROOT / "main.py"), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "--demo" in result.stdout


def test_demo_run_writes_heatmap_and_stats(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    out = tmp_path / "out"

    files = LiquidationHeatmapGenerator(assets=["BTC"], output_dir=str(out)).run(demo=True)

    names = [Path(f).name for f in files]
    assert any(n.startswith("BTC_combined_heatmap_") and n.endswith(".png") for n in names)
    assert any(n.startswith("BTC_liquidation_stats_") and n.endswith(".json") for n in names)
    assert all(Path(f).is_file() for f in files)
