import re,glob,sys
d=sys.argv[1]
M={
"Envoy Hostel과 루프탑 Cafe · 호스텔 사이트 연결":"Stay with Envoy",
"Envoy Way · 가치 3가지":"Envoy Way",
"Our Impact · Envoy Mission 실제 사례 (기존 Donation 개편)":"Our Impact",
"Our Story · 회사 이야기와 사진":"Our Story",
"Why Travel with Envoy · 팀, 가이드, 후기":"Why Travel with Envoy",
"① 메인 비주얼 · 대표 상품 슬라이더":"① 메인 비주얼",
"① 메인 비주얼 · 첫 화면에 상품과 버튼":"① 메인 비주얼",
"② 유형별 투어 · All Tours 바로가기":"② 유형별 투어",
"② 유형별 투어 · 가로 스크롤":"② 유형별 투어",
"③ Featured Tours · 상품 카드 4~6개":"③ Featured Tours",
"③ Featured Tours · 카드 세로 배열":"③ Featured Tours",
"④ Why Travel with Envoy · 2열":"④ Why Travel with Envoy",
"④ Why Travel with Envoy · 신뢰 포인트":"④ Why Travel with Envoy",
"⑤ 고객 후기 · 1건씩 넘김":"⑤ 고객 후기",
"⑤ 고객 후기 · 평점과 상세 후기 2~3건":"⑤ 고객 후기",
"⑦ Our Impact · Envoy Mission 사례 1건":"⑦ Our Impact",
"⑨ Stay with Envoy · 호스텔, 루프탑 Cafe":"⑨ Stay with Envoy",
"공통 1 · 대표 사진, 투어명, 한 줄 소개, 태그":"공통 1 · 대표 사진, 투어명, 소개, 태그",
"공통 10~11 · 후기, 관련 투어":"공통 10~11 · 고객 후기, 관련 투어",
"공통 1~4 · 첫 화면에 핵심 정보":"공통 1~4 · 대표 사진, 가격, 운영 정보, 포함 사항",
"공통 2 · 가격 정보와 요금 기준":"공통 2 · 가격 정보",
"공통 5 · 하이라이트 4~6개":"공통 5 · 하이라이트",
"공통 6 · 일자별 일정 (일정 안에 큰 사진)":"공통 6 · 일정",
"공통 6 · 일정 (접고 펼치기)":"공통 6 · 일정",
"공통 7~9 · 포함 사항, 출발일, 예약 조건":"공통 7~9 · 포함·불포함 사항, 출발일, 예약 조건",
"공통 8 · 출발일 및 기타 날짜 문의":"공통 8 · 출발일",
"문의 유형 선택 · 공통 양식으로 연결":"문의 유형 선택",
"상단 소개 · 페이지 내 바로가기":"상단 소개",
"상품 카드 목록 · 사진, 상품명, 기간·국가, 그룹/프라이빗, 시작 가격과 요금 기준":"상품 카드 목록",
"선택 · 숙박 정보, 경로 지도 (다일 상품)":"선택 · 숙박 정보, 경로 지도",
"선택 항목 · 상품별 적용":"선택 항목",
"일반 문의 · 공통 양식":"일반 문의",
"필터 영역 · 여행 조건으로 찾기":"필터 영역",
"하단 고정 바 · 가격과 Request a Booking":"하단 고정 바",
}
for f in glob.glob(d+"/*.html"):
    s=open(f,encoding="utf-8").read()
    for a,b in M.items(): s=s.replace(">"+a+"<",">"+b+"<")
    s=s.replace("Footer (same as home)","Footer")
    open(f,"w",encoding="utf-8").write(s)
