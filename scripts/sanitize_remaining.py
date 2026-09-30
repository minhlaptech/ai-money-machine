import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

# 1. benchmarks/index.html
p_bm = ROOT / "benchmarks/index.html"
txt = p_bm.read_text(encoding="utf-8")
txt = txt.replace('$1,002,600 ARR', '$83,550/mo Target Pipeline')
p_bm.write_text(txt, encoding="utf-8")
print("✓ Updated benchmarks/index.html")

# 2. packages/index.html
p_pkg = ROOT / "packages/index.html"
txt = p_pkg.read_text(encoding="utf-8")
txt = txt.replace('$1,002,600 ARR', '$83,550/mo Target Pipeline')
txt = txt.replace('>Empire Total ARR<', '>Pipeline Target ARR<')
p_pkg.write_text(txt, encoding="utf-8")
print("✓ Updated packages/index.html")

# 3. sandboxes/index.html
p_sb = ROOT / "sandboxes/index.html"
txt = p_sb.read_text(encoding="utf-8")
txt = txt.replace('$1,002,600 ARR', '$83,550/mo Target Pipeline')
txt = txt.replace('>Empire Total ARR<', '>Pipeline Target ARR<')
p_sb.write_text(txt, encoding="utf-8")
print("✓ Updated sandboxes/index.html")

# 4. telemetry/index.html
p_tl = ROOT / "telemetry/index.html"
txt = p_tl.read_text(encoding="utf-8")
txt = txt.replace('$1,002,600 ARR', '$83,550/mo Target Pipeline')
p_tl.write_text(txt, encoding="utf-8")
print("✓ Updated telemetry/index.html")
