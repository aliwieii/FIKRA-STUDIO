# نظام الجودة والاختبارات — STRICT QA SYSTEM

يميز هذا النظام بصرامة بين الفحص النظري والتنفيذ الفعلي، ويمنع الادعاء بأي اختبار لم يُنفَّذ.

## حالات الاختبار المعتمدة
- `PASS`: نُفّذ الاختبار فعليًا واجتاز المعيار بدليل موثق.
- `FAIL`: نُفّذ الاختبار وفشل؛ يتطلب إصلاحًا وإعادة اختبار.
- `BLOCKED`: تعذر التنفيذ بسبب قيد بيئي حقيقي (مثل غياب الإنترنت لتثبيت حزم Node، أو غياب محرك رندر/STT).
- `NOT_RUN`: لم يُنفّذ في هذه الدورة.
- `NOT_APPLICABLE`: لا ينطبق على نطاق البناء الحالي (مثل اختبار تصدير فيديو جديد عند بناء الأرشيف المرجعي فقط).

## فئات الاختبارات الثمانية عشر (18 Categories)
1. Structural Tests
2. Duplicate Tests
3. Conflict Tests
4. Dependency Tests
5. Archive Integrity Tests
6. Asset Presence Tests
7. Metadata Tests
8. Reference Link Tests
9. Prompt Consistency Tests
10. Workflow Tests
11. Code Tests
12. Build Tests
13. Render Tests
14. Visual Tests
15. Audio Tests
16. Synchronization Tests
17. Export Tests
18. Final Delivery Tests
