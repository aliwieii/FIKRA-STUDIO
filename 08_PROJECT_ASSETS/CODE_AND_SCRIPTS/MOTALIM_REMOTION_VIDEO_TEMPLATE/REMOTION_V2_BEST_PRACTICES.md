# REMOTION V2.0 ENGINEERING STANDARDS — FIKRA STUDIO V2.0

مستند مرجعي مبني على قواعد [remotion-best-practices](https://www.skills.sh/remotion-dev/skills/remotion-best-practices) ومكيَّف خصيصًا لمشاريع **FIKRA STUDIO V2.0**:

1. **التحريك الإطاري الحتمي (`useCurrentFrame()`):**
   - يُمنع استخدام CSS `transition` أو كلاسات تحريك Tailwind؛ كل حركة يجب أن تُحسب من `useCurrentFrame()` و`interpolate()` أو `spring()` لضمان مطابقة 100% عند الرندر.
2. **لا عشوائية غير حتمية:**
   - يُمنع استخدام `Math.random()` داخل مكونات المشاهد؛ استخدم دوال جيبية (`Math.sin`) أو بذورًا ثابتة (`random('seed')`).
3. **الخطوط العربية واتجاه RTL:**
   - استخدم دائمًا `src/utils/rtl.ts` لضبط `direction: 'rtl'` و`unicodeBidi: 'plaintext'` والهوامش الآمنة `SAFE_ZONE_9_16` لتطبيقات TikTok وYouTube Shorts وReels.
4. **مزامنة الكابشن والآيات القرآنية:**
   - استخدم `<ArabicCaptionOverlay mode="narrative" />` للنصوص السردية (أبيض) و`<ArabicCaptionOverlay mode="quran" />` للآيات القرآنية (ذهبي `#F59E0B` مع منع أي موسيقى أو مؤثرات فوق التلاوة).
5. **أمر الرندر الصريح:**
   - مرّر دائمًا معرّف الـComposition (`npx remotion render Main out/video.mp4`) وتحقق من الأنواع عبر `npm run typecheck` قبل الرندر.
