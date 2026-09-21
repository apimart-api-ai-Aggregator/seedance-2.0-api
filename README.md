# Seedance 2.0 API (seedance-2.0)

<!-- conv-kit:v1 -->

<p align="center">
  <img src="assets/badges/price.svg" alt="observed unit price"> <img src="assets/badges/billing.svg" alt="billing model"> <img src="assets/badges/compat.svg" alt="OpenAI-compatible endpoint">
</p>

<p align="center">
  <img src="assets/01-product-ad-ceramic-mug-thumb.jpg" width="820" alt="Seedance 2.0 (seedance-2.0) output generated through APIMart">
</p>

> **from $0.066 per second** at 480P — one OpenAI-compatible endpoint at `https://api.apimart.ai/v1`, no monthly plan required. *(observed 2026-09-17)*

**[Get an API key](https://go.apimart.ai/k-2c05d3)** · **[Live pricing](https://go.apimart.ai/k-4f6960)** · **[Model page](https://go.apimart.ai/k-fdfd81)** · [⚡ 60-second quickstart](#quickstart)

**Why teams call Seedance 2.0 (`seedance-2.0`) through APIMart**

- **One key, entire catalog.** The same `https://api.apimart.ai/v1` base URL and `Authorization` header reach Seedance 2.0 (`seedance-2.0`) and 300+ other image, video and language models — switch the `model` field, not your client.
- **$1 minimum, pay as you go.** No subscription and no prepaid plan to size up front: top up from $1 and spend it on calls. There is no free quota to burn through first, so the price in this table is the price you pay.
- **The charge comes back in the response.** Every call reports the amount billed (`cost` / `credits_cost`), so a spend number is read per call instead of guessed at month end.
- **Async by design.** Submit, take the `task_id`, poll `GET /v1/tasks/{id}` — batching and retries are ordinary queue work, not a bespoke integration.

<!-- /conv-kit:v1 -->

Seedance 2.0 is a per-second video route on APIMart: text-to-video, first/last-frame, reference video and reference audio, 4–15 seconds per job, and cheaper `-mini` and `-fast` variants for volume.

## Model id and routes

| Route | `model` value | Billing | Notes |
| --- | --- | --- | --- |
| Per-image (default here) | `seedance-2.0` | per delivered image, by resolution | alias `seedance-2.0-fast / seedance-2.0-mini / seedance-2.0-face` is documented as equivalent |
| Token-billed official | `` | per million tokens | no `official_fallback` on this id |

Endpoint: `POST https://api.apimart.ai/v1/videos/generations` (OpenAI-compatible), then poll `GET /v1/tasks/{task_id}`.
Result links are valid for 24 hours.

## Pricing

<!-- pricing:model:start -->
| Output | List price | Effective price |
| --- | --- | --- |
| 1080P | $0.443 | $0.3544 |
| 1080P-input | $0.2696 | $0.2157 |
| 480P | $0.0825 | $0.066 |
| 480P-input | $0.05 | $0.04 |
| 4K | $0.9025 | $0.722 |
| 4K-input | $0.5554 | $0.4443 |
| 720P | $0.1775 | $0.142 |
| 720P-input | $0.1073 | $0.0858 |
<!-- pricing:model:end -->

Prices are a snapshot; the [pricing page](https://go.apimart.ai/k-4f6960) and [`data/model.json`](data/model.json) are refreshed by
CI, and a completed task reports the exact amount in its `cost` field.

## Request parameters

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `model` | string | required | `seedance-2.0`; also documented: `seedance-2.0-fast`, `seedance-2.0-mini`, `seedance-2.0-face` |
| `prompt` | string | required for text-to-video | subject, action, camera movement and style; optional when a first frame is supplied |
| `duration` | integer | `5` | 4–15 seconds; every second is billed |
| `size` | string | `16:9` | aspect ratio 0.5–2.5: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, plus adaptive ratios |
| `resolution` | string | `720p` | `480p`, `720p`, `1080p`, `4k` (1080p/4k only on this model, not on the variants) |
| `generate_audio` | boolean | `false` | adds AI-generated audio; billed the same per second |
| `seed` | integer | — | same seed + same request is similar, not guaranteed identical |
| `return_last_frame` | boolean | `false` | returns the last frame URL for chaining the next clip |
| `image_urls` | string[] | — | image-to-video references (URL or `asset://` id) |
| `image_with_roles` | array | — | explicit `first_frame` / `last_frame` / `reference_image` roles |
| `video_urls` | string[] | — | reference videos for motion or style transfer |
| `audio_urls` | string[] | — | reference audio for lip-sync or rhythm |
| `tools` | array | — | e.g. `[{"type": "web_search"}]` for retrieval-assisted generation |
| `nsfw_check` | boolean | `false` | runs `omni-moderation-latest` before submitting |

Supported aspect ratios: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9` and adaptive ratios.

## Quickstart

```bash
curl --request POST --url https://api.apimart.ai/v1/images/generations \
  --header "Authorization: Bearer $APIMART_API_KEY" --header 'Content-Type: application/json' \
  -d '{"model":"seedance-2.0","prompt":"A bamboo forest path under moonlight","size":"1:1","resolution":"1K","n":1}'
```

```python
import os, time, requests

BASE = "https://api.apimart.ai/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['APIMART_API_KEY']}", "Content-Type": "application/json"}

created = requests.post(f"{BASE}/images/generations", headers=HEADERS, timeout=60, json={
    "model": "seedance-2.0", "prompt": "A bamboo forest path under moonlight",
    "size": "1:1", "resolution": "1K", "n": 1,
}).json()
task_id = created["data"]["id"]

while True:
    task = requests.get(f"{BASE}/tasks/{task_id}", headers=HEADERS, timeout=60).json()["data"]
    if task["status"] in ("completed", "failed"):
        break
    time.sleep(5)
print(task.get("cost"), task.get("result", {}).get("images", [{}])[0].get("url"))
```

```javascript
const res = await fetch("https://api.apimart.ai/v1/images/generations", {
  method: "POST",
  headers: { Authorization: `Bearer ${process.env.APIMART_API_KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({ model: "seedance-2.0", prompt: "A bamboo forest path under moonlight",
                          size: "1:1", resolution: "1K", n: 1 }),
});
const { data } = await res.json();      // data.id is the task id — poll /v1/tasks/<id>
```

Runnable versions: [`examples/`](examples). The task lifecycle is `pending → processing → completed | failed`, and the
finished task carries `cost`, `credits_cost` and expiring result URLs.

## Sample outputs

Every render below came from a single call with the model id above, at the ratio shown; the cost column is what the task
reported.

| Preview | Recipe | Ratio | Duration | Cost | Prompt |
| --- | --- | --- | --- | --- | --- |
| <img src="assets/01-product-ad-ceramic-mug-thumb.jpg" width="220" alt="Seedance 2.0 video preview"><br>[watch mp4](assets/01-product-ad-ceramic-mug.mp4) | Product ad | 16:9 | 5s | $0.33 | `Product ad shot: a matte ceramic mug on a rotating stone pedestal, soft studio light with a slow parallax camera move, shallow depth of field, clean beige backdrop` |
| <img src="assets/02-cinematic-rainy-street-thumb.jpg" width="220" alt="Seedance 2.0 video preview"><br>[watch mp4](assets/02-cinematic-rainy-street.mp4) | Cinematic | 16:9 | 5s | $0.33 | `Cinematic tracking shot down a rainy city street at night, neon reflections on wet asphalt, a lone cyclist passes, camera dollies forward slowly, film grain` |
| <img src="assets/03-food-ad-steam-thumb.jpg" width="220" alt="Seedance 2.0 video preview"><br>[watch mp4](assets/03-food-ad-steam.mp4) | Food ad | 9:16 | 5s | $0.33 | `Vertical food ad: a bowl of ramen with rising steam, chopsticks lift noodles toward the camera, warm side light, slow push in, appetising colour grade` |
| <img src="assets/04-architecture-flythrough-thumb.jpg" width="220" alt="Seedance 2.0 video preview"><br>[watch mp4](assets/04-architecture-flythrough.mp4) | Architecture | 16:9 | 5s | $0.33 | `Slow drone flythrough of a minimalist concrete villa at golden hour, infinity pool reflecting the sky, camera glides forward, ultra sharp architectural detail` |

Recipes and measured costs are also in [`data/samples.json`](data/samples.json).

<!-- conv-kit:v1:fix -->
## First-call troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `401` / `invalid api key` | key missing, truncated, or a stray newline pasted into the header | Re-copy it from the console; the header is `Authorization: Bearer $APIMART_API_KEY` |
| balance / credit error | the account has no balance | Top up from $1 in the console — there is no free quota to fall back on |
| `429` | concurrent requests on one key | Back off, then retry the same request with the same `Idempotency-Key` |
| `400` / model not found | wrong route for the id: the per-unit alias needs its `version`, the official id must not send one | Copy the exact `model` value from the route table above |
| task ends `failed` | prompt rejected by the filter, or a reference image URL expired | Re-submit with a **new** `Idempotency-Key` and re-host the reference image |
| result URL stops working | result links expire | Download the file as soon as the task reports `completed` |
<!-- /conv-kit:v1:fix -->

## FAQ

**How much does a Seedance 2.0 video cost?**

It is billed per second of output, by resolution: the pricing table above lists the effective rate for each tier, so a 5-second 480P clip is simply rate × 5. The task response reports the exact `cost`.

**What is the difference between seedance-2.0, -fast, -mini and -face?**

`seedance-2.0` is the full model (1080p and 4k, audio, reference video/audio). `-fast` and `-mini` trade resolution and features for a much lower per-second rate, and `-face` targets human-face consistency at a higher rate.

**How do I control the first and last frame?**

Use `image_with_roles` with `role: first_frame` and/or `role: last_frame` instead of the plain `image_urls` array, which is treated as reference images.

**Can I extend an existing clip?**

Enable `return_last_frame` so the completed task also returns the final frame, then submit that frame as the first frame of the next job — the chaining approach this route is designed for.

## Related searches

- `seedance 2.0 api`
- `seedance api pricing`
- `seedance 2.0 api key`
- `text to video api`
- `image to video api`
- `ai video generation cost`
- `cheapest video generation api`

<!-- conv-kit:v1:cta -->
---

**Start with $1.** [Get an API key](https://go.apimart.ai/k-2c05d3) → [check live pricing](https://go.apimart.ai/k-4f6960) → [open Seedance 2.0 (`seedance-2.0`) in the model library](https://go.apimart.ai/k-fdfd81). The first call is three steps: submit, poll `task_id`, read the charged amount off the response.
<!-- /conv-kit:v1:cta -->

## Attributed links (how this repository is measured)

| Purpose | Attributed link | Target |
| --- | --- | --- |
| Open Seedance 2.0 on APIMart | <https://go.apimart.ai/k-fdfd81> | `docs.apimart.ai` model page |
| Current pricing page | <https://go.apimart.ai/k-4f6960> | `apimart.ai/pricing` |
| Get an API key | <https://go.apimart.ai/k-2c05d3> | `apimart.ai/keys` |

Outbound APIMart links are minted through the promo link API; hand-made tracking parameters are rejected by
`tools/check_links.py` in CI.

## Disclosure

Seedance 2.0 is a third-party model served through APIMart; this repository documents how to call it and publishes
real outputs, model ids and prices, and does not claim official status. Model names, prices and documentation belong to
their respective owners. Endpoint reference: [https://docs.apimart.ai/en/api-reference/videos/seedance-2-0/generation](https://docs.apimart.ai/en/api-reference/videos/seedance-2-0/generation).

## Repository map

```text
README.md             model id, pricing, parameters, quickstart, samples, FAQ
data/model.json       the pricing record for this model (CI-refreshed)
data/samples.json     prompt recipes with measured cost
tools/snapshot.py     refresh this model's prices from the public pricing payload
tools/check_links.py  attribution guard
examples/             curl, Python and JavaScript clients
assets/               real sample renders (JPEG, resized for the README)
.github/workflows/    daily price refresh + validation
```

## License

MIT — see [LICENSE](LICENSE).
