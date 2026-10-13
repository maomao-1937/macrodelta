# MacroDelta

MacroDelta helps a support manager review **existing saved replies after a policy change**. Supply the previous and current policy clauses plus an export of your macros. A real local sentence-embedding model finds macros semantically related to changed clauses; a separate exact check highlights old-only numeric values. The report links each candidate to the old and new clause. It does not edit, approve, or send customer replies.

## Run the synthetic example

Requires Python 3.11+ and [`uv`](https://docs.astral.sh/uv/). The [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model downloads on first use; afterward inference is local. No paid API key is required.

```bash
uv sync --python 3.11 --extra test
uv run macrodelta examples/old-policy.json examples/new-policy.json examples/macros.json --out report.md --json-out report.json
uv run pytest -q
uv build
```

The synthetic example changes a refund window from 30 to 14 days. `refund-reply` still promises 30 days, so it should appear in `report.md`. The other macros are unrelated or reference an unchanged clause. The fixture demonstrates wiring, **not real-world precision or recall**.

## Input and review contract

All three inputs are JSON arrays of `{ "id": "stable-id", "text": "..." }`. Policy clauses must keep the same `id` between versions; deleting an old id is an error rather than a silent pass. Export the macros your agents actually use. The tool reads these files only and writes Markdown plus optional JSON. `--threshold` (default 0.42) changes the semantic *candidate retrieval* cutoff, not a safety threshold.

The text and IDs may contain customer-sensitive material. Use sanitized exports; do not commit real policy drafts, macros, customer tickets or credentials to a public repo. The program does not call a hosted AI API, but the model is downloaded on first use. Running on a separate machine or untrusted files should be reviewed by your organization.

Limits: up to 200 clauses per version, 500 macros, 8,000 characters per text. Only changed clauses are checked. A changed number occurring in a macro might be unrelated; a paraphrased outdated promise might be missed. The multilingual and legal/policy accuracy of the model is unmeasured. It cannot establish whether the new policy is valid or whether a customer is entitled to a refund. Review every finding and sample unflagged macros before updating anything.

## Design choice and alternatives

This is a narrow local, read-only *diff-to-macro review queue*. [Zendesk Copilot Recommendations](https://support.zendesk.com/hc/en-us/articles/10621284039962-Announcing-macro-content-suggestions-and-trust-safety-recommendations) proposes edits from ticket data inside Zendesk; [Policy Change Briefing Agent](https://completeaitraining.com/ai-agents/agent/policy-change-briefing/) sketches a broader connected rollout, briefing and quiz. MacroDelta instead accepts three explicit local exports, works before sending anything and leaves approval to a person. That is a workflow difference, not a claim of superior accuracy. See [RESEARCH.md](RESEARCH.md) for the original user evidence, counterevidence and validation plan.

Application code and synthetic examples are original MIT-licensed work. The model is Apache-2.0 and dependencies retain their own licenses. No competitor code, data or large prompts were copied.
