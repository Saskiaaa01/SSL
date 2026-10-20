/**
 * SSLGuard 🛡️ — Frontend Controller & Interactive Engine
 * Versi 1.0 | PKL 2026 KOMINFO
 */

// ============================================================================
// DATA STATE (MOCK INVENTARIS DOMAIN REALISTIS)
// ============================================================================
let websites = [
  {
    id: "w1",
    domain: "portal.dinas.go.id",
    port: 443,
    owner: "Diskominfo",
    daysRemaining: 3,
    status: "CRITICAL_7",
    issuer: "Let's Encrypt Authority R3",
    validFrom: "2026-07-28",
    expiresAt: "2026-10-23",
    lastChecked: "5 menit yang lalu",
    fingerprint: "8C:64:1D:4B:92:07:95:EA:3A:41:8F:D2:C3:48:9A:F0:22:15:37:EB",
    cn: "*.dinas.go.id",
    sans: "portal.dinas.go.id, *.dinas.go.id, dinas.go.id",
    serial: "04:3a:9e:12:87:6b:15:c2",
    keyInfo: "RSA 2048 bit (SHA256withRSA)",
    chainValid: true,
    hostnameMatch: true
  },
  {
    id: "w2",
    domain: "jdih.kota.go.id",
    port: 443,
    owner: "Bagian Hukum",
    daysRemaining: 12,
    status: "WARNING_14",
    issuer: "Google Trust Services LLC",
    validFrom: "2026-08-03",
    expiresAt: "2026-11-01",
    lastChecked: "18 menit yang lalu",
    fingerprint: "3A:9F:88:C1:44:B0:18:22:90:5E:AA:77:23:44:11:09:BB:66:77:88",
    cn: "jdih.kota.go.id",
    sans: "jdih.kota.go.id, hukum.kota.go.id",
    serial: "12:bb:44:aa:66:cc:01:89",
    keyInfo: "ECDSA 256 bit (SHA256withECDSA)",
    chainValid: true,
    hostnameMatch: true
  },
  {
    id: "w3",
    domain: "bkpsdm.kab.go.id",
    port: 443,
    owner: "BKPSDM",
    daysRemaining: 25,
    status: "WARNING_30",
    issuer: "Sectigo RSA Domain Validation Secure Server CA",
    validFrom: "2025-11-15",
    expiresAt: "2026-11-14",
    lastChecked: "42 menit yang lalu",
    fingerprint: "5B:44:99:11:AA:FF:EE:88:22:66:11:99:33:44:55:66:77:88:99:00",
    cn: "bkpsdm.kab.go.id",
    sans: "bkpsdm.kab.go.id, simpeg.kab.go.id",
    serial: "55:88:99:aa:bb:cc:dd:ee",
    keyInfo: "RSA 2048 bit (SHA256withRSA)",
    chainValid: true,
    hostnameMatch: true
  },
  {
    id: "w4",
    domain: "dinkes.kotakab.go.id",
    port: 443,
    owner: "Dinas Kesehatan",
    daysRemaining: 185,
    status: "VALID",
    issuer: "DigiCert Global Root G2",
    validFrom: "2026-04-20",
    expiresAt: "2027-04-23",
    lastChecked: "1 jam yang lalu",
    fingerprint: "99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88:99:AA:BB:CC",
    cn: "*.kotakab.go.id",
    sans: "dinkes.kotakab.go.id, *.kotakab.go.id",
    serial: "09:11:22:33:44:55:66:77",
    keyInfo: "RSA 2048 bit (SHA256withRSA)",
    chainValid: true,
    hostnameMatch: true
  },
  {
    id: "w5",
    domain: "dispendukcapil.kab.go.id",
    port: 443,
    owner: "Dispendukcapil",
    daysRemaining: 92,
    status: "VALID",
    issuer: "Let's Encrypt Authority R3",
    validFrom: "2026-07-22",
    expiresAt: "2027-01-20",
    lastChecked: "2 jam yang lalu",
    fingerprint: "11:22:33:44:55:66:77:88:99:00:AA:BB:CC:DD:EE:FF:11:22:33:44",
    cn: "dispendukcapil.kab.go.id",
    sans: "dispendukcapil.kab.go.id, kependudukan.kab.go.id",
    serial: "44:55:66:77:88:99:aa:bb",
    keyInfo: "RSA 2048 bit (SHA256withRSA)",
    chainValid: true,
    hostnameMatch: true
  },
  {
    id: "w6",
    domain: "kecamatan-barat.kab.go.id",
    port: 443,
    owner: "Kecamatan Kota",
    daysRemaining: 64,
    status: "VALID",
    issuer: "ZeroSSL RSA Domain Secure CA",
    validFrom: "2026-06-25",
    expiresAt: "2026-12-23",
    lastChecked: "3 jam yang lalu",
    fingerprint: "FF:EE:DD:CC:BB:AA:00:99:88:77:66:55:44:33:22:11:00:AA:BB:CC",
    cn: "kecamatan-barat.kab.go.id",
    sans: "kecamatan-barat.kab.go.id",
    serial: "77:88:99:aa:bb:cc:dd:11",
    keyInfo: "RSA 2048 bit (SHA256withRSA)",
    chainValid: true,
    hostnameMatch: true
  },
  {
    id: "w7",
    domain: "rsud.kotakab.go.id",
    port: 443,
    owner: "Dinas Kesehatan",
    daysRemaining: -4,
    status: "EXPIRED",
    issuer: "Let's Encrypt Authority R3",
    validFrom: "2026-04-18",
    expiresAt: "2026-10-16",
    lastChecked: "12 menit yang lalu",
    fingerprint: "EE:AA:77:11:44:99:22:55:88:33:11:00:BB:CC:DD:EE:FF:11:22:33",
    cn: "rsud.kotakab.go.id",
    sans: "rsud.kotakab.go.id",
    serial: "99:11:aa:22:bb:33:cc:44",
    keyInfo: "RSA 2048 bit (SHA256withRSA)",
    chainValid: false,
    hostnameMatch: true
  },
  {
    id: "w8",
    domain: "internal.layanan.kominfo.go.id",
    port: 443,
    owner: "Diskominfo",
    daysRemaining: null,
    status: "FAILED",
    issuer: "Tidak Diketahui",
    validFrom: "-",
    expiresAt: "-",
    lastChecked: "7 menit yang lalu",
    fingerprint: "-",
    cn: "-",
    sans: "-",
    serial: "-",
    keyInfo: "-",
    chainValid: false,
    hostnameMatch: false,
    errorMessage: "Connection Timeout / Host Unreachable"
  }
];

// DATA NOTIFIKASI WHATSAPP LOGS
let notificationLogs = [
  {
    id: "log1",
    time: "2026-10-20 07:01:14 WIB",
    domain: "portal.dinas.go.id",
    recipient: "Budi Santoso (Owner Diskominfo)",
    phone: "+6281234567890",
    threshold: "H-7 (Kritis)",
    providerId: "wamid.HBgLMTYyODEx...",
    status: "READ"
  },
  {
    id: "log2",
    time: "2026-10-20 07:01:15 WIB",
    domain: "portal.dinas.go.id",
    recipient: "Admin KOMINFO (Pengawas Pusat)",
    phone: "+6281198765432",
    threshold: "H-7 (Kritis)",
    providerId: "wamid.HBgLMTYyODIy...",
    status: "DELIVERED"
  },
  {
    id: "log3",
    time: "2026-10-20 07:02:05 WIB",
    domain: "jdih.kota.go.id",
    recipient: "Siti Rahma (Owner Bagian Hukum)",
    phone: "+6281345678901",
    threshold: "H-14 (Lanjutan)",
    providerId: "wamid.HBgLMTYyODMz...",
    status: "DELIVERED"
  },
  {
    id: "log4",
    time: "2026-10-20 07:02:30 WIB",
    domain: "bkpsdm.kab.go.id",
    recipient: "Agus Pratama (Owner BKPSDM)",
    phone: "+6281987654321",
    threshold: "H-30 (Awal)",
    providerId: "wamid.HBgLMTYyODQ0...",
    status: "READ"
  }
];

// DATA USERS & ROLE
let users = [
  {
    id: "u1",
    name: "Admin KOMINFO",
    email: "admin@kominfo.go.id",
    phone: "+6281198765432",
    role: "Super Admin",
    domainsCount: "Semua (8)",
    status: "Aktif"
  },
  {
    id: "u2",
    name: "Budi Santoso",
    email: "budi@dinas.go.id",
    phone: "+6281234567890",
    role: "Owner (Diskominfo)",
    domainsCount: "2 Domain",
    status: "Aktif"
  },
  {
    id: "u3",
    name: "Siti Rahma",
    email: "siti@hukum.kota.go.id",
    phone: "+6281345678901",
    role: "Owner (Bag. Hukum)",
    domainsCount: "1 Domain",
    status: "Aktif"
  },
  {
    id: "u4",
    name: "Agus Pratama",
    email: "agus@bkpsdm.kab.go.id",
    phone: "+6281987654321",
    role: "Owner (BKPSDM)",
    domainsCount: "1 Domain",
    status: "Aktif"
  }
];

// ============================================================================
// AUTHENTICATION & USER SESSION STATE
// ============================================================================
const DEMO_USERS = {
  "admin@kominfo.go.id": {
    id: "u1",
    name: "Admin KOMINFO",
    email: "admin@kominfo.go.id",
    role: "admin",
    roleLabel: "Super Administrator",
    avatar: "AD",
    department: null // akses seluruh domain
  },
  "budi@dinas.go.id": {
    id: "u2",
    name: "Budi Santoso",
    email: "budi@dinas.go.id",
    role: "owner",
    roleLabel: "Owner (Diskominfo)",
    avatar: "BS",
    department: "Diskominfo"
  },
  "siti@hukum.kota.go.id": {
    id: "u3",
    name: "Siti Rahma",
    email: "siti@hukum.kota.go.id",
    role: "owner",
    roleLabel: "Owner (Bagian Hukum)",
    avatar: "SR",
    department: "Bagian Hukum"
  }
};

let currentUser = JSON.parse(localStorage.getItem("sslguard_user")) || null;

// ============================================================================
// INITIALIZATION & EVENT LISTENERS
// ============================================================================
document.addEventListener("DOMContentLoaded", () => {
  initLiveClock();
  initAuth();
  initNavigation();
  initModals();
  initFilters();

  if (currentUser) {
    applyUserSession(currentUser);
  } else {
    showLoginScreen();
  }
});


// ============================================================================
// LIVE CLOCK
// ============================================================================
function initLiveClock() {
  const clockEl = document.getElementById("live-time");
  function updateTime() {
    const now = new Date();
    const options = { 
      weekday: 'short', 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric', 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit',
      timeZoneName: 'short' 
    };
    clockEl.textContent = now.toLocaleDateString('id-ID', options);
  }
  updateTime();
  setInterval(updateTime, 1000);
}

// ============================================================================
// AUTHENTICATION CONTROLLER (LOGIN, DEMO & LOGOUT)
// ============================================================================
function showLoginScreen() {
  document.getElementById("auth-wrapper").classList.remove("hidden");
  document.getElementById("app-layout").style.display = "none";
}

function applyUserSession(user) {
  currentUser = user;
  localStorage.setItem("sslguard_user", JSON.stringify(user));

  document.getElementById("auth-wrapper").classList.add("hidden");
  document.getElementById("app-layout").style.display = "flex";

  // Update Sidebar Profile
  document.getElementById("sidebar-avatar").textContent = user.avatar || "U";
  document.getElementById("sidebar-user-name").textContent = user.name;
  document.getElementById("sidebar-user-role").textContent = user.roleLabel;

  // Role-Based UI Elements Visibility (RBAC)
  const adminLabel = document.getElementById("section-admin-label");
  const navUsers = document.getElementById("nav-users");

  if (user.role === "admin") {
    if (adminLabel) adminLabel.style.display = "block";
    if (navUsers) navUsers.style.display = "flex";
  } else {
    // Owner role: Sembunyikan menu Pengguna & Role
    if (adminLabel) adminLabel.style.display = "none";
    if (navUsers) navUsers.style.display = "none";
  }

  // Render components according to role
  renderDashboard();
  renderWebsitesTable();
  renderNotificationsTable();
  renderUsersTable();
}

function initAuth() {
  const formLogin = document.getElementById("form-login");
  const inputEmail = document.getElementById("login-email");
  const inputPassword = document.getElementById("login-password");
  const errorBanner = document.getElementById("login-error-banner");
  const btnTogglePw = document.getElementById("btn-toggle-pw");
  const btnLogout = document.getElementById("btn-logout");
  const btnForgot = document.getElementById("btn-forgot-password");

  // Toggle Password Visibility
  if (btnTogglePw) {
    btnTogglePw.addEventListener("click", () => {
      const type = inputPassword.getAttribute("type") === "password" ? "text" : "password";
      inputPassword.setAttribute("type", type);
    });
  }

  // Forgot Password Prompt
  if (btnForgot) {
    btnForgot.addEventListener("click", () => {
      showToast("Silakan hubungi Administrator KOMINFO di ruang NOC untuk reset kata sandi.", "info");
    });
  }

  // Login Form Submission
  if (formLogin) {
    formLogin.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = inputEmail.value.trim().toLowerCase();
      const password = inputPassword.value;

      errorBanner.classList.add("hidden");
      const btnSubmit = document.getElementById("btn-submit-login");
      btnSubmit.disabled = true;
      btnSubmit.innerHTML = `<span>Logging in...</span>`;

      setTimeout(() => {
        btnSubmit.disabled = false;
        btnSubmit.innerHTML = `Login`;

        // Check against demo accounts (email atau username pendek)
        let matchedUser = DEMO_USERS[email];
        if (!matchedUser) {
          if (email === "admin") matchedUser = DEMO_USERS["admin@kominfo.go.id"];
          else if (email === "budi") matchedUser = DEMO_USERS["budi@dinas.go.id"];
          else if (email === "siti") matchedUser = DEMO_USERS["siti@hukum.kota.go.id"];
        }

        if (matchedUser) {
          applyUserSession(matchedUser);
          showToast(`Selamat datang kembali, ${matchedUser.name}!`, "success");
        } else if (email.endsWith("@kominfo.go.id")) {
          // Fallback auto-grant admin for kominfo.go.id
          const newAdmin = {
            id: "u_custom",
            name: email.split("@")[0].toUpperCase(),
            email: email,
            role: "admin",
            roleLabel: "Administrator",
            avatar: email.substring(0, 2).toUpperCase(),
            department: null
          };
          applyUserSession(newAdmin);
          showToast(`Login berhasil sebagai Administrator!`, "success");
        } else {
          errorBanner.textContent = "Username / email atau kata sandi tidak cocok.";
          errorBanner.classList.remove("hidden");
        }
      }, 500);
    });
  }

  // Register Link Handler
  const linkRegister = document.getElementById("link-register");
  if (linkRegister) {
    linkRegister.addEventListener("click", () => {
      showToast("Pendaftaran akun pengguna baru dikelola secara terpusat oleh Administrator KOMINFO.", "info");
    });
  }

  // Logout Button Handler
  if (btnLogout) {
    btnLogout.addEventListener("click", () => {
      if (confirm("Apakah Anda yakin ingin keluar dari akun ini?")) {
        localStorage.removeItem("sslguard_user");
        currentUser = null;
        showLoginScreen();
        showToast("Anda telah berhasil keluar dari akun (Logout).", "info");
      }
    });
  }
}

// Quick Demo Fill Helper (Global Function)
window.fillDemoAccount = function(type) {
  const inputEmail = document.getElementById("login-email");
  const inputPassword = document.getElementById("login-password");
  const errorBanner = document.getElementById("login-error-banner");
  if (errorBanner) errorBanner.classList.add("hidden");

  if (type === "admin") {
    inputEmail.value = "admin@kominfo.go.id";
    inputPassword.value = "Admin@2026";
  } else if (type === "owner_diskominfo") {
    inputEmail.value = "budi@dinas.go.id";
    inputPassword.value = "Budi@2026";
  } else if (type === "owner_hukum") {
    inputEmail.value = "siti@hukum.kota.go.id";
    inputPassword.value = "Siti@2026";
  }

  showToast(`Akun ${type} dipilih. Klik "Masuk ke Dashboard".`, "info");
};


// ============================================================================
// VIEW NAVIGATION (TAB SWITCHING)
// ============================================================================
function initNavigation() {
  const navItems = document.querySelectorAll(".nav-item");
  const views = document.querySelectorAll(".view-container");
  const pageTitle = document.getElementById("page-title");
  const pageSubtitle = document.getElementById("page-subtitle");

  const titles = {
    dashboard: {
      title: "Executive Dashboard",
      sub: "Ringkasan status inspeksi SSL/TLS seluruh domain instansi binaan KOMINFO"
    },
    websites: {
      title: "Kelola & Monitoring Website",
      sub: "Daftar seluruh domain, status port TLS 443, dan inspeksi langsung on-demand"
    },
    notifications: {
      title: "Log Audit WhatsApp Alert",
      sub: "Riwayat peringatan kedaluwarsa SSL H-30, H-14, H-7 dan status pengiriman Meta"
    },
    users: {
      title: "Manajemen Pengguna & Penanggung Jawab",
      sub: "Pengelolaan akun administrator dan nomor WhatsApp resmi penerima notifikasi"
    }
  };

  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const targetView = item.getAttribute("data-view");

      navItems.forEach(n => n.classList.remove("active"));
      item.classList.add("active");

      views.forEach(v => {
        v.classList.remove("active");
        if (v.id === `view-${targetView}`) {
          v.classList.add("active");
        }
      });

      if (titles[targetView]) {
        pageTitle.textContent = titles[targetView].title;
        pageSubtitle.textContent = titles[targetView].sub;
      }
    });
  });

  // Shortcut from dashboard
  document.getElementById("btn-view-all-websites").addEventListener("click", () => {
    document.getElementById("nav-websites").click();
  });
}

// ============================================================================
// ROLE-BASED ACCESS CONTROL HELPER (RBAC)
// ============================================================================
function getAccessibleWebsites() {
  if (currentUser && currentUser.role === "owner" && currentUser.department) {
    return websites.filter(w => w.owner === currentUser.department);
  }
  return websites;
}

// ============================================================================
// DASHBOARD VIEW LOGIC
// ============================================================================
function renderDashboard() {
  const accessible = getAccessibleWebsites();
  const total = accessible.length;
  const valid = accessible.filter(w => w.status === "VALID").length;
  const warning = accessible.filter(w => w.status === "WARNING_30" || w.status === "WARNING_14").length;
  const critical = accessible.filter(w => w.status === "CRITICAL_7" || w.status === "EXPIRED" || w.status === "FAILED").length;

  document.getElementById("stat-total-domains").textContent = total;
  document.getElementById("sidebar-domain-count").textContent = total;
  document.getElementById("stat-valid-domains").textContent = valid;
  document.getElementById("stat-warning-domains").textContent = warning;
  document.getElementById("stat-critical-domains").textContent = critical;

  // Urgent list
  const urgentContainer = document.getElementById("urgent-domains-container");
  urgentContainer.innerHTML = "";

  const urgentItems = accessible
    .filter(w => w.status === "CRITICAL_7" || w.status === "EXPIRED" || w.status === "WARNING_14" || w.status === "FAILED")
    .sort((a, b) => {
      const da = a.daysRemaining === null ? 999 : a.daysRemaining;
      const db = b.daysRemaining === null ? 999 : b.daysRemaining;
      return da - db;
    });

  if (urgentItems.length === 0) {
    urgentContainer.innerHTML = `<div style="text-align: center; color: var(--text-muted); padding: 20px;">Semua domain berada dalam kondisi aman (>30 hari).</div>`;
    return;
  }

  urgentItems.forEach(item => {
    const el = document.createElement("div");
    el.className = "urgent-item";
    
    let pillClass = "pill-amber";
    let pillText = `${item.daysRemaining} Hari`;

    if (item.status === "EXPIRED") {
      pillClass = "pill-red";
      pillText = `Kedaluwarsa (${Math.abs(item.daysRemaining)}h lalu)`;
    } else if (item.status === "CRITICAL_7") {
      pillClass = "pill-red";
      pillText = `Kritis (${item.daysRemaining} Hari)`;
    } else if (item.status === "FAILED") {
      pillClass = "pill-red";
      pillText = "Koneksi Gagal";
    }

    el.innerHTML = `
      <div class="urgent-domain-meta">
        <span class="urgent-domain-name">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="${item.status === 'EXPIRED' ? '#F43F5E' : '#F59E0B'}" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          ${item.domain}
        </span>
        <span class="urgent-owner-tag">${item.owner} • Port ${item.port}</span>
      </div>
      <div class="urgent-countdown">
        <span class="pill-days ${pillClass}">${pillText}</span>
        <button class="btn btn-outline btn-xs" onclick="inspectWebsiteDetail('${item.id}')">Inspeksi</button>
      </div>
    `;
    urgentContainer.appendChild(el);
  });
}

// ============================================================================
// WEBSITES TABLE LOGIC
// ============================================================================
function renderWebsitesTable(dataToRender = null) {
  const accessible = getAccessibleWebsites();
  const currentList = dataToRender !== null ? dataToRender : accessible;
  const tbody = document.getElementById("tbody-websites");
  tbody.innerHTML = "";

  document.getElementById("table-info-text").textContent = `Menampilkan ${currentList.length} dari ${accessible.length} domain`;

  if (dataToRender.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 30px; color: var(--text-muted);">Tidak ditemukan domain yang sesuai kriteria pencarian.</td></tr>`;
    return;
  }

  dataToRender.forEach(w => {
    const tr = document.createElement("tr");

    let statusBadge = "";
    let daysDisplay = "";

    if (w.status === "VALID") {
      statusBadge = `<span class="status-badge status-valid"><span class="status-indicator online"></span> Valid Aman</span>`;
      daysDisplay = `<span class="pill-days pill-green">${w.daysRemaining} Hari</span>`;
    } else if (w.status === "WARNING_30") {
      statusBadge = `<span class="status-badge status-warning">⚠ Peringatan H-30</span>`;
      daysDisplay = `<span class="pill-days pill-amber">${w.daysRemaining} Hari</span>`;
    } else if (w.status === "WARNING_14") {
      statusBadge = `<span class="status-badge status-warning">⚠ Peringatan H-14</span>`;
      daysDisplay = `<span class="pill-days pill-amber">${w.daysRemaining} Hari</span>`;
    } else if (w.status === "CRITICAL_7") {
      statusBadge = `<span class="status-badge status-critical">⛔ Kritis H-7</span>`;
      daysDisplay = `<span class="pill-days pill-red">${w.daysRemaining} Hari</span>`;
    } else if (w.status === "EXPIRED") {
      statusBadge = `<span class="status-badge status-critical">✖ KEDALUWARSA</span>`;
      daysDisplay = `<span class="pill-days pill-red">Lewat ${Math.abs(w.daysRemaining)}h</span>`;
    } else {
      statusBadge = `<span class="status-badge status-failed">❓ Jaringan Gagal</span>`;
      daysDisplay = `<span class="pill-days" style="color:#94A3B8;">-</span>`;
    }

    tr.innerHTML = `
      <td>
        <div class="cell-domain">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="${w.status === 'VALID' ? '#10B981' : (w.status === 'EXPIRED' ? '#F43F5E' : '#F59E0B')}" stroke-width="2.2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <div>
            <div class="domain-name">${w.domain}</div>
            <span class="domain-port">:${w.port}</span>
          </div>
        </div>
      </td>
      <td><strong>${w.owner}</strong></td>
      <td>${daysDisplay}</td>
      <td>${statusBadge}</td>
      <td class="text-xs">${w.issuer}</td>
      <td class="text-xs text-muted">${w.lastChecked}</td>
      <td class="text-right">
        <div class="action-btns">
          <button class="btn-icon" title="Periksa SSL Sekarang" onclick="triggerManualCheck('${w.id}', this)">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
          </button>
          <button class="btn-icon" title="Lihat Detail Sertifikat x509" onclick="inspectWebsiteDetail('${w.id}')">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
          </button>
          <button class="btn-icon" title="Pratinjau Pesan WA" onclick="previewWAMessage('${w.id}')">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#22C55E" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          </button>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// ============================================================================
// FILTERING & SEARCH
// ============================================================================
function initFilters() {
  const searchInput = document.getElementById("input-search-domain");
  const filterStatus = document.getElementById("filter-status");
  const filterOwner = document.getElementById("filter-owner");

  function applyFilters() {
    const q = searchInput.value.toLowerCase().trim();
    const st = filterStatus.value;
    const ow = filterOwner.value;

    const baseList = getAccessibleWebsites();
    const filtered = baseList.filter(item => {
      const matchSearch = item.domain.toLowerCase().includes(q) || item.owner.toLowerCase().includes(q);
      const matchStatus = (st === "ALL") || (item.status === st);
      const matchOwner = (ow === "ALL") || (item.owner === ow);
      return matchSearch && matchStatus && matchOwner;
    });

    renderWebsitesTable(filtered);
  }

  searchInput.addEventListener("input", applyFilters);
  filterStatus.addEventListener("change", applyFilters);
  filterOwner.addEventListener("change", applyFilters);

  // Export CSV Action
  document.getElementById("btn-export-csv").addEventListener("click", exportMonitoringToCSV);

  // Scan All Action
  document.getElementById("btn-run-all-check").addEventListener("click", scanAllDomains);
}

// ============================================================================
// MANUAL CHECK SIMULATION
// ============================================================================
function triggerManualCheck(websiteId, btnEl) {
  const website = websites.find(w => w.id === websiteId);
  if (!website) return;

  btnEl.classList.add("spinning");
  btnEl.disabled = true;

  showToast(`Melakukan TLS Handshake ke ${website.domain}:${website.port}...`, "info");

  setTimeout(() => {
    btnEl.classList.remove("spinning");
    btnEl.disabled = false;
    website.lastChecked = "Baru saja";

    showToast(`Inspeksi berhasil: ${website.domain} (${website.daysRemaining !== null ? website.daysRemaining + ' hari tersisa' : 'Status: ' + website.status})`, "success");
    renderWebsitesTable();
    renderDashboard();
  }, 1200);
}

function scanAllDomains() {
  const btn = document.getElementById("btn-run-all-check");
  btn.disabled = true;
  btn.innerHTML = `<span>Memindai...</span>`;

  showToast("Menjalankan tugas scheduler otomatis: menginspeksi domain...", "info");

  setTimeout(() => {
    websites.forEach(w => {
      w.lastChecked = "Baru saja";
    });
    btn.disabled = false;
    btn.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
      <span>Scan Semua Domain</span>
    `;
    showToast("Pemindaian massal selesai! Seluruh hasil pemeriksaan & log telah diperbarui.", "success");
    renderWebsitesTable();
    renderDashboard();
  }, 1800);
}

// ============================================================================
// EXPORT CSV FEATURE (REAL GENERATION & DOWNLOAD)
// ============================================================================
function exportMonitoringToCSV() {
  const accessible = getAccessibleWebsites();
  const headers = ["Domain", "Port", "Pemilik_OPD", "Sisa_Hari", "Status", "Penerbit_CA", "Tanggal_Mulai", "Tanggal_Kedaluwarsa", "Fingerprint_SHA256", "Terakhir_Diperiksa"];
  const rows = accessible.map(w => [
    w.domain,
    w.port,
    `"${w.owner}"`,
    w.daysRemaining !== null ? w.daysRemaining : "N/A",
    w.status,
    `"${w.issuer}"`,
    w.validFrom,
    w.expiresAt,
    `"${w.fingerprint}"`,
    `"${w.lastChecked}"`
  ]);

  const csvContent = "data:text/csv;charset=utf-8," 
    + [headers.join(","), ...rows.map(r => r.join(","))].join("\n");

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  const dateStr = new Date().toISOString().split("T")[0];
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `SSLGuard_Report_KOMINFO_${dateStr}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  showToast("Berkas CSV berhasil diekspor dan diunduh!", "success");
}

// ============================================================================
// MODALS LOGIC (ADD DOMAIN WITH SSRF PROTECTION, DETAIL, WA PREVIEW)
// ============================================================================
let currentDetailWebsiteId = null;

function initModals() {
  // Modal Add Domain
  const modalAdd = document.getElementById("modal-add-domain");
  const btnOpenAdd = document.getElementById("btn-open-add-modal");
  const btnCloseAdd = document.getElementById("btn-close-modal-add");
  const btnCancelAdd = document.getElementById("btn-cancel-modal-add");
  const formAdd = document.getElementById("form-add-domain");
  const errorBanner = document.getElementById("modal-add-error");

  btnOpenAdd.addEventListener("click", () => {
    formAdd.reset();
    errorBanner.classList.add("hidden");
    modalAdd.classList.add("open");
  });

  const closeAdd = () => modalAdd.classList.remove("open");
  btnCloseAdd.addEventListener("click", closeAdd);
  btnCancelAdd.addEventListener("click", closeAdd);

  // Form Submission with SSRF Check
  formAdd.addEventListener("submit", (e) => {
    e.preventDefault();
    let rawDomain = document.getElementById("modal-input-domain").value.trim().toLowerCase();
    const port = parseInt(document.getElementById("modal-input-port").value, 10);
    const owner = document.getElementById("modal-select-owner").value;

    // Bersihkan prefix jika ada
    rawDomain = rawDomain.replace(/^https?:\/\//, '').replace(/\/.*$/, '');

    // 1. SSRF PROTECTION VALIDATION TEST
    const restrictedHosts = [
      "localhost", 
      "127.0.0.1", 
      "0.0.0.0", 
      "::1", 
      "169.254.169.254"
    ];

    const isPrivateIP = rawDomain.startsWith("192.168.") || 
                        rawDomain.startsWith("10.") || 
                        rawDomain.startsWith("172.16.") || 
                        rawDomain.endsWith(".local") || 
                        rawDomain.endsWith(".internal");

    if (restrictedHosts.includes(rawDomain) || isPrivateIP) {
      errorBanner.innerHTML = `
        <strong>🚨 BLOKIR KEAMANAN (SSRF DETECTED):</strong><br>
        Domain atau alamat IP <code>${rawDomain}</code> berada dalam rentang terlarang (Localhost / IP Privat / Cloud Metadata). Sistem menolak koneksi demi keamanan jaringan server!
      `;
      errorBanner.classList.remove("hidden");
      return;
    }

    // Success flow
    const newWebsite = {
      id: "w" + (websites.length + 1),
      domain: rawDomain,
      port: port,
      owner: owner,
      daysRemaining: 89,
      status: "VALID",
      issuer: "Let's Encrypt Authority R3",
      validFrom: "2026-10-20",
      expiresAt: "2027-01-17",
      lastChecked: "Baru saja",
      fingerprint: "AA:11:BB:22:CC:33:DD:44:EE:55:FF:66:77:88:99:00:11:22:33:44",
      cn: rawDomain,
      sans: `${rawDomain}, *.${rawDomain}`,
      serial: "77:11:88:22:99:33:00",
      keyInfo: "RSA 2048 bit (SHA256withRSA)",
      chainValid: true,
      hostnameMatch: true
    };

    websites.unshift(newWebsite);
    closeAdd();
    renderWebsitesTable();
    renderDashboard();
    showToast(`Domain ${rawDomain} berhasil didaftarkan dan diinspeksi!`, "success");
    inspectWebsiteDetail(newWebsite.id);
  });

  // Modal Detail
  const modalDetail = document.getElementById("modal-cert-detail");
  const btnCloseDetail = document.getElementById("btn-close-modal-detail");
  const btnCloseDetail2 = document.getElementById("btn-close-detail-modal");
  const btnRecheckCurrent = document.getElementById("btn-recheck-current");

  const closeDetail = () => modalDetail.classList.remove("open");
  btnCloseDetail.addEventListener("click", closeDetail);
  btnCloseDetail2.addEventListener("click", closeDetail);

  btnRecheckCurrent.addEventListener("click", () => {
    if (currentDetailWebsiteId) {
      const item = websites.find(w => w.id === currentDetailWebsiteId);
      if (item) {
        showToast(`Memperbarui sertifikat untuk ${item.domain}...`, "info");
        setTimeout(() => {
          item.lastChecked = "Baru saja";
          showToast(`Sertifikat ${item.domain} berhasil diperiksa ulang!`, "success");
          inspectWebsiteDetail(currentDetailWebsiteId);
          renderWebsitesTable();
        }, 800);
      }
    }
  });

  // Modal WA Preview
  const modalWA = document.getElementById("modal-wa-preview");
  const btnCloseWA = document.getElementById("btn-close-modal-wa");
  const btnCloseWA2 = document.getElementById("btn-close-wa-preview");
  const btnSimulateWA = document.getElementById("btn-simulate-send-wa");
  const btnTestModal = document.getElementById("btn-test-wa-modal");
  const btnTriggerTest = document.getElementById("btn-trigger-wa-test");

  const closeWA = () => modalWA.classList.remove("open");
  btnCloseWA.addEventListener("click", closeWA);
  btnCloseWA2.addEventListener("click", closeWA);

  btnTestModal.addEventListener("click", () => previewWAMessage("w1"));
  btnTriggerTest.addEventListener("click", () => previewWAMessage("w1"));

  btnSimulateWA.addEventListener("click", () => {
    showToast("Mengirim request ke Meta WhatsApp Cloud API...", "info");
    setTimeout(() => {
      closeWA();
      showToast("Pesan WhatsApp resmi berhasil dikirim ke nomor Owner & Admin!", "success");
      
      // Tambahkan ke log
      notificationLogs.unshift({
        id: "log" + (notificationLogs.length + 1),
        time: "Baru saja",
        domain: "portal.dinas.go.id",
        recipient: "Budi Santoso (Owner Diskominfo)",
        phone: "+6281234567890",
        threshold: "H-7 (Kritis)",
        providerId: "wamid." + Math.random().toString(36).substring(7),
        status: "SENT"
      });
      renderNotificationsTable();
    }, 1200);
  });
}

// ============================================================================
// INSPECT WEBSITE DETAIL MODAL
// ============================================================================
function inspectWebsiteDetail(websiteId) {
  const item = websites.find(w => w.id === websiteId);
  if (!item) return;

  currentDetailWebsiteId = websiteId;

  document.getElementById("detail-modal-domain").textContent = `${item.domain}:${item.port}`;
  document.getElementById("detail-cn").textContent = item.cn || item.domain;
  document.getElementById("detail-issuer").textContent = item.issuer;
  document.getElementById("detail-sans").textContent = item.sans;
  document.getElementById("detail-fingerprint").textContent = item.fingerprint;
  document.getElementById("detail-key-info").textContent = item.keyInfo;
  document.getElementById("detail-serial").textContent = item.serial;

  const badgeEl = document.getElementById("detail-badge-status");
  const daysTextEl = document.getElementById("detail-days-text");
  const validityEl = document.getElementById("detail-validity-dates");

  if (item.status === "VALID") {
    badgeEl.className = "banner-badge status-valid";
    badgeEl.textContent = "VALID & AMAN";
    daysTextEl.textContent = `${item.daysRemaining} Hari Tersisa`;
    validityEl.textContent = `Masa Aktif: ${item.validFrom} s.d. ${item.expiresAt} (UTC)`;
  } else if (item.status === "EXPIRED") {
    badgeEl.className = "banner-badge status-critical";
    badgeEl.textContent = "KEDALUWARSA";
    daysTextEl.textContent = `Telah Habis Tempo (${Math.abs(item.daysRemaining)} Hari Lalu)`;
    validityEl.textContent = `Kedaluwarsa Sejak: ${item.expiresAt} (UTC)`;
  } else if (item.status === "CRITICAL_7") {
    badgeEl.className = "banner-badge status-critical";
    badgeEl.textContent = "KRITIS (H-7)";
    daysTextEl.textContent = `Segera Berakhir dalam ${item.daysRemaining} Hari!`;
    validityEl.textContent = `Batas Terakhir: ${item.expiresAt} (UTC)`;
  } else if (item.status.startsWith("WARNING")) {
    badgeEl.className = "banner-badge status-warning";
    badgeEl.textContent = "PERINGATAN";
    daysTextEl.textContent = `${item.daysRemaining} Hari Tersisa`;
    validityEl.textContent = `Batas Terakhir: ${item.expiresAt} (UTC)`;
  } else {
    badgeEl.className = "banner-badge status-failed";
    badgeEl.textContent = "GAGAL JARINGAN";
    daysTextEl.textContent = item.errorMessage || "Tidak dapat diakses";
    validityEl.textContent = "Koneksi handshake TLS batas waktu habis (Timeout)";
  }

  // Render Check History
  const historyTbody = document.getElementById("detail-history-tbody");
  historyTbody.innerHTML = `
    <tr>
      <td>${item.lastChecked}</td>
      <td><strong>${item.daysRemaining !== null ? item.daysRemaining + ' Hari' : '-'}</strong></td>
      <td><span class="status-badge ${item.status === 'VALID' ? 'status-valid' : 'status-critical'}">${item.status}</span></td>
      <td>Sistem (Scheduler Harian)</td>
    </tr>
    <tr>
      <td>1 hari yang lalu (07:00 WIB)</td>
      <td><strong>${item.daysRemaining !== null ? (item.daysRemaining + 1) + ' Hari' : '-'}</strong></td>
      <td><span class="status-badge ${item.status === 'VALID' ? 'status-valid' : 'status-critical'}">${item.status}</span></td>
      <td>Sistem (Scheduler Harian)</td>
    </tr>
    <tr>
      <td>2 hari yang lalu (07:00 WIB)</td>
      <td><strong>${item.daysRemaining !== null ? (item.daysRemaining + 2) + ' Hari' : '-'}</strong></td>
      <td><span class="status-badge ${item.status === 'VALID' ? 'status-valid' : 'status-critical'}">${item.status}</span></td>
      <td>Admin (Manual Trigger)</td>
    </tr>
  `;

  document.getElementById("modal-cert-detail").classList.add("open");
}

// ============================================================================
// PREVIEW WHATSAPP MESSAGE
// ============================================================================
function previewWAMessage(websiteId) {
  const item = websites.find(w => w.id === websiteId) || websites[0];

  document.getElementById("wa-preview-user").textContent = item.owner;
  document.getElementById("wa-preview-domain").textContent = item.domain;
  document.getElementById("wa-preview-status").textContent = item.status === "VALID" ? "PEMANTAUAN RUTIN" : item.status;
  document.getElementById("wa-preview-days").textContent = item.daysRemaining !== null ? item.daysRemaining : "N/A";
  document.getElementById("wa-preview-exp").textContent = item.expiresAt;

  document.getElementById("modal-wa-preview").classList.add("open");
}

// ============================================================================
// NOTIFICATIONS LOG VIEW LOGIC
// ============================================================================
function renderNotificationsTable() {
  const tbody = document.getElementById("tbody-notifications");
  tbody.innerHTML = "";

  document.getElementById("wa-total-sent").textContent = `${notificationLogs.length} Pesan`;

  notificationLogs.forEach(log => {
    const tr = document.createElement("tr");

    let statusBadge = "";
    if (log.status === "READ") {
      statusBadge = `<span class="status-badge status-valid">✓✓ Terbaca (Read)</span>`;
    } else if (log.status === "DELIVERED") {
      statusBadge = `<span class="status-badge" style="background: rgba(56, 189, 248, 0.15); color: #38BDF8;">✓✓ Diterima</span>`;
    } else if (log.status === "SENT") {
      statusBadge = `<span class="status-badge status-warning">✓ Terkirim</span>`;
    } else {
      statusBadge = `<span class="status-badge status-critical">✖ Gagal</span>`;
    }

    tr.innerHTML = `
      <td class="text-xs">${log.time}</td>
      <td><strong>${log.domain}</strong></td>
      <td>
        <div>${log.recipient}</div>
        <span class="text-xs code-font text-muted">${log.phone}</span>
      </td>
      <td><span class="pill-days pill-amber">${log.threshold}</span></td>
      <td class="code-font text-xs text-muted">${log.providerId}</td>
      <td>${statusBadge}</td>
      <td class="text-right">
        <button class="btn btn-outline btn-xs" onclick="previewWAMessage('w1')">Lihat Template</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// ============================================================================
// USERS TABLE LOGIC
// ============================================================================
function renderUsersTable() {
  const tbody = document.getElementById("tbody-users");
  tbody.innerHTML = "";

  users.forEach(u => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${u.name}</strong></td>
      <td>${u.email}</td>
      <td class="code-font">${u.phone}</td>
      <td><span class="pill-days ${u.role.includes('Admin') ? 'pill-green' : 'pill-amber'}">${u.role}</span></td>
      <td>${u.domainsCount}</td>
      <td><span class="status-badge status-valid">${u.status}</span></td>
      <td class="text-right">
        <button class="btn btn-outline btn-xs" onclick="showToast('Fitur edit akun dapat diakses pada rilis backend.', 'info')">Edit</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// ============================================================================
// TOAST NOTIFICATION SYSTEM
// ============================================================================
function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;

  let icon = `ℹ`;
  if (type === "success") icon = `✓`;
  if (type === "error") icon = `✖`;
  if (type === "warning") icon = `⚠`;

  toast.innerHTML = `
    <span style="font-size: 1.1rem; font-weight: bold;">${icon}</span>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(50px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, 3500);
}
