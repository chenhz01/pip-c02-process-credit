# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L06 — 确定性重放（过程信用）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""

import zlib

def l06_digest(decisions, seed=0):
    """决策序列 → 稳定指纹。用 crc32，不用 hash()（后者每进程随机）。"""
    h = zlib.crc32(str(seed).encode())
    for d in decisions:
        h = zlib.crc32(str(d).encode(), h)
    return "%08x" % h


def l06_replay(decisions, scorer, seed=0):
    digest = l06_digest(decisions, seed)
    return {"digest": digest, "score": scorer(list(decisions))}


def l06_demo():
    sc = lambda ds: round(sum(d if isinstance(d, int) else len(str(d)) for d in ds), 4)
    a = l06_replay([1, 2, 3], sc)
    b = l06_replay([1, 2, 3], sc)
    c = l06_replay([3, 2, 1], sc)
    print("  同序两次 ->", a["digest"] == b["digest"], a["digest"])
    print("  换序一次 ->", a["digest"] != c["digest"], c["digest"])


def l06_selftest():
    sc = lambda ds: sum(ds)
    a = l06_replay([1, 2, 3], sc)
    b = l06_replay([1, 2, 3], sc)
    c = l06_replay([3, 2, 1], sc)
    assert a == b and a["digest"] != c["digest"]
    # 种子不同 → 指纹不同（防跨实验串味）
    assert l06_digest([1], 0) != l06_digest([1], 7)
    return True


if __name__ == "__main__":
    l06_demo()
