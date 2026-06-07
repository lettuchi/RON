# Meshy setup — image-to-3D for Toa & Kaoru

Meshy turns locked VN sprite PNGs into draft **GLB** meshes for Blender cleanup. This repo wires **Cursor MCP** (agent tools) and a **REST script** (batch download).

**Related:** [`docs/3d-character-spec-toa-kaoru.md`](3d-character-spec-toa-kaoru.md), [`docs/3d-pipeline-options-toa-kaoru.md`](3d-pipeline-options-toa-kaoru.md), [`scripts/3d_model_request_template.md`](../scripts/3d_model_request_template.md)

---

## 1. API key

1. Sign in at [meshy.ai](https://www.meshy.ai/) (API access may require a paid plan).
2. Create a key at [meshy.ai/settings/api](https://www.meshy.ai/settings/api) (`msy_…`).
3. Add to **`scripts/.env`** (copy from `scripts/.env.example`):

   ```env
   MESHY_API_KEY=msy_your_key_here
   ```

   Never commit `scripts/.env` or paste a live key into git.

---

## 2. Cursor MCP (Windows)

1. Copy [`.cursor/mcp.json.example`](../.cursor/mcp.json.example) to **`.cursor/mcp.json`** (or edit the existing file).
2. Set `MESHY_API_KEY` in `env` to your `msy_…` key **or** keep the key only in `scripts/.env` and duplicate it into `mcp.json` (Cursor does not read `scripts/.env` for MCP).
3. **Restart Cursor** fully.
4. **Settings → MCP** — enable the **meshy** server; wait until it shows connected.
5. In chat, ask the agent to **list Meshy tools** (e.g. `meshy_check_balance`, `meshy_image_to_3d`).

The Windows config uses `cmd /c npx` so `npx` resolves correctly on PATH.

---

## 3. REST script (no MCP)

From the project root:

```bash
python scripts/meshy_image_to_3d.py --check
python scripts/meshy_image_to_3d.py --dry-run --character toa
python scripts/meshy_image_to_3d.py --character kaoru
python scripts/meshy_image_to_3d.py --image game/images/sprites/toa/toa-neutral.png
```

- **`--check`** — `GET /openapi/v1/balance` only (no generation).
- Outputs go to **`assets/3d/raw/meshy-YYYY-MM-DD/`** (large GLBs are gitignored).
- Image-to-3D **consumes credits**; download GLBs promptly (Meshy URLs expire in a few days).

---

## 4. Workflow checklist

1. Run `--check` after adding the key.
2. Generate **Toa witness** and **Kaoru default** separately (`--character toa` / `kaoru`).
3. Import GLB in Blender; scale to **180 cm / 173 cm** per the character spec.
4. Use [`scripts/3d_model_request_template.md`](../scripts/3d_model_request_template.md) for prompts, negatives, and export naming.

---

## 5. Troubleshooting

| Issue | Fix |
|-------|-----|
| MCP server won’t start | Install Node.js; run `npx -y @meshy-ai/meshy-mcp-server` in a terminal to see errors |
| `401 Unauthorized` | Wrong or expired `MESHY_API_KEY` |
| `402 Payment Required` | Add credits on Meshy |
| Empty MCP tools | Restart Cursor; re-enable meshy in MCP settings |

Docs: [Meshy API](https://docs.meshy.ai/), [AI / MCP integration](https://docs.meshy.ai/en/api/ai).
