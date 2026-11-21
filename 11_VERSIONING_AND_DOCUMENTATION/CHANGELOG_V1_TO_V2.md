# سجل التغييرات — CHANGELOG (V1.0 → V2.0)

**تاريخ الإصدار:** 2026-11-20

## أبرز الترقيات في FIKRA STUDIO V2.0
1. **مركز القيادة التفاعلي الموحّد (`00_START_HERE/FIKRA_STUDIO_V2_HUB.html`):**
   - لوحة تحكم عربية RTL تعمل دون إنترنت، تضم بحثًا فوريًا في الـ32 ستايلًا والـ17 حركة شعار، وموجّه أوضاع تفاعليًا (`FIKRA_CHANNEL_MODE` مقابل `UNIVERSAL_VIDEO_MODE`) مع نسخ فوري لبرومبتات البدء.
2. **ترقية قالب Remotion 4 + React 19 (`MOTALIM_REMOTION_VIDEO_TEMPLATE/`):**
   - إضافة إعدادات المقاسات القياسية (`VERTICAL_9_16` و`LANDSCAPE_16_9` و`SQUARE_1_1`).
   - إضافة مكونات جاهزة للإنتاج: `ArabicCaptionOverlay.tsx` (كابشن عربي متزامن مع دعم الوضع القرآني الذهبي)، `AudioSpectrumBar.tsx`، `FikraChannelOutro.tsx`، `rtl.ts`، ومشهد `SampleFikraHook.tsx`، مع دليل `REMOTION_V2_BEST_PRACTICES.md`.
3. **إضافة محرك إنتاج ثانٍ (`HYPERFRAMES_HTML_VIDEO_TEMPLATE/`):**
   - قالب فيديو عمودي 9:16 مبني على HTML5 + متغيرات JSON (`variables.json`) + تحكم إطاري حتمي (`seekToFrame`).
4. **تعبئة مجلد Storyboards وترقية Style Bible:**
   - إنشاء `FIKRA_VISUAL_STORYBOARD_V2_TEMPLATE.html` و`SAMPLE_STORYBOARD_WORKED_EXAMPLE.md` داخل `07_REFERENCE_MEDIA/STORYBOARDS/`.
   - ترقية `06_PROMPT_LIBRARY/PRODUCTION_TEMPLATES/STYLE_BIBLE_TEMPLATE.md` بمنهجية الفلسفة البصرية.
5. **إصلاحات الجودة والتدقيق (QA Fixes from V1.0 Audit):**
   - إزالة جميع مجلدات `__pycache__` وملفات `.pyc` (7 ملفات غير لازمة).
   - إصلاح جميع الروابط النسبية المعطوبة في `motalim_26_styles_gallery.html` و`motalim_17_logo_gallery.html` (أصبحت 0 روابط معطوبة).
   - إعادة توليد `ARCHIVE_INDEX.md` و`ASSET_INDEX.csv` و`HASH_MANIFEST.csv` آليًا بدقة 100% مع تقرير تدقيق `10_QA_AND_TESTING/V2_FORENSIC_QA_REPORT.md`.
