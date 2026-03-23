(() => {
  const state = {
    token: localStorage.getItem("token") || "",
    user: null,
    termWS: null
  };

  const $ = (id) => document.getElementById(id);
  const panels = document.querySelectorAll(".panel");
  const tabs = document.querySelectorAll(".tab");

  function api(path, opts = {}) {
    const headers = opts.headers || {};
    if (state.token) headers["Authorization"] = "Bearer " + state.token;
    headers["Content-Type"] = "application/json";
    return fetch(path, { ...opts, headers }).then(r => r.json());
  }

  function setView(name) {
    panels.forEach(p => p.classList.toggle("hidden", p.dataset.view !== name));
    tabs.forEach(t => t.classList.toggle("active", t.dataset.view === name));
    if (name === "terminal") openTerminal();
  }

  function setLoggedIn(loggedIn) {
    $("login").classList.toggle("hidden", loggedIn);
    $("main").classList.toggle("hidden", !loggedIn);
    $("app").classList.toggle("auth-mode", !loggedIn);
  }

  function login() {
    api("/api/login", {
      method: "POST",
      body: JSON.stringify({
        email: $("login-email").value,
        password: $("login-pass").value
      })
    }).then(res => {
      if (res.error) {
        $("login-error").textContent = res.error;
        return;
      }
      state.token = res.token;
      localStorage.setItem("token", res.token);
      $("login-error").textContent = "";
      loadMe();
    });
  }

  function logout() {
    api("/api/logout", { method: "POST" }).finally(() => {
      state.token = "";
      localStorage.removeItem("token");
      setLoggedIn(false);
    });
  }

  function loadMe() {
    api("/api/me").then(res => {
      if (res.user) {
        state.user = res.user;
        $("user-email").textContent = res.user.email;
        setLoggedIn(true);
        setView("dashboard");
      } else {
        setLoggedIn(false);
      }
    });
  }

  function runCommand() {
    const cmd = $("cmd-input").value.trim();
    if (!cmd) return;
    api("/api/tasks", {
      method: "POST",
      body: JSON.stringify({ command: cmd })
    }).then(res => {
      if (res.error) {
        $("cmd-output").textContent = res.error;
        return;
      }
      $("cmd-output").textContent = "已加入队列 #" + res.task.id;
      loadTasks();
    });
  }

  function formatStatus(status) {
    const map = {
      queued: "排队中",
      running: "运行中",
      done: "已完成",
      success: "已完成",
      failed: "失败",
      error: "失败",
      canceled: "已取消"
    };
    return map[status] || status || "";
  }

  function formatRole(role) {
    const map = {
      admin: "管理员",
      user: "用户"
    };
    return map[role] || role || "";
  }

  function loadTasks() {
    api("/api/tasks").then(res => {
      const list = $("task-list");
      list.innerHTML = "";
      (res.tasks || []).forEach(t => {
        const item = document.createElement("div");
        item.className = "item";
        item.textContent = "#" + t.id + " [" + formatStatus(t.status) + "] " + t.command;
        item.onclick = () => loadTaskDetail(t.id);
        list.appendChild(item);
      });
    });
  }

  function loadTaskDetail(id) {
    api("/api/tasks/" + id).then(res => {
      if (!res.task) return;
      const out = res.task.output || res.task.error || "";
      $("task-output").textContent = out;
    });
  }

  function loadConfig() {
    api("/api/config").then(res => {
      if (res.content !== undefined) $("config-editor").value = res.content;
    });
  }

  function saveConfig() {
    api("/api/config", {
      method: "POST",
      body: JSON.stringify({ content: $("config-editor").value })
    }).then(res => {
      $("config-editor").value = $("config-editor").value;
    });
  }

  function loadUsers() {
    api("/api/users").then(res => {
      const list = $("user-list");
      list.innerHTML = "";
      (res.users || []).forEach(u => {
        const item = document.createElement("div");
        item.className = "item";
        item.textContent = u.email + " [" + formatRole(u.role) + "] " + (u.is_active ? "启用" : "禁用");
        list.appendChild(item);
      });
    });
  }

  function addUser() {
    api("/api/users", {
      method: "POST",
      body: JSON.stringify({
        email: $("user-email").value,
        password: $("user-pass").value,
        role: $("user-role").value
      })
    }).then(res => {
      loadUsers();
    });
  }

  function loadAudit() {
    api("/api/audit").then(res => {
      const lines = (res.audit || []).map(a => {
        return a.created_at + " " + a.action + " " + (a.target || "");
      });
      $("audit-output").textContent = lines.join("\n");
    });
  }

  function loadLogs() {
    api("/api/logs").then(res => {
      $("logs-output").textContent = res.content || "";
    });
  }

  function openTerminal() {
    if (state.termWS) return;
    const ws = new WebSocket(
      (location.protocol === "https:" ? "wss://" : "ws://") +
      location.host + "/ws/terminal?token=" + encodeURIComponent(state.token)
    );
    state.termWS = ws;
    ws.onmessage = (evt) => {
      $("term-output").textContent += evt.data;
      $("term-output").scrollTop = $("term-output").scrollHeight;
    };
    ws.onclose = () => { state.termWS = null; };
  }

  $("btn-login").onclick = login;
  $("btn-logout").onclick = logout;
  $("btn-run").onclick = runCommand;
  $("btn-refresh-tasks").onclick = loadTasks;
  $("btn-load-config").onclick = loadConfig;
  $("btn-save-config").onclick = saveConfig;
  $("btn-add-user").onclick = addUser;
  $("btn-refresh-audit").onclick = loadAudit;
  $("btn-refresh-logs").onclick = loadLogs;

  tabs.forEach(t => t.onclick = () => setView(t.dataset.view));

  $("term-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && state.termWS) {
      state.termWS.send(e.target.value + "\n");
      e.target.value = "";
    }
  });

  setLoggedIn(false);
  loadMe();
})();
