# دليل التطوير المستقبلي — DEVELOPMENT GUIDE

لإضافة ميزات أو ستايلات أو مراجع جديدة دون كسر التوافق العكسي:
1. **المعرفات الثابتة (Stable IDs):**
   - ستايل جديد: يبدأ من `STY-033` في `03_STYLE_LIBRARY/STYLE_REGISTRY.csv` + ملف في `STYLE_SPECIFICATIONS/`.
   - حركة شعار جديدة: تبدأ من `L18` في `04_LOGO_ANIMATION_LIBRARY/LOGO_REGISTRY.csv`.
   - فيديو مرجعي جديد: يبدأ من `REF-023` (مع فحص `SHA-256` قبل الإضافة).
2. **مصدر وحيد للحقيقة (Single Source of Truth):** لا تنسخ القواعد في عدة ملفات؛ عدّلها في `01_SYSTEM_CORE/SYSTEM_RULES.md` وأحِل إليها.
3. **إدارة الإصدارات:** سجّل كل تعديل وسببه وأثره في `11_VERSIONING_AND_DOCUMENTATION/CHANGELOG.md`، وأعد تشغيل اختبارات `10_QA_AND_TESTING/` قبل إصدار نسخة جديدة.
