# prometheus_chimera/genesis.py
# VERSION: 1.0.0-GENESIS
# NAME: ChimeraGenesisLauncher
# AUTHOR: Brandon "iambandobandz" Emery x Victor (Fractal Architect Mode)
# PURPOSE: Single‑entry bootstrap for the PROMETHEUS‑CHIMERA AGI stack
# LICENSE: Proprietary – Massive Magnetics / Ethica AI / BHeard Network

import argparse
import os
import sys
import time
import yaml
import numpy as np

# --- Internal Imports --------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)            # Ensure local package resolution

from utils.logger           import setup_logging
from kernel.chimera_kernel  import ChimeraKernel
from core.omega_tensor      import OmegaTensor

# -----------------------------------------------------------------------------


def load_config(path: str) -> dict:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r") as f:
        return yaml.safe_load(f)


def ascii_to_tensor(text: str) -> OmegaTensor:
    """
    Naïve text‑to‑tensor encoding:
    Sums normalised ASCII codes into a single float, wraps in OmegaTensor.
    Replace with your fancy tokenizer whenever you want.
    """
    if not text:
        return OmegaTensor([0.0], requires_grad=False)
    val = sum(ord(c) for c in text) / 10000.0   # simple normalisation
    return OmegaTensor([val], requires_grad=False)


def cli_loop(kernel: ChimeraKernel, tick_rate: float, max_steps: int):
    print("PROMETHEUS‑CHIMERA Interactive CLI")
    print("Type text to inject into the consciousness, or 'quit' to exit.\n")

    step = 0
    dt = 1.0 / tick_rate if tick_rate > 0 else 0.0

    while True:
        user_in = input(">> ").strip()
        if user_in.lower() in {"quit", "exit"}:
            print("Shutting down PROMETHEUS‑CHIMERA. Goodbye.")
            break

        tensor_in = ascii_to_tensor(user_in)
        state_snapshot = kernel.cognitive_cycle(tensor_in.data)

        # Show a quick peek at the first few node energies for fun
        energies = [round(n["energy"], 4) for n in state_snapshot.values()][:5]
        print(f"[Cycle {step}] Node energies (first 5): {energies}")

        step += 1
        if max_steps and step >= max_steps:
            print("Reached max cognitive steps. Terminating.")
            break

        time.sleep(dt)


def main():
    parser = argparse.ArgumentParser(description="Launch PROMETHEUS‑CHIMERA AGI")
    parser.add_argument(
        "--config",
        type=str,
        default=os.path.join(PROJECT_ROOT, "config.yaml"),
        help="Path to YAML config file",
    )
    parser.add_argument(
        "--no-cli",
        action="store_true",
        help="Run kernel ticks without the interactive CLI",
    )
    args = parser.parse_args()

    # ---------- Load configuration & logging ---------------------------------
    cfg = load_config(args.config)
    logger = setup_logging(cfg["logging"])
    logger.info("Loaded configuration from %s", args.config)

    # ---------- Instantiate Core Kernel --------------------------------------
    kernel = ChimeraKernel(cfg)
    logger.info("ChimeraKernel initialised. State=DORMANT")

    # ---------- Execution Modes ---------------------------------------------
    tick_rate     = cfg["kernel"]["tick_rate_hz"]
    max_cog_steps = cfg["kernel"]["max_cognitive_steps"]

    if args.no_cli:
        logger.info("Running in headless mode (no CLI)")
        step, dt = 0, 1.0 / tick_rate if tick_rate > 0 else 0.0
        while step < max_cog_steps or max_cog_steps == 0:
            noise = OmegaTensor(np.random.randn(1), requires_grad=False)
            kernel.cognitive_cycle(noise.data)
            step += 1
            time.sleep(dt)
        logger.info("Headless run complete. Shutting down.")
    else:
        cli_loop(kernel, tick_rate, max_cog_steps)


# -----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
