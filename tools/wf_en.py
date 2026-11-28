#!/usr/bin/env python3
"""Build English wireframes: wireframes/*.html -> wireframes/en/*.html.
Run after any wireframe change (and after tools/hostel_wf.py). Fails if Korean text remains."""
import os, re, glob

BASE = os.path.join(os.path.dirname(__file__), "..", "wireframes")
OUT = os.path.join(BASE, "en")

T = {
    "1. 재오픈 안내": "1. Reopening notice",
    "2. 사전 예약": "2. Pre-booking",
    "3. 정상 운영": "3. Regular operation",
    "Plan Your Trip 추가 항목": "Plan Your Trip additional fields",
    "와이어프레임 목록": "Wireframe list",
    "①-1 재오픈 단계별 첫 화면": "①-1 First screen by reopening stage",
    "메인 비주얼": "Main visual",
    "페이지 상단": "Page header",
    "예약 바": "Booking bar",
    "유형별 투어": "Tours by type",
    "이용 정보": "Visitor information",
    "지도·도보 시간": "Map and walking times",
    "Envoy 추천 장소": "Envoy local picks",
    "객실 카드": "Room cards",
    "건물의 이야기·연혁": "The building and history",
    "공간 소개": "The space",
    "투숙객이 꼽은 강점": "Strengths cited by guests",
    "개인실 공통 설비": "Private room standard facilities",
    "대표 메뉴": "Signature menu",
    "도미토리 공통 기준": "Dormitory standards",
    "여행 정보": "Travel information",
    "단체·장기 체류 문의": "Group and long-stay inquiry",
    "이벤트": "Events",
    "가족·장기 체류 안내": "Families and long stays",
    "고객 후기": "Customer reviews",
    "루프탑 전망·Cafe": "Rooftop view and Cafe",
    "직접 예약 혜택·하우스 정보": "Direct booking benefits and house information",
    "투숙객 혜택": "Guest benefits",
    "투어 전후 숙박": "Stays before and after tours",
    "Envoy Tours 연결": "Link to Envoy Tours",
    "투숙객 후기": "Guest reviews",
    "후기·Instagram": "Reviews and Instagram",
    "Our Impact, 문의, Stay with Envoy": "Our Impact, Inquiries, Stay with Envoy",
    "여행·단체·파트너 문의": "Trip, group and partner inquiries",
    "연계 안내": "Related links",
    "추천 투어": "Recommended tours",
    "푸터": "Footer",
    "Instagram·소식": "Instagram and news",
    "대표 사진, 투어명, 소개, 태그": "Main photo, tour name, introduction, tags",
    "고객 후기, 관련 투어": "Customer reviews, related tours",
    "관련 투어": "Related tours",
    "대표 사진, 가격, 운영 정보, 포함 사항": "Main photo, price, tour details, inclusions",
    "가격 정보": "Price",
    "운영 정보": "Tour details",
    "핵심 포함 사항 요약": "Key inclusions",
    "하이라이트": "Highlights",
    "포함·불포함 사항, 출발일, 예약 조건": "Inclusions and exclusions, departures, booking terms",
    "포함·불포함 사항": "Inclusions and exclusions",
    "운영 요일, 요금 기준": "Operating days, price basis",
    "출발일": "Departures",
    "예약 조건, FAQ": "Booking terms, FAQ",
    "일정": "Itinerary",
    "공통 항목": "Common items",
    "공통 ": "Common ",
    "국가별 소개": "Country introductions",
    "기본 정보": "Basic information",
    "대표 사례": "Featured story",
    "대표 사진, 국가명, 소개": "Main photo, country name, introduction",
    "대표 사진, 소개, 문의 버튼": "Main photo, introduction, inquiry button",
    "대표 사진, 소개": "Main photo, introduction",
    "데이 투어 상세": "Day tour detail",
    "두 국가 연계 여행": "Two-country journeys",
    "맞춤 여행 예시": "Custom trip examples",
    "모바일 All Tours": "Mobile All Tours",
    "모바일 Cafe": "Mobile Cafe",
    "모바일 Plan Your Trip": "Mobile Plan Your Trip",
    "모바일 객실": "Mobile Rooms",
    "모바일 상품 상세": "Mobile tour detail",
    "모바일 홈": "Mobile Home",
    "문의 유형 선택": "Inquiry type",
    "사례 목록": "Story list",
    "사무소와 연락처": "Offices and contacts",
    "상단 소개": "Introduction",
    "상품 상세": "Tour detail",
    "상품 카드 목록": "Tour card list",
    "서비스 구성": "Services",
    "가이드 소개, Our Impact, Stay with Envoy": "Guide, Our Impact, Stay with Envoy",
    "숙박 정보, 경로 지도": "Accommodation, route map",
    "여행 준비 정보": "Travel preparation",
    "선택 항목": "Optional items",
    "선택 · ": "Optional · ",
    "수치 지표": "Key figures",
    "여행 기본 정보": "Trip basics",
    "여행 문의": "Trip inquiry",
    "여행·숙박 연결": "Tours and stays",
    "예약 흐름 안내": "Booking process",
    "와이어프레임": "Wireframe",
    "유형별 추가 항목": "Additional fields by type",
    "일반 문의": "General inquiry",
    "제출 후 화면": "After submission",
    "조지아 투어": "Georgia tours",
    "주요 지역": "Key regions",
    "진행 방식": "How it works",
    "필터 영역": "Filters",
    "하단 고정 바": "Sticky bottom bar",
    "헤더·하단 버튼": "Header and bottom button",
    "예약 바: 노출": "Booking bar: shown",
    "예약 바: 미노출": "Booking bar: hidden",
    "소개": "Introduction",
    "문의": "Inquiry",
    "홈": "Home",
}
KEYS = sorted(T, key=len, reverse=True)
HANGUL = re.compile(r"[가-힣]")

def tr(s):
    for k in KEYS:
        s = s.replace(k, T[k])
    return s

def main():
    os.makedirs(OUT, exist_ok=True)
    bad = []
    for f in sorted(glob.glob(os.path.join(BASE, "*.html"))):
        s = open(f, encoding="utf-8").read()
        s = s.replace('lang="ko"', 'lang="en"').replace("../index.html", "../../index.html")
        s = tr(s)
        for m in re.findall(r"[^<>\"]*[가-힣][^<>\"]*", s):
            bad.append((os.path.basename(f), m.strip()))
        open(os.path.join(OUT, os.path.basename(f)), "w", encoding="utf-8").write(s)
    if bad:
        for b in bad: print("UNTRANSLATED", *b)
        raise SystemExit(1)
    print("ok", len(glob.glob(os.path.join(OUT, "*.html"))))

if __name__ == "__main__":
    main()
