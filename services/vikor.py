import numpy as np
import re
import math

# ======================================
# DATA ALTERNATIF TERNAK
# ======================================

livestock_data = [
    {
        "name": "Ayam Petelur",
        "modal": 2500000,
        "modal_minimal_realistis": 2500000,
        "modal_aman": 4000000,
        "biaya_per_ekor": 220000,
        "min_ekor": 10,
        "breakdown": {
            "bibit": 90000,
            "kandang": 50000,
            "pakan_awal": 60000,
            "lainnya": 20000
        },
        "lahan": 4,
        "waktu": 2,
        "pengalaman": 1,
        "roi": 18,
        "alasan": "Cocok untuk pemula dengan modal kecil dan lahan sempit.",
        "deskripsi": "Ayam petelur mudah dirawat dan menghasilkan telur secara rutin.",
        "kebutuhan_pakan": [
            "Jagung",
            "Dedak",
            "Konsentrat"
        ],
        "tips": [
            "Jaga kebersihan kandang",
            "Lakukan vaksin rutin",
            "Berikan pakan teratur"
        ]
    },

    {
        "name": "Bebek Petelur",
        "modal": 3500000,
        "modal_minimal_realistis": 3500000,
        "modal_aman": 5000000,
        "biaya_per_ekor": 250000,
        "min_ekor": 10,
        "breakdown": {
            "bibit": 100000,
            "kandang": 50000,
            "pakan_awal": 70000,
            "lainnya": 30000
        },
        "lahan": 6,
        "waktu": 3,
        "pengalaman": 2,
        "roi": 25,
        "alasan": "Memiliki daya tahan tubuh baik dan cocok produksi telur.",
        "deskripsi": "Bebek petelur cocok untuk lingkungan lembab.",
        "kebutuhan_pakan": [
            "Bekatul",
            "Keong",
            "Konsentrat"
        ],
        "tips": [
            "Pastikan area tidak terlalu kering",
            "Berikan air cukup",
            "Jaga sanitasi kandang"
        ]
    },

    {
        "name": "Kambing Etawa",
        "modal": 12000000,
        "modal_minimal_realistis": 12000000,
        "modal_aman": 18000000,
        "biaya_per_ekor": 4800000,
        "min_ekor": 2,
        "breakdown": {
            "bibit": 2500000,
            "kandang": 1200000,
            "pakan_awal": 800000,
            "lainnya": 300000
        },
        "lahan": 10,
        "waktu": 3,
        "pengalaman": 3,
        "roi": 25,
        "alasan": "Cocok untuk peternak dengan modal dan lahan menengah.",
        "deskripsi": "Kambing Etawa terkenal sebagai penghasil susu dan daging.",
        "kebutuhan_pakan": [
            "Rumput",
            "Daun singkong",
            "Konsentrat"
        ],
        "tips": [
            "Pastikan kandang tidak lembab",
            "Berikan hijauan segar",
            "Cek kesehatan rutin"
        ]
    },

    {
        "name": "Domba Garut",
        "modal": 14000000,
        "modal_minimal_realistis": 14000000,
        "modal_aman": 20000000,
        "biaya_per_ekor": 5500000,
        "min_ekor": 2,
        "breakdown": {
            "bibit": 2800000,
            "kandang": 1300000,
            "pakan_awal": 1000000,
            "lainnya": 400000
        },
        "lahan": 15,
        "waktu": 4,
        "pengalaman": 3,
        "roi": 22,
        "alasan": "Memiliki potensi keuntungan tinggi untuk peternakan menengah.",
        "deskripsi": "Domba Garut memiliki pertumbuhan cepat dan pasar yang baik.",
        "kebutuhan_pakan": [
            "Rumput gajah",
            "Jerami",
            "Konsentrat"
        ],
        "tips": [
            "Pisahkan domba sakit",
            "Jaga sanitasi kandang",
            "Berikan vitamin tambahan"
        ]
    },

    {
        "name": "Sapi Limousin",
        "modal": 75000000,
        "modal_minimal_realistis": 75000000,
        "modal_aman": 100000000,
        "biaya_per_ekor": 32000000,
        "min_ekor": 2,
        "breakdown": {
            "bibit": 22000000,
            "kandang": 5000000,
            "pakan_awal": 3500000,
            "lainnya": 1500000
        },
        "lahan": 40,
        "waktu": 5,
        "pengalaman": 5,
        "roi": 30,
        "alasan": "Cocok untuk peternak berpengalaman dengan modal besar.",
        "deskripsi": "Sapi Limousin memiliki kualitas daging premium.",
        "kebutuhan_pakan": [
            "Rumput fermentasi",
            "Konsentrat",
            "Vitamin ternak"
        ],
        "tips": [
            "Pastikan stok pakan cukup",
            "Kontrol kesehatan rutin",
            "Perhatikan kebersihan kandang"
        ]
    }
]

# ======================================
# BOBOT KRITERIA
# ======================================

# Adjusted weights (recommended): prioritize total modal so recommendations
# favor alternatives that match user's available capital for practical UX.
weights = np.array([
    0.45,  # modal (total modal capability)
    0.10,  # biaya_per_ekor (per-unit cost penalization)
    0.25,  # lahan
    0.10,  # waktu
    0.10   # pengalaman
])

# ======================================
# KONVERSI INPUT USER
# ======================================
pengalaman_map = {
    "belum": 1,
    "kurang_1_tahun": 2,
    "1_3_tahun": 3,
    "3_5_tahun": 4,
    "lebih_5_tahun": 5
}


def _parse_number(value):
    if isinstance(value, str):
        text = value.strip()
        matches = re.findall(r"\d[\d\.,]*", text)

        if not matches:
            return 0.0

        numbers = []
        for match in matches:
            cleaned = match.replace(".", "").replace(",", ".")
            try:
                numbers.append(float(cleaned))
            except ValueError:
                continue

        if not numbers:
            return 0.0

        if len(numbers) == 1:
            return numbers[0]

        return sum(numbers) / len(numbers)

    return float(value)


def _parse_experience(value):
    if isinstance(value, str):
        normalized = value.strip().lower()

        if normalized in pengalaman_map:
            return pengalaman_map[normalized]

        numbers = re.findall(r"\d[\d\.,]*", normalized)
        if numbers:
            parsed = []
            for number in numbers:
                cleaned = number.replace(".", "").replace(",", ".")
                try:
                    parsed.append(float(cleaned))
                except ValueError:
                    continue

            if parsed:
                return int(round(sum(parsed) / len(parsed)))

        return 1

    try:
        return int(value)
    except (TypeError, ValueError):
        return 1


def convert_user_input(data):

    return {
        "modal": _parse_number(data["modal"]),
        "lahan": _parse_number(data["lahan"]),
        "waktu": int(_parse_number(data["waktu"])),
        "pengalaman": _parse_experience(data.get("pengalaman", 1)),
    }


# ======================================
# BUILD COMPATIBILITY MATRIX
# ======================================

def build_compatibility_matrix(
    matrix,
    user_vector
):

    compatibility = np.zeros_like(
        matrix,
        dtype=float
    )

    for i in range(matrix.shape[0]):

        for j in range(matrix.shape[1]):

            requirement = float(matrix[i][j])
            capacity = float(user_vector[j])

            # hindari pembagian nol
            if requirement <= 0 or capacity <= 0:

                compatibility[i][j] = 0.0

            else:

                # Jika kapasitas user sudah cukup, beri skor penuh.
                # Jika belum cukup, skornya turun proporsional.
                compatibility[i][j] = min(
                    capacity / requirement,
                    1.0
                )

    return compatibility


def _build_user_aligned_matrix(livestock_items, user_vector):
    user_modal = max(float(user_vector["modal"]), 1e-9)
    user_lahan = max(float(user_vector["lahan"]), 1e-9)
    user_waktu = max(float(user_vector["waktu"]), 1e-9)
    user_pengalaman = max(float(user_vector["pengalaman"]), 1e-9)

    matrix = []

    for item in livestock_items:
        item_modal = max(float(item.get("modal", 1.0)), 1e-9)
        item_lahan = max(float(item.get("lahan", 1.0)), 1e-9)
        item_biaya = float(item.get("biaya_per_ekor", item_modal))

        # Modal & lahan as benefit: higher user capacity relative to requirement -> better score
        modal_score = min(user_modal / item_modal, 1e6)
        lahan_score = min(user_lahan / item_lahan, 1e6)

        # biaya_per_ekor as cost: higher biaya -> worse (we normalize relative to user modal)
        biaya_score = item_biaya / max(user_modal, 1e-9)

        # waktu and pengalaman remain relative requirement (cost-like)
        waktu_score = float(item.get("waktu", 1.0)) / user_waktu
        pengalaman_score = float(item.get("pengalaman", 1.0)) / user_pengalaman

        # Business rule: if user_modal is much larger than item_modal, prefer larger-scale items
        # Apply a modest boost to modal_score based on log10(capacity_ratio)
        capacity_ratio = user_modal / item_modal
        if capacity_ratio >= 10:
            boost = min(math.log10(capacity_ratio) / 2.0, 1.0)  # 10x -> 0.5, 100x -> 1.0
            modal_score *= (1.0 + 0.5 * boost)

        matrix.append([
            float(modal_score),
            float(biaya_score),
            float(lahan_score),
            float(waktu_score),
            float(pengalaman_score),
        ])

    return np.array(matrix, dtype=float)


def _get_reference_heads(livestock):

    biaya_per_ekor = float(livestock.get("biaya_per_ekor", livestock["modal"]))

    if biaya_per_ekor <= 400000:
        return 20
    if biaya_per_ekor <= 7000000:
        return 5

    return 2


def _estimate_land_capacity(livestock, user_lahan):

    reference_heads = max(_get_reference_heads(livestock), 1)
    land_requirement = max(float(livestock.get("lahan", 1.0)), 1e-9)
    capacity_units = float(user_lahan) / land_requirement

    return max(int(capacity_units * reference_heads), 0)


def _estimate_head_capacity(livestock, user_modal, user_lahan, reserve_ratio=0.0):

    projection = _estimate_financial_projection(
        livestock,
        user_modal,
        user_lahan,
        reserve_ratio=reserve_ratio,
        feasible=True
    )

    return int(projection.get("estimasi_ekor", 0))


def _estimate_financial_projection(livestock, user_modal, user_lahan, reserve_ratio=0.0, feasible=True):

    breakdown_per_ekor = {
        key: round(float(value), 0)
        for key, value in livestock.get("breakdown", {}).items()
    }

    kandang_dasar = breakdown_per_ekor.get("kandang", 0.0)
    biaya_variabel_per_ekor = round(
        breakdown_per_ekor.get("bibit", 0.0)
        + breakdown_per_ekor.get("pakan_awal", 0.0)
        + breakdown_per_ekor.get("lainnya", 0.0),
        0
    )
    reference_heads = max(_get_reference_heads(livestock), 1)
    kandang_tambahan_per_ekor = round(kandang_dasar / reference_heads, 0)
    biaya_per_ekor = round(biaya_variabel_per_ekor + kandang_tambahan_per_ekor, 0)
    effective_modal = max(float(user_modal) * (1.0 - reserve_ratio), 0.0)
    kapasitas_lahan_estimasi = _estimate_land_capacity(livestock, user_lahan)

    if not feasible:
        estimated_ekor = 0
    elif biaya_variabel_per_ekor <= 0:
        estimated_ekor = 0
    elif effective_modal <= kandang_dasar:
        estimated_ekor = 0
    else:
        estimated_ekor = int((effective_modal - kandang_dasar) // biaya_per_ekor)
        if estimated_ekor <= 0 and effective_modal >= (kandang_dasar + biaya_per_ekor):
            estimated_ekor = 1

    if kapasitas_lahan_estimasi > 0:
        estimated_ekor = min(estimated_ekor, kapasitas_lahan_estimasi)

    kandang_total = round(kandang_dasar + kandang_tambahan_per_ekor * max(estimated_ekor - 1, 0), 0)

    breakdown_total = {
        "bibit": round(breakdown_per_ekor.get("bibit", 0.0) * estimated_ekor, 0),
        "kandang": kandang_total,
        "pakan_awal": round(breakdown_per_ekor.get("pakan_awal", 0.0) * estimated_ekor, 0),
        "lainnya": round(breakdown_per_ekor.get("lainnya", 0.0) * estimated_ekor, 0),
    }

    modal_terpakai = round(
        breakdown_total["kandang"]
        + breakdown_total["bibit"]
        + breakdown_total["pakan_awal"]
        + breakdown_total["lainnya"],
        0
    )
    sisa_modal = round(float(user_modal) - modal_terpakai, 0)

    potensi_keuntungan_per_ekor = round(
        (biaya_per_ekor * float(livestock["roi"])) / 100,
        0
    )
    potensi_keuntungan_total = round(
        potensi_keuntungan_per_ekor * estimated_ekor,
        0
    )

    min_ekor = max(int(livestock.get("min_ekor", 1)), 1)
    if estimated_ekor <= 0:
        kecocokan_kapasitas_persen = 0.0
        status_kelayakan = "Tidak Layak"
    else:
        kecocokan_kapasitas_persen = round(min(estimated_ekor / min_ekor, 1.0) * 100, 0)
        status_kelayakan = "Layak" if estimated_ekor >= min_ekor else "Kurang Layak"

    return {
        "estimasi_ekor": estimated_ekor,
        "modal_efektif": round(effective_modal, 0),
        "modal_terpakai_estimasi": modal_terpakai,
        "sisa_modal_estimasi": sisa_modal,
        "kapasitas_lahan_estimasi": kapasitas_lahan_estimasi,
        "min_ekor_minimum": min_ekor,
        "kecocokan_kapasitas_persen": kecocokan_kapasitas_persen,
        "status_kelayakan": status_kelayakan,
        "biaya_kandang_estimasi": breakdown_total["kandang"],
        "biaya_variabel_per_ekor": biaya_variabel_per_ekor,
        "biaya_kandang_tambahan_per_ekor": kandang_tambahan_per_ekor,
        "biaya_per_ekor_estimasi": biaya_per_ekor,
        "breakdown_per_ekor": breakdown_per_ekor,
        "breakdown_total_estimasi": breakdown_total,

        # ======================================
        # FIELD TAMBAHAN UNTUK FLUTTER UI
        # ======================================

        "breakdown_biaya": breakdown_total,
        "sisa_modal": sisa_modal,
        "estimasi_modal": modal_terpakai,
        "estimasi_biaya_per_ekor": biaya_per_ekor,
        # ======================================
        "potensi_keuntungan_per_ekor": potensi_keuntungan_per_ekor,
        "potensi_keuntungan_total": potensi_keuntungan_total,
    }



def _compute_vikor_scores(matrix, weights, criteria_types):

    f_star = np.zeros(matrix.shape[1], dtype=float)
    f_minus = np.zeros(matrix.shape[1], dtype=float)

    for j in range(matrix.shape[1]):
        column = matrix[:, j]

        if criteria_types[j] == "benefit":
            f_star[j] = column.max()
            f_minus[j] = column.min()
        else:
            f_star[j] = column.min()
            f_minus[j] = column.max()

    S = []
    R = []

    for row in matrix:
        gap = np.zeros_like(row, dtype=float)

        for j in range(matrix.shape[1]):
            if criteria_types[j] == "benefit":
                denominator = f_star[j] - f_minus[j]

                if denominator <= 1e-9:
                    gap[j] = 0.0
                else:
                    gap[j] = weights[j] * ((f_star[j] - row[j]) / denominator)
            else:
                denominator = f_minus[j] - f_star[j]

                if denominator <= 1e-9:
                    gap[j] = 0.0
                else:
                    gap[j] = weights[j] * ((row[j] - f_star[j]) / denominator)

        S.append(gap.sum())
        R.append(gap.max())

    S = np.array(S)
    R = np.array(R)

    S_star = S.min()
    S_minus = S.max()
    R_star = R.min()
    R_minus = R.max()

    s_range = S_minus - S_star
    r_range = R_minus - R_star

    if s_range <= 1e-9:
        s_component = np.zeros_like(S)
    else:
        s_component = (S - S_star) / s_range

    if r_range <= 1e-9:
        r_component = np.zeros_like(R)
    else:
        r_component = (R - R_star) / r_range

    v = 0.5
    Q = (v * s_component) + ((1 - v) * r_component)

    return Q


def _build_result_rows(q_values, q_values_pure=None, index_map=None, user_modal=None, user_lahan=None, reserve_ratio=0.02):

    if index_map is None:
        index_map = list(range(len(livestock_data)))

    ranking = np.argsort(q_values)
    results = []

    for rank, pos in enumerate(ranking):
        idx = index_map[pos]
        livestock = livestock_data[idx]

        item = {
            "index": idx,
            "ranking": rank + 1,
            "ternak": livestock["name"],
            "jenis_hewan": livestock["name"],
            "q_value": round(float(q_values[pos]), 4),
            "feasible": True,
            "modal_minimum": livestock["modal"],
            "modal_minimal_realistis": livestock.get("modal_minimal_realistis", livestock["modal"]),
            "modal_aman": livestock.get("modal_aman", livestock["modal"]),
            "lahan_minimum": livestock["lahan"],
            "waktu_perawatan": livestock["waktu"],
            "pengalaman_minimum": livestock["pengalaman"],
            "roi": livestock["roi"],
            "biaya_awal": livestock["modal"],
            "biaya_per_ekor": livestock.get("biaya_per_ekor", livestock["modal"]),
            "potensi_keuntungan": round(((
                livestock.get("biaya_per_ekor", livestock["modal"])
            ) * livestock["roi"]) / 100, 0),
            "alasan": livestock["alasan"],
            "deskripsi": livestock["deskripsi"],
            "kebutuhan_pakan": livestock["kebutuhan_pakan"],
            "tips": livestock["tips"],
        }

        if user_modal is not None:
            item.update(
                _estimate_financial_projection(
                    livestock,
                    user_modal,
                    user_lahan if user_lahan is not None else livestock["lahan"],
                    reserve_ratio=reserve_ratio
                )
            )

        if q_values_pure is not None:
            # q_values_pure aligns with q_values positions
            item["q_value_pure"] = round(float(q_values_pure[pos]), 4)

        results.append(item)

    return results


# ======================================
# PERHITUNGAN VIKOR
# ======================================

def calculate_vikor(user_input, mode="pure", preset="menengah"):

    user_vector = convert_user_input(user_input)

    # Preset weights for adjusted scoring (modal, biaya_per_ekor, lahan, waktu, pengalaman)
    presets = {
        "pemula": np.array([0.35, 0.15, 0.25, 0.15, 0.10]),
        "menengah": np.array([0.55, 0.05, 0.25, 0.05, 0.10]),
        "besar": np.array([0.50, 0.05, 0.25, 0.10, 0.10])
    }

    pure_weights = presets.get(preset, presets["menengah"])

    # Feasibility is used as a status flag, but scoring runs on the full set so
    # Q stays a continuous ranking signal even when only a few items are feasible.
    user_modal = float(user_vector["modal"])
    user_lahan = float(user_vector["lahan"])
    user_waktu = int(user_vector["waktu"])
    user_pengalaman = int(user_vector["pengalaman"])

    feasibility_flags = []
    for item in livestock_data:
        estimated_heads = _estimate_head_capacity(item, user_modal, user_lahan, reserve_ratio=0.0)
        min_required = int(item.get("min_ekor", 1))
        is_feasible = (
            (user_modal >= item["modal"]) and
            (user_lahan >= item["lahan"]) and
            (user_waktu >= item["waktu"]) and
            (user_pengalaman >= item["pengalaman"]) and
            (estimated_heads >= min_required)
        )
        feasibility_flags.append(is_feasible)

    matrix_aligned_f = _build_user_aligned_matrix(
        livestock_data,
        user_vector
    )

    if mode == "pure":
        q_pure = _compute_vikor_scores(
            matrix_aligned_f,
            pure_weights,
            ["cost", "cost", "cost", "cost", "benefit"]
        )

        results_feasible = _build_result_rows(
            q_pure,
            q_values_pure=q_pure,
            index_map=list(range(len(livestock_data))),
            user_modal=user_modal,
            user_lahan=user_lahan,
            reserve_ratio=0.02
        )

        for i, it in enumerate(results_feasible):
            idx = it.get("index", i)
            item = livestock_data[idx]
            feasible_flag = bool(feasibility_flags[idx])
            it["feasible"] = feasible_flag
            it.update(
                _estimate_financial_projection(
                    item,
                    user_modal,
                    user_lahan,
                    reserve_ratio=0.02,
                    feasible=feasible_flag
                )
            )

        results_feasible = sorted(
            results_feasible,
            key=lambda item: (
                0 if item.get("feasible", False) else 1,
                item.get("q_value", 1.0),
                -float(item.get("roi", 0.0)),
                float(item.get("biaya_per_ekor", 0.0))
            )
        )

        for i, it in enumerate(results_feasible):
            it["ranking"] = i + 1 if it.get("feasible", True) else None

        return results_feasible

    if mode == "normal":
        q_normal_f = _compute_vikor_scores(
            matrix_aligned_f,
            presets.get(preset, presets["menengah"]),
            ["cost", "cost", "cost", "cost", "benefit"]
        )

        results_feasible = _build_result_rows(
            q_normal_f,
            q_values_pure=None,
            index_map=list(range(len(livestock_data))),
            user_modal=user_modal,
            user_lahan=user_lahan,
            reserve_ratio=0.02
        )

        for i, it in enumerate(results_feasible):
            idx = it.get("index", i)
            item = livestock_data[idx]
            feasible_flag = bool(feasibility_flags[idx])
            it["feasible"] = feasible_flag
            it.update(
                _estimate_financial_projection(
                    item,
                    user_modal,
                    user_lahan,
                    reserve_ratio=0.02,
                    feasible=feasible_flag
                )
            )

        results_feasible = sorted(
            results_feasible,
            key=lambda item: (
                0 if item.get("feasible", False) else 1,
                item.get("q_value", 1.0),
                -float(item.get("roi", 0.0)),
                float(item.get("biaya_per_ekor", 0.0))
            )
        )

        for i, it in enumerate(results_feasible):
            it["ranking"] = i + 1 if it.get("feasible", True) else None

        return results_feasible

    return calculate_vikor(user_input, mode="normal")


def get_startup_cost_table():
    return [
        {
            "ternak": item["name"],
            "minimal_realistis": item.get("modal_minimal_realistis", item["modal"]),
            "modal_aman": item.get("modal_aman", item["modal"]),
            "min_ekor": item.get("min_ekor", 1),
            "biaya_per_ekor": item.get("biaya_per_ekor", item["modal"]),
        }
        for item in livestock_data
    ]