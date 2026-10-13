# Selection record — 2026-10-13 (Asia/Shanghai)

Hypothesis: support teams that maintain saved replies after policy changes may value a local, review-first candidate queue. No user adoption, accuracy, time-saving or market-size claim is verified.

## Direct user voices

1. [r/CustomerService original question and replies](https://www.reddit.com/r/CustomerService/comments/1t12r0s/do_you_keep_your_old_macros_around_or_rewrite/), 2026-05-01/02. One manager inherited two years of mismatched macros; another describes six years of macros where old ones rot; a Gorgias user says a big policy change triggers manual review of every related macro. Three distinct users, one channel. Supports recurring maintenance friction; cannot prove a local CLI is desirable.
2. [Intercom knowledge-manager discussion](https://community.intercom.com/knowledge-base-6/how-do-you-keep-your-faq-and-knowledge-base-accurate-releases-after-releases-7754), 2024-09-11 with follow-ups into 2026. An Intercom knowledge manager says product changes require updating articles, internal content, macros and snippets; another participant says their CX team has little bandwidth or ownership. Independent channel and cross-time signal; Intercom is also a vendor and has commercial interest, so it does not establish neutral market size.

The demand evidence spans 2024–2026. [Zendesk's April 2026 macro content recommendations](https://support.zendesk.com/hc/en-us/articles/10621284039962-Announcing-macro-content-suggestions-and-trust-safety-recommendations) is an attention/product investment signal, **not** user-demand proof or a forecast for this repository.

## Existing choices and counterevidence

- Zendesk Copilot's [macro recommendations](https://support.zendesk.com/hc/en-us/articles/10621284039962-Announcing-macro-content-suggestions-and-trust-safety-recommendations) use ticket history, link to supporting tickets, and are integrated. They may already be sufficient for Zendesk customers with the add-on; access and price depend on their plan.
- [Policy Change Briefing Agent](https://completeaitraining.com/ai-agents/agent/policy-change-briefing/) describes finding stale macros plus full communication and quiz workflow. The page is a product/prompt listing, not independent evidence its claimed example outcomes were measured. It overlaps the core idea and is broader than this MVP.
- [Pythia's macro reporting](https://community.zendesk.com/admin-center-29/tip-how-to-optimise-your-macros-usage-in-zendesk-10213?fid=29&tid=10213) supports usage and export; basic spreadsheet search or manual review may outperform this prototype for small macro libraries.

Differentiation to test: no helpdesk connection, no sending or rewrite, local model plus exact old-only value cue, and a report with clause/macro IDs from *explicit exports*. This is potentially useful when a team cannot or does not want to use a vendor-specific integrated system. It is not a claim of market vacancy.

## Product contract

- Value: reduce manual searching for saved replies potentially affected by a changed policy clause, without making a policy decision.
- User task: export old/new stable-ID clauses and macros, run the CLI, inspect candidates and update approved macros in the source platform manually.
- Non-goals: pull from Zendesk/Intercom, auto-edit, legal advice, correctness guarantee, customer-message sending, multilingual guarantee.
- Acceptance: fresh Python 3.11+ environment installs; real local embedding model finds the synthetic outdated refund macro; unchanged policy skips inference; bad input fails clearly; tests/build and offline model rerun pass.
- Next validation: ask two support managers for sanitized old/new policy clauses plus actual macro exports; collect their prior manual stale-macro labels before running the tool, then measure false negatives, false positives and review time. This has not happened.

Product framing, not copied code: [Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins) suggested an explicit input-to-review artifact; [Agency Agents](https://github.com/msitarzewski/agency-agents) suggested competitor and reality-check perspectives; today's newly examined [local-first-customer-support-agent](https://github.com/hofri/local-first-customer-support-agent) (MIT) separates local evidence from escalation and frankly labels mock tests as not proving answer quality, reinforcing this MVP's local, review-only boundary. These are three independent repositories; none proves customer demand. No role prompts or source code were copied.
