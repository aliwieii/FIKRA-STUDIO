# القيود والنواقص المعروفة — KNOWN LIMITATIONS

تُوثَّق هذه القيود بكل شفافية التزامًا بقواعد الصدق وعدم ادعاء اكتمال ما لم يكتمل:

1. **اختلاف رقم إصدار المصدر الأول:** أشار نص المهمة إلى «FIKRA AI STUDIO V18»، لكن الملف الفعلي المرفق هو **`FIKRA_AI_STUDIO_V17.zip`**، وقد بُني النظام عليه وحده دون افتراض أي ميزات من إصدار غير مرفق.
2. **التحليل الصوتي للفيديوهات (Audio Listening / STT):** تم فحص جميع الفيديوهات الـ52 تقنيًا عبر `ffprobe`، وتم فحص الـ14 فيديو غير المفهرسة في المصدر 01 بصريًا عبر لقطات موزعة، لكن لم يُجرَ استماع أو تفريغ صوتي (STT غير متوفر محليًا). لذا صُنفت بطاقات `REF-001`..`REF-022` بحالة `PARTIAL_SAMPLE_REVIEW`.
3. **اختبارات بناء ورندر Remotion (`Build` & `Render Tests`):** البيئة المعزولة (Sandbox) لا تملك اتصالًا بالإنترنت لتشغيل `npm install` وتنزيل حزم Remotion، لذا صُنفت اختبارات البناء والرندر بحالة `BLOCKED` / `NOT_APPLICABLE` ولم يُدّعَ تنفيذ رندر جديد.
4. **جاهزية الستايلات الـ32:** 10 ستايلات من مكتبة متعلّم لديها حزم مرجعية كاملة (`SPEC_READY`)، و16 ستايلًا من معرض `gallery/index.html` لديها أمثلة HTML/SVG حية دون فيديو MP4 مستقل (`CATALOG_ONLY` أو `REFERENCE_ONLY`)، و6 ستايلات موسّعة من V17 (`REFERENCE_ONLY` أو `CATALOG_ONLY`). فقط مكتبة تحريك الشعارات الـ17 تحمل حالة `RENDER_TESTED` استنادًا إلى فيديوهات وكود المصدر 02.
5. **غياب ملفات الصوت والخطوط المستقلة في المصدرين:** لا يحتوي أي من المصدرين على ملفات `.mp3`/`.wav` منفصلة ولا على ملفات خطوط `.ttf`/`.otf`؛ تم توثيق ذلك بوضوح في `07_REFERENCE_MEDIA/AUDIO/` و`08_PROJECT_ASSETS/FONTS_AND_RESOURCES/`.
6. **تفاوت قدرات منصات الذكاء الاصطناعي مستقبلًا:** عند رفع الأرشيف لاحقًا إلى ChatGPT أو Gemini، قد لا تستطيع المنصة مشاهدة الفيديوهات تلقائيًا دون أداة مخصصة؛ لذا وُضع بروتوكول واضح في `00_START_HERE/PROJECT_BOOTSTRAP_PROMPT_AR.md`.

## V3.6 Environment Boundaries
- Offline VM sandboxes without `node_modules` cannot run `tsc` or Playwright Chromium locally (`BLOCKED` locally, verified green in GitHub Actions `remotion-typecheck` matrix).
