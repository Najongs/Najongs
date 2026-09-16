#!/usr/bin/env python3
"""프로필 통계 패널 생성 — assets/research-stats.svg

네 곳에서 숫자를 끌어온다. 하나가 실패해도 마지막으로 성공한 값을 쓴다
(assets/stats.json 에 보관) — 토큰이 없는 환경에서도 패널이 비지 않게 하려는 것이다.

  GitHub        api.github.com/graphql          GH_TOKEN (Actions 는 GITHUB_TOKEN 자동)
  Hugging Face  huggingface.co/api              HF_TOKEN (없으면 공개분만 센다)
  W&B           api.wandb.ai/graphql            WANDB_API_KEY 필요
  지식그래프      najongs.github.io/knowledge-vault/graph.json   공개, 인증 불필요

**잔디는 셋만 그린다.** GitHub 기여 · HF 커밋 · W&B 런 — 전부 "그날 무엇을 했나"다.
지식그래프는 흐름이 아니라 축적량이라 숫자로만 둔다. 공개 피드의 `observed_at` 은
584개 중 291개뿐이라 잔디로 그리면 활동이 없었던 것처럼 보인다.

**날짜 격자는 GitHub 달력을 정본으로 쓴다.** 셋이 같은 53주 위에 놓여야 나란히
비교된다 — 각자 자기 기간을 쓰면 같은 열이 다른 날을 가리킨다.

숫자는 **전체 기준**(공개+비공개)이다. W&B 프로젝트가 전부 비공개라 공개분만 세면
0 이 되어 패널이 거짓말을 한다. 대신 하단에 "public + private" 를 적어 밝힌다.

실행: python3 tools/build_stats.py
"""
import base64
import collections
import datetime
import json
import os
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "assets" / "stats.json"
OUT = ROOT / "assets" / "research-stats.svg"
WB_ENT = "najyeol99-daegu-gyeongbuk-institute-of-science-technology"
USER = "Najongs"


def _read(p):
    try:
        return p.read_text().strip()
    except OSError:
        return ""


def get(url, headers=None, timeout=40):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return json.load(f)


def post(url, payload, headers, timeout=60):
    req = urllib.request.Request(url, method="POST",
                                 data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return json.load(f)


# ── 수집 ──────────────────────────────────────────────────────────────────

def fetch_github():
    tok = (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
           or _read(pathlib.Path.home() / ".gh_token"))
    if not tok:
        raise RuntimeError("GH_TOKEN 없음")
    q = ("query($login:String!){ user(login:$login){ contributionsCollection{"
         " contributionCalendar{ totalContributions"
         " weeks{ contributionDays{ date contributionCount } } } } } }")
    d = post("https://api.github.com/graphql", {"query": q, "variables": {"login": USER}},
             {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    cal = d["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    grid = [[(dd["date"], dd["contributionCount"]) for dd in w["contributionDays"]]
            for w in cal["weeks"]]
    return {"total": cal["totalContributions"], "grid": grid}


def fetch_hf():
    tok = os.environ.get("HF_TOKEN") or _read(pathlib.Path.home() / ".hf_najongs_token")
    h = {"Authorization": f"Bearer {tok}"} if tok else {}
    ms = get(f"https://huggingface.co/api/models?author={USER}&limit=100", h)
    ds = get(f"https://huggingface.co/api/datasets?author={USER}&limit=100", h)
    days = collections.Counter()
    for items, rt in ((ms, "models"), (ds, "datasets")):
        for m in items:
            try:
                cs = get(f"https://huggingface.co/api/{rt}/{m['id']}/commits/main?limit=500", h)
            except Exception:
                continue
            for c in cs if isinstance(cs, list) else []:
                d = str(c.get("date", ""))[:10]
                if d:
                    days[d] += 1
    return {"models": len(ms), "datasets": len(ds),
            "downloads": sum(x.get("downloads", 0) for x in ms + ds),
            "commits": sum(days.values()), "days": dict(days)}


def fetch_wandb():
    key = os.environ.get("WANDB_API_KEY") or _read(pathlib.Path.home() / ".wandb_key")
    if not key:
        raise RuntimeError("WANDB_API_KEY 없음")
    H = {"Content-Type": "application/json",
         "Authorization": "Basic " + base64.b64encode(f"api:{key}".encode()).decode()}
    U = "https://api.wandb.ai/graphql"
    names = [e["node"]["name"] for e in post(
        U, {"query": "query($e:String!){models(entityName:$e,first:500){edges{node{name}}}}",
            "variables": {"e": WB_ENT}}, H)["data"]["models"]["edges"]]
    Q = ("query($e:String!,$p:String!,$c:String){ project(entityName:$e,name:$p){"
         " runs(first:500, after:$c){ pageInfo{hasNextPage endCursor}"
         " edges{ node{ createdAt } } } } }")
    days = collections.Counter()
    runs = 0
    for n in names:
        cur = None
        while True:
            r = post(U, {"query": Q, "variables": {"e": WB_ENT, "p": n, "c": cur}},
                     H)["data"]["project"]["runs"]
            for e in r["edges"]:
                d = (e["node"].get("createdAt") or "")[:10]
                if d:
                    days[d] += 1
                runs += 1
            if not r["pageInfo"]["hasNextPage"]:
                break
            cur = r["pageInfo"]["endCursor"]
    return {"projects": len(names), "runs": runs, "days": dict(days)}


def fetch_vault():
    g = get("https://najongs.github.io/knowledge-vault/graph.json")
    return {"nodes": g.get("n_nodes") or len(g.get("nodes", [])),
            "edges": g.get("n_edges") or len(g.get("edges", []))}


# ── 렌더 ──────────────────────────────────────────────────────────────────

F = 'font-family="ui-sans-serif,-apple-system,Segoe UI,Helvetica,Arial"'
CELL, GAP = 11, 3
ROW = 7 * (CELL + GAP) + 42


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def strip(o, y, label, colour, scale, summary, grid, counts):
    """잔디 한 줄. grid 는 GitHub 달력(날짜 격자), counts 는 날짜→건수."""
    o.append(f'<rect x="28" y="{y-14}" width="3" height="{7*(CELL+GAP)+22}" rx="1.5"'
             f' fill="{colour}"/>')
    o.append(f'<text x="44" y="{y}" {F} font-size="11" font-weight="700"'
             f' fill="{colour}" letter-spacing="0.6">{esc(label)}</text>')
    o.append(f'<text x="44" y="{y+18}" {F} font-size="11" fill="#7d8da1">{esc(summary)}</text>')
    vals = [counts.get(d, 0) for w in grid for d, _ in w]
    nz = sorted(v for v in vals if v > 0)
    cap = max(nz[int(len(nz) * 0.92)] if nz else 1, 1)
    gx, gy = 268, y - 12
    for wi, w in enumerate(grid):
        for di, (date, _) in enumerate(w):
            c = counts.get(date, 0)
            lvl = 0 if c == 0 else min(4, 1 + int(3 * min(c, cap) / cap))
            o.append(f'<rect x="{gx+wi*(CELL+GAP)}" y="{gy+di*(CELL+GAP)}" width="{CELL}"'
                     f' height="{CELL}" rx="2.5" fill="{scale[lvl]}"/>')
    peak = max(vals) if vals else 0
    active = sum(1 for v in vals if v > 0)
    lx = gx + len(grid) * (CELL + GAP) + 18
    o.append(f'<text x="{lx}" y="{gy+26}" {F} font-size="10" fill="#5c6b7f">'
             f'{active} active days</text>')
    o.append(f'<text x="{lx}" y="{gy+42}" {F} font-size="10" fill="#5c6b7f">peak {peak}/day</text>')
    for i, c in enumerate(scale):
        o.append(f'<rect x="{lx+i*13}" y="{gy+54}" width="9" height="9" rx="2" fill="{c}"/>')
    return y + ROW


def render(stats, stale):
    W = 1200
    gh = stats.get("github") or {}
    grid = gh.get("grid") or []
    H = 88 + 3 * ROW if grid else 150
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"'
         f' role="img" aria-label="Research at a glance">',
         f'<rect width="{W}" height="{H}" rx="14" fill="#0b1220"/>',
         f'<text x="28" y="34" {F} font-size="12.5" font-weight="700" fill="#8b949e"'
         f' letter-spacing="0.8">RESEARCH AT A GLANCE</text>']
    v = stats.get("vault") or {}
    if v:
        # text-anchor="end" + tspan 조합은 렌더러에 따라 tspan 이 전부 같은 점에
        # 앵커돼 글자가 겹친다. 한 줄로 합치고 색을 하나만 쓴다.
        o.append(f'<text x="{W-28}" y="34" {F} font-size="12" text-anchor="end"'
                 f' fill="#7d8da1">{v.get("nodes",0):,} knowledge nodes'
                 f' · {v.get("edges",0):,} typed edges</text>')
    if grid:
        hf = stats.get("hf") or {}
        wb = stats.get("wandb") or {}
        y = 84
        y = strip(o, y, "GITHUB", "#39d353",
                  ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"],
                  f'{gh.get("total",0):,} contributions in the last year',
                  grid, {d: c for w in grid for d, c in w})
        y = strip(o, y, "HUGGING FACE", "#FFD21E",
                  ["#161b22", "#4a3d00", "#8a7000", "#d0a800", "#FFD21E"],
                  f'{hf.get("models",0)} models · {hf.get("datasets",0)} datasets · '
                  f'{hf.get("downloads",0):,} downloads',
                  grid, hf.get("days") or {})
        strip(o, y, "WEIGHTS & BIASES", "#FFBE00",
              ["#161b22", "#4a3800", "#8a6800", "#d09800", "#FFBE00"],
              f'{wb.get("projects",0)} projects · {wb.get("runs",0):,} runs',
              grid, wb.get("days") or {})
    note = "public + private · refreshed " + stats["built"]
    if stale:
        note += " · " + ", ".join(stale) + " unreachable, last known values shown"
    o.append(f'<text x="28" y="{H-12}" {F} font-size="10.5" fill="#5c6b7f">{esc(note)}</text>')
    o.append("</svg>")
    return "\n".join(o)


def main():
    stats = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    stale = []
    for key, fn in (("github", fetch_github), ("hf", fetch_hf),
                    ("wandb", fetch_wandb), ("vault", fetch_vault)):
        try:
            stats[key] = fn()
        except Exception as e:
            stale.append(key)
            stats.setdefault(key, {})
            print(f"  ! {key}: {str(e)[:100]}", file=sys.stderr)
    stats["built"] = datetime.date.today().isoformat()
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(stats, indent=1, ensure_ascii=False) + "\n")
    OUT.write_text(render(stats, stale) + "\n")
    brief = {k: {kk: vv for kk, vv in (stats.get(k) or {}).items()
                 if kk not in ("days", "grid")} for k in ("github", "hf", "wandb", "vault")}
    print(f"  {OUT.relative_to(ROOT)} · {json.dumps(brief, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
