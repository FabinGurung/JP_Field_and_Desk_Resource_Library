"use strict";
// Only observes the already-public document catalogue timestamp.
// NEVER fetch private workforce or payment Sheet IDs from browser JavaScript.
fetch("./catalog.json",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("Public catalogue unavailable");return r.json()})
.then(data=>{
  const el=document.getElementById("money-sync-status");
  if(!el)return;
  const manifest=data.source_manifest||{};
  const stamp=data.verified_on_npt||"unavailable";
  el.textContent="Reviewed site-resource catalogue: "+stamp+
    ". Private worker money and contractor payment feeds: not connected to this public website.";
  if(manifest.private_payroll_connected!==false){
    el.textContent="Private feed status cannot be verified. Do not rely on this site for worker payments.";
  }
}).catch(()=>{
  const el=document.getElementById("money-sync-status");
  if(el)el.textContent="Public catalogue status is temporarily unavailable. No private money data is shown.";
});
