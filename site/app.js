"use strict";
(() => {
  const $ = id => document.getElementById(id);
  const make = (tag, value, cls) => {
    const el = document.createElement(tag);
    if (value !== null && value !== undefined) el.textContent = value;
    if (cls) el.className = cls;
    return el;
  };
  const text = (parent, tag, value, cls) => { const child = make(tag, value, cls); parent.append(child); return child; };
  const safeDrive = url => /^https:\/\/drive\.google\.com\/(?:file\/d\/[A-Za-z0-9_-]+\/view|drive\/folders\/[A-Za-z0-9_-]+)$/.test(url || "");
  const state = { data: null, company: "", project: "", selected: "", query: "" };
  const params = new URLSearchParams(location.search);
  state.company = params.get("company") || "";
  state.project = params.get("project") || "";

  function syncURL() {
    const u = new URL(location.href);
    for (const key of ["company", "project"]) u.searchParams.delete(key);
    if (state.company) u.searchParams.set("company", state.company);
    if (state.project) u.searchParams.set("project", state.project);
    history.replaceState(null, "", u);
  }
  function setLocation(company = "", project = "") {
    state.company = company;
    state.project = project;
    state.selected = "";
    state.query = "";
    $("library-search").value = "";
    syncURL();
    render();
    $("main").scrollIntoView({behavior: "auto", block: "start"});
  }
  function detail(r) {
    const root = $("record-detail");
    root.replaceChildren();
    if (!r) {
      text(root, "p", "Choose an individual record to inspect its source and recorded review status.", "soft");
      return;
    }
    text(root, "h3", r.title);
    const fields = [
      ["Project", r.project + " · " + r.project_id],
      ["Resource group", (state.data.groups.find(g => g.key === r.group) || {}).label || r.group],
      ["Document slot", r.document_slot || "Not classified"],
      ["Format", r.format],
      ["Owner's approval note", r.approval || "Unverified"],
      ["Source access", r.access === "PUBLIC_LINK" ? "Reviewed link · original access still enforced by Drive" : "Google Drive permission required"],
      ["Source register", r.origin_tab + " + " + r.readback_tab],
      ["Owner-entered readback", r.readback_checked_on || "Not supplied"],
      ["Stable record ID", r.id]
    ];
    for (const [label, value] of fields) {
      text(root, "h4", label);
      text(root, "p", value);
    }
    if (safeDrive(r.url)) {
      const a = text(root, "a", "Open original in Google Drive", "source-button");
      a.href = r.url;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
    }
  }
  function nav() {
    const root = $("company-nav"); root.replaceChildren();
    const choices = [{key: "", name: "All companies", project_count: state.data.projects.length}, ...state.data.companies];
    for (const c of choices) {
      const btn = make("button", null, "company-btn");
      btn.type = "button";
      btn.setAttribute("aria-pressed", String(c.key === state.company));
      text(btn, "strong", c.name);
      text(btn, "span", c.project_count + (c.project_count === 1 ? " project" : " projects"));
      btn.addEventListener("click", () => setLocation(c.key));
      root.append(btn);
    }
  }
  function crumbs() {
    const root = $("breadcrumbs"); root.replaceChildren();
    const step = (name, company, project) => {
      const btn = text(root, "button", name);
      btn.type = "button";
      btn.addEventListener("click", () => setLocation(company, project));
    };
    step("All companies", "", "");
    const c = state.data.companies.find(x => x.key === state.company);
    if (c) {
      text(root, "span", " / ");
      step(c.name, c.key, "");
    }
    if (state.project) {
      const p = state.data.projects.find(x => x.project_id === state.project);
      if (p) { text(root, "span", " / "); text(root, "span", p.name); }
    }
  }
  const matches = (...values) => values.some(value => String(value || "").toLocaleLowerCase().includes(state.query));
  const orderedProjects = company => state.data.projects.filter(p => p.company_key === company);
  const groupLabel = group => state.data.groups.find(g => g.key === group)?.label || group;

  function introCards() {
    const root = $("workspace"); root.replaceChildren();
    const top = make("div", null, "section-top");
    const left = make("div");
    text(left, "p", "01 / CHOOSE AN ORGANIZATION", "eyebrow");
    text(left, "h2", "Companies & source owners");
    text(left, "p", "Choose a company to browse projects. Unassigned entries are surfaced for correction.");
    top.append(left); root.append(top);
    const grid = make("div", null, "company-grid");
    const shown = state.data.companies.filter(c => matches(
      c.name, ...orderedProjects(c.key).flatMap(p => [
        p.name, p.project_id, ...state.data.resources.filter(r => r.project_id === p.project_id).map(r => r.title)
      ])
    ));
    for (const c of shown) {
      const btn = make("button", null, "company-card");
      btn.type = "button";
      text(btn, "strong", c.name);
      text(btn, "small", c.project_count + " projects · " + c.resource_count + " references · " + c.document_count + " packet files");
      text(btn, "em", c.status === "NEEDS_OWNER_CONFIRMATION" ? "Company needs owner confirmation" : "Browse projects");
      btn.addEventListener("click", () => setLocation(c.key));
      grid.append(btn);
    }
    root.append(shown.length ? grid : text(make("div"), "p", "No organization matches the search.", "empty"));
  }
  function companyProjects() {
    const root = $("workspace"); root.replaceChildren();
    const c = state.data.companies.find(x => x.key === state.company);
    if (!c) return introCards();
    const top = make("div", null, "section-top");
    const left = make("div");
    text(left, "p", "02 / CHOOSE A PROJECT", "eyebrow");
    text(left, "h2", c.name);
    text(left, "p", c.project_count + " projects · " + c.resource_count + " references · " + c.document_count + " packet files");
    if (c.status === "NEEDS_OWNER_CONFIRMATION") text(left, "p", "Company name is not present in the packet source. Owner confirmation is required.", "review");
    top.append(left); root.append(top);
    const grid = make("div", null, "project-grid");
    const shown = orderedProjects(c.key).filter(p => matches(
      p.name, p.project_id, p.company_project_code, ...state.data.resources.filter(r => r.project_id === p.project_id).map(r => r.title)
    ));
    for (const p of shown) {
      const btn = make("button", null, "project-card");
      btn.type = "button";
      text(btn, "strong", p.name);
      text(btn, "small", p.project_id + (p.company_project_code ? " · " + p.company_project_code : ""));
      text(btn, "small", p.resource_count + " resource links · " + p.document_count + " packet documents");
      btn.addEventListener("click", () => setLocation(c.key, p.project_id));
      grid.append(btn);
    }
    root.append(shown.length ? grid : text(make("div"), "p", "No projects match the search.", "empty"));
  }
  function projectResources() {
    const root = $("workspace"); root.replaceChildren();
    const p = state.data.projects.find(x => x.project_id === state.project && x.company_key === state.company);
    if (!p) {setLocation(); return;}
    const header = make("div", null, "section-top");
    const left = make("div");
    text(left, "p", "03 / RESOURCE CATEGORIES", "eyebrow");
    text(left, "h2", p.name);
    text(left, "p", p.project_id + (p.company_project_code ? " · " + p.company_project_code : "") + " · " + p.resource_count + " resources · " + p.document_count + " packet files");
    header.append(left);
    const back = text(header, "button", "All projects", "utility-btn");
    back.addEventListener("click", () => setLocation(state.company));
    root.append(header);
    if (p.company_assignment === "NEEDS_OWNER_CONFIRMATION") {
      text(root, "p", "Company assignment is missing from the original packet register; this is not an approval or ownership inference.", "review");
    }
    const stack = make("div", null, "group-stack");
    let displayed = 0;
    for (const group of state.data.groups) {
      const records = state.data.resources.filter(r => r.project_id === p.project_id && r.group === group.key &&
        matches(r.title, r.document_slot, r.format, r.id, r.approval, group.label));
      const packets = group.key === "project-packets" && p.document_count &&
        matches("", "agreements", "documents", "materials", "project packets", group.label, p.name);
      if (!records.length && !packets) continue;
      displayed += records.length + (packets ? p.document_count : 0);
      const details = make("details", null, "resource-group");
      details.open = true;
      const summ = make("summary");
      text(summ, "span", group.label);
      text(summ, "small", records.length + (packets ? p.document_count : 0) + " items");
      details.append(summ);
      const body = make("div", null, "resource-items");
      for (const r of records) {
        const btn = make("button", null, "resource-line");
        btn.type = "button";
        btn.setAttribute("aria-pressed", String(state.selected === r.id));
        text(btn, "strong", r.title);
        text(btn, "span", [r.document_slot, r.format, r.access === "PUBLIC_LINK" ? "Link reviewed" : "Drive permission required"].filter(Boolean).join(" · "));
        btn.addEventListener("click", () => {
          state.selected = r.id; detail(r); render();
          if (window.matchMedia("(max-width:700px)").matches) $("east").scrollIntoView({block:"start", behavior:"auto"});
        });
        body.append(btn);
      }
      if (packets) {
        const a = text(body, "a", "Open A/B/C document register · " + p.document_count + " original-linked PDFs", "packet-link");
        a.href = "./resources/project-documents.html?project=" + encodeURIComponent(p.project_id);
      }
      details.append(body);
      stack.append(details);
    }
    root.append(displayed ? stack : text(make("div"), "p", "No resources match this search in the selected project.", "empty"));
  }
  function render() {
    if (!state.data) return;
    if (!state.company && state.project) {
      const fromLink = state.data.projects.find(p => p.project_id === state.project);
      if (fromLink) state.company = fromLink.company_key;
    }
    if (!state.data.companies.some(c => c.key === state.company)) {
      state.company = ""; state.project = "";
    }
    const current = state.data.projects.find(p => p.project_id === state.project);
    if (!current || current.company_key !== state.company) state.project = "";
    syncURL(); nav(); crumbs();
    if (!state.company) introCards();
    else if (!state.project) companyProjects();
    else projectResources();
    if (state.selected) {
      const selected = state.data.resources.find(r => r.id === state.selected);
      detail(selected || null);
    } else detail(null);
  }
  $("library-search").addEventListener("input", value => {
    state.query = value.target.value.trim().toLocaleLowerCase();
    render();
  });
  $("clear-search").addEventListener("click", () => {
    $("library-search").value = ""; state.query = ""; render(); $("library-search").focus();
  });
  fetch("./catalog.json", {cache:"no-store"}).then(response => {
    if (!response.ok) throw Error("Unable to load catalog.json");
    return response.json();
  }).then(data => {
    if (data.schema_version !== "2.0.0" || !Array.isArray(data.companies) ||
        !Array.isArray(data.projects) || !Array.isArray(data.resources) || !Array.isArray(data.groups)) {
      throw Error("Unrecognized catalogue version");
    }
    if (data.resources.some(r => !safeDrive(r.url))) throw Error("Invalid Drive source route");
    state.data = data;
    $("metric-companies").textContent = String(data.companies.length);
    $("metric-projects").textContent = String(data.projects.length);
    $("metric-records").textContent = String(data.resources.length + data.projects.reduce((n,p) => n+p.document_count, 0));
    $("site-status").textContent = "Published from the reviewed owner register · " + data.verified_on_npt +
      " · Source file approvals remain independent";
    render();
  }).catch(error => {
    $("site-status").textContent = "Directory unavailable: " + error.message;
    $("workspace").replaceChildren(text(make("div"), "p", "The reviewed index cannot be loaded. No source approval should be inferred.", "empty"));
  });
})();