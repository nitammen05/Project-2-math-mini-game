Rules for programming:

1. Only write in Python  
2. Do not edit or delete original files  
3. The program should be runnable from a terminal  
4. The program should have tests after and during the implementation of every method, function, or function to make sure it runs properly  
5. Do not ask me any questions about how to implement the project, as long as it works, its good   
6. You may make your own REASONABLE decisions

Standing rules for every round (added after Round 2):

7. Never undo or amend a commit. Commit in small steps with messages that say what changed and why.
8. Spec.md is the one exception to rule 2: each round may append a "## Round <N>" section, but never change earlier text.
9. Number requirements R1, R2, ... across all rounds, and put the requirement ID in every test name (for example `test_R4_...`).
10. Run the whole test suite (`python3 -m unittest discover -s tests -t .`) before and after each change; earlier rounds' tests must keep passing.
11. Record at least one real decision per round in `docs/decisions/NNNN-title.md` (0001, 0002, ...) as a Y-statement.
12. Each round's handoff goes in `handoff-round-<N>.md`; the student reviews it and CLAUDE.md before they are committed.

Standing rules added after Round 3:

13. When a new test fails, read why before changing code: the test may be the thing that is wrong. Never change an earlier round's test to make new code pass.
14. Tests only check the HTML text, so check anything visual (layout, sprites, animations) by looking at it too, for example with a headless Chrome screenshot, and ask the student to try it in the browser.

Standing rule added after Round 4:

15. Every page contains the whole `<style>` block, and end screens also contain the hero picker. So a test that checks something is *absent* (a class name, an `<svg>`) must look inside the right part of the page (for example with `between(...)`), not the whole page.

Standing rule added after Round 5:

16. A headless screenshot with `--virtual-time-budget` can show the page before any animation has run, so don't trust it for timing. Check end states by freezing the elements (`animation-play-state: paused` with a negative `animation-delay`), and ask the student to watch the order and speed of animations in a real browser.
