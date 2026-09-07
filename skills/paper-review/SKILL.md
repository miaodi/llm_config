---
name: paper-review
description: Review a research paper consistently, explaining its main contribution, results, assumptions, and lemma-to-theorem proof structure in accessible language, followed by a separately labelled critical assessment. Use for individual paper reviews and proof roadmaps, including papers in Zotero.
---

# Paper review

The reader is a technically capable student who wants help with mathematical analysis. Explain what an argument accomplishes before presenting its machinery. Be precise without assuming familiarity with functional analysis. Default to a substantive individual-paper review, not a literature survey.

## Sources and workflow

1. Identify the exact paper and version. Prefer Zotero MCP for library discovery, metadata, attachments, and full text. Confirm that an attached PDF actually matches the item; filenames and metadata can be wrong. Prefer the published version when available, recording any preprint differences that matter.
2. Read the full paper, including relevant appendices and supplementary proofs. Inspect rendered pages when extraction loses equations, theorem labels, plots, or table structure. An abstract-only review is explicitly provisional; do not invent results or proof dependencies to fill gaps.
3. Track evidence while reading: contribution claims, main results, assumptions, theorem/lemma labels, proof dependencies, experiments, and source locators. Keep this working record internal. In the finished review, place source locators beside the supported claims and in proof tables; do not append a standalone evidence ledger, extraction-file paths, or a processing log. State reading coverage and material verification limitations once in the reading-scope section. Distinguish PDF page numbers from printed pages.
4. Write the fixed structure below. Explain first, show only useful equations, then interpret them. Keep paper-derived summaries separate from the reviewer’s judgement and outside background. External reading may clarify prerequisites or verify comparisons; label and cite it separately rather than attributing it to the paper.
5. Audit scope, proof dependencies, equations, evidence, and source coverage before delivering. A summary is not an independent proof verification; do not claim to have verified correctness unless that work was actually done.

## Fixed review structure

Use these headings and order in every full review. Keep a heading with an honest “not applicable” or “not available” explanation when necessary. Scale detail to the paper rather than forcing identical length. Aim for an overview readable in two minutes, with deeper material below.

### 1. Paper identity and reading scope

Give title, authors, year, venue, DOI/URL, verified Zotero library/item key and item link when available, and the exact version reviewed. Record reviewed sections, access gaps, and review date. Use a verified citation key if available; never guess one. For saved Markdown, include compact YAML properties: type: paper-review, review_schema: 1, title, authors, year, doi, zotero_key, zotero_uri, citekey, reviewed_on, source_version, review_status, and topics. Leave unavailable values empty. Distinguish complete from provisional coverage.

### 2. Main contribution in plain language

Lead with the single most important contribution in one or two sentences. Explain the problem, the prior obstacle, what the authors introduce, and why it matters. List secondary contributions only when distinct. Say “the authors claim” for unverified novelty or priority assertions. Do not equate popularity or citation count with technical quality.

### 3. Main results and their scope

State what the paper actually establishes. Separate proved guarantees, numerical observations, and conjectures or interpretations. For the principal result give a plain-language statement, the mathematical statement when useful, essential assumptions, and what it does not imply. Explain the meaning of norms, rates, constants, parameter dependence, and asymptotic qualifiers. Do not conflate existence, uniqueness, stability, consistency, convergence, error rates, and solver convergence.

### 4. Method and mathematical setup

Explain the central idea, governing problem, unknowns, and how the proposed approach works. Define symbols when introduced, preferably with a small notation table when needed. Use $...$ and $$...$$ for math. Retain the paper’s notation or provide an explicit mapping to normalized notation. Distinguish modelling assumptions, discretization choices, and solver choices. Provide prerequisite intuition locally instead of sending the reader away to a textbook.

### 5. Analysis: what the authors are trying to prove

Start with the destination: “The authors want to establish X under assumptions Y; the main obstacle is Z.” Explain the proof strategy before individual lemmas.

For each theorem supporting the central conclusions, give a dependency table:

| Result (paper label and locator) | Plain-language meaning | Assumptions and earlier results used | Why this step is needed | Where it is used next |
|---|---|---|---|---|

Account for the lemmas and propositions on each main proof path; identify side results and auxiliary branches instead of forcing everything into a single chain. Use the paper’s actual labels. Explain what would be missing without a step. Trace dependencies from the proof text, not the order of presentation. Distinguish facts proved here from imported theorems and explicit assumptions.

Add a small Mermaid dependency graph when it clarifies the proof. An edge A --> B means B uses A; include assumptions and external results as labelled nodes. Use simple node text and explain equations outside the diagram. Mark inferred dependencies explicitly and do not portray an uncertain reconstruction as the authors’ argument.

Finish with a connected plain-language walkthrough from assumptions to the main conclusion. Explain technical terms at the point of use: for example, what coercivity prevents or what a compactness step allows. Preserve the mathematical qualifications when simplifying. If a proof is omitted, deferred, incomplete in the supplied material, or cannot be reliably reconstructed, state that precisely. For a paper without formal analysis, say so and explain its argument/evidence chain instead; never invent lemmas.

### 6. Experiments and supporting evidence

Explain which claim each important experiment tests, its setup and baselines, key outcomes with figure/table locators, and limitations of the evidence. Retain units, conditions, problem sizes, and hardware when reporting performance. Separate a theorem’s scope from the situations tested numerically. If no experiments are presented, state this without treating it as an automatic flaw.

### 7. Reviewer’s reflections: value, strengths, and limitations

Clearly label this section as the reviewer’s judgement. Evaluate the conceptual contribution, strength of evidence, assumptions versus intended use, computational/practical tradeoffs, reproducibility, and relevance to the reader’s research where known. Tie each material strength or concern to the paper. Separate author-acknowledged limitations, reviewer-inferred limitations, and unresolved questions. Do not invent a mandatory number of pros or cons or criticize a paper merely for not solving a different problem. Distinguish a possible concern from a demonstrated defect. Discuss historical value versus present usefulness only with adequate evidence. Give a calibrated recommendation about what is worth learning or reusing, without unsupported novelty or superiority claims.

### 8. Takeaways, questions, and connections

End with three to five memorable takeaways and focused questions for a second reading. Record meaningful connections to verified papers/concepts using typed relationships such as extends, uses, proves, compares-with, discretizes, or preconditions. Label reviewer-inferred relationships. For future graphs, a small table of source, relation, target, evidence locator, and status is sufficient; do not create empty concept notes just to populate a graph.

## Persistence and consistency

Deliver in chat or a Markdown file unless a destination is established. Do not guess the Obsidian vault location. Once an Obsidian destination is selected, keep the full review there and use a short Zotero child note with takeaways and a backlink when requested or covered by standing authorization. Preserve the user’s annotations and unrelated notes. Update the matching review by DOI or Zotero key rather than creating duplicates. Record meaningful source/version changes.

Consistency means the same questions, evidence distinctions, notation discipline, and heading order, not boilerplate or identical length. The review is incomplete if it omits the main contribution, the actual result and conditions, the proof/evidence roadmap, or the separately labelled assessment. Keep inaccessible material visibly marked instead of silently substituting speculation.
