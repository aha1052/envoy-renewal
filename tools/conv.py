import re,sys,os
src,dst=sys.argv[1],sys.argv[2]
names={"Main":"홈","AllTours":"All Tours","TourDetail":"상품 상세","PlanYourTrip":"Plan Your Trip","About":"About Envoy","Contact":"Contact","MobileHome":"모바일 홈","MobileDetail":"모바일 상품 상세"}
outn={"Main":"home"}
def fn(n): return outn.get(n, re.sub(r'(?<!^)([A-Z])',r'-\1',n).lower())
for n,t in names.items():
    h=open(f"{src}/{n}.dc.html",encoding="utf-8").read()
    style=re.search(r'<helmet>\s*<style>(.*?)</style>\s*</helmet>',h,re.S).group(1)
    body=re.search(r'</helmet>(.*)</x-dc>',h,re.S).group(1)
    # drop original grey label bar (first div with lang=ko at top)
    body=re.sub(r'\s*<div style="background: #efefef; padding: [^"]*"[^>]*>(.*?)</div>',lambda m:'',body,count=1,flags=re.S)
    note=re.search(r'<div style="background: #efefef; padding: [^"]*"[^>]*>(.*?)</div>',h,re.S).group(1)
    body=re.sub(r'href="(\w+)\.dc\.html"',lambda m:f'href="{fn(m.group(1))}.html"',body)
    mobile=n.startswith("Mobile")
    wrap_open='<div class="phone">' if mobile else ''
    wrap_close='</div>' if mobile else ''
    order=list(names)
    i=order.index(n); prev=order[i-1] if i>0 else None; nxt=order[i+1] if i<len(order)-1 else None
    nav=''
    if prev: nav+=f'<a href="{fn(prev)}.html">← {names[prev]}</a>'
    if nxt: nav+=f'<a href="{fn(nxt)}.html">{names[nxt]} →</a>'
    out=f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>와이어프레임 · {t}</title>
<style>
{style}
.wf-bar{{position:sticky;top:0;z-index:5;background:#22312c;color:#f3f1ea;font:13px/1.4 "Noto Sans KR",system-ui,sans-serif;display:flex;flex-wrap:wrap;gap:8px 20px;align-items:center;padding:10px max(16px,env(safe-area-inset-left,0px))}}
.wf-bar a{{color:#f3f1ea;text-decoration:none}}.wf-bar a:hover{{text-decoration:underline}}
.wf-bar .t{{flex:1 1 240px;opacity:.85}}
.phone-stage{{background:#e9e9e6;padding:32px 16px;display:flex;justify-content:center}}
.phone{{width:390px;max-width:100%;background:#fff;box-shadow:0 0 0 1px #c9c9c4;overflow:hidden}}
</style>
</head>
<body>
<div class="wf-bar"><a href="../index.html#tours-wireframes">← 와이어프레임 목록</a><span class="t">{t}</span>{nav}</div>
{'<div class="phone-stage">' if mobile else ''}{wrap_open}{body}{wrap_close}{'</div>' if mobile else ''}
</body>
</html>
'''
    open(f"{dst}/{fn(n)}.html","w",encoding="utf-8").write(out)
    print(fn(n))
