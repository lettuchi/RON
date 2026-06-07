import json, os, sys, traceback
from urllib import request, error
sys.path.insert(0, os.path.dirname(__file__))
import generate_voice as gv

gv.load_env_file(gv.ENV_FILE)
key = os.environ["ELEVENLABS_API_KEY"].strip()

def raw_tts(voice_id, text="This is a pipeline test."):
    url = f"{gv.API_BASE}/v1/text-to-speech/{voice_id}"
    body = json.dumps({"text": text, "model_id": gv.DEFAULT_MODEL}).encode()
    req = request.Request(url, data=body, method="POST", headers={
        "xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    try:
        with request.urlopen(req, timeout=120) as r:
            data = r.read()
            return (r.status, f"{len(data)} bytes audio")
    except error.HTTPError as e:
        return (e.code, e.read().decode("utf-8", "replace"))

# Premade voice (Sarah) — should be allowed on free plan
print("RAW premade (Sarah):", raw_tts("EXAVITQu4vr4xnSDxMaL"))
# Library voice (Carla / Toa)
print("RAW library (Carla/Toa):", raw_tts("l32B8XDoylOsZKiSdfhE"))

# Verify gv.synthesize works (catch full traceback to surface any bug)
try:
    audio = gv.synthesize("Pipeline test via synthesize.", "EXAVITQu4vr4xnSDxMaL",
                          gv.DEFAULT_MODEL, key)
    print(f"gv.synthesize premade OK: {len(audio)} bytes")
except Exception:
    print("gv.synthesize premade raised:")
    traceback.print_exc()
