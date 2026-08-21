# Creatives

Builds up incrementally (`SPEC.md` decision #11) — there's no attempt to backfill every creative
already running in Ads Manager on day one. This fills in over time via:

- `ad-intake` (mode 8) discoveries worth keeping as reference.
- A one-time manual export of whatever's live when this repo is stood up.
- New assets commissioned through `ad-setup-loop` (mode 5) briefs.

## Layout

```
creatives/
  <slug>/
    asset.<ext>        the actual image/video file
    brief.md           what it is, the hook/persona it's built for, source (commissioned / competitor
                        reference / exported from Ads Manager)
```

`<slug>` should be human-readable and referenced by `ad-agent propose --creative-ref creatives/<slug>`
so a campaign record and its creative are one lookup apart, not a name to remember.

## Before adding anything

Check it against `rules/compliance.md` first — a man's real unenhanced photo, unlabeled AI imagery, or
anything implying money/provider-energy as an attraction signal should never land here even as a
"reference," since it's one copy-paste away from shipping.
