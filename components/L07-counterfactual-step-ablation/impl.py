# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L07 — 步骤反事实消融（过程信用）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l07_ablate(n_steps, score_fn):
    """依次去掉第 i 步重跑，量化该步的因果贡献（不是自评）。"""
    base = score_fn(list(range(n_steps)))
    rows = []
    for i in range(n_steps):
        keep = [j for j in range(n_steps) if j != i]
        s = score_fn(keep)
        rows.append({"step": i, "without": round(s, 4), "delta": round(base - s, 4)})
    rows.sort(key=lambda r: -r["delta"])
    return {"base": round(base, 4), "rows": rows}


def l07_demo():
    r = l07_ablate(5, lambda ks: sum(ks) * 1.0)
    print("  基线 %.2f；逐项去掉后的损失排序：" % r["base"])
    for x in r["rows"]:
        print("    去 step%d -> 损失 %.2f" % (x["step"], x["delta"]))
    # 一个「看起来重要但其实无用」的例子
    r2 = l07_ablate(4, lambda ks: 10.0 if 0 in ks else 0.0)
    print("  单点依赖 ->", [(x["step"], x["delta"]) for x in r2["rows"]])


def l07_selftest():
    r = l07_ablate(4, lambda ks: sum(ks))
    assert r["base"] == 6.0
    assert r["rows"][0]["step"] == 3 and r["rows"][0]["delta"] == 3.0
    r2 = l07_ablate(4, lambda ks: 10.0 if 0 in ks else 0.0)
    assert r2["rows"][0]["delta"] == 10.0 and r2["rows"][-1]["delta"] == 0.0
    return True


if __name__ == "__main__":
    l07_demo()
