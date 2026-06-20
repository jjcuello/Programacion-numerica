window.PlatformApi = (() => {
    const API_BASE_URL_STORAGE_KEY = "numerical_api_base_url";

    function normalizeApiBaseUrl(value) {
        const normalized = String(value || "").trim();
        return normalized.replace(/\/+$/, "");
    }

    function getMetaConfiguredApiBaseUrl() {
        const meta = document.querySelector('meta[name="numerical-api-base-url"]');
        return meta ? meta.getAttribute("content") : null;
    }

    function getStoredApiBaseUrl() {
        try {
            return localStorage.getItem(API_BASE_URL_STORAGE_KEY);
        } catch (error) {
            return null;
        }
    }

    function inferDefaultApiBaseUrl() {
        const { protocol, hostname, origin } = window.location;
        const isHttp = protocol === "http:" || protocol === "https:";
        const isLocalHost = hostname === "localhost" || hostname === "127.0.0.1";
        if (isHttp && !isLocalHost) {
            return origin;
        }
        return "http://127.0.0.1:8000";
    }

    function getApiBaseUrl() {
        const configuredValue =
            window.NUMERICAL_API_BASE_URL ||
            getMetaConfiguredApiBaseUrl() ||
            getStoredApiBaseUrl() ||
            inferDefaultApiBaseUrl();
        return normalizeApiBaseUrl(configuredValue);
    }

    function setApiBaseUrl(apiBaseUrl) {
        const normalized = normalizeApiBaseUrl(apiBaseUrl);
        if (!normalized) {
            throw new Error("La URL base del backend no puede estar vacia.");
        }
        try {
            localStorage.setItem(API_BASE_URL_STORAGE_KEY, normalized);
        } catch (error) {
            return normalized;
        }
        return normalized;
    }

    function resetApiBaseUrl() {
        try {
            localStorage.removeItem(API_BASE_URL_STORAGE_KEY);
        } catch (error) {
            return;
        }
    }

    function getSession() {
        const raw = localStorage.getItem("user_session");
        if (!raw) return null;
        try {
            return JSON.parse(raw);
        } catch (error) {
            localStorage.removeItem("user_session");
            return null;
        }
    }

    function saveSession(session) {
        localStorage.setItem("user_session", JSON.stringify(session));
    }

    function clearSession() {
        localStorage.removeItem("user_session");
        localStorage.removeItem("active_assignment_context");
    }

    async function request(path, { method = "GET", body = null, token = null } = {}) {
        const headers = {};
        const apiBaseUrl = getApiBaseUrl();
        if (body !== null) {
            headers["Content-Type"] = "application/json";
        }
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        const response = await fetch(`${apiBaseUrl}${path}`, {
            method,
            headers,
            body: body !== null ? JSON.stringify(body) : undefined
        });

        let data = null;
        try {
            data = await response.json();
        } catch (error) {
            data = null;
        }

        if (!response.ok) {
            const detail = data && (data.detail || data.error);
            throw new Error(typeof detail === "string" ? detail : "No se pudo completar la solicitud al backend.");
        }

        return data;
    }

    function roleToFrontend(roleName) {
        const normalized = String(roleName || "").toLowerCase();
        if (normalized === "teacher") return "profesor";
        if (normalized === "student") return "estudiante";
        if (normalized === "admin") return "admin";
        return normalized || "usuario";
    }

    function buildFrontendSession(loginResponse) {
        const user = loginResponse.user || {};
        const roles = Array.isArray(user.roles) ? user.roles : [];
        const primaryRole = roles[0] || "student";
        const username = String(user.email || "usuario").split("@")[0];

        return {
            token: loginResponse.token,
            userId: user.id,
            username,
            role: roleToFrontend(primaryRole),
            roles: roles.map(roleToFrontend),
            name: user.full_name || username,
            email: user.email || `${username}@numerica.local`,
            joined: "Junio 2026",
            status: "Activo"
        };
    }

    async function register(payload) {
        return request("/api/auth/register", { method: "POST", body: payload });
    }

    async function login(email, password) {
        return request("/api/auth/login", { method: "POST", body: { email, password } });
    }

    async function createSection(payload, token) {
        return request("/api/academic/sections", { method: "POST", body: payload, token });
    }

    async function createAssignment(payload, token) {
        return request("/api/academic/assignments", { method: "POST", body: payload, token });
    }

    async function enroll(payload, token) {
        return request("/api/academic/enrollments", { method: "POST", body: payload, token });
    }

    async function getAssignment(assignmentId, token) {
        return request(`/api/academic/assignments/${assignmentId}`, { token });
    }

    async function getMyAssignments(token) {
        return request("/api/academic/my-assignments", { token });
    }

    async function solveRoots(payload, token = null) {
        return request("/api/roots/solve", { method: "POST", body: payload, token });
    }

    async function compareRoots(payload, token = null) {
        return request("/api/roots/compare", { method: "POST", body: payload, token });
    }

    return {
        get API_BASE_URL() {
            return getApiBaseUrl();
        },
        buildFrontendSession,
        clearSession,
        compareRoots,
        createAssignment,
        createSection,
        enroll,
        getApiBaseUrl,
        getAssignment,
        getMyAssignments,
        getSession,
        login,
        register,
        resetApiBaseUrl,
        request,
        roleToFrontend,
        saveSession,
        setApiBaseUrl,
        solveRoots
    };
})();
