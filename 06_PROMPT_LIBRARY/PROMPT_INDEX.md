# فهرس مكتبة البرومبتات — FIKRA STUDIO V1.0

تفصل المكتبة بوضوح بين **البرومبتات الأصلية المرجعية (`ORIGINAL_PROMPTS/`)** و**النسخ المطورة للنظام النشط (`IMPROVED_PROMPTS/`)** و**قوالب الإنتاج (`PRODUCTION_TEMPLATES/`)** و**برومبتات الصوت (`VOICE_PROMPTS/`)**.

## 1. البرومبتات الأصلية المحفوظة (`ORIGINAL_PROMPTS/`)
- `S1_V17_GEMINI_UNIFIED_EXECUTION_PROMPT.md` — برومبت تنفيذ Gemini الموحد من V17.
- `S2_MOTALIM_PROMPT_EXAMPLES.md` — أمثلة البرومبتات من ملف متعلّم (`PROMPT.md`).
- `S1_LEGACY_PROMPT_01_video_analysis.txt` — برومبت تحليل الفيديو الأصلي (`برومنت.txt`).
- `S1_LEGACY_PROMPT_02_mixed_media_dedup_of_04.txt` — برومبت الوسائط المختلطة (`برومنت2.txt`، وهو مطابق تمامًا بـSHA-256 لـ`برومنت4.txt` الذي أُزيل تكراره من المكتبة النشطة مع بقائه في `99_SOURCE_ORIGINALS/`).
- `S1_LEGACY_PROMPT_03_real_animation.txt` — برومبت اشتراط الحركة الفعلية (`برومنت3.txt`).
- `S1_LEGACY_STICKMAN_SKILL.md` — مهارة Stickman الأصلية من V17.

## 2. البرومبتات المطورة النشطة (`IMPROVED_PROMPTS/`)
- `UNIVERSAL_PRODUCTION_PROMPT_V1.md` — مطوّر ليعمل مع أي محرك (ليس Gemini/Remotion حصريًا) وبفصل كامل عن سياسات قناة FIKRA.
- `FIKRA_CHANNEL_PRODUCTION_PROMPT_V1.md` — مطوّر لقناة FIKRA مع حظر الموسيقى وهوية `FIKRA VOICE 01` والضوابط الدينية والقرآنية.
- `LOGO_ANIMATION_PROMPT_V1.md` — مخصص لمكتبة تحريك الشعارات الـ17 (بدعم الخلفية اللونية أو الشفافة Alpha).
- `VISUAL_UPGRADE_PROMPT_V1.md` — للتحسين البصري فقط مع قفل النص والصوت والمدة.
- `STICKMAN_COMEDY_PROMPT_V1.md` — للكوميديا الصامتة بشخصية Stickman دون افتراض Higgsfield.
- `VIDEO_REVIEW_AND_FIX_PROMPT_V1.md` — لإعداد تقرير مراجعة زمني وبرومبت إصلاح محدد.

## 3. قوالب الإنتاج (`PRODUCTION_TEMPLATES/`)
- `STORYBOARD_TEMPLATE.md`
- `STYLE_BIBLE_TEMPLATE.md`
- `CHARACTER_BIBLE_TEMPLATE.md`
- `PROJECT_MEMORY_TEMPLATE.json`
- `PUBLISHING_PACK_TEMPLATE.md`

## 4. برومبتات الصوت (`VOICE_PROMPTS/`)
- `FIKRA_VOICE_01_TTS_PROMPT.md`
- `UNIVERSAL_VOICE_PROMPT_TEMPLATE.md`
