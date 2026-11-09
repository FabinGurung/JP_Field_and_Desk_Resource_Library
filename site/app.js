"use strict";
const byId = id => document.getElementById(id);
const buttons = [...document.querySelectorAll("[data-filter]")];
const search = byId("catalog-search");
const sort = byId("sort-order");
let category = "all";
let entries = [];
let refreshed = "";
const node = (tag, value, css) => {
  const e = document.createElement(tag);
  e.textContent = value;
  if (css) e.className = css;
  return e;
};
function render() {
  const query = search.value.trim().toLocaleLowerCase();
  const displayed = entries.filter(entry => (category === "all" || category === entry.kind) &&
    [entry.title, entry.project, entry.project_id, entry.site, entry.id, entry.format].some(value =>
      (value || "").toLocaleLowerCase().includes(query)));
  if (sort.value !== "priority") {
    displayed.sort((a, b) => a[sort.value].localeCompare(b[sort.value]));
  }
  byId("catalog-count").textContent = displayed.length + (displayed.length === 1 ? " record" : " records") +
    (refreshed ? " · Sheets readback " + refreshed : "");
  const cards = displayed.map(entry => {
    const card = node("article", "", "result-card");
    card.append(node("span", entry.kind, "result-type"), node("h3", entry.title),
      node("p", [entry.project, entry.format, entry.approval].filter(Boolean).join(" · ")));
    const a = node("a", entry.kind === "projects" ? "Open project documents" : "Open in Google Drive");
    a.href = entry.url;
    if (entry.kind !== "projects") {
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      card.append(node("p", entry.access === "PUBLIC_LINK" ? "Drive link available" : "Drive permission required"));
    }
    card.append(a);
    return card;
  });
  byId("catalog-results").replaceChildren(...(cards.length ? cards : [node("p", "No reviewed records match.", "empty-state")]));
}
function select(categoryName) {
  category = categoryName;
  buttons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.filter === category)));
  render();
}
buttons.forEach(button => button.addEventListener("click", () => select(button.dataset.filter)));
for (const name of ["field", "desk", "projects"]) {
  const link = document.querySelector('nav a[href="#' + name + '"]');
  link.href = "#search-heading";
  link.addEventListener("click", () => select(name));
  const card = byId(name);
  const a = node("a", card.querySelector(".category-state").textContent, "category-state");
  a.href = "#search-heading";
  a.addEventListener("click", () => select(name));
  card.querySelector(".category-state").replaceWith(a);
}
search.addEventListener("input", render);
sort.addEventListener("change", render);
search.value = new URLSearchParams(location.search).get("project") || "";
fetch("./catalog.json", {cache: "no-cache"}).then(response => {
  if (!response.ok) throw Error();
  return response.json();
}).then(catalog => {
  refreshed = catalog.verified_on_npt;
  entries = [...catalog.projects.map(p => ({
    id: p.project_id, project_id: p.project_id, site: p.company_project_code,
    title: p.name, project: p.name, format: "A/B/C document register", kind: "projects",
    url: "./resources/project-documents.html?project=" + encodeURIComponent(p.project_id)
  })), ...catalog.resources.filter(r =>
    /^https:\/\/drive\.google\.com\/(?:file\/d\/[A-Za-z0-9_-]+\/view|drive\/folders\/[A-Za-z0-9_-]+)$/.test(r.url))];
  render();
}).catch(() => {
  byId("catalog-count").textContent = "Catalogue unavailable";
  byId("catalog-results").replaceChildren(node("p", "The published catalogue could not be loaded.", "empty-state"));
});
