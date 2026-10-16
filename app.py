"""
app.py — Entry Point LaptopExpert (Enterprise SaaS Dark Login)
"""
import streamlit as st
from services.auth_service import login, set_session, is_authenticated
from services.ui_theme import inject_custom_css, clean_html

st.set_page_config(
    page_title="LaptopExpert — Masuk ke Sistem",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Injeksi CSS Design System Global
inject_custom_css()

# Custom Styling Khusus Halaman Login SaaS
st.markdown("""
<style>
[data-testid="collapsedControl"] {display: none;}

.login-container {
    max-width: 460px;
    margin: 1.5rem auto;
    background: #131622;
    border: 1px solid rgba(80, 87, 159, 0.4);
    border-radius: 24px;
    padding: 2.5rem 2.25rem;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6), 0 0 20px rgba(80, 87, 159, 0.15);
}

.brand-avatar {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, #50579f 0%, #3e4482 100%);
    border: 1px solid rgba(222, 226, 99, 0.5);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin: 0 auto 1.25rem auto;
    box-shadow: 0 0 24px rgba(80, 87, 159, 0.5);
}
</style>
""", unsafe_allow_html=True)

# Jika sudah login langsung alihkan ke Dashboard
if is_authenticated():
    st.switch_page("pages/1_Dashboard.py")

col1, col2, col3 = st.columns([0.5, 3, 0.5])

with col2:
    login_header_html = """
<div style="text-align: center; padding: 1rem 0 1.25rem 0;">
<div class="brand-avatar">💻</div>
<h2 style="margin: 0; font-size: 2rem; font-weight: 800; color: #f8f9fa; letter-spacing: -0.025em;">LaptopExpert</h2>
<p style="color: #9ea3c0; font-size: 0.95rem; margin-top: 6px;">Sistem Pakar Rekomendasi Laptop Mahasiswa</p>
<div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(222, 226, 99, 0.12); color: #dee263; border: 1px solid rgba(222, 226, 99, 0.4); font-size: 0.75rem; font-weight: 800; padding: 4px 14px; border-radius: 9999px; letter-spacing: 0.04em;">
<span style="width: 6px; height: 6px; border-radius: 50%; background: #dee263;"></span>
SWI-PROLOG ENGINE v10.0
</div>
</div>
"""
    st.markdown(clean_html(login_header_html), unsafe_allow_html=True)
    
    with st.form("login_form_saas", clear_on_submit=False):
        st.markdown("<p style='font-weight: 700; color: #f8f9fa; font-size: 0.95rem; margin-bottom: 0.75rem;'>Autentikasi Pengguna</p>", unsafe_allow_html=True)
        
        username = st.text_input(
            "Username",
            placeholder="Masukkan username (cth: mahasiswa / admin)",
            key="login_username"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Masukkan password",
            key="login_password"
        )
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🚀 Masuk ke Dashboard",
            use_container_width=True,
            type="primary"
        )
    
    if submitted:
        if not username or not password:
            st.error("⚠️ Username dan password wajib diisi.")
        else:
            with st.spinner("Memverifikasi kredensial sistem pakar..."):
                berhasil, role, nama = login(username, password)
            
            if berhasil:
                set_session(username.strip().lower(), role, nama)
                st.success(f"✅ Berhasil masuk! Selamat datang, {nama}.")
                st.rerun()
            else:
                st.error("❌ Kredensial tidak valid. Silakan periksa kembali kombinasi username dan password.")
    
    # Petunjuk Kredensial Demo SaaS
    demo_creds_html = """
<div style="background: rgba(15, 17, 26, 0.85); border: 1px dashed rgba(80, 87, 159, 0.5); border-radius: 14px; padding: 14px 16px; margin-top: 1.5rem; font-size: 0.82rem; color: #9ea3c0;">
<strong style="color: #dee263;">🔑 Akun Pengujian Demo:</strong><br>
<div style="margin-top: 6px; line-height: 1.6;">
• <strong>Mahasiswa:</strong> <code style="color: #dee263; background: #131622;">mahasiswa</code> / <code style="color: #dee263; background: #131622;">user123</code><br>
• <strong>Administrator:</strong> <code style="color: #dee263; background: #131622;">admin</code> / <code style="color: #dee263; background: #131622;">admin123</code>
</div>
</div>
"""
    st.markdown(clean_html(demo_creds_html), unsafe_allow_html=True)
