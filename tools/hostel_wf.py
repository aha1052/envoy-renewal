#!/usr/bin/env python3
"""Generate Envoy Hostel wireframes (same low-fidelity format as the tours wireframes).
Usage: python3 tools/hostel_wf.py  -> writes wireframes/hostel-*.html
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "wireframes")
FP = "https://commons.wikimedia.org/wiki/Special:FilePath/"
IMG = {
    "city": "Tbilisi_city_view.jpg",
    "wine": "Kakheti%2C_Georgia_%E2%80%94_Georgian_vineyards.jpg",
    "food": "Khinkali_551.jpg",
    "kazbeg": "Gergeti_Trinity_Church_and_Mt._Kazbeg_01.jpg",
    "mtskheta": "Svetitskhoveli_%282%29.jpg",
    "geghard": "Geghard_Monastery%2C_Geghard%2C_Armenia.jpg",
    "sevan": "Lake_Sevan_%285063530234%29.jpg",
}

def u(k, w):
    return f"{FP}{IMG[k]}?width={w}"

def bg(k, w, dark=False):
    if dark:
        return f"background: linear-gradient(180deg, rgba(0,0,0,.05) 35%, rgba(0,0,0,.6)), url(&quot;{u(k,w)}&quot;) center / cover no-repeat, #e4e4e4"
    return f"background: url(&quot;{u(k,w)}&quot;) center / cover no-repeat, #e4e4e4"

GREY = "background: #e4e4e4"

HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>와이어프레임 · {title}</title>
<style>

body{{margin:0;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;color:#1f1f1f;background:#fff}}
a{{color:#1f1f1f}}a:hover{{color:#000}}

.wf-bar{{position:sticky;top:0;z-index:5;background:#22312c;color:#f3f1ea;font:13px/1.4 "Noto Sans KR",system-ui,sans-serif;display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;padding:10px max(16px,env(safe-area-inset-left,0px))}}
.wf-bar a{{color:#f3f1ea;text-decoration:none}}.wf-bar a:hover{{text-decoration:underline}}
.wf-bar .t{{flex:1 1 240px;opacity:.85}}
.phone-stage{{background:#e9e9e6;padding:32px 16px;display:flex;justify-content:center}}
.phone{{width:390px;max-width:100%;background:#fff;box-shadow:0 0 0 1px #c9c9c4;overflow:hidden}}
.ph-dark,.ph-dark *{{color:#fff !important}}.ph-dark a[style*="background: #1f1f1f"]{{background:#fff !important;color:#1f1f1f !important}}
</style>
</head>
<body>
"""

PAGES = [
    ("hostel-home", "홈"),
    ("hostel-rooms", "Dormitory Rooms"),
    ("hostel-cafe", "Cafe"),
    ("hostel-tbilisi", "Old Tbilisi Guide"),
    ("hostel-about", "About Envoy"),
    ("hostel-contact", "Contact"),
    ("hostel-mobile-home", "모바일 홈"),
    ("hostel-mobile-rooms", "모바일 객실"),
]

def bar(i):
    f, t = PAGES[i]
    s = f'<div class="wf-bar"><a href="../index.html#hostel-wireframes">← 와이어프레임 목록</a><span class="t">{t}</span>'
    if i > 0:
        s += f'<a href="{PAGES[i-1][0]}.html">← {PAGES[i-1][1]}</a>'
    if i < len(PAGES) - 1:
        s += f'<a href="{PAGES[i+1][0]}.html">{PAGES[i+1][1]} →</a>'
    return s + "</div>\n"

# ---------- shared pieces ----------
BTN = "display: inline-flex; align-items: center; justify-content: center; min-height: 44px; padding: 0 20px; background: #1f1f1f; color: #fff; border-radius: 6px; text-decoration: none; font-weight: 600"
BTN2 = "display: inline-flex; align-items: center; justify-content: center; min-height: 44px; padding: 0 20px; border: 1px solid #1f1f1f; border-radius: 6px; text-decoration: none; font-weight: 600"
CARD = "border: 1px solid #bdbdbd; border-radius: 8px"
SUB = "font-size: 13px; color: #555"

def tag(label, m=False):
    if m:
        return f'<div lang="ko" style="display: inline-block; background: #3d3d3d; color: #fff; font-size: 11px; padding: 1px 6px; border-radius: 4px; margin-bottom: 8px">{label}</div>'
    return f'<div lang="ko" style="display: inline-block; background: #3d3d3d; color: #fff; font-size: 12px; padding: 2px 8px; border-radius: 4px; margin-bottom: 12px">{label}</div>'

def sec(label, body, last=False):
    b = "" if last else "; border-bottom: 1px dashed #c8c8c8"
    return f'    <section style="padding: 32px 0{b}">\n      {tag(label)}\n      {body}\n    </section>\n'

def msec(label, body, last=False):
    b = "" if last else "; border-bottom: 1px dashed #c8c8c8"
    return f'    <section style="padding: 16px 0{b}">\n      {tag(label, True)}\n      {body}\n    </section>\n'

def h2(t, mb=16):
    return f'<h2 style="margin: 0 0 {mb}px; font-size: 24px">{t}</h2>'

def lines(n=3, last=60):
    out = ""
    for i in range(n):
        w = f"; width: {last}%" if i == n - 1 else ""
        out += f'<div style="height: 10px; background: #d9d9d9; border-radius: 3px{w}"></div>'
    return out

def grid(n, items, gap=16):
    return f'<div style="display: grid; grid-template-columns: repeat({n}, minmax(0, 1fr)); gap: {gap}px">' + "".join(items) + "</div>"

def ph(h, k=None, w=700, radius=8, extra=""):
    b = bg(k, w) if k else GREY
    return f'<div style="height: {h}px; {b}; border: 1px solid #c4c4c4; border-radius: {radius}px{extra}"></div>'

NAV = [("Rooms", "hostel-rooms.html"), ("Cafe", "hostel-cafe.html"), ("Experience", "hostel-tbilisi.html"),
       ("About Envoy", "hostel-about.html"), ("Contact", "hostel-contact.html")]

def header():
    links = "".join(f'\n        <a href="{h}" style="text-decoration: none">{t}</a>' for t, h in NAV)
    return f"""  <header style="border-bottom: 1px solid #cfcfcf">
    <div style="max-width: 1200px; margin: 0 auto; padding: 12px 40px; display: flex; flex-wrap: wrap; align-items: center; gap: 24px">
      <a href="hostel-home.html" style="width: 120px; height: 40px; background: #e4e4e4; border: 1px solid #c4c4c4; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #555; text-decoration: none">LOGO</a>
      <nav style="display: flex; flex-wrap: wrap; gap: 28px; flex: 1 1 320px; font-weight: 600">{links}
      </nav>
      <a href="#" style="color: #555; font-size: 14px">WhatsApp</a>
      <a href="#" style="{BTN}">Book Now</a>
    </div>
  </header>
"""

def footer_sec():
    cols = [("Envoy Hostel", "[Street address], Old Tbilisi<br>+995 [000 000 000]<br>hostel@[domain]"),
            ("Stay", "Dormitory Rooms<br>Ensuite Rooms<br>Cafe"),
            ("Envoy", "About Envoy<br>Our Impact<br>Envoy Tours"),
            ("Policies", "Booking terms<br>House rules<br>Privacy")]
    items = [f'<div style="font-size: 13px; color: #555; line-height: 1.7"><strong style="color: #1f1f1f">{a}</strong><br>{b}</div>' for a, b in cols]
    return f'<div style="background: #f2f2f2; padding: 24px; border-radius: 8px">{grid(4, items)}</div>'

def page_desktop(i, body):
    f, t = PAGES[i]
    return (HEAD.format(title=t) + bar(i) + '\n<div style="width: 100%; min-height: 100%; font-size: 15px; line-height: 1.5">\n\n'
            + header() + '\n  <main style="max-width: 1200px; margin: 0 auto; padding: 0 40px">\n\n' + body
            + '\n  </main>\n</div>\n</body>\n</html>\n')

def booking_bar(compact=False):
    fields = [("Check-in", "[Date]"), ("Check-out", "[Date]"), ("Guests", "2")]
    fs = "".join(f'<div style="flex: 1 1 160px; border: 1px solid #9e9e9e; border-radius: 6px; padding: 8px 12px"><div style="{SUB}">{a}</div><strong>{b}</strong></div>' for a, b in fields)
    return (f'<div style="{CARD}; padding: 20px; display: flex; flex-direction: column; gap: 12px">'
            f'<div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: stretch">{fs}<a href="#" style="{BTN}">Check Availability</a></div>'
            f'<div style="{SUB}">Book direct: welcome drink · Cafe benefit · flexible changes [TBD]</div></div>')

ROOMS = [
    ("Dormitory", "8-Bed Dormitory", "8 beds · shared bathroom", "per bed"),
    ("Dormitory", "6-Bed Dormitory", "6 beds · shared bathroom", "per bed"),
    ("Dormitory", "4-Bed Dormitory", "4 beds · shared bathroom", "per bed"),
    ("Dormitory", "Accessible 4-Bed Dormitory", "4 beds · step-free access", "per bed"),
    ("Ensuite", "Double Ensuite", "1 double bed · private bathroom", "per room"),
    ("Ensuite", "Family Ensuite", "Up to [4] guests · private bathroom", "per room"),
]

def room_card(r, h=180):
    kind, name, spec, unit = r
    icons = "".join('<span style="width: 28px; height: 28px; background: #e4e4e4; border-radius: 50%; display: inline-block"></span>' for _ in range(4))
    return (f'<div style="{CARD}; overflow: hidden; display: flex; flex-direction: column">'
            f'<div style="height: {h}px; {GREY}; position: relative"><span style="position: absolute; bottom: 8px; right: 8px; background: #fff; font-size: 12px; padding: 2px 8px; border-radius: 10px">1 / 3</span></div>'
            f'<div style="padding: 16px; display: flex; flex-direction: column; gap: 8px; flex: 1">'
            f'<span style="font-size: 12px; color: #555">{kind}</span><strong style="font-size: 17px">{name}</strong>'
            f'<span style="{SUB}">{spec} · [m²]</span><div style="display: flex; gap: 8px">{icons}</div>'
            f'<div style="display: flex; align-items: center; gap: 12px; margin-top: auto; flex-wrap: wrap"><span style="flex: 1">From USD [TBD] {unit}</span><a href="#" style="{BTN}">Book Now</a></div>'
            f'</div></div>')

def tour_card(k, kind, name, w=700, h=160):
    return (f'<div style="{CARD}; overflow: hidden"><div style="height: {h}px; {bg(k, w)}"></div>'
            f'<div style="padding: 16px; display: flex; flex-direction: column; gap: 6px"><span style="font-size: 12px; color: #555">{kind}</span>'
            f'<strong>{name}</strong><span style="font-size: 13px; color: #444">From USD [TBD] per person</span><a href="#" style="font-size: 14px">View on Envoy Tours</a></div></div>')

# ---------- desktop pages ----------
def home():
    s = ""
    s += sec("① 메인 비주얼", f'''<div class="ph-dark" style="height: 480px; {bg("city", 1800, True)}; border: 1px solid #c4c4c4; border-radius: 8px; display: flex; flex-direction: column; justify-content: flex-end; padding: 40px; box-sizing: border-box; gap: 12px">
        <span style="font-size: 14px; font-weight: 600">Reopening April 2027</span>
        <h1 style="margin: 0; font-size: 40px; line-height: 1.15">A boutique hostel in Old Tbilisi</h1>
        <div style="font-size: 18px">Rooms, a rooftop cafe and tours under one roof</div>
      </div>''')
    s += sec("② 예약 바", booking_bar())
    s += sec("③ Stay with Envoy", f'''<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px; align-items: center">
        <div style="display: flex; flex-direction: column; gap: 10px">{h2("Stay with Envoy", 4)}{lines(4, 50)}<a href="hostel-about.html">Our story</a></div>
        {ph(280, "city", 900)}
      </div>''')
    cards = [
        f'<a href="hostel-rooms.html" style="{CARD}; overflow: hidden; text-decoration: none"><div style="height: 220px; {GREY}"></div><div style="padding: 16px; display: flex; flex-direction: column; gap: 6px"><strong style="font-size: 18px">Dormitory Rooms</strong><span style="{SUB}">4, 6 and 8 beds · curtains, reading lights, lockers</span><span>From USD [TBD] per bed</span><span style="text-decoration: underline">View Rooms</span></div></a>',
        f'<a href="hostel-rooms.html" style="{CARD}; overflow: hidden; text-decoration: none"><div style="height: 220px; {GREY}"></div><div style="padding: 16px; display: flex; flex-direction: column; gap: 6px"><strong style="font-size: 18px">Ensuite Rooms</strong><span style="{SUB}">Double and family rooms · private bathroom</span><span>From USD [TBD] per room</span><span style="text-decoration: underline">View Rooms</span></div></a>',
    ]
    s += sec("④ Rooms", h2("Rooms") + grid(2, cards))
    perks = ["Welcome drink", "Cafe benefit", "Flexible changes", "Tour benefit"]
    s += sec("⑤ Why Book Direct", h2("Why book direct") + grid(4, [f'<div style="{CARD}; padding: 20px"><div style="width: 40px; height: 40px; background: #e4e4e4; border-radius: 50%; margin-bottom: 12px"></div><strong>{p}</strong><p style="margin: 6px 0 0; {SUB}">[TBD]</p></div>' for p in perks]))
    s += sec("⑥ 루프탑 Cafe", f'''<div class="ph-dark" style="height: 320px; {bg("city", 1800, True)}; border: 1px solid #c4c4c4; border-radius: 8px; display: flex; flex-direction: column; justify-content: flex-end; padding: 32px; box-sizing: border-box; gap: 8px">
        <h2 style="margin: 0; font-size: 28px">[Cafe name] on the rooftop</h2>
        <span>Coffee by day, sunset over Old Tbilisi · Open [hours]</span>
        <a href="hostel-cafe.html" style="{BTN}; align-self: flex-start">Visit the Cafe</a>
      </div>''')
    trust = ["[Years] in Old Tbilisi", "Hostelworld [rating]", "TripAdvisor [rating]", "[Awards]"]
    s += sec("⑦ 신뢰 요소", grid(4, [f'<div style="{CARD}; padding: 20px; text-align: center"><strong style="font-size: 20px">{t}</strong></div>' for t in trust]))
    rv = f'<div style="{CARD}; padding: 20px; display: flex; flex-direction: column; gap: 8px">{lines(3, 70)}<span style="{SUB}">[Name, country]</span></div>'
    s += sec("⑧ 투숙객 후기", f'<div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: center; margin-bottom: 16px"><h2 style="margin: 0; font-size: 24px; flex: 1">Guest stories</h2><a href="hostel-about.html">All reviews</a></div>' + grid(3, [rv] * 3))
    tours = [tour_card("kazbeg", "Day tour", "[Day tour name]"), tour_card("mtskheta", "Day tour", "[Day tour name]"),
             tour_card("wine", "Day tour", "[Day tour name]"), tour_card("sevan", "Multi-day", "Envoy Boutique Journey")]
    s += sec("⑨ Tours with Envoy", f'<div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: center; margin-bottom: 16px"><h2 style="margin: 0; font-size: 24px; flex: 1">Tours with Envoy</h2><span style="{SUB}">Guest tour benefit [TBD]</span><a href="hostel-tbilisi.html">All tours</a></div>' + grid(4, tours))
    walks = "".join(f'<li style="display: flex; justify-content: space-between; border-bottom: 1px solid #e0e0e0; padding: 8px 0"><span>{a}</span><span style="color: #555">[min] walk</span></li>' for a in ["Freedom Square", "Abanotubani sulphur baths", "Narikala Fortress", "Dry Bridge"])
    s += sec("⑩ Old Tbilisi", f'''<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px; align-items: center">
        {ph(280)}
        <div>{h2("In the heart of Old Tbilisi", 8)}<ul style="list-style: none; margin: 0 0 12px; padding: 0">{walks}</ul><a href="hostel-tbilisi.html">Old Tbilisi Guide</a></div>
      </div>''')
    s += sec("⑪ Our Impact", f'''<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px; align-items: center">
        {ph(260)}
        <div style="display: flex; flex-direction: column; gap: 10px">{h2("Our Impact", 0)}<strong>[Story title]</strong>{lines(3)}<a href="hostel-about.html">Read the story</a></div>
      </div>''')
    s += sec("⑫ Instagram·소식", h2("Life at Envoy") + grid(6, ['<div style="aspect-ratio: 1; background: #e4e4e4; border-radius: 4px"></div>'] * 6, 12))
    s += sec("⑬ 푸터", footer_sec(), last=True)
    return page_desktop(0, s)

def rooms():
    s = ""
    s += sec("① 페이지 상단", f'''<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; font-size: 14px"><span style="border: 1px solid #1f1f1f; border-radius: 18px; padding: 6px 14px; font-weight: 600">Dormitory Rooms</span><a href="#" style="border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 14px; text-decoration: none">Ensuite Rooms</a><a href="#" style="border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 14px; text-decoration: none">Floor Guide</a><a href="#" style="border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 14px; text-decoration: none">Room Facilities</a><a href="#" style="border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 14px; text-decoration: none">Common Areas</a></div>
      <h1 style="margin: 0 0 8px; font-size: 36px">Dormitory Rooms</h1>
      <div style="max-width: 640px; display: flex; flex-direction: column; gap: 8px">{lines(2, 70)}</div>''')
    s += sec("② 예약 바", booking_bar())
    s += sec("③ 객실 카드", grid(2, [room_card(r, 240) for r in ROOMS[:4]], 24))
    std = ["Bed size [cm]", "Privacy curtain", "Reading light", "Power outlet and USB", "Large locker", "Shared bathroom on each floor", "Female-only option [TBD]", "Fresh linen and towel"]
    s += sec("④ 도미토리 공통 기준", h2("Every dorm bed comes with") + grid(4, [f'<div style="display: flex; gap: 10px; align-items: center"><span style="width: 32px; height: 32px; flex: none; background: #e4e4e4; border-radius: 50%"></span><span>{x}</span></div>' for x in std], 16))
    s += sec("⑤ Floor Guide", h2("Floor Guide") + grid(3, [f'<div style="{CARD}; padding: 16px; display: flex; flex-direction: column; gap: 8px"><strong>{f}</strong>{ph(140)}<span style="{SUB}">{d}</span></div>' for f, d in [("1F", "Reception · [rooms]"), ("2F", "[Rooms]"), ("3F", "[Rooms] · Rooftop Cafe")]]))
    s += sec("⑥ 직접 예약 혜택·하우스 정보", grid(2, [
        f'<div style="{CARD}; padding: 24px"><strong style="font-size: 18px">Why book direct</strong><ul style="margin: 8px 0 0; padding-left: 18px; color: #444"><li>Welcome drink [TBD]</li><li>Cafe benefit [TBD]</li><li>Flexible changes [TBD]</li></ul></div>',
        f'<div style="{CARD}; padding: 24px"><strong style="font-size: 18px">Good to know</strong><ul style="margin: 8px 0 0; padding-left: 18px; color: #444"><li>Check-in [time] · Check-out [time]</li><li>Luggage storage</li><li><a href="#">House rules</a></li></ul></div>']))
    s += sec("⑦ 단체·장기 체류 문의", f'<div style="{CARD}; padding: 32px; display: flex; flex-wrap: wrap; gap: 16px; align-items: center"><div style="flex: 1 1 400px"><h2 style="margin: 0 0 6px; font-size: 22px">Travelling as a group or staying longer?</h2><span style="color: #555">Groups, long stays and packages</span></div><a href="hostel-contact.html" style="{BTN2}">Group &amp; Long Stay Inquiry</a></div>')
    s += sec("⑧ 추천 투어", h2("While you are in Tbilisi") + grid(3, [tour_card("kazbeg", "Day tour", "[Day tour name]"), tour_card("mtskheta", "Day tour", "[Day tour name]"), tour_card("wine", "Day tour", "[Day tour name]")]), last=True)
    return page_desktop(1, s)

def cafe():
    s = ""
    s += sec("① 메인 비주얼", f'''<div class="ph-dark" style="height: 460px; {bg("city", 1800, True)}; border: 1px solid #c4c4c4; border-radius: 8px; display: flex; flex-direction: column; justify-content: flex-end; padding: 40px; box-sizing: border-box; gap: 10px">
        <span style="font-weight: 600">Rooftop · Envoy Hostel</span>
        <h1 style="margin: 0; font-size: 40px; line-height: 1.15">[Cafe name]</h1>
        <div style="font-size: 18px">Coffee by day, sunset over Old Tbilisi</div>
      </div>''')
    info = [("Open", "[Days] · [hours]"), ("Where", "Rooftop, [street address]"), ("Who", "Open to guests and visitors [TBD]")]
    s += sec("② 이용 정보", grid(3, [f'<div style="{CARD}; padding: 20px"><div style="{SUB}">{a}</div><strong>{b}</strong></div>' for a, b in info]) + '<div style="margin-top: 12px"><a href="hostel-contact.html">Getting here</a></div>')
    s += sec("③ 공간 소개", f'''<div style="display: grid; grid-template-columns: 2fr 1fr; gap: 16px">
        {ph(380, "city", 1200)}
        <div style="display: flex; flex-direction: column; gap: 16px">{ph(182)}{ph(182)}</div>
      </div>
      <div style="max-width: 720px; margin-top: 16px; display: flex; flex-direction: column; gap: 8px">{lines(3)}</div>''')
    menu = [("Coffee", None), ("Breakfast", "food"), ("Georgian wine", "wine"), ("[Signature item]", None), ("[Signature item]", None), ("[Signature item]", None)]
    items = [f'<div style="{CARD}; overflow: hidden">{ph(160, k, 600, 0, "; border: 0")}<div style="padding: 12px; display: flex; justify-content: space-between"><strong>{n}</strong><span style="color: #555">GEL [TBD]</span></div></div>' for n, k in menu]
    s += sec("④ 대표 메뉴", f'<div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: center; margin-bottom: 16px"><h2 style="margin: 0; font-size: 24px; flex: 1">On the menu</h2><a href="#" style="{BTN2}">Full Menu</a></div>' + grid(3, items))
    ev = [("[Date]", "Sunset hour on the rooftop"), ("[Date]", "Weekend community evening"), ("[Date]", "[Event name]")]
    s += sec("⑤ 이벤트", h2("Events") + grid(3, [f'<div style="{CARD}; padding: 20px; display: flex; flex-direction: column; gap: 6px"><span style="{SUB}">{d}</span><strong>{t}</strong>{lines(2)}</div>' for d, t in ev]))
    s += sec("⑥ 투숙객 혜택", f'<div style="{CARD}; padding: 32px; display: flex; flex-wrap: wrap; gap: 16px; align-items: center"><div style="flex: 1 1 400px"><h2 style="margin: 0 0 6px; font-size: 22px">Staying with us?</h2><span style="color: #555">Welcome drink and sunset seating for direct bookings [TBD]</span></div><a href="#" style="{BTN}">Book Now</a></div>')
    s += sec("⑦ 후기·Instagram", f'<div style="display: flex; flex-wrap: wrap; gap: 16px; align-items: center; margin-bottom: 16px"><h2 style="margin: 0; font-size: 24px; flex: 1">From the rooftop</h2><span style="border: 1px solid #bdbdbd; border-radius: 6px; padding: 8px 12px; font-size: 13px">Google [rating]</span></div>' + grid(6, ['<div style="aspect-ratio: 1; background: #e4e4e4; border-radius: 4px"></div>'] * 6, 12))
    s += sec("⑧ 연계 안내", grid(2, [
        f'<a href="hostel-rooms.html" style="{CARD}; overflow: hidden; text-decoration: none"><div style="height: 180px; {GREY}"></div><div style="padding: 16px"><strong>Stay with Envoy</strong><div style="{SUB}">Rooms in the same building</div></div></a>',
        f'<a href="hostel-tbilisi.html" style="{CARD}; overflow: hidden; text-decoration: none"><div style="height: 180px; {bg("kazbeg", 900)}"></div><div style="padding: 16px"><strong>Tours with Envoy</strong><div style="{SUB}">Day trips from Tbilisi</div></div></a>']), last=True)
    return page_desktop(2, s)

def tbilisi():
    s = ""
    s += sec("① 페이지 상단", f'''<div class="ph-dark" style="height: 360px; {bg("city", 1800, True)}; border: 1px solid #c4c4c4; border-radius: 8px; display: flex; flex-direction: column; justify-content: flex-end; padding: 40px; box-sizing: border-box; gap: 10px">
        <h1 style="margin: 0; font-size: 40px; line-height: 1.15">Old Tbilisi Guide</h1>
        <div style="font-size: 18px">Walk, eat and explore from our door</div>
      </div>
      <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; font-size: 14px"><span style="border: 1px solid #1f1f1f; border-radius: 18px; padding: 6px 14px; font-weight: 600">Old Tbilisi Guide</span><a href="#tours" style="border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 14px; text-decoration: none">Tours with Envoy</a><a href="#" style="border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 14px; text-decoration: none">Events</a></div>''')
    walks = "".join(f'<li style="display: flex; justify-content: space-between; border-bottom: 1px solid #e0e0e0; padding: 10px 0"><span>{a}</span><span style="color: #555">[min] walk</span></li>' for a in ["Freedom Square", "Abanotubani sulphur baths", "Narikala Fortress", "Dry Bridge", "Rustaveli Avenue"])
    s += sec("② 지도·도보 시간", f'<div style="display: grid; grid-template-columns: 3fr 2fr; gap: 32px">{ph(380)}<div>{h2("Around the hostel", 8)}<ul style="list-style: none; margin: 0; padding: 0">{walks}</ul></div></div>')
    pl = [("Eat", "food"), ("Drink", "wine"), ("See", "city"), ("[Category]", None), ("[Category]", None), ("[Category]", None)]
    s += sec("③ Envoy 추천 장소", h2("Our local picks") + grid(3, [f'<div style="{CARD}; overflow: hidden">{ph(160, k, 600, 0, "; border: 0")}<div style="padding: 12px; display: flex; flex-direction: column; gap: 4px"><span style="{SUB}">{c}</span><strong>[Place name]</strong><span style="font-size: 13px; color: #444">[One line] · [min] walk</span></div></div>' for c, k in pl]))
    tips = ["From the airport", "Getting around", "Money and SIM cards", "Weather"]
    s += sec("④ 여행 정보", h2("Travel tips") + grid(4, [f'<div style="{CARD}; padding: 20px; display: flex; flex-direction: column; gap: 8px"><strong>{t}</strong>{lines(3)}</div>' for t in tips]))
    tours = [tour_card("kazbeg", "Day tour", "[Day tour name]"), tour_card("mtskheta", "Day tour", "[Day tour name]"),
             tour_card("wine", "Day tour", "[Day tour name]"), tour_card("geghard", "Cross-border day tour", "[Day tour name]")]
    s += sec("⑤ Tours with Envoy", f'<div id="tours" style="display: flex; flex-wrap: wrap; gap: 16px; align-items: center; margin-bottom: 16px"><h2 style="margin: 0; font-size: 24px; flex: 1">Tours with Envoy</h2><span style="{SUB}">Guest tour benefit [TBD]</span><a href="#" style="{BTN2}">All Tours on Envoy Tours</a></div>' + grid(4, tours))
    s += sec("⑥ 투어 전후 숙박", f'<div style="{CARD}; padding: 32px; display: flex; flex-wrap: wrap; gap: 16px; align-items: center"><div style="flex: 1 1 400px"><h2 style="margin: 0 0 6px; font-size: 22px">Joining a multi-day tour?</h2><span style="color: #555">Stay with us the night before and after your journey</span></div><a href="#" style="{BTN}">Book Now</a></div>', last=True)
    return page_desktop(3, s)

def about():
    s = ""
    s += sec("① 페이지 상단", f'''<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; font-size: 14px"><span style="border: 1px solid #1f1f1f; border-radius: 18px; padding: 6px 14px; font-weight: 600">Our Story</span><a href="#" style="border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 14px; text-decoration: none">Envoy Way</a><a href="#" style="border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 14px; text-decoration: none">Reviews &amp; Guest Stories</a><a href="#" style="border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 14px; text-decoration: none">Our Impact</a></div>
      <h1 style="margin: 0 0 16px; font-size: 36px">About Envoy</h1>
      {ph(360, "city", 1800)}''')
    s += sec("② Our Story", f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px; align-items: center"><div style="display: flex; flex-direction: column; gap: 10px">{h2("Our Story", 4)}{lines(5, 50)}</div>{ph(300)}</div>')
    tl = [("2005", "Envoy Hostel opens in Old Tbilisi"), ("[Year]", "[Milestone]"), ("2026", "Renovation"), ("April 2027", "Reopening as a boutique hostel")]
    s += sec("③ 건물의 이야기·연혁", h2("The building and our years") + grid(4, [f'<div style="border-top: 2px solid #1f1f1f; padding-top: 12px"><strong>{y}</strong><div style="{SUB}">{t}</div></div>' for y, t in tl]))
    vals = ["Warm hospitality", "Georgian culture", "Natural connection", "[Value]"]
    s += sec("④ Envoy Way", h2("Envoy Way") + grid(4, [f'<div style="{CARD}; padding: 20px"><div style="width: 40px; height: 40px; background: #e4e4e4; border-radius: 50%; margin-bottom: 12px"></div><strong>{v}</strong><p style="margin: 6px 0 0; {SUB}">[One line]</p></div>' for v in vals]))
    rv = f'<div style="{CARD}; padding: 20px; display: flex; flex-direction: column; gap: 8px">{lines(4, 70)}<span style="{SUB}">[Name, country]</span></div>'
    badges = "".join(f'<span style="border: 1px solid #bdbdbd; border-radius: 6px; padding: 8px 12px; font-size: 13px">{b}</span>' for b in ["Hostelworld [rating]", "TripAdvisor [rating]", "Google [rating]", "[Award]"])
    s += sec("⑤ Reviews &amp; Guest Stories", f'<div style="display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin-bottom: 16px"><h2 style="margin: 0; font-size: 24px; flex: 1">Reviews &amp; Guest Stories</h2>{badges}</div>' + grid(3, [rv] * 3))
    nums = [("[Number]", "[Impact measure]"), ("[Number]", "[Impact measure]"), ("[Number]", "[Impact measure]")]
    s += sec("⑥ Our Impact", f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px; align-items: center">{ph(300)}<div style="display: flex; flex-direction: column; gap: 10px">{h2("Our Impact", 0)}<strong>[Story title]</strong>{lines(3)}<a href="#">Read the story</a></div></div><div style="margin-top: 24px">' + grid(3, [f'<div style="{CARD}; padding: 20px; text-align: center"><strong style="font-size: 28px">{a}</strong><div style="{SUB}">{b}</div></div>' for a, b in nums]) + '</div>')
    s += sec("⑦ Envoy Tours 연결", f'<div style="{CARD}; padding: 32px; display: flex; flex-wrap: wrap; gap: 16px; align-items: center"><div style="flex: 1 1 400px"><h2 style="margin: 0 0 6px; font-size: 22px">Envoy Tours</h2><span style="color: #555">Journeys across Georgia and Armenia</span></div><a href="#" style="{BTN2}">Visit Envoy Tours</a></div>', last=True)
    return page_desktop(4, s)

def field(lbl, wide=False):
    span = "grid-column: 1 / -1; " if wide else ""
    h = 96 if wide else 44
    return f'<label style="{span}display: flex; flex-direction: column; gap: 4px; font-size: 13px"><span>{lbl}</span><span style="height: {h}px; border: 1px solid #9e9e9e; border-radius: 6px; display: block"></span></label>'

def contact():
    s = ""
    s += sec("① 페이지 상단", f'''<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; font-size: 14px"><span style="border: 1px solid #1f1f1f; border-radius: 18px; padding: 6px 14px; font-weight: 600">Location &amp; Getting Here</span><a href="#pickup" style="border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 14px; text-decoration: none">Airport Pickup</a><a href="#contact" style="border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 14px; text-decoration: none">Contact Us</a></div>
      <h1 style="margin: 0; font-size: 36px">Contact</h1>''')
    how = ["From the airport", "From the train station", "Walking up the hill", "Luggage help"]
    s += sec("② Location &amp; Getting Here", f'<div style="display: grid; grid-template-columns: 3fr 2fr; gap: 32px">{ph(360)}<div style="display: flex; flex-direction: column; gap: 12px"><strong style="font-size: 18px">Envoy Hostel</strong><span style="color: #444">[Street address], Old Tbilisi</span><a href="#">Open in Google Maps</a>' + "".join(f'<div style="border-top: 1px solid #e0e0e0; padding-top: 8px"><strong>{h}</strong><div style="{SUB}">[One line]</div></div>' for h in how) + '</div></div>')
    pick = grid(2, [field("Full name"), field("Email"), field("Arrival date and time"), field("Flight number"), field("Guests"), field("Bags"), field("Requests", True)])
    s += sec("③ Airport Pickup", f'<div id="pickup" style="display: grid; grid-template-columns: 1fr 2fr; gap: 32px"><div style="display: flex; flex-direction: column; gap: 8px">{h2("Airport Pickup", 0)}<span style="color: #444">From USD [TBD] per vehicle</span>{lines(3)}</div><div style="{CARD}; padding: 24px; display: flex; flex-direction: column; gap: 16px">{pick}<a href="#" style="{BTN}; align-self: flex-start">Request Pickup</a></div></div>')
    grp = grid(2, [field("Full name"), field("Email"), field("Dates"), field("Guests"), field("Inquiry type: Group / Long stay / Package"), field("Country"), field("Message", True)])
    s += sec("④ Group &amp; Long Stay Inquiry", f'<div style="display: grid; grid-template-columns: 1fr 2fr; gap: 32px"><div style="display: flex; flex-direction: column; gap: 8px">{h2("Groups and long stays", 0)}{lines(3)}</div><div style="{CARD}; padding: 24px; display: flex; flex-direction: column; gap: 16px">{grp}<a href="#" style="{BTN}; align-self: flex-start">Send Inquiry</a></div></div>')
    ch = [("WhatsApp", "+995 [000 000 000]"), ("Email", "hostel@[domain]"), ("Reception", "[Hours]")]
    cu = grid(2, [field("Full name"), field("Email"), field("Message", True)])
    s += sec("⑤ Contact Us", f'<div id="contact" style="display: grid; grid-template-columns: 1fr 2fr; gap: 32px"><div style="display: flex; flex-direction: column; gap: 12px">{h2("Contact Us", 0)}' + "".join(f'<div><div style="{SUB}">{a}</div><strong>{b}</strong></div>' for a, b in ch) + f'</div><div style="{CARD}; padding: 24px; display: flex; flex-direction: column; gap: 16px">{cu}<a href="#" style="{BTN}; align-self: flex-start">Send Message</a></div></div>', last=True)
    return page_desktop(5, s)

# ---------- mobile ----------
def mheader():
    return f'''  <header style="display: flex; align-items: center; gap: 8px; padding: 8px 16px; border-bottom: 1px solid #cfcfcf">
    <div style="width: 96px; height: 32px; background: #e4e4e4; border: 1px solid #c4c4c4; display: flex; align-items: center; justify-content: center; font-size: 11px; color: #555">LOGO</div>
    <span style="flex: 1"></span>
    <a href="#" style="display: inline-flex; align-items: center; min-height: 44px; padding: 0 12px; background: #1f1f1f; color: #fff; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 13px">Book Now</a>
    <button type="button" aria-label="Open menu" style="width: 44px; height: 44px; border: 1px solid #9e9e9e; background: #fff; border-radius: 6px; display: flex; align-items: center; justify-content: center"><svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 5h14M3 10h14M3 15h14" stroke="#1f1f1f" stroke-width="1.6" fill="none"/></svg></button>
  </header>
'''

def mbottom(left, right):
    return f'''  <div style="position: absolute; left: 0; right: 0; bottom: 0; padding: 12px 16px; background: #fff; border-top: 1px solid #9e9e9e; display: flex; gap: 8px; align-items: center">
    <span lang="ko" style="position: absolute; top: -22px; left: 16px; background: #3d3d3d; color: #fff; font-size: 11px; padding: 1px 6px; border-radius: 4px">하단 고정 바</span>
    {left}
    <a href="#" style="flex: 1; display: inline-flex; align-items: center; justify-content: center; min-height: 44px; background: #1f1f1f; color: #fff; border-radius: 6px; text-decoration: none; font-weight: 600">{right}</a>
  </div>
'''

def page_mobile(i, h, body, bottom):
    f, t = PAGES[i]
    return (HEAD.format(title=t) + bar(i) + f'<div class="phone-stage"><div class="phone">\n<div style="position: relative; width: 390px; min-height: {h}px; padding-bottom: 96px; box-sizing: border-box; overflow: hidden; font-size: 14px; line-height: 1.5; background: #fff">\n\n'
            + mheader() + '\n  <div style="padding: 0 16px">\n' + body + '  </div>\n\n' + bottom + '</div>\n</div></div>\n</body>\n</html>\n')

def mbook():
    f = "".join(f'<div style="flex: 1; border: 1px solid #9e9e9e; border-radius: 6px; padding: 6px 10px"><div style="font-size: 11px; color: #555">{a}</div><strong style="font-size: 13px">{b}</strong></div>' for a, b in [("Check-in", "[Date]"), ("Check-out", "[Date]"), ("Guests", "2")])
    return f'<div style="{CARD}; padding: 12px; display: flex; flex-direction: column; gap: 8px"><div style="display: flex; gap: 6px">{f}</div><a href="#" style="{BTN}">Check Availability</a><span style="font-size: 12px; color: #555">Book direct: welcome drink · Cafe benefit [TBD]</span></div>'

def mhome():
    s = ""
    s += msec("① 메인 비주얼", f'''<div class="ph-dark" style="height: 360px; {bg("city", 900, True)}; border: 1px solid #c4c4c4; border-radius: 8px; display: flex; flex-direction: column; justify-content: flex-end; padding: 16px; box-sizing: border-box; gap: 6px">
        <span style="font-size: 12px; font-weight: 600">Reopening April 2027</span>
        <strong style="font-size: 24px; line-height: 1.2">A boutique hostel in Old Tbilisi</strong>
        <span style="font-size: 13px">Rooms, a rooftop cafe and tours under one roof</span>
      </div>''')
    s += msec("② 예약 바", mbook())
    rc = lambda t, d: f'<a href="hostel-mobile-rooms.html" style="{CARD}; overflow: hidden; text-decoration: none; display: block"><div style="height: 150px; {GREY}"></div><div style="padding: 12px"><strong>{t}</strong><div style="font-size: 13px">{d}</div></div></a>'
    s += msec("③ Rooms", f'<strong style="display: block; font-size: 18px; margin-bottom: 8px">Rooms</strong><div style="display: flex; flex-direction: column; gap: 12px">{rc("Dormitory Rooms", "From USD [TBD] per bed")}{rc("Ensuite Rooms", "From USD [TBD] per room")}</div>')
    s += msec("④ Why Book Direct", '<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; font-size: 13px">' + "".join(f'<div style="{CARD}; padding: 12px"><strong>{p}</strong></div>' for p in ["Welcome drink", "Cafe benefit", "Flexible changes", "Tour benefit"]) + '</div>')
    s += msec("⑤ 루프탑 Cafe", f'<div class="ph-dark" style="height: 200px; {bg("city", 900, True)}; border-radius: 8px; display: flex; flex-direction: column; justify-content: flex-end; padding: 12px; box-sizing: border-box"><strong style="font-size: 18px">[Cafe name] on the rooftop</strong><span style="font-size: 13px">Open [hours]</span></div>')
    s += msec("⑥~⑦ 신뢰 요소·후기", f'<div style="{CARD}; padding: 16px; display: flex; flex-direction: column; gap: 8px"><span style="font-size: 12px; color: #555">Hostelworld [rating] · TripAdvisor [rating]</span>{lines(2, 70)}<span style="font-size: 12px; color: #555">[Name, country]</span></div>')
    s += msec("⑧ Tours with Envoy", '<div style="display: flex; gap: 12px; overflow: hidden">' + "".join(f'<div style="flex: none; width: 240px; {CARD}; overflow: hidden"><div style="height: 130px; {bg(k, 600)}"></div><div style="padding: 10px"><strong style="font-size: 13px">[Day tour name]</strong><div style="font-size: 12px">From USD [TBD]</div></div></div>' for k in ["kazbeg", "mtskheta"]) + '</div>')
    s += msec("⑨~⑪ Old Tbilisi, Our Impact, Instagram", '<div style="display: flex; flex-direction: column; gap: 8px"><div style="height: 72px; background: #e4e4e4; border-radius: 6px; display: flex; align-items: center; padding: 0 12px; font-weight: 600">Old Tbilisi Guide</div><div style="height: 72px; background: #e4e4e4; border-radius: 6px; display: flex; align-items: center; padding: 0 12px; font-weight: 600">Our Impact</div></div><div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 6px; margin-top: 12px"><div style="aspect-ratio: 1; background: #e4e4e4"></div><div style="aspect-ratio: 1; background: #e4e4e4"></div><div style="aspect-ratio: 1; background: #e4e4e4"></div></div>')
    s += msec("⑫ 푸터", '<div style="background: #f2f2f2; padding: 16px; font-size: 12px; color: #555">[Street address], Old Tbilisi · WhatsApp · hostel@[domain] · Booking terms · Envoy Tours</div>', last=True)
    return page_mobile(6, 800, s, mbottom('<a href="#" style="display: inline-flex; align-items: center; justify-content: center; min-height: 44px; padding: 0 14px; border: 1px solid #9e9e9e; border-radius: 6px; text-decoration: none">WhatsApp</a>', "Book Now"))

def mrooms():
    s = ""
    s += msec("① 페이지 상단", '<div style="display: flex; gap: 8px; overflow: hidden; font-size: 13px; margin-bottom: 12px"><span style="flex: none; border: 1px solid #1f1f1f; border-radius: 18px; padding: 6px 12px; font-weight: 600">Dormitory</span><span style="flex: none; border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 12px">Ensuite</span><span style="flex: none; border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 12px">Floor Guide</span><span style="flex: none; border: 1px solid #9e9e9e; border-radius: 18px; padding: 6px 12px">Facilities</span></div><strong style="display: block; font-size: 24px">Dormitory Rooms</strong>' + f'<div style="display: flex; flex-direction: column; gap: 6px; margin-top: 8px">{lines(2, 70)}</div>')
    s += msec("② 예약 바", mbook())
    s += msec("③ 객실 카드", '<div style="display: flex; flex-direction: column; gap: 16px">' + "".join(room_card(r, 200) for r in ROOMS[:3]) + '</div>')
    s += msec("④ 도미토리 공통 기준", '<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; font-size: 13px">' + "".join(f'<div style="display: flex; gap: 8px; align-items: center"><span style="width: 24px; height: 24px; flex: none; background: #e4e4e4; border-radius: 50%"></span>{x}</div>' for x in ["Privacy curtain", "Reading light", "Power outlet", "Large locker"]) + '</div>')
    s += msec("⑤ 단체·장기 체류 문의", f'<div style="{CARD}; padding: 12px"><strong>Group or long stay?</strong><div style="font-size: 13px"><a href="hostel-contact.html">Group &amp; Long Stay Inquiry</a></div></div>', last=True)
    return page_mobile(7, 800, s, mbottom('<span style="font-size: 13px">From USD [TBD]<br><span style="color: #555">per bed</span></span>', "Book Now"))

def main():
    out = {"hostel-home": home(), "hostel-rooms": rooms(), "hostel-cafe": cafe(), "hostel-tbilisi": tbilisi(),
           "hostel-about": about(), "hostel-contact": contact(), "hostel-mobile-home": mhome(), "hostel-mobile-rooms": mrooms()}
    for k, v in out.items():
        with open(os.path.join(OUT, k + ".html"), "w", encoding="utf-8") as fh:
            fh.write(v)
        print(k, len(v))

if __name__ == "__main__":
    main()
