#!/usr/bin/env python3
"""프로필 통계 패널 생성 — assets/research-stats.svg

세 곳에서 숫자를 끌어온다. 하나가 실패해도 마지막으로 성공한 값을 쓴다
(assets/stats.json 에 보관) — 그래야 토큰이 없는 환경에서도 패널이 비지 않는다.

  지식그래프  najongs.github.io/knowledge-vault/graph.json   공개, 인증 불필요
  Hugging Face  huggingface.co/api/{models,datasets}          HF_TOKEN (없으면 공개분만)
  W&B          api.wandb.ai/graphql                           WANDB_API_KEY 필요
  GitHub       api.github.com/graphql                         GH_TOKEN (기여 잔디)

숫자는 **전체 기준**이다 — 비공개 저장소·프로젝트를 포함한다. W&B 프로젝트가
전부 비공개라 공개분만 세면 0 이 되어 패널이 거짓말을 하게 된다. 대신 패널에
"public + private" 라고 적어 방문자가 눈으로 센 것과 다른 이유를 밝힌다.

실행: python3 tools/build_stats.py
"""
import json, os, sys, base64, urllib.request, urllib.error, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "assets" / "stats.json"
OUT = ROOT / "assets" / "research-stats.svg"
WB_ENT = "najyeol99-daegu-gyeongbuk-institute-of-science-technology"


def get(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return json.load(f)


def fetch_vault():
    g = get("https://najongs.github.io/knowledge-vault/graph.json")
    return {"nodes": g.get("n_nodes") or len(g.get("nodes", [])),
            "edges": g.get("n_edges") or len(g.get("edges", []))}


def fetch_hf():
    tok = os.environ.get("HF_TOKEN") or _read(pathlib.Path.home() / ".hf_najongs_token")
    h = {"Authorization": f"Bearer {tok}"} if tok else {}
    ms = get("https://huggingface.co/api/models?author=Najongs&limit=100", h)
    ds = get("https://huggingface.co/api/datasets?author=Najongs&limit=100", h)
    return {"models": len(ms), "datasets": len(ds),
            "downloads": sum(x.get("downloads", 0) for x in ms + ds),
            "authed": bool(tok)}


def fetch_wandb():
    key = os.environ.get("WANDB_API_KEY") or _read(pathlib.Path.home() / ".wandb_key")
    if not key:
        raise RuntimeError("WANDB_API_KEY 없음")
    auth = base64.b64encode(f"api:{key}".encode()).decode()
    q = """query($entity:String!){ models(entityName:$entity, first:500){
             edges{ node{ name runCount } } } }"""
    req = urllib.request.Request(
        "https://api.wandb.ai/graphql", method="POST",
        data=json.dumps({"query": q, "variables": {"entity": WB_ENT}}).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Basic " + auth})
    with urllib.request.urlopen(req, timeout=40) as f:
        d = json.load(f)
    nodes = [e["node"] for e in d["data"]["models"]["edges"]]
    return {"projects": len(nodes),
            "runs": sum((n.get("runCount") or 0) for n in nodes)}


def fetch_github():
    tok = (os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
           or _read(pathlib.Path.home() / ".gh_token"))
    if not tok:
        raise RuntimeError("GH_TOKEN 없음")
    q = ("query($login:String!){ user(login:$login){ contributionsCollection{"
         " contributionCalendar{ totalContributions"
         " weeks{ contributionDays{ date contributionCount weekday } } } } } }")
    req = urllib.request.Request(
        "https://api.github.com/graphql", method="POST",
        data=json.dumps({"query": q, "variables": {"login": "Najongs"}}).encode(),
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as f:
        d = json.load(f)
    cal = d["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[dd["contributionCount"] for dd in w["contributionDays"]] for w in cal["weeks"]]
    return {"total": cal["totalContributions"], "weeks": weeks}


def _read(p):
    try:
        return p.read_text().strip()
    except OSError:
        return ""


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render(stats, stale):
    W = 1200
    GH = stats.get("github") or {}
    weeks = GH.get("weeks") or []
    HEAT_H = (7*16 + 60) if weeks else 0
    H = 176 + HEAT_H
    F = 'font-family="ui-sans-serif,-apple-system,Segoe UI,Helvetica,Arial"'
    tiles = [
        ("KNOWLEDGE GRAPH", "#58a6ff", [
            (f"{stats['vault']['nodes']:,}", "nodes"),
            (f"{stats['vault']['edges']:,}", "typed edges")]),
        ("HUGGING FACE", "#FFD21E", [
            (f"{stats['hf']['models']}", "models"),
            (f"{stats['hf']['datasets']}", "datasets"),
            (f"{stats['hf']['downloads']:,}", "downloads")]),
        ("WEIGHTS & BIASES", "#FFBE00", [
            (f"{stats['wandb']['projects']}", "projects"),
            (f"{stats['wandb']['runs']:,}", "runs")]),
    ]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"'
         f' role="img" aria-label="Research at a glance">',
         f'<rect width="{W}" height="{H}" rx="14" fill="#0b1220"/>',
         f'<text x="28" y="30" {F} font-size="12.5" font-weight="700" fill="#8b949e"'
         f' letter-spacing="0.8">RESEARCH AT A GLANCE</text>']
    x = 28
    colw = (W - 56) / len(tiles)
    for title, col, vals in tiles:
        o.append(f'<rect x="{x:.0f}" y="52" width="3" height="84" rx="1.5" fill="{col}"/>')
        o.append(f'<text x="{x+16:.0f}" y="66" {F} font-size="11" font-weight="700"'
                 f' fill="{col}" letter-spacing="0.6">{esc(title)}</text>')
        vx = x + 16
        for v, lab in vals:
            o.append(f'<text x="{vx:.0f}" y="104" {F} font-size="30" font-weight="700"'
                     f' fill="#e6edf3">{esc(v)}</text>')
            o.append(f'<text x="{vx:.0f}" y="124" {F} font-size="11.5"'
                     f' fill="#7d8da1">{esc(lab)}</text>')
            vx += max(len(v) * 19 + 34, 104)
        x += colw

    if weeks:
        cell, gap = 13, 3
        top, gx = 176, 44
        gy = top + 12
        o.append(f'<rect x="28" y="{top-24}" width="3" height="{7*(cell+gap)+34}" rx="1.5" fill="#39d353"/>')
        o.append(f'<text x="{gx}" y="{top-10}" {F} font-size="11" font-weight="700"'
                 f' fill="#39d353" letter-spacing="0.6">GITHUB</text>')
        o.append(f'<text x="{gx+68}" y="{top-10}" {F} font-size="11.5" fill="#7d8da1">'
                 f'{GH["total"]:,} contributions in the last year</text>')
        flat = [c for wk in weeks for c in wk]
        mx = max(flat) if flat else 1
        srt = sorted(c for c in flat if c > 0)
        cap = max(srt[int(len(srt) * 0.92)] if srt else 1, 1)
        SCALE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
        for wi, wk in enumerate(weeks):
            for di, c in enumerate(wk):
                lvl = 0 if c == 0 else min(4, 1 + int(3 * min(c, cap) / cap))
                o.append(f'<rect x="{gx + wi*(cell+gap)}" y="{gy + di*(cell+gap)}"'
                         f' width="{cell}" height="{cell}" rx="3" fill="{SCALE[lvl]}"/>')
        gw = len(weeks) * (cell + gap)
        lx, ly = gx + gw + 26, gy + 3*(cell+gap) + 4
        o.append(f'<text x="{lx}" y="{ly}" {F} font-size="10.5" fill="#5c6b7f">less</text>')
        for i, c in enumerate(SCALE):
            o.append(f'<rect x="{lx+32+i*15}" y="{ly-9}" width="11" height="11" rx="2.5" fill="{c}"/>')
        o.append(f'<text x="{lx+32+5*15+6}" y="{ly}" {F} font-size="10.5" fill="#5c6b7f">more</text>')
        o.append(f'<text x="{lx}" y="{ly+24}" {F} font-size="10" fill="#5c6b7f">peak {mx}/day</text>')

    note = "public + private · refreshed " + stats["built"]
    if stale:
        note += " · " + ", ".join(stale) + " unreachable, last known values shown"
    o.append(f'<text x="28" y="{H-12}" {F} font-size="10.5" fill="#5c6b7f">{esc(note)}</text>')
    o.append("</svg>")
    return "\n".join(o)


def main():
    stats = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    stale = []
    for key, fn in (("vault", fetch_vault), ("hf", fetch_hf),
                    ("wandb", fetch_wandb), ("github", fetch_github)):
        try:
            stats[key] = fn()
        except Exception as e:
            if key not in stats:
                print(f"  ! {key} 실패하고 캐시도 없음: {e}", file=sys.stderr)
                stats[key] = {}
            stale.append(key)
            print(f"  ! {key}: {str(e)[:90]}", file=sys.stderr)
    stats["built"] = datetime.date.today().isoformat()
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(stats, indent=1, ensure_ascii=False) + "\n")
    OUT.write_text(render(stats, stale) + "\n")
    print(f"  {OUT.relative_to(ROOT)} · {json.dumps({k: v for k, v in stats.items() if k != 'built'}, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
