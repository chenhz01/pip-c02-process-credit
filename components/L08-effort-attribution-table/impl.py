# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L08 — 投入产出归因表（过程信用）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l08_table(rows):
    """rows: [(名称, 投入, 产出)]。返回按 ROI 排序 + 总计 + 处置建议。"""
    out = []
    for n, e, g in rows:
        roi = None if not e else round(g / e, 3)
        out.append({"name": n, "effort": e, "gain": g, "roi": roi})
    out.sort(key=lambda r: (-1e9 if r["roi"] is None else -r["roi"]))
    te = sum(e for _, e, _ in rows)
    tg = sum(g for _, _, g in rows)
    neg = [r["name"] for r in out if r["roi"] is not None and r["roi"] < 0]
    return {
        "rows": out,
        "total": {"effort": te, "gain": round(tg, 3), "roi": round(tg / te, 3) if te else None},
        "cut": neg,
        "advice": ("先砍负 ROI：" + ",".join(neg)) if neg else "无负 ROI 项",
    }


def l08_demo():
    r = l08_table([("查论文", 2, 6), ("写代码", 5, 20), ("调格式", 4, -1), ("跑基准", 1, 3)])
    for x in r["rows"]:
        print("  %-6s 投入%-3s 产出%-4s ROI=%s" % (x["name"], x["effort"], x["gain"], x["roi"]))
    print("  合计:", r["total"], "|", r["advice"])


def l08_selftest():
    r = l08_table([("a", 2, 6), ("b", 4, -1)])
    assert r["rows"][0]["name"] == "a" and r["rows"][0]["roi"] == 3.0
    assert r["cut"] == ["b"]
    assert r["total"]["roi"] == round(5 / 6, 3)
    assert l08_table([("x", 0, 5)])["rows"][0]["roi"] is None
    return True


if __name__ == "__main__":
    l08_demo()
