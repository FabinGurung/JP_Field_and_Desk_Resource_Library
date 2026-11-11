"use strict";
/* Public projection of owner-approved historical clean Payment source.
 * No browser Google credentials, private source workbook fetch, or invented amounts.
 */
(() => {
  const $ = id => document.getElementById(id);
  const money = new Intl.NumberFormat("en-NP", {minimumFractionDigits:2, maximumFractionDigits:2});
  const state = {data:null, worker:"", category:"", site:"", page:0};
  const PAGE_SIZE = 40;
  function option(select,label,value) {
    const o=document.createElement("option");
    o.value=value; o.textContent=label; select.append(o);
  }
  function fillSelect(select, options, allLabel) {
    select.replaceChildren();
    option(select,allLabel,"");
    for(const value of options.sort((a,b)=>a.localeCompare(b))) option(select,value,value);
  }
  function putRow(parent, values) {
    const tr=document.createElement("tr");
    for(const [value,cls] of values) {
      const td=document.createElement("td");
      td.textContent=String(value??"");
      if(cls)td.className=cls;
      tr.append(td);
    }
    parent.append(tr);
  }
  function currentRecords() {
    if(!state.data) return [];
    return state.data.records.filter(r=>
      (!state.worker || r.worker_id===state.worker) &&
      (!state.category || r.category===state.category) &&
      (!state.site || r.site===state.site)
    );
  }
  function render() {
    const values=currentRecords();
    const pages=Math.max(1,Math.ceil(values.length/PAGE_SIZE));
    state.page=Math.min(state.page,pages-1);
    const portion=values.slice(state.page*PAGE_SIZE,(state.page+1)*PAGE_SIZE);
    const body=$("payment-record-body");
    body.replaceChildren();
    for(const r of portion) {
      putRow(body,[
        [r.date,""],
        [r.worker,""],
        [r.site || "Not specified in source",""],
        [r.category,""],
        [money.format(r.amount_npr),"payment-amount"],
        [r.source_row+" · "+r.source_cell,"payment-source"]
      ]);
    }
    if(!portion.length){
      const row=document.createElement("tr");
      const td=document.createElement("td");
      td.colSpan=6; td.textContent="No original clean-payment rows match these filters.";
      row.append(td);body.append(row);
    }
    const subtotal=values.reduce((a,b)=>a+b.amount_npr,0);
    $("payment-summary").textContent=values.length+" of "+state.data.count+
      " recorded payments · selected sum NPR "+money.format(subtotal)+
      " · negative source adjustments retained";
    $("payment-page").textContent="Page "+(state.page+1)+" of "+pages;
    $("payment-prev").disabled=state.page===0;
    $("payment-next").disabled=state.page>=pages-1;
  }
  function bind(name,field) {
    const el=$(name);
    el.addEventListener("change",()=>{state[field]=el.value;state.page=0;render()});
  }
  async function init() {
    const target=$("payments-load-status");
    try {
      const response=await fetch("./field-payments.json",{cache:"no-store"});
      if(!response.ok)throw Error("Published data unavailable");
      const json=await response.json();
      if(json.schema_version!=="1.0.0" || !Array.isArray(json.records) ||
          json.count!==json.records.length ||
          json.source?.source_status!=="HISTORICAL_CLEANED_PAYMENT_NOT_CERTIFIED_PAYROLL")
        throw Error("Unexpected source publication");
      state.data=json;
      fillSelect($("payment-worker"),
        [...new Map(json.records.map(r=>[r.worker_id,r.worker])).entries()].map(([id,name])=>({id,name})).map(x=>x.id), "All workers");
      // Worker IDs remain exactly as the clean source provided; no fabricated WKR joins.
      for(const node of $("payment-worker").options) {
        if(node.value){const r=json.records.find(v=>v.worker_id===node.value);node.textContent=r.worker}
      }
      fillSelect($("payment-category"), [...new Set(json.records.map(r=>r.category))],"All categories");
      fillSelect($("payment-site"), [...new Set(json.records.map(r=>r.site).filter(Boolean))],"All sites");
      target.textContent="Fetched from original CLEAN Payment Google Sheet on "+json.fetched_on_npt+
        " · "+json.count+" recorded rows, "+json.worker_count+" workers. Historical source — not an approved payroll settlement.";
      $("payment-controls").hidden=false;
      $("payment-view").hidden=false;
      bind("payment-worker","worker");bind("payment-category","category");bind("payment-site","site");
      $("payment-prev").addEventListener("click",()=>{state.page--;render()});
      $("payment-next").addEventListener("click",()=>{state.page++;render()});
      $("payment-reset").addEventListener("click",()=>{
        state.worker=state.category=state.site="";state.page=0;
        for(const id of ["payment-worker","payment-category","payment-site"])$(id).value="";
        render();
      });
      render();
    } catch(error) {
      target.textContent="Clean Payment publication unavailable or not yet source-verified. No amounts are guessed.";
      $("payment-controls").hidden=true;$("payment-view").hidden=true;
    }
  }
  init();
})();
