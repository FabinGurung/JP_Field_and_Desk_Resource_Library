/* Derived public navigation only. Original files and permissions remain in Drive. */
(() => {
  "use strict";
  const results = document.getElementById("catalog-results");
  const count = document.getElementById("catalog-count");
  const input = document.getElementById("catalog-search");
  const filters = Array.from(document.querySelectorAll("[data-filter]"));
  const allowedKinds = new Set(["field", "desk", "projects"]);
  const state = { filter: "all", query: "", items: [] };

  function newElement(tag, className, text) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (typeof text === "string") el.textContent = text;
    return el;
  }

  function isSafeWebUrl(value) {
    if (typeof value !== "string") return false;
    try {
      const parsed = new URL(value);
      return parsed.protocol === "https:" &&
        new Set(["github.com", "drive.google.com", "docs.google.com"]).has(parsed.hostname);
    } catch (_error) {
      return false;
    }
  }

  function itemAdmitted(item, catalog, blockedProjectIds) {
    if (!item || typeof item !== "object") return false;
    if (!allowedKinds.has(item.kind)) return false;
    if (item.project_id && blockedProjectIds.has(item.project_id)) return false;
    if (item.public_admission !== "APPROVED_PUBLIC") return false;
    if (item.is_public !== true || item.current_source_permission_verified !== true) return false;
    if (typeof item.source_id !== "string" || !item.source_id.trim()) return false;
    if (typeof item.review_id !== "string" || !item.review_id.trim()) return false;
    if (typeof item.title !== "string" || !item.title.trim()) return false;
    if (!isSafeWebUrl(item.url)) return false;
    return catalog.status === "PUBLIC_APPROVED_PUBLISHED" &&
      catalog.deployment?.github_pages_enabled === true;
  }

  function drawEmpty(message) {
    const empty = newElement("div", "empty-state");
    empty.appendChild(newElement("h3", "", "No reviewed items available"));
    empty.appendChild(newElement("p", "", message));
    results.replaceChildren(empty);
  }

  function render() {
    const q = state.query.trim().toLocaleLowerCase();
    const shown = state.items.filter(item =>
      (state.filter === "all" || item.kind === state.filter) &&
      (!q || [item.title, item.source_id, item.kind].some(value =>
        String(value || "").toLocaleLowerCase().includes(q)))
    );
    count.textContent = shown.length + (shown.length === 1 ? " reviewed resource" : " reviewed resources") + " visible";
    if (!shown.length) {
      drawEmpty(state.items.length
        ? "No admitted public records match the current search or category."
        : "No client documents or source links have passed this preview's publication gate. Original records and sharing permissions remain with their registered source owners.");
      return;
    }
    const fragment = document.createDocumentFragment();
    for (const item of shown) {
      const card = newElement("article", "result-card");
      card.appendChild(newElement("span", "result-type", item.kind));
      card.appendChild(newElement("h3", "", item.title));
      card.appendChild(newElement("p", "", item.source_id));
      const link = newElement("a", "", "Open verified source");
      link.href = item.url; link.target = "_blank"; link.rel = "noopener noreferrer";
      card.appendChild(link); fragment.appendChild(card);
    }
    results.replaceChildren(fragment);
  }

  input.addEventListener("input", () => { state.query = input.value; render(); });
  for (const button of filters) {
    button.addEventListener("click", () => {
      state.filter = button.dataset.filter;
      for (const candidate of filters) {
        candidate.setAttribute("aria-pressed", String(candidate === button));
      }
      render();
    });
  }

  fetch("./catalog/public-index.v0.1.json", { cache: "no-store" })
    .then(resp => { if (!resp.ok) throw new Error("Catalogue unavailable"); return resp.json(); })
    .then(catalog => {
      const blocked = new Set((catalog.privacy_holds || []).map(item => item.canonical_project_id));
      const rawItems = Array.isArray(catalog.resources) ? catalog.resources : [];
      state.items = rawItems.filter(item => itemAdmitted(item, catalog, blocked));
      render();
    })
    .catch(() => {
      state.items = [];
      count.textContent = "Catalogue unavailable — no public entries displayed";
      drawEmpty("Source admission cannot be verified at this time. This fail-closed preview does not expose any document links.");
    });
})();
