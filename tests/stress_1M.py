#!/usr/bin/env python3
"""
Reproduce the 1 000-instance / 1 M-agent public-goods benchmark
Run:  python tests/stress_1M.py
"""
import random, time, os, psutil
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gisn import GlobalCoordinationNetwork, Decision

N_INSTANCES = 1_000
PLAYERS_PER_INSTANCE = 1_000
TIMEOUT = 300  # seconds

def stress():
    net = GlobalCoordinationNetwork()
    start = time.time()
    latencies = []
    adoptions = []

    for i in range(N_INSTANCES):
        mpcr = random.uniform(0.25, 0.35)
        d = Decision(
            context=f"Public-Goods Game MPCR={mpcr:.2f}",
            stakeholders=[f"player_{j}" for j in range(PLAYERS_PER_INSTANCE)],
            options=["contribute 0", "contribute full"],
            constraints={"mpcr": mpcr},
            timeframe=1,
            impact_scale="global",
            uncertainty_level=0.2,
        )
        t0 = time.perf_counter()
        res = net.intelligence_engine.synthesize_decision(d)
        lat = time.perf_counter() - t0
        latencies.append(lat)
        # adoption ≈ score of "contribute full"
        score_full = res["decision_synthesis"]["option_scores"].get("contribute full", 0)
        adoptions.append(score_full)

    elapsed = time.time() - start
    rss = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 3

    # Assertions
    assert elapsed < TIMEOUT, f"timeout {elapsed:.1f}s"
    assert sum(adoptions) / len(adoptions) >= 0.70, "adoption too low"
    assert max(latencies) <= 2.0, f"latency {max(latencies):.2f}s"

    print("✅ 1 M-agent benchmark PASSED")
    print(f"wall-clock: {elapsed:.1f}s")
    print(f"latency-p95: {sorted(latencies)[int(0.95*len(latencies))]:.2f}s")
    print(f"RSS: {rss:.1f} GB")
    print(f"adoption-mean: {sum(adoptions)/len(adoptions):.3f}")

if __name__ == "__main__":
    stress()
