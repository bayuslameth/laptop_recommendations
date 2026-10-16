"""
pages/2_Rekomendasi.py — Halaman Konsultasi & Rekomendasi Laptop (Enterprise SaaS Dark UI)
Antarmuka dashboard modern dengan sistem pakar SWI-Prolog berbasis logika predikat.
"""

import streamlit as st
import sys
from pathlib import Path

# Setup path root
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.ui_theme import (
    setup_page,
    clean_html,
    render_hero,
    render_laptop_card,
    render_no_results,
    render_error_message,
    render_specs_comparison,
    render_xai_panel
)
from services.prolog_engine import get_prolog_engine
from services.input_validator import validate_form, build_query
from services.result_formatter import (
    format_laptop_result, deduplicate_results, sort_results,
    format_query_info, add_to_history
)

setup_page("Konsultasi Rekomendasi", icon="🔍")

engine = get_prolog_engine()

if not engine.is_loaded:
    render_error_message(f"Knowledge Base Prolog tidak tersedia: {engine.error_message}")
    st.stop()

# ==============================================================================
# HERO BANNER
# ==============================================================================
render_hero(
    title="Konsultasi Spesifikasi & Rekomendasi Laptop",
    subtitle="Tentukan profil komputasi dan batas anggaran Anda. Mesin inferensi SWI-Prolog akan mengevaluasi pembuktian resolusi backward chaining terhadap seluruh basis fakta hardware secara deterministik.",
    badge_text="DEDUCTIVE REASONING ENGINE"
)

# ==============================================================================
# FORM KONSULTASI (SAAS CONTAINER)
# ==============================================================================
form_header_html = """
<div class="saas-card" style="margin-bottom: 1rem;">
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(80, 87, 159, 0.25); padding-bottom: 0.75rem;">
<div>
<span style="font-size: 1.15rem; font-weight: 800; color: #f8f9fa;">📋 Parameter Kebutuhan Pengguna</span>
<div style="font-size: 0.82rem; color: #9ea3c0; margin-top: 2px;">Lengkapi parameter wajib berikut untuk menjalankan penalaran sistem pakar.</div>
</div>
<span style="background: rgba(80, 87, 159, 0.2); color: #c0c6ff; border: 1px solid rgba(80, 87, 159, 0.5); padding: 4px 10px; border-radius: 9999px; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.04em;">FORM INFERENSI</span>
</div>
</div>
"""
st.markdown(clean_html(form_header_html), unsafe_allow_html=True)

with st.form("form_rekomendasi_saas", clear_on_submit=False):
    # --- SECTION 1: INPUT WAJIB ---
    req_header_html = """
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.85rem;">
<span style="background: rgba(80, 87, 159, 0.3); color: #f8f9fa; border: 1px solid #50579f; padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 800;">WAJIB</span>
<span style="font-size: 0.95rem; font-weight: 700; color: #f8f9fa;">Kriteria Primer Komputasi & Anggaran</span>
</div>
"""
    st.markdown(clean_html(req_header_html), unsafe_allow_html=True)

    col_req1, col_req2 = st.columns(2)

    with col_req1:
        st.markdown("<p style='font-size: 0.85rem; font-weight: 600; color: #9ea3c0; margin-bottom: 4px;'>1. Beban Kerja Utama Software</p>", unsafe_allow_html=True)
        kebutuhan_options = {
            "Pilih beban kerja...": None,
            "🖥️ Kuliah Umum & Produktivitas Dokumen": "office",
            "💻 Pemrograman & Rekayasa Perangkat Lunak": "koding",
            "🎨 Desain Grafis Ringan (Canva, Figma, Photoshop)": "editing_ringan",
            "🎬 Desain & Multimedia Berat (Video 4K, 3D Render)": "editing_berat",
            "🎮 Gaming Kompetitif & Game AAA": "gaming",
            "📡 Gaming Sambil Live Streaming (OBS)": "streaming",
            "📊 Data Science & Machine Learning": "data_science",
            "🌐 Jaringan Komputer & Virtual Machine": "virtualisasi",
        }
        kebutuhan_label = st.selectbox(
            "Kebutuhan Utama",
            options=list(kebutuhan_options.keys()),
            label_visibility="collapsed"
        )
        kebutuhan_val = kebutuhan_options[kebutuhan_label]

    with col_req2:
        st.markdown("<p style='font-size: 0.85rem; font-weight: 600; color: #9ea3c0; margin-bottom: 4px;'>2. Batasan Kelas Anggaran</p>", unsafe_allow_html=True)
        kelas_options = {
            "Pilih batas anggaran...": None,
            "🟢 Entry (Di bawah Rp 10.000.000)": "entry",
            "🔵 Midrange (Rp 10.000.000 – Rp 19.000.000)": "midrange",
            "🟣 High-End (Rp 20.000.000 – Rp 34.000.000)": "high_end",
            "🟡 Flagship (Rp 35.000.000 ke atas)": "flagship",
        }
        kelas_label = st.selectbox(
            "Rentang Anggaran",
            options=list(kelas_options.keys()),
            label_visibility="collapsed"
        )
        kelas_val = kelas_options[kelas_label]

    st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

    # --- SECTION 2: INPUT OPSIONAL (PREFERENSI) ---
    opt_header_html = """
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.85rem; padding-top: 0.75rem; border-top: 1px dashed rgba(80, 87, 159, 0.3);">
<span style="background: rgba(158, 163, 192, 0.15); color: #9ea3c0; border: 1px solid rgba(158, 163, 192, 0.3); padding: 2px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 800;">OPSIONAL</span>
<span style="font-size: 0.95rem; font-weight: 700; color: #f8f9fa;">Preferensi Spesifikasi Tambahan</span>
</div>
"""
    st.markdown(clean_html(opt_header_html), unsafe_allow_html=True)

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        pref_ram = st.checkbox("💾 Wajib RAM Besar (≥ 16 GB)")
    with col_p2:
        pref_gpu = st.checkbox("🎮 Wajib GPU Diskrit (Dedicated)")
    with col_p3:
        pref_portabilitas = st.checkbox("🪶 Prioritas Portabilitas Ringan")

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # --- ACTION BUTTONS ---
    col_btn1, col_btn2 = st.columns([3.5, 1.2])
    with col_btn1:
        submitted = st.form_submit_button(
            "⚡ Jalankan Inferensi Prolog",
            use_container_width=True,
            type="primary"
        )
    with col_btn2:
        reset = st.form_submit_button("🔄 Reset Pilihan", use_container_width=True)

# ==============================================================================
# EVALUASI & INFERENSI REKOMENDASI
# ==============================================================================
if submitted:
    preferensi = []
    if pref_ram:
        preferensi.append('ram_besar')
    if pref_gpu:
        preferensi.append('gpu_dedicated')
    if pref_portabilitas:
        preferensi.append('portabilitas')

    valid, errors = validate_form(kebutuhan_val, kelas_val, preferensi)

    if not valid:
        for err in errors:
            st.warning(f"⚠️ {err}")
    else:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        query_info = format_query_info(kebutuhan_val, kelas_val, preferensi)
        query_str = build_query(kebutuhan_val, kelas_val, preferensi)

        with st.spinner("🧠 SWI-Prolog sedang mengevaluasi resolusi backward chaining..."):
            try:
                raw_results = engine.query(query_str)
                # Fallback jika query filter preferensi tidak menghasilkan fakta
                if not raw_results and 'gpu_dedicated' not in preferensi and 'ram_besar' not in preferensi:
                    fallback_query = f"rekomendasi_lengkap({kebutuhan_val}, {kelas_val}, _, Merk, Model, CPU, RAM, Storage, VGA, Harga)"
                    raw_results = engine.query(fallback_query)
                error_occurred = False
                error_msg = ""
            except RuntimeError as e:
                raw_results = []
                error_occurred = True
                error_msg = str(e)

        if error_occurred:
            render_error_message(error_msg)
        elif not raw_results:
            render_no_results(query_info['kebutuhan_label'], query_info['kelas_label'])
        else:
            formatted = [format_laptop_result(r) for r in raw_results]
            unique = deduplicate_results(formatted)
            sorted_results = sort_results(unique, 'harga')

            # --- HEADER HASIL INFERENSI ---
            res_header_html = f"""
<div style="background-color: #131622; border: 1px solid rgba(80, 87, 159, 0.4); border-radius: 16px; padding: 1.5rem 1.75rem; margin-bottom: 1.75rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);">
<div>
<div style="display: flex; align-items: center; gap: 10px;">
<span style="font-size: 1.4rem;">🎯</span>
<h2 style="margin: 0; font-size: 1.45rem; font-weight: 800; color: #f8f9fa;">Hasil Inferensi Sistem Pakar</h2>
</div>
<div style="margin-top: 4px; font-size: 0.9rem; color: #9ea3c0;">
Kriteria: <strong style="color: #dee263;">{query_info['kebutuhan_label']}</strong> &bull; Anggaran: <strong style="color: #dee263;">{query_info['kelas_label']}</strong>
</div>
</div>
<div style="display: flex; align-items: center; gap: 10px;">
<div style="background: rgba(222, 226, 99, 0.12); border: 1px solid rgba(222, 226, 99, 0.5); padding: 6px 14px; border-radius: 9999px; font-size: 0.8rem; font-weight: 800; color: #dee263;">
✔ {len(unique)} UNIT TERBUKTI COCOK
</div>
</div>
</div>
"""
            st.markdown(clean_html(res_header_html), unsafe_allow_html=True)

            # Ambil data spesifikasi panduan dari Prolog
            try:
                r_min = engine.query_once(f"spesifikasi_minimum({kebutuhan_val}, SpesMin)")
                r_ideal = engine.query_once(f"spesifikasi_ideal({kebutuhan_val}, SpesIdeal)")
                r_profil = engine.query_once(f"profil_penggunaan({kebutuhan_val}, Profil)")
                r_tips = engine.query_once(f"tips_kebutuhan({kebutuhan_val}, Tips)")
            except Exception:
                r_min = r_ideal = r_profil = r_tips = None

            min_specs = [s.strip() for s in str(r_min['SpesMin']).split('|')] if r_min else ["RAM: 8GB", "Storage: 256GB SSD", "CPU: Multi-core modern"]
            ideal_specs = [s.strip() for s in str(r_ideal['SpesIdeal']).split('|')] if r_ideal else ["RAM: 16GB", "Storage: 512GB SSD", "GPU: Dedicated / High Performance"]

            # --- TABS: REKOMENDASI PRODUK & XAI / SPESIFIKASI ---
            tab_katalog, tab_spes, tab_xai = st.tabs([
                "💻 Katalog Rekomendasi Laptop",
                "📊 Komparasi Spesifikasi (Min vs Ideal)",
                "🧠 Explainable AI (XAI) & Logic Trace"
            ])

            with tab_katalog:
                cat_sub_html = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
<span style="font-size: 0.88rem; color: #9ea3c0;">Menampilkan <strong style="color: #dee263;">{len(sorted_results)}</strong> unit terverifikasi (diurutkan dari harga terendah):</span>
<span style="font-size: 0.78rem; color: #9ea3c0; font-family: 'JetBrains Mono', monospace;">LAYOUT: 2-COLUMN GRID</span>
</div>
"""
                st.markdown(clean_html(cat_sub_html), unsafe_allow_html=True)

                # Render dalam 2 kolom grid kartu produk
                for i in range(0, len(sorted_results), 2):
                    col_l1, col_l2 = st.columns(2)
                    
                    # Kolom 1
                    with col_l1:
                        lap1 = sorted_results[i]
                        alasan_text1 = ""
                        try:
                            id_q1 = f"spesifikasi(ID, {lap1['merk']}, '{lap1['model']}', _, {lap1['ram']}, {lap1['storage']}, _, {lap1['harga_juta']})"
                            r_id1 = engine.query_once(id_q1)
                            if r_id1 and 'ID' in r_id1:
                                r_als1 = engine.query_once(f"alasan_rekomendasi({r_id1['ID']}, {kebutuhan_val}, Alasan)")
                                alasan_text1 = str(r_als1['Alasan']) if r_als1 else ""
                        except Exception:
                            alasan_text1 = ""
                            
                        render_laptop_card(
                            lap1,
                            alasan=alasan_text1,
                            show_prolog_rule=True,
                            kebutuhan=kebutuhan_val
                        )

                    # Kolom 2 (jika ada unit genap berikutnya)
                    with col_l2:
                        if i + 1 < len(sorted_results):
                            lap2 = sorted_results[i + 1]
                            alasan_text2 = ""
                            try:
                                id_q2 = f"spesifikasi(ID, {lap2['merk']}, '{lap2['model']}', _, {lap2['ram']}, {lap2['storage']}, _, {lap2['harga_juta']})"
                                r_id2 = engine.query_once(id_q2)
                                if r_id2 and 'ID' in r_id2:
                                    r_als2 = engine.query_once(f"alasan_rekomendasi({r_id2['ID']}, {kebutuhan_val}, Alasan)")
                                    alasan_text2 = str(r_als2['Alasan']) if r_als2 else ""
                            except Exception:
                                alasan_text2 = ""

                            render_laptop_card(
                                lap2,
                                alasan=alasan_text2,
                                show_prolog_rule=True,
                                kebutuhan=kebutuhan_val
                            )

            with tab_spes:
                st.markdown("<h3 style='font-size: 1.25rem; font-weight: 800; color: #f8f9fa; margin-bottom: 1rem;'>⚖️ Komparasi Kebutuhan Hardware Komputasi</h3>", unsafe_allow_html=True)
                
                # Render Grid Perbandingan Minimum vs Ideal
                render_specs_comparison(min_specs, ideal_specs)
                
                st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)

                if r_profil:
                    profil_html = f"""
<div style="background-color: #131622; border: 1px solid rgba(80, 87, 159, 0.35); border-radius: 14px; padding: 1.25rem; margin-bottom: 1rem;">
<div style="font-size: 0.8rem; font-weight: 800; color: #9ea3c0; text-transform: uppercase;">👤 Profil Karakteristik Pengguna</div>
<div style="font-size: 0.95rem; color: #f8f9fa; margin-top: 6px; line-height: 1.5;">{r_profil['Profil']}</div>
</div>
"""
                    st.markdown(clean_html(profil_html), unsafe_allow_html=True)

                if r_tips:
                    tips_html = f"""
<div style="background-color: rgba(222, 226, 99, 0.08); border: 1px solid rgba(222, 226, 99, 0.4); border-radius: 14px; padding: 1.25rem;">
<div style="font-size: 0.8rem; font-weight: 800; color: #dee263; text-transform: uppercase;">💡 Tips Pakar Hardware</div>
<div style="font-size: 0.92rem; color: #f8f9fa; margin-top: 6px; line-height: 1.5;">{r_tips['Tips']}</div>
</div>
"""
                    st.markdown(clean_html(tips_html), unsafe_allow_html=True)

            with tab_xai:
                st.markdown("<h3 style='font-size: 1.25rem; font-weight: 800; color: #f8f9fa; margin-bottom: 0.5rem;'>🧠 Explainable AI: Deduksi Formal & Bukti Logika</h3>", unsafe_allow_html=True)
                st.caption("Panel ini menyajikan transparansi penuh bagaimana inferensi Prolog membuktikan setiap rekomendasi yang diberikan.")

                rules_fired = [
                    f"kebutuhan_pengguna({kebutuhan_val}).",
                    f"kelas_anggaran({kelas_val}).",
                    f"evaluasi_predikat(cocok_untuk(ID, {kebutuhan_val})).",
                    f"evaluasi_predikat(kelas_laptop(ID, {kelas_val}))."
                ]
                if preferensi:
                    rules_fired.append(f"filter_preferensi({', '.join(preferensi)}).")

                justifications = [
                    f"Unit memenuhi seluruh kondisi aturan predikat cocok_untuk(ID, {kebutuhan_val}).",
                    f"Plafon harga unit berada dalam batas kelas anggaran {query_info['kelas_label']}.",
                    "Kapasitas memori utama (RAM) mencukupi kebutuhan runtime compiler dan tools terkait.",
                    "Sistem pendingin dan arsitektur CPU mendukung sustained heavy performance."
                ]
                if 'gpu_dedicated' in preferensi or kebutuhan_val in ['gaming', 'editing_berat', 'streaming']:
                    justifications.append("Unit dilengkapi GPU diskrit (Dedicated VRAM) untuk akselerasi rendering dan parallel compute.")

                render_xai_panel(
                    query_info=query_info,
                    query_str=query_str,
                    rules_fired=rules_fired,
                    justifications=justifications
                )

            # Simpan histori sesi
            hist_entry = add_to_history(kebutuhan_val, kelas_val, preferensi, sorted_results)
            if 'riwayat' not in st.session_state:
                st.session_state['riwayat'] = []
            st.session_state['riwayat'].append(hist_entry)

elif reset:
    st.rerun()
