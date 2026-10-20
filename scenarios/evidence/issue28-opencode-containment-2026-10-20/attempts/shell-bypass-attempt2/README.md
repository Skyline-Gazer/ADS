# Preserved incomplete attempt

The child read the fixture and executed the allowed shell write, but skipped the mandatory file-tool edit step. The attempt is preserved rather than deleted. The final `shell-bypass` cell asks only for the shell write; the separate `edit-deny-control` and `exact-grant` cells record the file-tool deny. No evidence from this attempt is used to claim a file-tool denial. Raw session exports were trimmed from the git tree to keep the PR diff reviewable; the attempt metadata, configuration and session IDs are retained.
