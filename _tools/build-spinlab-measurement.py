"""Rebuild the SpinLab XR scientific figure (Python 3 + matplotlib + numpy).

By default, plots the checked-in native Godot output. To recapture from the app:
  python _tools/build-spinlab-measurement.py --lab-root PATH --godot GODOT_EXE

The capture calls RotorLab's actual signal generator and least-squares analysis.
Only an isolated temporary harness is written; app sources are never changed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "projects" / "spinlab-xr"
DATA = ASSETS / "physics-measurement-data.json"

HARNESS = '''extends SceneTree
const Lab = preload("res://scripts/rotor_lab.gd")
func _init() -> void:
    var lab = Lab.new()
    var record: Dictionary = lab._measure(600.0, true)
    var response: Array = []
    for speed in range(300, 1801, 5):
        var ratio: float = float(speed) / 60.0 / Lab.RESONANCE_HZ
        var dynamics: Vector2 = lab._cdiv(Vector2(ratio * ratio, 0.0), Vector2(1.0 - ratio * ratio, 2.0 * Lab.DAMPING_RATIO * ratio))
        response.append({"rpm": speed, "normalized_magnitude": dynamics.length()})
    var payload: Dictionary = {
        "synthetic": true,
        "native_source": "native/scripts/rotor_lab.gd",
        "natural_frequency_hz": Lab.RESONANCE_HZ,
        "damping_ratio": Lab.DAMPING_RATIO,
        "response_kind": "Quasi-steady unbalance response: abs(r^2 / (1-r^2 + i*2*zeta*r))",
        "response": response,
        "record": record,
        "waveform": lab.waveform
    }
    var output = FileAccess.open("__OUTPUT__", FileAccess.WRITE)
    output.store_string(JSON.stringify(payload, "  "))
    output.close()
    quit()
'''


def recapture(lab_root: Path, godot: Path) -> None:
    source = lab_root / "native" / "scripts" / "rotor_lab.gd"
    with tempfile.TemporaryDirectory(prefix="spinlab-figure-") as temporary:
        harness = Path(temporary) / "figure_capture.gd"
        exported = Path(temporary) / "capture.json"
        harness.write_text(
            HARNESS.replace("__OUTPUT__", exported.as_posix()), encoding="utf-8"
        )
        subprocess.run(
            [str(godot), "--headless", "--xr-mode", "off", "--path", str(lab_root / "native"),
             "--script", str(harness)],
            check=True, timeout=60,
        )
        payload = json.loads(exported.read_text(encoding="utf-8"))
    payload["native_source_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    payload["source_tag"] = "v0.8.0"
    DATA.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lab-root", type=Path)
    parser.add_argument("--godot", type=Path)
    args = parser.parse_args()
    if bool(args.lab_root) != bool(args.godot):
        parser.error("--lab-root and --godot must be supplied together")
    if args.lab_root:
        recapture(args.lab_root.resolve(), args.godot.resolve())

    data = json.loads(DATA.read_text(encoding="utf-8"))
    assert data["synthetic"] is True
    record = data["record"]
    assert record["measurement"]["samples"] == 1024
    assert record["measurement"]["sample_rate_hz"] == 1024
    assert record["rpm"] == 600
    time_s = np.array([sample["t"] for sample in data["waveform"]])
    raw_um = np.array([sample["a"] for sample in data["waveform"]])
    assert len(time_s) == 256
    assert np.all(np.diff(time_s) > 0)
    assert np.all(np.isfinite(raw_um))
    dc_um = record["dc_offsets_um"][0]
    re_um, im_um = record["phasors"][0]
    theta = 2 * np.pi * (record["rpm"] / 60) * time_s + 0.37
    fitted_1x = re_um * np.cos(theta) - im_um * np.sin(theta)
    assert np.isclose(np.hypot(re_um, im_um), record["amplitude_um"], rtol=1e-6)

    speed = np.array([point["rpm"] for point in data["response"]])
    magnitude = np.array([point["normalized_magnitude"] for point in data["response"]])
    ratio = speed / 60 / data["natural_frequency_hz"]
    expected = ratio**2 / np.hypot(1 - ratio**2, 2 * data["damping_ratio"] * ratio)
    assert np.allclose(magnitude, expected, rtol=1e-6)

    ink, muted, teal, amber = "#132a3b", "#566a78", "#007f86", "#bb6b19"
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 18,
        "axes.labelsize": 20, "xtick.labelsize": 17, "ytick.labelsize": 17,
        "text.color": ink, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "axes.edgecolor": "#abbcc5",
        "svg.fonttype": "path", "svg.hashsalt": "spinlab-measurement-v080",
        "savefig.facecolor": "#f7fafb",
    })
    fig = plt.figure(figsize=(8.4, 11.2), facecolor="#f7fafb")
    fig.text(.12, .965, "FROM ROTATION TO MEASUREMENT", fontsize=13.5,
             weight="bold", color=teal)
    fig.text(.12, .921, "Why speed matters", fontsize=27, weight="bold")
    fig.text(.12, .886, "22 Hz support mode · damping ratio 0.11", fontsize=17, color=muted)
    a = fig.add_axes([.14, .594, .81, .245])
    a.plot(speed, magnitude, color=teal, linewidth=3)
    natural_rpm = data["natural_frequency_hz"] * 60
    a.axvline(natural_rpm, color=amber, linewidth=1.6, linestyle=(0, (4, 4)))
    a.text(1370, 2.2, "22 Hz\n1,320 rpm", fontsize=16, color=amber, va="center")
    a.set(xlim=(300, 1800), ylim=(0, 5), xlabel="Rotational speed (rpm)",
          ylabel="Normalized response")
    a.set_xticks([300, 600, 900, 1200, 1500, 1800])
    a.set_yticks([0, 1, 2, 3, 4, 5])
    a.set_axisbelow(True)
    a.grid(axis="y", color="#dce5e9", linewidth=.9)
    a.spines[["top", "right"]].set_visible(False)
    a.set_facecolor("#f7fafb")

    fig.text(.12, .485, "Finding the once-per-turn signal", fontsize=25, weight="bold")
    fig.text(.12, .451, "600 rpm · sensor A · synthetic capture", fontsize=17, color=muted)
    b = fig.add_axes([.14, .153, .81, .224])
    milliseconds = time_s * 1000
    b.plot(milliseconds, raw_um - dc_um, color="#8b9da8", linewidth=1.4,
           label="Samples, offset removed")
    b.plot(milliseconds, fitted_1x, color=teal, linewidth=3,
           label="Fitted 1× component")
    b.set(xlim=(750, 1000), ylim=(-1, 1), xlabel="Time within capture (ms)",
          ylabel="Displacement (µm)")
    b.set_xticks([750, 800, 850, 900, 950, 1000])
    b.set_yticks([-1, -.5, 0, .5, 1])
    b.set_axisbelow(True)
    b.grid(axis="y", color="#dce5e9", linewidth=.9)
    b.spines[["top", "right"]].set_visible(False)
    b.set_facecolor("#f7fafb")
    b.legend(loc="lower left", bbox_to_anchor=(-.02, 1.015), frameon=False,
             fontsize=15, ncol=1, handlelength=2, borderaxespad=0, labelspacing=.25)
    fig.text(.12, .057, "1× fit: %.3f µm peak · DC and 2× fitted jointly" % record["amplitude_um"],
             fontsize=15.5, color=muted)
    fig.text(.12, .029, "Native lab output · quasi-steady model · no physical sensor data", fontsize=13, color=muted)
    for suffix in ("svg", "png"):
        fig.savefig(ASSETS / f"physics-measurement.{suffix}", dpi=170,
                    metadata={"Date": None} if suffix == "svg" else None)
    plt.close(fig)
    svg_path = ASSETS / "physics-measurement.svg"
    svg = svg_path.read_text(encoding="utf-8")
    svg = svg.replace('<svg ', '<svg role="img" aria-labelledby="measurement-title measurement-description" ', 1)
    svg = svg.replace(" <metadata>",
        '<title id="measurement-title">SpinLab XR rotor response and tachometer-referenced measurement</title>\n'
        '<desc id="measurement-description">Top: normalized quasi-steady unbalance response, with a 22 hertz support mode '
        'and damping ratio 0.11. Bottom: offset-removed synthetic sensor A samples at 600 rpm and the fitted '
        'once-per-revolution component, 0.683 micrometres peak. The fit jointly accounts for DC and twice-per-revolution motion. '
        'All values come from the native lab model; no physical sensor measurements are shown.</desc>\n <metadata>', 1)
    svg_path.write_text(svg, encoding="utf-8")
    ET.parse(svg_path)
    print("Saved physics-measurement.svg and .png; native data and model checks passed.")
    print("1x amplitude: %.6f um peak; fitted residual: %.6f um RMS" %
          (record["amplitude_um"], record["noise_rms_um"]))


if __name__ == "__main__":
    main()
