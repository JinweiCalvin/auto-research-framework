# Idea2Paper Integration Overlay

`idea2paper/frontend/server/app.py` is the local-workspace adapter used by this framework. It serves the project dashboard, routes workspace project/story endpoints, and keeps the Idea2Paper app available under `/idea2paper/`.

The overlay is based on the pinned Idea2Paper commit `64170d4d9ca9068b26bd561648ce5c576bf1a2fb`. `setup.sh` applies it only when the target file is clean. It refuses to overwrite a different local modification and is safe to rerun after the overlay has been applied.

The adapted source retains the Idea2Paper upstream license and attribution. When updating the pinned upstream commit, review and rebase this adapter before changing the pin.
