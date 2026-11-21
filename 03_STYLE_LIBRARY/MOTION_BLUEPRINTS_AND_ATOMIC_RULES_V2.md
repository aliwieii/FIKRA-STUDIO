# مخططات الحركة والقواعد الذرية — MOTION BLUEPRINTS V2.0

مبني على منهجية [hyperframes-animation](https://www.skills.sh/heygen-com/hyperframes/hyperframes-animation) (1.0M تثبيت) لرفع جودة الحركة في Remotion وHyperFrames:

## 1. القواعد الذرية للحركة (Atomic Motion Rules)
- **خصائص الـCompositor فقط:** حرّك `transform` (`translate`, `scale`, `rotate`) و`opacity` فقط؛ يُمنع تحريك `width` أو `height` أو `top` أو `left` لتجنب الاهتزاز وتباطؤ الرندر.
- **إيقاع موحّد للمشهد (Single-Voice Choreography):** كل مشهد يتبع 3 نبضات واضحة: `Entrance` (0.35s–0.55s) -> `Emphasis / Hold` (مرتبط بالكلمة المنطوقة) -> `Exit / Transition` (0.25s–0.40s).
- **الانتقالات بين المشاهد:** لا تترك قطعًا جافًا إلا في الكوميديا (`Stickman`)؛ في حلقات قناة فكرة استخدم Crossfade ضوئي، Wipe ناعم، أو Push-in مستمر.

## 2. مخططات المشاهد القياسية (Multi-Phase Scene Blueprints)
| المخطط | الاستخدام المثالي | منحنى التسارع | المدة |
|---|---|---|---|
| **Blueprint A — Cosmic Reveal** | الخطاف التأملي والعلمي | `Cubic Out` + Scale 1.00 -> 1.08 | 4–6 ثوانٍ |
| **Blueprint B — Kinetic Counter** | الأرقام والمقارنات الكونية | `Expo Out` مع تزامن صوتي | 3–5 ثوانٍ |
| **Blueprint C — Sacred Stillness** | الآيات القرآنية (ذهبي `#F59E0B`) | ثبات تأملي بطيء (صفر مؤثرات صاخبة) | طول التلاوة كاملًا |
| **Blueprint D — Brand Signature** | خاتمة `فِكْرَة` (`L08-LightSweep`) | `Spring(damping:14, stiffness:120)` | 4–5 ثوانٍ |
