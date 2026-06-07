missing = []
for line in open("scripts/bad_end_voice_ids.txt", encoding="utf-8"):
    vid = line.strip()
    if not vid:
        continue
    import json
    perf = {e["id"] for e in json.load(open("scripts/voice_performance_manifest.json", encoding="utf-8"))["entries"]}
    if vid in perf:
        missing.append(vid)
# ids that failed before
failed = '''narrator_214 narrator_215 narrator_216 narrator_217 narrator_218 narrator_219 narrator_220 narrator_221 narrator_222 narrator_223 narrator_224 narrator_225 narrator_226 narrator_227 narrator_228 toa_202 toa_203 toa_204 toa_205 toa_206 toa_207 toa_208 toa_209 toa_210'''.split()
import json
perf = {e["id"] for e in json.load(open("scripts/voice_performance_manifest.json", encoding="utf-8"))["entries"]}
retry = [i for i in failed if i in perf]
open("scripts/bad_end_voice_retry.txt","w",encoding="utf-8").write("\n".join(retry)+"\n")
print("retry", len(retry), retry)
