"""Write #007 boards (template B) as .dc.html files matching the #003/#005 structure."""
import json, os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
TOTAL = 8
NUM = "#007"
SHORT = "التفكير العكسي"

def hl(word, pad=12):
    return ('<span style="position:relative;display:inline-block;isolation:isolate;padding:0 %dpx">'
            '<span style="position:absolute;left:-6px;right:-8px;top:26%%;bottom:4%%;background:#FFD93D;border-radius:10px 26px 8px 30px / 18px 8px 22px 10px;transform:rotate(-1.2deg);z-index:-1"></span>'
            '<span style="position:absolute;left:8px;right:-2px;top:44%%;bottom:10%%;background:#FFD93D;opacity:0.5;mix-blend-mode:multiply;border-radius:22px 8px 26px 6px / 10px 18px 8px 20px;transform:rotate(1deg);z-index:-1"></span>'
            '%s</span>') % (pad, word)

def ruqaa(text):
    return f'<div style="align-self:flex-start;font-family:\'Aref Ruqaa\',serif;font-size:58px;font-weight:700;color:#E0544A;line-height:1.2;transform:rotate(-3deg)">{text}</div>'

def x_mark(size=44, sw=5):
    return (f'<svg style="flex:none" width="{size}" height="{size}" viewBox="0 0 44 44" fill="none" stroke="#E0544A" stroke-width="{sw}" stroke-linecap="round" aria-hidden="true">'
            '<path d="M9 10 C 17 18, 26 26, 35 35"></path><path d="M34 9 C 27 17, 18 26, 10 35"></path></svg>')

def box(rot):
    return (f'<div style="flex:none;margin-top:12px;width:62px;height:62px;box-sizing:border-box;border:4px solid #16181D;'
            f'border-radius:6px 10px 5px 9px / 9px 5px 10px 6px;transform:rotate({rot}deg)"></div>')

def scribble(width, color="#62666F", seed=0):
    # a hand-written-looking wavy line standing in for words
    w = width
    d = f"M2 14 C {w*0.12:.0f} 4, {w*0.2:.0f} 22, {w*0.32:.0f} 12 S {w*0.5:.0f} 6, {w*0.62:.0f} 14 S {w*0.82:.0f} {20 if seed else 6}, {w-2} 11"
    return (f'<svg style="flex:none" width="{w}" height="26" viewBox="0 0 {w} 26" fill="none" stroke="{color}" stroke-width="4" '
            f'stroke-linecap="round" aria-hidden="true"><path d="{d}"></path></svg>')

def board(title, i, body, gap=48, header_label=SHORT, footer_next="←"):
    nxt = "" if footer_next is None else f'<span style="font-size:30px;font-weight:700;color:#16181D">{footer_next}</span>'
    counter = (f'<div style="display:flex;align-items:center;gap:16px"><span class="n" style="font-size:24px;color:#62666F">{i}/{TOTAL}</span>{nxt}</div>'
               if nxt else f'<span class="n" style="font-size:24px;color:#62666F">{i}/{TOTAL}</span>')
    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>{NUM} {title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;700&amp;family=Aref+Ruqaa:wght@400;700&amp;family=IBM+Plex+Mono:wght@400;500;600&amp;display=swap">
<style>
body{{margin:0}}
.n{{font-family:'IBM Plex Mono',monospace;direction:ltr;unicode-bidi:isolate}}
</style>
</helmet>
<div dir="rtl" style="width:1080px;height:1440px;box-sizing:border-box;position:relative;overflow:hidden;padding:88px 184px 80px 96px;display:flex;flex-direction:column;background-color:#FAFAF7;background-image:repeating-linear-gradient(180deg, rgba(250,250,247,0) 0px, rgba(250,250,247,0) 70px, #E5EAF1 70px, #E5EAF1 72px);font-family:'IBM Plex Sans Arabic',sans-serif;color:#16181D">
<div style="position:absolute;top:0;bottom:0;right:136px;width:3px;background:#E0544A"></div>
<div style="position:relative;display:flex;justify-content:space-between;align-items:center;height:44px">
<div style="display:flex;align-items:center;gap:18px"><span class="n" style="font-size:30px;font-weight:600;color:#16181D">{NUM}</span><span style="font-size:26px;font-weight:500;color:#62666F">{header_label}</span></div>
<div style="font-size:26px;font-weight:700;color:#62666F">دفتر محمود</div>
</div>
<div style="position:relative;flex:1;display:flex;flex-direction:column;justify-content:center;gap:{gap}px">
{body}
</div>
<div style="position:relative;display:flex;justify-content:space-between;align-items:center;height:40px">
<span class="n" style="font-size:24px;color:#62666F">@daftar.mahmoud</span>
{counter}
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1080,"height":1440}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
'''

boards = []

# 1 · Cover
cover = f'''<div style="font-size:96px;font-weight:700;line-height:1.3">أسرع طريق للنجاح:</div>
<div style="font-size:110px;font-weight:700;line-height:1.3;white-space:nowrap">اعرف كيف {hl("تفشل", 14)}.</div>
<div style="display:flex;justify-content:flex-end;padding-top:8px">
<div style="display:flex;align-items:flex-start;gap:10px;transform:rotate(-5deg)">
<span style="font-family:'Aref Ruqaa',serif;font-size:66px;font-weight:700;color:#E0544A;line-height:1.3">والطريقة؟</span>
<svg width="96" height="130" viewBox="0 0 96 130" fill="none" stroke="#E0544A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M78 14 C 44 30, 26 66, 34 116"></path><path d="M20 100 L34 118 L50 104"></path></svg>
</div>
</div>'''
boards.append(("Main.dc.html", "1 · الغلاف", "الغلاف", cover, 44, "نموذج ذهني · التفكير والقرارات", "اسحب ←"))

# 2 · Mirror
rows = "".join(
    f'<div style="display:flex;align-items:center;gap:26px"><div style="flex:none;width:44px;height:44px;box-sizing:border-box;border:3.5px solid #16181D;border-radius:6px 9px 5px 8px / 8px 5px 9px 6px;transform:rotate({r}deg)"></div>{scribble(w, "#62666F", s)}</div>'
    for r, w, s in [(-2, 470, 0), (1.5, 380, 1), (-1, 520, 0)])
mirror = f'''<div style="display:flex;flex-direction:column;gap:14px">
<div style="font-size:52px;font-weight:500;line-height:1.5">عندك مشروع أو امتحان أو هدف جديد.</div>
<div style="font-size:52px;font-weight:500;line-height:1.5;color:#62666F">تسأل: <span style="color:#16181D;font-weight:700">«كيف أنجح؟»</span></div>
</div>
<div style="position:relative;margin:0 10px;transform:rotate(-1.5deg)">
<div style="position:absolute;top:-24px;left:50%;margin-left:-84px;width:168px;height:46px;background:#E5EAF1;opacity:0.9;transform:rotate(4deg)"></div>
<div style="background:#FFFFFF;border:3px solid #16181D;border-radius:6px 14px 4px 12px / 12px 4px 14px 6px;padding:56px 52px 56px;box-shadow:8px 8px 0 #E5EAF1;display:flex;flex-direction:column;gap:30px">
<div style="font-size:70px;font-weight:700;line-height:1.35">خطة {hl("مثالية")}</div>
{rows}
</div>
</div>
<div style="font-size:52px;font-weight:500;line-height:1.5">وتتعثر بأشياء كانت واضحة من البداية.</div>
<div style="font-size:76px;font-weight:700;line-height:1.3">مألوف؟</div>'''
boards.append(("S2-Mirror.dc.html", "2 · المرآة", "المرآة", mirror, 52, SHORT, "←"))

# 3 · Idea
fail_list = "".join(
    f'<div style="display:flex;align-items:center;gap:20px">{x_mark(40, 5)}{scribble(w, "#16181D", s)}</div>'
    for w, s in [(250, 0), (200, 1), (230, 0)])
idea = f'''{ruqaa("الفكرة")}
<div style="font-size:84px;font-weight:700;line-height:1.3">اعكس السؤال.</div>
<div style="font-size:64px;font-weight:700;line-height:1.45">اكتب كيف {hl("تفشل")} بالتأكيد، ثم تجنّب ما كتبته.</div>
<div style="display:flex;flex-direction:column;gap:40px;padding-top:24px">
<div style="display:flex;align-items:center;gap:26px">
<div style="flex:none;width:250px;white-space:nowrap;font-size:42px;font-weight:700;line-height:1.3;color:#62666F">«كيف أنجح؟»</div>
<div style="font-size:50px;font-weight:700;color:#62666F">←</div>
<div style="position:relative;width:300px;height:150px">
<svg width="300" height="150" viewBox="0 0 300 150" fill="none" stroke="#62666F" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M58 112 C 22 114, 14 78, 42 66 C 34 34, 78 18, 104 38 C 118 12, 170 8, 186 36 C 214 18, 262 34, 252 70 C 288 80, 282 120, 244 118 C 226 136, 188 134, 172 120 C 150 138, 104 138, 92 118 C 80 124, 66 120, 58 112 Z"></path></svg>
<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:54px;font-weight:700;color:#62666F;padding-top:6px">؟؟</div>
</div>
</div>
<div style="height:3px;background:repeating-linear-gradient(90deg, #62666F 0px, #62666F 14px, rgba(0,0,0,0) 14px, rgba(0,0,0,0) 26px);opacity:0.45"></div>
<div style="display:flex;align-items:center;gap:26px">
<div style="flex:none;width:250px;white-space:nowrap;font-size:42px;font-weight:700;line-height:1.3">«كيف أفشل؟»</div>
<div style="font-size:50px;font-weight:700">←</div>
<div style="background:#FFFFFF;border:3px solid #16181D;border-radius:8px 14px 6px 12px / 12px 6px 14px 8px;box-shadow:6px 6px 0 #E5EAF1;padding:26px 30px;display:flex;flex-direction:column;gap:18px">{fail_list}</div>
</div>
</div>'''
boards.append(("S3-Idea.dc.html", "3 · الفكرة", "الفكرة", idea, 40, SHORT, "←"))

# 4 · Origin
origin = f'''{ruqaa("من أين؟")}
<div class="n" style="align-self:flex-start;font-size:112px;font-weight:600;line-height:1.1">1986</div>
<div style="font-size:54px;font-weight:500;line-height:1.55">طُلب من تشارلي منغر، شريك وارن بافت، كلمة تخرّج لطلاب مدرسة ثانوية.</div>
<div style="font-size:70px;font-weight:700;line-height:1.45">بدل وصفة النجاح، أعطاهم وصفة حياة {hl("بائسة")}.</div>
<div style="background:#FAFAF7;border:3px solid #62666F;border-radius:14px 6px 18px 8px / 8px 16px 6px 14px;padding:36px 44px;display:flex;flex-direction:column;gap:10px">
<div style="font-size:60px;font-weight:700;line-height:1.4">«اعكس، دائمًا اعكس»</div>
<div style="font-size:38px;font-weight:500;color:#62666F">— كارل ياكوبي</div>
</div>'''
boards.append(("S4-Origin.dc.html", "4 · الأصل", "الأصل", origin, 44, SHORT, "←"))

# 5 · Examples
def ex_card(tag, q, items, style):
    li = "".join(f'<div style="display:flex;align-items:center;gap:18px">{x_mark(38, 5)}<span style="font-size:42px;font-weight:500;line-height:1.4">{t}</span></div>' for t in items)
    return (f'<div style="{style};padding:30px 40px;display:flex;flex-direction:column;gap:14px">'
            f'<div style="display:flex;align-items:baseline;gap:18px"><span style="font-size:32px;font-weight:500;color:#62666F">{tag}</span><span style="font-size:52px;font-weight:700;line-height:1.35">{q}</span></div>{li}</div>')
c1 = ex_card("شغلك", "كيف أخسر عميلًا؟", ["أتأخر ولا أخبره.", "أبدأ بلا اتفاق واضح.", "أختفي بعد التسليم."],
             "background:#FAFAF7;border:3px solid #16181D;border-radius:14px 6px 18px 8px / 8px 16px 6px 14px")
c2 = ex_card("حياتك", "كيف أرسب؟", ["أذاكر ليلة الامتحان.", "الجوال بجانبي.", "أقرأ ولا أحل أسئلة."],
             "background:#FAFAF7;border:3px solid #16181D;border-radius:8px 16px 6px 14px / 14px 6px 18px 8px")
examples = f'''{ruqaa("مثالان")}
<div style="display:flex;flex-direction:column;gap:32px">
{c1}
{c2}
</div>
<div style="display:flex;align-items:center;gap:16px;font-size:62px;font-weight:700;line-height:1.45"><span>كل</span>{x_mark(52, 6)}<span>= شيء {hl("تمنعه")}.</span></div>'''
boards.append(("S5-Examples.dc.html", "5 · مثالان", "مثالان", examples, 44, SHORT, "←"))

# 6 · Try today
steps = [(-2, "اختر هدفًا واحدًا لهذا الأسبوع."),
         (1.5, 'اكتب <span class="n">5</span> طرق مؤكدة لإفشاله.'),
         (-1, 'حوّل كل طريقة إلى <span style="white-space:nowrap">«لن أفعل…».</span>' )]
step_html = "".join(f'<div style="display:flex;align-items:flex-start;gap:34px">{box(r)}<div style="font-size:56px;font-weight:700;line-height:1.45">{t}</div></div>' for r, t in steps)
try_today = f'''<div style="font-size:96px;font-weight:700;line-height:1.2">جرّبها {hl("اليوم")}</div>
<div style="display:flex;flex-direction:column;gap:52px">
{step_html}
</div>'''
boards.append(("S6-TryToday.dc.html", "6 · جرّبها اليوم", "جرّبها اليوم", try_today, 56, SHORT, "←"))

# 7 · Summary
check = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#62666F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5"></path></svg>'
qmark = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#62666F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8.5 8.8 C 8.6 5.6, 15.6 5.2, 15.4 9 C 15.3 11.6, 12 11.8, 12 14.6"></path><path d="M12 18.6v0.4"></path></svg>'
summary = f'''{ruqaa("الخلاصة")}
<div style="font-size:68px;font-weight:700;line-height:1.45">الخطة تخبرك بما تفعله. قائمة الفشل تخبرك بما {hl("تتجنبه")}.</div>
<div style="display:flex;flex-direction:column;gap:32px">
<div style="background:#FAFAF7;border:3px solid #16181D;border-radius:14px 6px 18px 8px / 8px 16px 6px 14px;padding:36px 44px;display:flex;flex-direction:column;gap:12px">
<div style="display:flex;align-items:center;gap:14px;font-size:34px;font-weight:500;color:#62666F">{check}ينفع</div>
<div style="font-size:47px;font-weight:700;line-height:1.45">قبل مشروع، أو امتحان، أو قرار كبير.</div>
</div>
<div style="background:#FAFAF7;border:3px solid #16181D;border-radius:8px 16px 6px 14px / 14px 6px 18px 8px;padding:36px 44px;display:flex;flex-direction:column;gap:12px">
<div style="display:flex;align-items:center;gap:14px;font-size:34px;font-weight:500;color:#62666F">{qmark}متى لا يكفي؟</div>
<div style="font-size:47px;font-weight:700;line-height:1.45">القائمة تمنع الأخطاء، ولا تصنع خطة.</div>
</div>
</div>'''
boards.append(("S7-Summary.dc.html", "7 · الخلاصة", "الخلاصة", summary, 48, SHORT, "←"))

# 8 · Source
source = f'''{ruqaa("المصدر")}
<div style="margin:0 8px;transform:rotate(1deg);background:#FFFFFF;border:3px solid #16181D;border-radius:6px 14px 4px 12px / 12px 4px 14px 6px;box-shadow:8px 8px 0 #E5EAF1;padding:48px 52px 52px">
<div dir="ltr" style="display:flex;flex-direction:column;gap:12px;text-align:left">
<div style="font-size:34px;font-weight:500;color:#62666F">Charlie Munger · <span class="n">2005</span></div>
<div style="font-size:68px;font-weight:700;line-height:1.15;color:#16181D">Poor Charlie's Almanack</div>
</div>
<div style="height:3px;background:#E0544A;margin:32px 0 28px"></div>
<div style="font-size:42px;font-weight:500;line-height:1.5">الحديث الأول: كلمة تخرّج <span class="n">1986</span></div>
<div dir="ltr" style="font-size:30px;font-weight:500;line-height:1.5;color:#62666F;text-align:left">Harvard School · Los Angeles</div>
</div>
<div style="display:flex;align-items:center;gap:34px;padding-top:12px">
<svg style="flex:none" width="92" height="92" viewBox="0 0 24 24" fill="none" stroke="#16181D" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h12v18l-6-4.5L6 21z"></path></svg>
<div style="font-size:64px;font-weight:700;line-height:1.45">{hl("احفظها")} قبل قرارك القادم.</div>
</div>
<div style="font-size:32px;font-weight:500;color:#62666F;padding-top:8px">دفتر محمود · فكرة واحدة. تطبيق اليوم.</div>'''
boards.append(("S8-Source.dc.html", "8 · المصدر", "المصدر", source, 56, SHORT, None))

canvas = {"v": 3, "attachments": {}, "boards": {}, "createdOnFiles": {"at": "2026-10-11T12:00:00Z", "v": 1},
          "designSystems": [], "launch": {"view": "canvas"},
          "notes": {"t1": {"kind": "title1", "maxW": 4560, "text": "#007 · التفكير العكسي · كاروسيل 1080×1440 · القالب B", "w": 240, "x": 0, "y": -300}},
          "order": [], "pages": [], "title": "#007 التفكير العكسي"}
for idx, (fname, ctitle, ttl, body, gap, label, nxt) in enumerate(boards, 1):
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(board(ttl, idx, body, gap, label, nxt))
    col, row = (idx - 1) % 4, (idx - 1) // 4
    canvas["boards"][fname] = {"h": 1440, "title": ctitle, "w": 1080, "x": col * 1160, "y": row * 1560}
    canvas["order"].append(fname)
json.dump(canvas, open(os.path.join(OUT, "canvas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", len(boards), "boards to", OUT)
