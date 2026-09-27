# Git History Policy

The distributed v4.1.0 ZIP did not contain a `.git` directory. PersonaMetrica therefore does **not** fabricate an earlier commit history.

For v4.2.0, a new repository history starts from one explicit baseline commit:

`chore: import PersonaMetrica v4.1.0 release snapshot`

All Evidence Layer work after that point is committed incrementally as it is actually performed. Commit timestamps are the real creation timestamps in this build session; they are not backdated to simulate a longer development history.

Use `git log --oneline --decorate --graph` in the full v4.2.0 release to inspect the history. The anonymous submission bundle intentionally does not include `.git`.
