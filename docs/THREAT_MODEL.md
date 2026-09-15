# Threat model

| Threat | Control |
|---|---|
| Attacker submits arbitrary HTTPS evidence | Sources are derived from repository and path bound in the watch. |
| Mutable branch changes after submission | Only full 40-character commits are accepted. |
| Raw endpoint does not correspond to the commit tree | Commit identity, complete tree and Git blob SHA-1 are verified. |
| Truncated GitHub tree hides path conflicts | `truncated=true` fails closed. |
| Content changes in transit or supplied digest is false | Raw SHA-256 is recomputed inside validator execution. |
| Policy text injects instructions | Prompt declares evidence untrusted and output is schema/allowlist validated. |
| Model invents a crawler or path | Every affected entry must belong to the configured Cartesian product. |
| Empty restriction claim | Restriction/expansion without affected entries becomes `AMBIGUOUS_POLICY`. |
| Duplicate or retroactive history | Duplicate commits are rejected and parent links are assigned by contract state. |
| Reassessment creates multiple alerts | Each snapshot can be assessed once. |
| Unauthorized shutdown | Only the recorded watch creator may deactivate it. |
