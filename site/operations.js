"use strict";
(() => {
 const $=id=>document.getElementById(id), filters=[...document.querySelectorAll("[data-group]")];
 const states={PUBLISHED_CATALOGUE:"REVIEWED DIRECTORY",RESTRICTED_NOT_CONNECTED:"PRIVATE / NOT CONNECTED",ROLLOUT_UNVERIFIED:"ROLLOUT UNVERIFIED",DERIVED_REFERENCE:"HISTORIC DERIVATIVE",INTAKE_PENDING:"SOURCE INTAKE PENDING"};
 let sources=[],group="all",selected=null;
 const element=(tag,value,cls)=>{const e=document.createElement(tag);e.textContent=value;if(cls)e.className=cls;return e;};
 function show(s){const out=$("details");out.replaceChildren(element("h3",s.name),element("p",states[s.status],"status-detail"));
  for(const [name,value] of [["Authority",s.authority],["Original custody",s.custody],["Integration",s.integration],["Outstanding boundary",s.limit]])out.append(element("h4",name),element("p",value));
 }
 function render(){const q=$("search").value.trim().toLowerCase();
  const visible=sources.filter(s=>(group==="all"||s.group===group)&&[s.name,s.authority,s.custody,s.limit,s.integration].some(x=>x.toLowerCase().includes(q)));
  $("count").textContent=visible.length+" source families · public-safe classifications";
  const cards=visible.map(s=>{const b=element("button","","record");b.type="button";b.setAttribute("aria-pressed",String(s.id===selected));
   b.append(element("span",states[s.status],"status"),element("strong",s.name),element("small",s.authority));
   b.addEventListener("click",()=>{selected=s.id;show(s);render();});return b;});
  $("sources").replaceChildren(...(cards.length?cards:[element("p","No matching source classification.","empty")]));
 }
 filters.forEach(b=>b.addEventListener("click",()=>{group=b.dataset.group;filters.forEach(x=>x.setAttribute("aria-pressed",String(b===x)));render();}));
 $("search").addEventListener("input",render);
 fetch("./source-custody.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{
  if(data.schema_version!=="1.1.0"||data.live_worker_sync!==false||data.authenticated_private_payroll_reads!==false||
   !Array.isArray(data.subjects)||data.subjects.some(s=>!states[s.status]))throw Error();
  sources=data.subjects;const age=Math.floor((Date.now()-new Date(data.as_of_npt+"T00:00:00+05:45").getTime())/86400000);
  $("audited").textContent="Audit: "+data.as_of_npt+(age>30?" · historical, re-audit needed":" · owner classification");
  const cons=data.consumers.map(c=>{const el=element("div","","consumer-card");el.append(element("strong",c.system),element("p",c.policy));return el;});
  $("consumers").replaceChildren(...cons);
  selected=sources[0]?.id||null;if(sources[0])show(sources[0]);render();
 }).catch(()=>{$("count").textContent="Audit snapshot unavailable";$("sources").replaceChildren(element("p","Source status cannot be inferred from missing data.","empty"));});
})();
// Current public document readback only. Never read private payroll in browser JS.
fetch("./catalog.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("unavailable");return r.json()}).then(d=>{
  const target=document.getElementById("live-catalogue-readback");
  if(target)target.textContent="Reviewed catalogue published: "+(d.verified_on_npt||"unknown")+". Original worker Money & Goods ledger not connected. Historical CLEAN Payment is published separately.";
}).catch(()=>{const target=document.getElementById("live-catalogue-readback");if(target)target.textContent="Catalogue refresh unavailable; private worker data not connected.";});
