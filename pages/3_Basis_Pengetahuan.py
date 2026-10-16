"""
pages/3_Basis_Pengetahuan.py — Basis Pengetahuan & Aturan Inferensi (Admin Only)
Enterprise SaaS Dark UI untuk inspeksi, verifikasi fakta, dan eksekusi predikat SWI-Prolog.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Setup path root
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.ui_theme import (
    setup_page,
    clean_html,
    render_hero,
    render_metric_card,
    render_error_message
)
from services.prolog_engine import get_prolog_engine
from services.result_formatter import parse_prolog_atom

setup_page("Basis Pengetahuan", icon="📚", admin_only=True)

engine = get_prolog_engine()

if not engine.is_loaded:
    render_error_message(f"Knowledge Base SWI-Prolog tidak tersedia: {engine.error_message}")
    st.stop()

# ==============================================================================
# HERO BANNER
# ==============================================================================
render_hero(
    title="Basis Pengetahuan & Aturan Logika Orde Pertama",
    subtitle="Pusat inspeksi fakta hardware, evaluasi aturan predikat cocok_untuk/2, dan konsol eksekusi query interaktif SWI-Prolog.",
    badge_text="KNOWLEDGE BASE AUDIT",
    role="ADMINISTRATOR PRIVILEGED"
)

# ==============================================================================
# TABS INTERFACE (GLOWING ACID LIME ACTIVE HIGHLIGHT)
# ==============================================================================
tab_laptop, tab_aturan, tab_prolog = st.tabs([
    "💾 Basis Data Fakta Laptop",
    "⚙️ Aturan Inferensi & Klasifikasi",
    "🔍 Konsol Query Prolog (REPL)"
])

# ------------------------------------------------------------------------------
# TAB 1: DATA LAPTOP
# ------------------------------------------------------------------------------
with tab_laptop:
    kb_header_html = """
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
<div>
<h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #f8f9fa;">💾 Fakta Spesifikasi Laptop (Knowledge Base)</h3>
<p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #9ea3c0;">
Data fakta <code>spesifikasi(ID, Merk, Model, CPU, RAM, Storage, VGA, Harga)</code> yang terdaftar dalam berkas <code>knowledge_base.pl</code>.
</p>
</div>
</div>
"""
    st.markdown(clean_html(kb_header_html), unsafe_allow_html=True)
    
    # Filter Card Container
    col_f1, col_f2 = st.columns([2.5, 1.5])
    with col_f1:
        merks = ['Semua Merek', 'apple', 'asus', 'lenovo', 'acer', 'hp', 'msi']
        filter_merk = st.selectbox(
            "Filter Merek Laptop:",
            options=merks,
            format_func=lambda x: f"🏷️ {x.upper()}" if x != 'Semua Merek' else "🌐 SEMUA MEREK"
        )
    with col_f2:
        sort_choice = st.selectbox(
            "Urutkan Berdasarkan:",
            ["Harga Terendah", "Harga Tertinggi", "RAM Terbesar", "Storage Terbesar"]
        )
    
    try:
        if filter_merk == 'Semua Merek':
            query = "spesifikasi(ID, Merk, Model, CPU, RAM, Storage, VGA, Harga)"
        else:
            query = f"spesifikasi(ID, {filter_merk}, Model, CPU, RAM, Storage, VGA, Harga)"
        
        results = engine.query(query)
        
        if results:
            data = []
            for r in results:
                data.append({
                    "ID": str(r['ID']),
                    "Merek": parse_prolog_atom(r.get('Merk', '')).upper() if filter_merk == 'Semua Merek' else filter_merk.upper(),
                    "Model": parse_prolog_atom(r['Model']),
                    "CPU": parse_prolog_atom(r['CPU']),
                    "RAM (GB)": int(r['RAM']),
                    "Storage (GB)": int(r['Storage']),
                    "GPU/VGA": parse_prolog_atom(r['VGA']),
                    "Harga (Juta Rp)": int(r['Harga']),
                })
            
            df = pd.DataFrame(data)

            # Sort data
            if sort_choice == "Harga Terendah":
                df = df.sort_values(by="Harga (Juta Rp)", ascending=True)
            elif sort_choice == "Harga Tertinggi":
                df = df.sort_values(by="Harga (Juta Rp)", ascending=False)
            elif sort_choice == "RAM Terbesar":
                df = df.sort_values(by="RAM (GB)", ascending=False)
            elif sort_choice == "Storage Terbesar":
                df = df.sort_values(by="Storage (GB)", ascending=False)
            
            # Metric Summary Cards
            m1, m2, m3 = st.columns(3)
            with m1:
                render_metric_card("Total Unit Ditampilkan", len(df), icon="💻", caption="Fakta aktif terfilter")
            with m2:
                render_metric_card("Rentang Harga Terendah", f"Rp {df['Harga (Juta Rp)'].min()} Jt", icon="🏷️", caption="Harga minimum database")
            with m3:
                render_metric_card("Rentang Harga Tertinggi", f"Rp {df['Harga (Juta Rp)'].max()} Jt", icon="💎", caption="Harga flagship database")

            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

            # Styled Dataframe
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Harga (Juta Rp)": st.column_config.NumberColumn(
                        label="Estimasi Harga",
                        format="Rp %d.000.000"
                    ),
                    "RAM (GB)": st.column_config.NumberColumn(label="RAM", format="%d GB"),
                    "Storage (GB)": st.column_config.NumberColumn(label="SSD", format="%d GB"),
                }
            )
        else:
            st.warning("⚠️ Tidak ada fakta spesifikasi yang cocok dengan filter.")
            
    except Exception as e:
        render_error_message(f"Gagal mengambil fakta spesifikasi: {e}")

# ------------------------------------------------------------------------------
# TAB 2: ATURAN KECOCOKAN & KLASIFIKASI
# ------------------------------------------------------------------------------
with tab_aturan:
    rule_header_html = """
<div style="margin-bottom: 1.25rem;">
<h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #f8f9fa;">⚙️ Aturan Inferensi Logika Orde Pertama</h3>
<p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #9ea3c0;">
Aturan predikat <code>cocok_untuk/2</code> dan <code>kelas_laptop/2</code> yang mengontrol penalaran sistem pakar.
</p>
</div>
"""
    st.markdown(clean_html(rule_header_html), unsafe_allow_html=True)
    
    kategori_info = [
        {
            "Kategori": "office",
            "Label": "Kuliah Umum & Produktivitas",
            "Predikat": "cocok_untuk(ID, office)",
            "Kondisi": "Semua laptop memenuhi syarat tanpa filter tambahan",
            "RuleProlog": "cocok_untuk(ID, office) :-\n    spesifikasi(ID, _, _, _, _, _, _, _)."
        },
        {
            "Kategori": "koding",
            "Label": "Pemrograman & Software Engineering",
            "Predikat": "cocok_untuk(ID, koding)",
            "Kondisi": "RAM >= 8 GB (mencukupi untuk IDE, runtime, docker dasar)",
            "RuleProlog": "cocok_untuk(ID, koding) :-\n    spesifikasi(ID, _, _, _, RAM, _, _, _),\n    RAM >= 8."
        },
        {
            "Kategori": "editing_ringan",
            "Label": "Desain Grafis Ringan (Canva, Figma)",
            "Predikat": "cocok_untuk(ID, editing_ringan)",
            "Kondisi": "RAM >= 8 GB dan Harga >= Rp 7 Juta",
            "RuleProlog": "cocok_untuk(ID, editing_ringan) :-\n    spesifikasi(ID, _, _, _, RAM, _, _, Harga),\n    RAM >= 8,\n    Harga >= 7."
        },
        {
            "Kategori": "editing_berat",
            "Label": "Desain & Multimedia Berat (4K / 3D)",
            "Predikat": "cocok_untuk(ID, editing_berat)",
            "Kondisi": "RAM >= 16 GB dan GPU Dedicated (RTX / RX / Apple / Arc)",
            "RuleProlog": "cocok_untuk(ID, editing_berat) :-\n    spesifikasi(ID, _, _, _, RAM, _, VGA, _),\n    RAM >= 16,\n    (sub_atom(VGA, _, _, _, 'RTX') ;\n     sub_atom(VGA, _, _, _, 'Apple') ;\n     sub_atom(VGA, _, _, _, 'RX 6') ;\n     sub_atom(VGA, _, _, _, 'Arc'))."
        },
        {
            "Kategori": "gaming",
            "Label": "Gaming Kompetitif & AAA",
            "Predikat": "cocok_untuk(ID, gaming)",
            "Kondisi": "GPU dedicated (NVIDIA RTX/GTX atau AMD RX)",
            "RuleProlog": "cocok_untuk(ID, gaming) :-\n    spesifikasi(ID, _, _, _, _, _, VGA, _),\n    (sub_atom(VGA, _, _, _, 'RTX') ;\n     sub_atom(VGA, _, _, _, 'GTX') ;\n     sub_atom(VGA, _, _, _, 'RX'))."
        },
        {
            "Kategori": "streaming",
            "Label": "Gaming Sambil Live Streaming (OBS)",
            "Predikat": "cocok_untuk(ID, streaming)",
            "Kondisi": "RAM >= 16 GB dan GPU RTX atau RX (Hardware Encoder NVENC/AMF)",
            "RuleProlog": "cocok_untuk(ID, streaming) :-\n    spesifikasi(ID, _, _, _, RAM, _, VGA, _),\n    RAM >= 16,\n    (sub_atom(VGA, _, _, _, 'RTX') ;\n     sub_atom(VGA, _, _, _, 'RX'))."
        },
        {
            "Kategori": "data_science",
            "Label": "Data Science & Machine Learning",
            "Predikat": "cocok_untuk(ID, data_science)",
            "Kondisi": "RAM >= 16 GB dan CPU performa tinggi (bukan Celeron/N40)",
            "RuleProlog": "cocok_untuk(ID, data_science) :-\n    spesifikasi(ID, _, _, CPU, RAM, _, _, _),\n    RAM >= 16,\n    \\+ sub_atom(CPU, _, _, _, 'Celeron'),\n    \\+ sub_atom(CPU, _, _, _, 'N40')."
        },
        {
            "Kategori": "virtualisasi",
            "Label": "Jaringan Komputer & Virtual Machine",
            "Predikat": "cocok_untuk(ID, virtualisasi)",
            "Kondisi": "RAM >= 16 GB (alokasi memori dedicated host + guest OS)",
            "RuleProlog": "cocok_untuk(ID, virtualisasi) :-\n    spesifikasi(ID, _, _, _, RAM, _, _, _),\n    RAM >= 16."
        },
    ]
    
    # 2 Kolom untuk menampilkan rule cards
    for idx in range(0, len(kategori_info), 2):
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            info1 = kategori_info[idx]
            with st.expander(f"🔹 **{info1['Label']}** (`{info1['Kategori']}`)", expanded=False):
                st.markdown(f"**Predikat:** `{info1['Predikat']}`")
                st.markdown(f"**Kondisi Hardware:** {info1['Kondisi']}")
                st.code(info1['RuleProlog'], language="prolog")
                try:
                    count_q1 = f"findall(ID, cocok_untuk(ID, {info1['Kategori']}), IDs), length(IDs, N)"
                    r1 = engine.query_once(count_q1)
                    if r1:
                        st.markdown(f"<span style='color: #dee263; font-weight: 700; font-family: JetBrains Mono;'>✔ Terpenuhi oleh {r1['N']} unit laptop</span>", unsafe_allow_html=True)
                except Exception:
                    pass

        with col_r2:
            if idx + 1 < len(kategori_info):
                info2 = kategori_info[idx + 1]
                with st.expander(f"🔹 **{info2['Label']}** (`{info2['Kategori']}`)", expanded=False):
                    st.markdown(f"**Predikat:** `{info2['Predikat']}`")
                    st.markdown(f"**Kondisi Hardware:** {info2['Kondisi']}")
                    st.code(info2['RuleProlog'], language="prolog")
                    try:
                        count_q2 = f"findall(ID, cocok_untuk(ID, {info2['Kategori']}), IDs), length(IDs, N)"
                        r2 = engine.query_once(count_q2)
                        if r2:
                            st.markdown(f"<span style='color: #dee263; font-weight: 700; font-family: JetBrains Mono;'>✔ Terpenuhi oleh {r2['N']} unit laptop</span>", unsafe_allow_html=True)
                    except Exception:
                        pass
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    klas_header_html = """
<div class="saas-card">
<h4 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; font-weight: 800; color: #f8f9fa;">🏷️ Aturan Partisi Kelas Anggaran (Plafon Finansial)</h4>
<p style="color: #9ea3c0; font-size: 0.85rem; margin-bottom: 0.75rem;">
Klasifikasi rentang harga <code>kelas_laptop/2</code> membagi laptop ke dalam 4 domain harga terpisah.
</p>
</div>
"""
    st.markdown(clean_html(klas_header_html), unsafe_allow_html=True)

    st.code("""
% Partisi Kelas Anggaran Mahasiswa
kelas_laptop(ID, entry)    :- spesifikasi(ID, _, _, _, _, _, _, Harga), Harga < 10.
kelas_laptop(ID, midrange) :- spesifikasi(ID, _, _, _, _, _, _, Harga), Harga >= 10, Harga < 20.
kelas_laptop(ID, high_end) :- spesifikasi(ID, _, _, _, _, _, _, Harga), Harga >= 20, Harga < 35.
kelas_laptop(ID, flagship) :- spesifikasi(ID, _, _, _, _, _, _, Harga), Harga >= 35.
    """, language="prolog")

# ------------------------------------------------------------------------------
# TAB 3: KONSOL QUERY PROLOG (REPL INTERAKTIF)
# ------------------------------------------------------------------------------
with tab_prolog:
    repl_header_html = """
<div style="margin-bottom: 1.25rem;">
<h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #f8f9fa;">🔍 SWI-Prolog Interactive Execution Terminal</h3>
<p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #9ea3c0;">
Ketik predikat Prolog dan jalankan evaluasi query resolusi secara langsung. Dilindungi sandboxing query read-only.
</p>
</div>
"""
    st.markdown(clean_html(repl_header_html), unsafe_allow_html=True)
    
    contoh_queries = [
        "Pilih contoh query predikat...",
        "jumlah_laptop(N)",
        "laptop_cocok(office, entry, Merk, Model, Harga)",
        "rekomendasi_ideal(koding, midrange, Merk, Model, RAM, VGA, Harga)",
        "rekomendasi_ideal(gaming, midrange, Merk, Model, RAM, VGA, Harga)",
        "rekomendasi_ideal(editing_berat, high_end, Merk, Model, RAM, VGA, Harga)",
        "rekomendasi_ideal(data_science, midrange, Merk, Model, RAM, VGA, Harga)",
        "cocok_untuk(asus_tuf_a15_4050, gaming)",
        "spesifikasi_minimum(koding, SpesMin)",
        "alasan_rekomendasi(lenovo_ip_5, koding, Alasan)",
    ]
    
    selected_example = st.selectbox("Preset Query Contoh:", contoh_queries)
    
    default_text = selected_example if selected_example != contoh_queries[0] else ""
    query_input = st.text_area(
        "Kueri Goal Prolog:",
        value=default_text,
        height=85,
        placeholder="Contoh: rekomendasi_ideal(koding, midrange, Merk, Model, RAM, VGA, Harga)"
    )
    
    FORBIDDEN_TERMS = ['assert', 'retract', 'abolish', 'halt', 'shell', 'process_create']
    
    col_run, col_clean = st.columns([3, 1])
    with col_run:
        btn_run = st.button("▶️ Eksekusi Goal Prolog", type="primary", use_container_width=True)
        
    if btn_run:
        if not query_input.strip():
            st.warning("⚠️ Masukkan predikat query terlebih dahulu.")
        elif any(term in query_input.lower() for term in FORBIDDEN_TERMS):
            st.error("🚫 Keamanan: Query mengandung perintah mutasi yang dilarang.")
        else:
            with st.spinner("Mengevaluasi goal pada mesin SWI-Prolog..."):
                try:
                    results = engine.query(query_input.strip())
                    
                    if not results:
                        false_box_html = """
<div style="background-color: rgba(15, 17, 26, 0.9); border: 1px solid rgba(80, 87, 159, 0.4); border-radius: 12px; padding: 1.25rem; font-family: 'JetBrains Mono', monospace; color: #9ea3c0;">
?- false. // Query berhasil dievaluasi tetapi tidak ada unifikasi yang valid.
</div>
"""
                        st.markdown(clean_html(false_box_html), unsafe_allow_html=True)
                    else:
                        sol_header_html = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
<span style="font-size: 0.9rem; font-weight: 700; color: #dee263;">✔ Ditemukan {len(results)} Solusi Unifikasi</span>
<span style="font-size: 0.75rem; color: #9ea3c0; font-family: 'JetBrains Mono', monospace;">STATUS: SUCCESS</span>
</div>
"""
                        st.markdown(clean_html(sol_header_html), unsafe_allow_html=True)
                        
                        # Terminal IDE Output Box
                        st.markdown('<div style="background-color: rgba(15, 17, 26, 0.95); border: 1px solid rgba(80, 87, 159, 0.4); border-radius: 12px; padding: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
                        
                        for i, r in enumerate(results[:20], 1):
                            if r:
                                st.json({
                                    k: str(v) if hasattr(v, 'decode') else v
                                    for k, v in r.items()
                                })
                            else:
                                st.markdown(f"<span style='color: #dee263; font-family: JetBrains Mono;'>Solusi {i}: true.</span>", unsafe_allow_html=True)
                                
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        if len(results) > 20:
                            st.caption(f"Menampilkan 20 hasil teratas dari total {len(results)} unifikasi.")
                            
                except Exception as e:
                    render_error_message(f"Error saat mengeksekusi query: {e}")
