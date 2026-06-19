/* ==========================================================================
   LÓGICA COMPARTIDA DE AUTENTICACIÓN - AUTH-UI.JS
   Responsable: Leonardo González
   Aesthetics: Avatar, responsive dropdown profile, dynamic session links
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    const mainNav = document.querySelector(".main-nav");
    if (!mainNav) return;

    // Detectar ruta y directorios
    const isPagesDir = window.location.pathname.includes("/pages/");
    const loginUrl = isPagesDir ? "login.html" : "pages/login.html";
    const homeUrl = isPagesDir ? "../index.html" : "index.html";

    // Leer la sesión activa
    const activeSessionStr = localStorage.getItem("user_session");
    let session = null;
    if (activeSessionStr) {
        try {
            session = JSON.parse(activeSessionStr);
        } catch(e) {
            localStorage.removeItem("user_session");
        }
    }

    if (!session) {
        // --- CASO: NO LOGUEADO (Invitado) ---
        mainNav.innerHTML = `
            <a href="${loginUrl}" class="btn btn-primary" style="padding: 0.45rem 1rem; border-radius: var(--radius-sm); text-decoration: none; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.5rem;">
                <i class="fa-solid fa-right-to-bracket"></i> Iniciar Sesión
            </a>
        `;
    } else {
        // --- CASO: LOGUEADO ---
        const initial = session.username ? session.username.charAt(0) : "U";
        const profileUrl = isPagesDir ? "perfil.html" : "pages/perfil.html";
        
        // Determinar enlace y detalles del panel correspondiente al rol
        let panelUrl = "";
        let panelLabel = "";
        let panelIcon = "";
        
        if (session.role === "estudiante") {
            panelUrl = isPagesDir ? "estudiante.html" : "pages/estudiante.html";
            panelLabel = "Panel de Estudiante";
            panelIcon = "fa-graduation-cap";
        } else if (session.role === "profesor") {
            panelUrl = isPagesDir ? "profesor.html" : "pages/profesor.html";
            panelLabel = "Panel de Profesor";
            panelIcon = "fa-chalkboard-user";
        } else if (session.role === "admin") {
            panelUrl = isPagesDir ? "admin.html" : "pages/admin.html";
            panelLabel = "Consola de Admin";
            panelIcon = "fa-user-shield";
        }

        // Estructura del dropdown con enlace al panel correspondiente dentro del menú
        const dropdownHtml = `
            <div class="user-profile-menu" id="user-profile-menu-btn" style="margin-left: 0.5rem;">
                <div class="user-avatar">${initial}</div>
                <span class="user-name">${session.username}</span>
                <i class="fa-solid fa-chevron-down" style="font-size: 0.7rem; color: var(--text-secondary);"></i>
                
                <div class="profile-dropdown-menu" id="profile-dropdown-menu-list">
                    <a href="${panelUrl}" class="profile-dropdown-item"><i class="fa-solid ${panelIcon}"></i> ${panelLabel}</a>
                    <a href="${profileUrl}" class="profile-dropdown-item"><i class="fa-solid fa-user"></i> Ver Perfil</a>
                    <button type="button" id="logout-btn-action" class="profile-dropdown-item danger-item"><i class="fa-solid fa-right-from-bracket"></i> Cerrar Sesión</button>
                </div>
            </div>
        `;

        mainNav.innerHTML = dropdownHtml;

        // Comportamientos interactivos del dropdown
        const menuBtn = document.getElementById("user-profile-menu-btn");
        const dropdownList = document.getElementById("profile-dropdown-menu-list");
        
        if (menuBtn && dropdownList) {
            menuBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                dropdownList.classList.toggle("active");
            });

            document.addEventListener("click", () => {
                dropdownList.classList.remove("active");
            });
        }

        // Manejador del botón de cerrar sesión
        const logoutBtn = document.getElementById("logout-btn-action");
        if (logoutBtn) {
            logoutBtn.addEventListener("click", (e) => {
                e.preventDefault();
                e.stopPropagation();
                localStorage.removeItem("user_session");
                window.location.href = homeUrl;
            });
        }
    }
});
