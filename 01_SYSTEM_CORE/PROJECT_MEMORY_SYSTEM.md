# PROJECT MEMORY & VISUAL CONTINUITY SYSTEM

## 1. هيكل ذاكرة المشروع (`PROJECT_MEMORY`)
يُحتفظ لكل مشروع نشط بسجل حالة منظم (انظر القالب الجاهز في `06_PROMPT_LIBRARY/PRODUCTION_TEMPLATES/PROJECT_MEMORY_TEMPLATE.json`) يضم:
- `project_id`: معرف فريد ثابت (مثال: `PRJ-2026-001`).
- `mode`: وضع التشغيل النشط (`UNIVERSAL_VIDEO_MODE`, `FIKRA_CHANNEL_MODE`, إلخ).
- `topic`: الموضوع والهدف والجمهور والأبعاد والمدة.
- `current_stage`: المرحلة الحالية المؤكدة.
- `approved_decisions`: قائمة العناصر المقفلة (الفكرة، السيناريو، النص الصوتي، الصوت، الستايل، الشخصيات، المشاهد، المواصفات).
- `references_used`: المراجع من الأرشيف (IDs الستايلات والفيديوهات).
- `assets`: الأصول المرفقة أو المستعملة.
- `prompts`: إصدارات برومبتات الصوت والإنتاج.
- `reviews_and_tests`: نتائج مراجعة الفيديو واختبارات الجودة.
- `revision_log`: سجل التعديلات المعتمدة.
- `remaining_tasks`: المهام المتبقية.

## 2. نظام الشخصيات والاتساق البصري (Visual Continuity Bibles)
عندما يتطلب المشروع استمرارية عبر مشاهد متعددة، يُنشأ حسب الحاجة:

### أ. Character Bible (لكل شخصية)
- `Character ID`
- `Character Sheet` (وصف مرجعي شامل)
- `Face` (ملامح الوجه، العينان، التعبيرات الأساسية)
- `Body Proportions` (نسبة الرأس للجسم، سُمك الخطوط، الأبعاد)
- `Clothing` (الملابس الثابتة)
- `Colors` (رموز الألوان الدقيقة Hex)
- `Accessories` (الملحق المميز الثابت)
- `Expressions` (حالات الانفعال المسموحة)
- `Movement Rules` (طبيعة المشي والإيماء والفيزياء)
- `Camera References` (الزوايا المعتمدة)

### ب. Asset / Object Bible (لكل عنصر متكرر)
- `Object ID`, `Geometry`, `Materials`, `Colors`, `Positioning Rules`, `Continuity Rules`.

### ج. Style Bible & Scene Bible
- تثبيت لوحة الألوان، الإضاءة، الخامات، الخطوط، لغة الكاميرا، إيقاع الانتقالات، وقواعد الخلفية لمنع أي تغير غير مقصود بين المشاهد.
