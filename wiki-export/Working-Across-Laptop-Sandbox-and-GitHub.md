# Working Across Laptop, Sandbox, and GitHub

This repo can exist in three places at once: a laptop clone, a cloud Claude Code sandbox (spun up when
working in a browser/remote session rather than a terminal), and GitHub. Understanding how those three
actually relate to each other avoids a class of confusing bugs where "I just did this" doesn't show up
somewhere it's expected to.

## GitHub is the only bridge

A sandbox never sees a laptop directly, and a laptop never sees a sandbox directly. The only thing
either of them can see is GitHub. A sandbox gets code by cloning or pulling from GitHub; a laptop gets
a sandbox's work the same way, by pulling.

## New sandbox vs. a sandbox that's already running

A **brand-new** sandbox session clones fresh from GitHub the moment its container starts, so it
automatically has whatever was most recently pushed — no extra step. A sandbox that's **already
running**, though, doesn't notice anything pushed after it started; it needs an explicit `git pull` to
catch up, the same as any other long-lived git checkout.

## Uncommitted work is invisible, no matter how recent

Nothing that hasn't been pushed exists on the bridge. A local edit sitting uncommitted, or committed
but not pushed, is exactly as invisible to a sandbox as if it had never been made.

## The sync script

`scripts/sync.sh` commits anything uncommitted (with an automatic timestamped message), pulls with a
rebase so it never creates a messy merge commit, and pushes — safely: it never force-pushes and never
discards work, and if it can't fast-forward cleanly it stops rather than guessing. Run it manually, or
put it on a laptop cron/launchd schedule (see `README.md` for the exact line) as a safety net. The
actual discipline that matters more than the timer: push right after any meaningful unit of work, and
always as the last thing before ending a working session, so GitHub is guaranteed current the moment
you walk away.

## The one deliberate exception

`config.local.yaml` — the file holding real secrets (`ADS_AGENT_API_KEY`, the read-only database
connection string) — is gitignored on purpose and will never sync anywhere via git. A fresh clone,
anywhere, has neither value until someone puts them there by hand. This is not an oversight in the sync
process; it's the point of keeping secrets out of git in the first place.

## Creative files sync the same way

Images and video under `creatives/` are just files in the repo — committed, pushed, and pulled exactly
like everything else. GitHub has a 100MB-per-file limit on a normal push, which typical short vertical
ad creative is nowhere near. If the creative library eventually grows large or video-heavy enough that
cloning starts feeling slow, Git LFS is the standard next step — not something to set up ahead of an
actual need.
