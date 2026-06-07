# Ren'Py CI and local lint

GitHub Actions runs **Ren'Py 8.5.3** script lint on every push and pull request to `main` / `master`.

## Workflow

- **File:** `.github/workflows/renpy-lint.yml`
- **Action:** [remarkablegames/setup-renpy](https://github.com/remarkablegames/setup-renpy) (`cli-version: "8.5.3"`)
- **Command:** `renpy-cli . lint --error-code` (fails the job if lint reports errors)

This matches the project SDK at `renpy-8.5.3-sdk` locally; the workflow downloads the same version in CI (no need to commit the SDK).

## Run lint locally (Windows)

From the repo root:

```bat
_run_lint.bat
```

That invokes:

```text
"C:\Users\Amanda\Developer\renpy-sdk\renpy-8.5.3-sdk\renpy.exe" "C:\Users\Amanda\Developer\ryoko-owari" lint ... --error-code
```

Adjust the SDK path if your Ren'Py install lives elsewhere.

## Run lint locally (Ren'Py CLI)

If `renpy-cli` is on your PATH (from the SDK or [setup-renpy](https://github.com/remarkablegames/setup-renpy)):

```bash
cd /path/to/ryoko-owari
renpy-cli . lint --error-code
```

## Optional next steps (not enabled yet)

- Headless screenshot tests: `renpy-cli . test screenshot_capture` with `SDL_AUDIODRIVER=dummy` and `SDL_VIDEODRIVER=dummy` (see `docs/renpy-plugins-research.md`).
- Release builds: [renpy-build-action](https://github.com/ProjectAliceDev/renpy-build-action) after lint CI is stable.
