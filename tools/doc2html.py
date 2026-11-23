import sys, xml.etree.ElementTree as ET, html
x=open(sys.argv[1],encoding="utf-8").read()
root=ET.fromstring(x)
def inline(el):
    out=""
    for c in el:
        t=c.tag
        if t=="text": out+=textrun(c)
        elif t=="date": out+=c.get("value","")
        elif t=="mention": out+=""
        elif t=="link":
            out+=f'<a href="{html.escape(c.get("href",""))}">{inline(c) or html.escape(c.text or "")}</a>'
        else: out+=inline(c)
    return out
def textrun(el):
    s=html.escape(el.text or "")
    for c in el:
        inner=textrun(c)
        if c.tag=="bold": s+=f"<b>{inner}</b>"
        elif c.tag=="link": s+=f'<a href="{html.escape(c.get("href",""))}">{inner}</a>'
        else: s+=inner
        s+=html.escape(c.tail or "")
    return s
sec=[0]; out=[]; title=None
def block(el):
    t=el.tag
    if t=="paragraph":
        h=el.get("heading"); body=inline(el)
        if h=="1": return ""
        if h=="2":
            sec[0]+=1; return f'<h2 id="h{sec[0]}">{body}</h2>'
        if h: return f"<h4>{body}</h4>"
        if body.startswith("<b>") and body.endswith("</b>") and body.count("<b>")==1: return f"<h4>{body[3:-4]}</h4>"
        return f"<p>{body}</p>" if body.strip() else ""
    if t=="list":
        tag="ol" if el.get("kind")=="ordered" else "ul"
        items="".join("<li>"+"".join(block(p) if p.tag!="paragraph" else inline(p) for p in li)+"</li>" for li in el)
        return f"<{tag}>{items}</{tag}>"
    if t=="table":
        rows=list(el); head=[r for r in rows if r[0].get("header")=="true"]; body=[r for r in rows if r[0].get("header")!="true"]
        def cells(r,tg): return "".join(f"<{tg}>"+" ".join(inline(p) for p in c)+f"</{tg}>" for c in r)
        th="<thead><tr>"+cells(head[0],"th")+"</tr></thead>" if head else ""
        return '<div class="tbl"><table>'+th+"<tbody>"+"".join("<tr>"+cells(r,"td")+"</tr>" for r in body)+"</tbody></table></div>"
    return ""
blocks=list(root)
for b in blocks: 
    h=block(b)
    if h: out.append(h)
# first non-heading paragraphs: date line & intro
open(sys.argv[2],"w",encoding="utf-8").write("\n".join(out))
