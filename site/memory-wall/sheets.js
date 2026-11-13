"use strict";
(() => {
  const input = document.getElementById("sheet-search");
  const clear = document.getElementById("sheet-clear");
  const result = document.getElementById("sheet-results");
  const cards = [...document.querySelectorAll(".sheet-card")];
  const groups = [...document.querySelectorAll(".sheets-group")];
  const normalize = value => String(value).normalize("NFKD").toLocaleLowerCase().trim();
  function apply() {
    const query = normalize(input.value);
    let shown = 0;
    for (const card of cards) {
      const match = !query || normalize(card.dataset.sheet).includes(query);
      card.hidden = !match;
      if (match) shown++;
    }
    for (const section of groups) {
      const any = [...section.querySelectorAll(".sheet-card")].some(c => !c.hidden);
      section.hidden = !any;
    }
    result.textContent = query
      ? shown + " of " + cards.length + " Sheets found"
      : "Showing all " + cards.length + " Sheets";
  }
  input.addEventListener("input", apply);
  clear.addEventListener("click", () => {input.value = ""; apply(); input.focus();});
  apply();
})();
