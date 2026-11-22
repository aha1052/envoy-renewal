import re,sys
d=sys.argv[1]
W="https://commons.wikimedia.org/wiki/Special:FilePath/"
I={
"K":"Gergeti_Trinity_Church_and_Mt._Kazbeg_01.jpg","A":"Mount_Ararat_and_Khor_Virap%2C_Sunrise%2C_Ararat_Plain%2C_Armenia.jpg",
"G":"Geghard_Monastery%2C_Geghard%2C_Armenia.jpg","KA":"Kakheti%2C_Georgia_%E2%80%94_Georgian_vineyards.jpg",
"S":"Svetitskhoveli_%282%29.jpg","T":"Tbilisi_city_view.jpg","Y":"Yerevan_from_Cascade.jpg","SE":"Lake_Sevan_%285063530234%29.jpg",
"KV":"Khor_Virap._Ararat.jpg","KH":"Khinkali_551.jpg","M":"Mtsvadi.jpg","D":"Armenian_dolma_01.jpg"}
def u(k,w): return f"{W}{I[k]}?width={w}"
# file: {index: (key, width, dark)}
P={
"home":{1:("K",1800,1),2:("KA",500,0),3:("S",500,0),4:("T",500,0),5:("SE",500,0),6:("KA",700,0),7:("S",700,0),8:("T",700,0),9:("G",700,0),14:("K",900,1),15:("A",900,1),16:("KV",900,1)},
"all-tours":{1:("KA",700,0),2:("S",700,0),3:("T",700,0),4:("G",700,0),5:("KV",700,0)},
"tour-detail":{1:("A",1800,0),2:("K",200,0),3:("KA",200,0),4:("G",200,0),5:("KH",200,0),6:("T",1200,0),12:("S",500,0),13:("Y",500,0),14:("SE",500,0)},
"mobile-home":{1:("K",900,1),2:("KA",700,0),3:("S",700,0)},
"mobile-detail":{1:("A",900,0),2:("K",200,0),3:("KA",200,0),4:("G",200,0),5:("T",800,0)},
}
pat=re.compile(r'(<(?:div|a)\b[^>]*?style=")([^"]*background: #e4e4e4[^"]*)(")')
for f,m in P.items():
    p=f"{d}/{f}.html"; s=open(p,encoding="utf-8").read(); n=[-1]
    def rep(mm):
        n[0]+=1
        if n[0] not in m: return mm.group(0)
        k,w,dark=m[n[0]]
        bg=(f"linear-gradient(180deg, rgba(0,0,0,.05) 35%, rgba(0,0,0,.6)), url(&quot;{u(k,w)}&quot;) center / cover no-repeat, #e4e4e4" if dark
            else f"url(&quot;{u(k,w)}&quot;) center / cover no-repeat, #e4e4e4")
        st=mm.group(2).replace("background: #e4e4e4","background: "+bg)
        cls=' class="ph-dark"' if dark else ''
        tag=mm.group(1)
        return tag.replace(" style=\"",cls+" style=\"",1)+st+mm.group(3)
    s=pat.sub(rep,s)
    s=s.replace('<div style="position: absolute; top: 16px; right: 16px; font-size: 12px; color: #555">Photo / video</div>','')
    s=s.replace('>Hero photo or video<','><')
    s=s.replace("</style>",".ph-dark,.ph-dark *{color:#fff !important}.ph-dark a[style*=\"background: #1f1f1f\"]{background:#fff !important;color:#1f1f1f !important}\n</style>",1)
    open(p,"w",encoding="utf-8").write(s)
    print(f,n[0]+1,"placeholders scanned")
