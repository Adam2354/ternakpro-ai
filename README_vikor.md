README - VIKOR weights & normalization

Overview
- This file documents how `services/vikor.py` normalizes criteria, what the weights mean, and the business rule boost applied when user modal is much larger than an alternative's modal.

Normalization & Criteria types
- Matrix columns (in order): `modal`, `biaya_per_ekor`, `lahan`, `waktu`, `pengalaman`.
- `modal` and `lahan` are treated as BENEFIT criteria: higher user capacity relative to the item's requirement increases the score (we compute `user_modal / item_modal` and `user_lahan / item_lahan`).
- `biaya_per_ekor` is treated as a COST: higher per-unit cost penalizes the alternative. It is normalized relative to user modal (`item_biaya / user_modal`).
- `waktu` and `pengalaman` are handled as requirement ratios (cost-like): `item_value / user_value`.

Business boost rule
- If the user's modal is far larger than an item's modal (capacity_ratio >= 10), the `modal` score receives a modest boost based on `log10(capacity_ratio)`. This encourages recommending larger-scale livestock when the user clearly has ample capital.
- Boost formula (in code):
  - `boost = min(log10(capacity_ratio)/2.0, 1.0)`
  - `modal_score *= (1.0 + 0.5 * boost)`
  - Examples: 10× -> boost 0.5 -> modal_score scaled by 1.25; 100× -> boost 1.0 -> modal_score scaled by 1.5.

Preset weights
- Presets are arrays matching the matrix column order: `[modal, biaya_per_ekor, lahan, waktu, pengalaman]`.
- Current presets in `services/vikor.py`:
  - `pemula`: [0.35, 0.15, 0.25, 0.15, 0.10]
  - `menengah`: [0.55, 0.05, 0.25, 0.05, 0.10]  <-- tuned to prefer medium-scale livestock (e.g., Kambing)
  - `besar`: [0.50, 0.05, 0.25, 0.10, 0.10]

Notes & tuning suggestions
- Feasibility: the algorithm still enforces feasibility rules (user must meet minimum modal, lahan, waktu, pengalaman, and an estimated headcount) — an alternative that is infeasible will be deprioritized regardless of Q.
- If you want `Kambing` to appear for `menengah` users, ensure user experience (`pengalaman`) and `waktu` meet the item's minimums (Kambing requires `pengalaman >= 3`, `waktu >= 3` in the data). Otherwise increase `menengah` preset weight further or relax feasibility checks (not recommended).
- To prioritize different livestock, tune the `menengah` preset weights or adjust the business-boost threshold/scale.

Where to change
- `services/vikor.py` contains the normalization, boost, and presets. Update the `presets` dict, the boost logic, or the normalization in `_build_user_aligned_matrix` to change behavior.

Contact
- If you want, I can add unit tests demonstrating expected top recommendations for small/medium/large presets and document test cases in this repo.
