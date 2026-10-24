# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 chenhz01 (Process Iteration Primitives)
"""L05 — 过程信用回摊（过程信用）

零依赖，stdlib only。python impl.py 看 demo；python selftest.py 跑断言。
"""


def l05_assign(step_scores, final_score):
    """把最终成败按步骤权重回摊。step_scores 是每步自评/信号强度（>=0）。

    设计决定：全部步骤分为 0 时返回均分，而不是全 0。
    理由——没有信号时，任何「这一步更重要」的说法都是编的；
    均分是唯一不虚构信息的归因。全 0 会让下游误读成「每步都无贡献」。
    """
    if not step_scores:
        return []
    s = [max(0.0, float(x)) for x in step_scores]
    tot = sum(s)
    if tot <= 0:
        return [round(final_score / len(s), 4)] * len(s)
    return [round(final_score * (x / tot), 4) for x in s]


def l05_report(step_scores, final_score):
    cr = l05_assign(step_scores, final_score)
    if final_score <= 0 or not cr:
        return {"credit": cr, "hhi": 0.0, "verdict": "no-credit"}
    hhi = sum((c / final_score) ** 2 for c in cr)
    verdict = "single-step" if hhi > 0.5 else ("concentrated" if hhi > 0.3 else "diffuse")
    return {"credit": cr, "hhi": round(hhi, 4), "verdict": verdict}


def l05_demo():
    print("  均等五步  ->", l05_report([1, 1, 1, 1, 1], 0.8))
    print("  一步独大  ->", l05_report([0.05, 0.05, 9.0, 0.05, 0.05], 0.8))
    print("  最终为负  ->", l05_report([1, 1, 1], -0.2))


def l05_selftest():
    r = l05_report([1, 1, 1, 1], 1.0)
    assert abs(r["hhi"] - 0.25) < 1e-6 and r["verdict"] == "diffuse"
    assert l05_report([9, 0, 0, 0], 1.0)["verdict"] == "single-step"
    assert l05_report([], 1.0)["verdict"] == "no-credit"
    assert abs(sum(l05_assign([2, 3], 1.0)) - 1.0) < 1e-6
    # 全零步骤分不得除零崩
    assert l05_assign([0, 0], 1.0) == [0.5, 0.5]
    return True


if __name__ == "__main__":
    l05_demo()
