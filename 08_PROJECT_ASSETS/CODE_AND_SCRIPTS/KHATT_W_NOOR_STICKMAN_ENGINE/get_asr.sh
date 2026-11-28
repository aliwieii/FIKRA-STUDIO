#!/bin/bash
# bash get_asr.sh  -> /tmp/asr/small (Whisper small, CTranslate2 int8) + faster-whisper. ~250 MB, ~1 min. Idempotent.
set -e
D=/tmp/asr; [ -f $D/small/model.bin ] && python3 -c "import faster_whisper" 2>/dev/null && { echo "asr ready"; exit 0; }
pip install -q faster-whisper --break-system-packages 2>&1 | grep -v -i warning || true
mkdir -p $D/pkg $D/small && cd $D/pkg
for p in 0 1 2 3; do [ -f skillninja-shortmovie-telop-model-p$p-1.0.0.tgz ] || npm pack @skillninja/shortmovie-telop-model-p$p@1.0.0 --silent >/dev/null; done
for p in 0 1 2 3; do mkdir -p x$p && tar xzf skillninja-shortmovie-telop-model-p$p-1.0.0.tgz -C x$p; done
cat x0/package/model.bin.part0 x1/package/model.bin.part1 x2/package/model.bin.part2 x3/package/model.bin.part3 > $D/small/model.bin
cp x0/package/{config.json,tokenizer.json,vocabulary.json,preprocessor_config.json} $D/small/
echo "ca732cb1379efc49417d028465f543d83a39de2c61f3027678de103dc404ce73  $D/small/model.bin" | sha256sum -c - || { rm -f $D/small/model.bin; echo "HASH MISMATCH - not using it"; exit 1; }
echo "asr ready"
