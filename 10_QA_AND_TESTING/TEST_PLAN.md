# خطة الاختبارات — TEST PLAN (FIKRA STUDIO V1.0)

تحدد هذه الخطة الاختبارات الـ18 الواجب تقييمها قبل تسليم `FIKRA_STUDIO_V1.0_COMPLETE_ARCHIVE.zip`:
- **QA-01 Structural:** التحقق من وجود جميع المجلدات والملفات الجوهرية (`00_` إلى `11_` + `99_`).
- **QA-02 Duplicate:** التحقق من كشف التكرارات بالبصمة الرقمية `SHA-256` وتسجيلها دون حذف النسخ الأصلية من `99_SOURCE_ORIGINALS/`.
- **QA-03 Conflict:** التحقق من فصل `UNIVERSAL_VIDEO_MODE` عن `FIKRA_CHANNEL_MODE` وتوثيق سياسة فض التعارض.
- **QA-04 Dependency:** فحص الأدوات المتوفرة في البيئة (`python3`, `ffmpeg`, `ffprobe`, `node`, `npm`) وتسجيل الاعتماديات الخارجية.
- **QA-05 Archive Integrity:** اختبار فتح وفحص سلامة `FIKRA_STUDIO_V1.0_COMPLETE_ARCHIVE.zip` عبر `zipfile.testzip()`.
- **QA-06 Asset Presence:** التحقق من وجود جميع الـ52 فيديو أصلي والـ32 مواصفة ستايل والـ17 مواصفة شعار والنسختين الأصليتين غير المعدّلتين.
- **QA-07 Metadata:** التحقق من صحة `STYLE_REGISTRY.csv`, `LOGO_REGISTRY.csv`, `ALL_52_VIDEOS_TECHNICAL_METADATA.json`, `ASSET_INDEX.csv`, `HASH_MANIFEST.csv`.
- **QA-08 Reference Link:** التحقق من صحة المسارات الداخلية المشار إليها في الفهارس وسجلات الأصول.
- **QA-09 Prompt Consistency:** التحقق من فصل البرومبتات الأصلية عن المطوّرة وعدم تسرب حظر الموسيقى إلى الوضع العام.
- **QA-10 Workflow:** التحقق من اكتمال مراحل الوضع العام (11) وقناة FIKRA (12) والأوضاع المساعدة (7).
- **QA-11 Code Tests:** فحص الصياغة النحوية (`py_compile`) لجميع سكريبتات Python المرفقة في الأرشيف.
- **QA-12 Build Tests:** اختبار بناء Remotion (`npm install` / `tsc`) — يخضع لتوفر الإنترنت والاعتماديات.
- **QA-13 Render Tests:** رندر فيديو فعلي جديد — يخضع لتوفر بيئة Remotion مثبتة وطلب إنتاج فيديو.
- **QA-14 Visual Tests:** الفحص البصري للقطات الفيديوهات الـ14 غير المفهرسة في المصدر 01 عبر لوحات المعاينة.
- **QA-15 Audio Tests:** الاستماع والتفريغ الصوتي للمسارات الصوتية داخل الفيديوهات الـ52.
- **QA-16 Synchronization Tests:** اختبار مزامنة صوت وصورة لفيديو منتج جديد.
- **QA-17 Export Tests:** اختبار تصدير فيديو منتج جديد.
- **QA-18 Final Delivery Tests:** التحقق النهائي من وجود حزمة ZIP النهائية، سلامتها، تطابق بصمات المصدرين الأصليين، واكتمال التقرير.
