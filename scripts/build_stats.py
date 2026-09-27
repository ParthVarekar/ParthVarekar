#!/usr/bin/env python3
"""Build the GitHub activity card (light + dark) from the GitHub GraphQL API.

Runs in GitHub Actions (see .github/workflows/profile.yml):

    GITHUB_TOKEN=... python scripts/build_stats.py ParthVarekar dist/

Pass --sample to render from made-up numbers without calling the API (for local previews).
"""
import datetime as dt
import json
import os
import random
import sys
import urllib.request
from pathlib import Path

from theme import Canvas, width

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
}
"""


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if payload.get("errors"):
        raise SystemExit(f"GraphQL errors: {payload['errors']}")
    return payload["data"]["user"]


def sample():
    rnd = random.Random(7)
    start = dt.date.today() - dt.timedelta(days=364)
    days = [{"date": (start + dt.timedelta(d)).isoformat(),
             "contributionCount": max(0, int(rnd.gauss(3, 4)))} for d in range(365)]
    weeks = [{"contributionDays": days[i:i + 7]} for i in range(0, 365, 7)]
    langs = [("Python", 900), ("TypeScript", 800), ("JavaScript", 300), ("Java", 60), ("CSS", 50), ("HTML", 40)]
    return {
        "followers": {"totalCount": 12},
        "contributionsCollection": {
            "totalCommitContributions": 812, "totalPullRequestContributions": 14,
            "contributionCalendar": {"totalContributions": sum(d["contributionCount"] for d in days), "weeks": weeks}},
        "repositories": {"totalCount": 24, "nodes": [
            {"stargazerCount": 1, "languages": {"edges": [{"size": s, "node": {"name": n}} for n, s in langs]}}]},
    }


def summarize(user):
    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    counts = [d["contributionCount"] for d in days]

    longest = run = 0
    for n in counts:
        run = run + 1 if n else 0
        longest = max(longest, run)
    current, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:  # today may simply not have started yet
        i -= 1
    while i >= 0 and counts[i]:
        current += 1
        i -= 1

    weekly = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal["weeks"]]
    week_starts = [w["contributionDays"][0]["date"] for w in cal["weeks"]]

    langs = {}
    for repo in user["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])
    shown = [(n, s / total) for n, s in top[:5]]
    rest = 1 - sum(p for _, p in shown)
    if rest > 0.005:
        shown.append(("Other", rest))

    return dict(
        total=cal["totalContributions"],
        commits=user["contributionsCollection"]["totalCommitContributions"],
        prs=user["contributionsCollection"]["totalPullRequestContributions"],
        current=current, longest=longest, active=sum(1 for n in counts if n),
        repos=user["repositories"]["totalCount"],
        stars=sum(r["stargazerCount"] for r in user["repositories"]["nodes"]),
        followers=user["followers"]["totalCount"],
        weekly=weekly, week_starts=week_starts, langs=shown,
        updated=dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y"),
    )


def card(s, theme):
    W, H = 1200, 500
    cv = Canvas(W, H, theme)
    c = cv.c
    cv.add(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="{c["surface"]}" stroke="{c["line"]}"/>')
    cv.text(40, 54, "GITHUB ACTIVITY / LAST 12 MONTHS", "mono", 12.5, c["accent"], tracking=1.4)
    cv.text(W - 40, 54, f"Updated {s['updated']}", "mono", 12.5, c["muted"], anchor="end")

    fmt = lambda n: f"{n:,}"
    metrics = [
        (fmt(s["total"]), "contributions"),
        (fmt(s["commits"]), "commits"),
        (fmt(s["current"]), "current streak (days)"),
        (fmt(s["longest"]), "longest streak (days)"),
    ]
    col = (W - 80) / 4
    for i, (value, label) in enumerate(metrics):
        x = 40 + i * col
        if i:
            cv.add(f'<line x1="{x - 24}" y1="84" x2="{x - 24}" y2="150" stroke="{c["line"]}"/>')
        cv.text(x, 134, value, "display", 54, tracking=-1.5)
        cv.text(x, 158, label, "mono", 13, c["muted"])

    # weekly contribution bars
    top, bh = 196, 120
    weekly = s["weekly"]
    peak = max(weekly) or 1
    n = len(weekly)
    gap = 4
    bw = (W - 80 - gap * (n - 1)) / n
    cv.add(f'<line x1="40" y1="{top + bh}" x2="{W - 40}" y2="{top + bh}" stroke="{c["line"]}"/>')
    for i, v in enumerate(weekly):
        h = max(2, bh * v / peak) if v else 2
        x = 40 + i * (bw + gap)
        op = 0.35 + 0.65 * (v / peak) if v else 0.25
        fill = c["accent"] if v else c["line"]
        cv.add(f'<rect x="{x:.1f}" y="{top + bh - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="2" '
               f'fill="{fill}" fill-opacity="{op:.2f}" class="b" style="animation-delay:{i * 12}ms"/>')
    last_month, last_x = None, -1e9
    for i, d in enumerate(s["week_starts"]):
        m = dt.date.fromisoformat(d).strftime("%b")
        x = 40 + i * (bw + gap)
        if m != last_month:
            last_month = m
            if x - last_x >= 48 and i < n - 2:
                cv.text(x, top + bh + 22, m.upper(), "mono", 11, c["muted"], tracking=1)
                last_x = x
    cv.text(W - 40, top - 10, f"peak week: {peak}", "mono", 11.5, c["muted"], anchor="end")

    # languages
    ly = 380
    cv.text(40, ly, "LANGUAGES BY CODE SIZE (PUBLIC REPOS)", "mono", 12, c["accent"], tracking=1.2)
    shades = [c["accent"], "#ff8a5c" if theme == "dark" else "#ef6a33", c["accent2"],
              "#7a3a1f" if theme == "dark" else "#f4a57f", "#4a2618" if theme == "dark" else "#f8cdb4", c["line"]]
    x, bar_w = 40.0, W - 80
    cv.add(f'<clipPath id="lc"><rect x="40" y="{ly + 14}" width="{bar_w}" height="10" rx="5"/></clipPath><g clip-path="url(#lc)">')
    for i, (name, p) in enumerate(s["langs"]):
        cv.add(f'<rect x="{x:.1f}" y="{ly + 14}" width="{bar_w * p + 0.5:.1f}" height="10" fill="{shades[i % len(shades)]}"/>')
        x += bar_w * p
    cv.add("</g>")
    lx = 40.0
    for i, (name, p) in enumerate(s["langs"]):
        label = f"{name} {p * 100:.1f}%"
        cv.add(f'<rect x="{lx:.1f}" y="{ly + 40}" width="10" height="10" rx="2" fill="{shades[i % len(shades)]}"/>')
        cv.text(lx + 16, ly + 50, label, "mono", 12.5, c["text"])
        lx += 16 + width(label, "mono", 12.5) + 26
    pl = lambda n, word: f"{n:,} {word}{'' if n == 1 else 's'}"
    foot = "  ·  ".join([pl(s["active"], "active day"), pl(s["repos"], "public repo"), pl(s["stars"], "star"),
                         pl(s["followers"], "follower")])
    cv.add(f'<line x1="40" y1="{ly + 74}" x2="{W - 40}" y2="{ly + 74}" stroke="{c["line"]}"/>')
    cv.text(40, ly + 100, foot, "mono", 12.5, c["muted"], extra='xml:space="preserve"')

    cv.css.append("""
.b{transform-box:fill-box;transform-origin:bottom;animation:grow .7s cubic-bezier(.2,.8,.2,1) both}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@media (prefers-reduced-motion:reduce){.b{animation:none}}""")
    return cv.render()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    login, out = args[0], Path(args[1])
    out.mkdir(parents=True, exist_ok=True)
    user = sample() if "--sample" in sys.argv else fetch(login, os.environ["GITHUB_TOKEN"])
    s = summarize(user)
    for theme in ("dark", "light"):
        (out / f"stats-{theme}.svg").write_text(card(s, theme))
    print(json.dumps({k: v for k, v in s.items() if k not in ("weekly", "week_starts")}, indent=2))


if __name__ == "__main__":
    main()
