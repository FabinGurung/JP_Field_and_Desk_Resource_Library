"use strict";
const {chromium} = require("playwright");
const assert = require("node:assert/strict");
const ROOT = process.env.BROWSER_QA_URL || "http://127.0.0.1:8765";

async function qa() {
  const browser = await chromium.launch({headless: true, args:["--no-sandbox"]});
  try {
    const errors = [];
    const page = await browser.newPage({viewport:{width:1366,height:900},deviceScaleFactor:1});
    page.on("pageerror", error => errors.push(error.message));
    await page.goto(ROOT + "/", {waitUntil:"domcontentloaded"});
    await page.locator(".company-card").first().waitFor();
    assert.equal(await page.locator(".company-card").count(),3);
    assert.equal(await page.locator("#metric-projects").textContent(),"3");
    await page.locator(".company-card").first().click();
    assert.equal(await page.locator(".project-card").count(),1);
    await page.locator(".project-card").first().click();
    assert.equal(await page.locator(".resource-line").count(),1);
    // Architecture-only example still exposes empty Structural PDF/DWG slots.
    assert.equal(await page.locator(".resource-slot").count() >= 12, true);
    const emptyStructural = page.locator('[data-slot="structural-pdf"]');
    assert.equal(await emptyStructural.count(),1);
    await emptyStructural.locator("summary").click();
    assert.match(await emptyStructural.innerText(),/No structural drawings.*registered/i);
    assert.equal(await page.locator("#facet-panel").isVisible(), true);
    assert.equal(await page.locator("#facet-discipline option").count(), 2);
    await page.locator("#facet-discipline").selectOption({label: "Architecture"});
    await page.locator("#facet-format").selectOption("DWG");
    await page.locator("#facet-revision").selectOption({label: "Issue / revision not certified"});
    await page.locator("#facet-approval").selectOption("Review pending");
    assert.equal(await page.locator(".resource-line").count(),1);
    assert.match(await page.locator("#facet-count").innerText(),/1 of 1/);
    await page.locator("#clear-facets").click();
    assert.equal(await page.locator("#facet-discipline").inputValue(),"");
    await page.locator(".resource-line").first().click();
    assert.match(await page.locator("#record-detail").innerText(),/SOURCE REGISTER/i);
    assert.match(await page.locator("#record-detail").innerText(),/ARCHITECTURE/i);
    assert.match(await page.locator("#record-detail").innerText(),/REVISION/i);
    assert.equal(await page.locator("#record-detail .source-button").count(),1);
    assert.ok((await page.url()).includes("project=PRJ-000001"));
    await page.locator("#breadcrumbs button").first().click();
    assert.equal(await page.locator(".company-card").count(),3);
    await page.locator("#library-search").fill("Example Construction B");
    assert.equal(await page.locator(".company-card").count(),1);
    await page.locator("#clear-search").click();
    assert.equal(await page.locator(".company-card").count(),3);
    await page.goto(ROOT + "/editing.html", {waitUntil:"domcontentloaded"});
    assert.match(await page.locator("main").innerText(),/project_resources/);
    assert.equal(await page.locator("a[href*='gid=8000011']").count() > 0,true);
    await page.goto(ROOT + "/operations.html", {waitUntil:"domcontentloaded"});
    await page.locator("#sources .record").first().waitFor();
    await page.locator("#live-catalogue-readback").waitFor();
    await page.waitForFunction(() => document.getElementById("live-catalogue-readback").textContent.includes("Reviewed catalogue"));
    await page.goto(ROOT + "/workspaces.html", {waitUntil:"domcontentloaded"});
    assert.equal(await page.locator(".portal-card-primary").count(),2);
    assert.equal(await page.locator('nav[aria-label="Primary resource tabs"] a[href="./field.html"]').count(),1);
    await page.locator('.portal-card-primary[href="./field.html"]').click();
    assert.match(await page.locator("#fishtail").innerText(),/Worker Money/);
    assert.match(await page.locator("#rohini").innerText(),/NOT ADMITTED/);
    assert.match(await page.locator("#unassigned").innerText(),/Measurements of works/);
    assert.equal(await page.locator('a[href*="docs.google.com/spreadsheets/"]').count(),1);
    assert.equal(await page.locator('a[href*="drive.google.com/drive/folders/"]').count(),0);
    await page.goto(ROOT + "/workspaces.html", {waitUntil:"domcontentloaded"});
    await page.goto(ROOT + "/field.html", {waitUntil:"domcontentloaded"});
    await page.locator('#fishtail a[href="./money.html#workforce"]').first().click();
    await page.locator("#workforce").waitFor();
    assert.match(await page.locator("#workforce").innerText(),/W01–W21/);
    assert.match(await page.locator("#contractors").innerText(),/Cost Estimation/);
    await page.waitForFunction(() => document.getElementById("money-sync-status").textContent.includes("Reviewed site-resource catalogue"));
    assert.equal(await page.locator('a[href*="drive.google.com/drive/folders/"]').count(),0);
    await page.goto(ROOT + "/money.html", {waitUntil:"domcontentloaded"});
    assert.equal(await page.locator("#workforce").count(),1);
    assert.equal(await page.locator("#contractors").count(),1);
    assert.equal(await page.locator("#vendors").count(),1);
    await page.goto(ROOT + "/", {waitUntil:"domcontentloaded"});
    await page.locator(".company-card").first().waitFor();

    const mobile = await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
    mobile.on("pageerror", error => errors.push(error.message));
    await mobile.goto(ROOT + "/", {waitUntil:"domcontentloaded"});
    await mobile.locator(".company-card").first().waitFor();
    const fit = await mobile.evaluate(() => ({
      viewport:document.documentElement.clientWidth,
      scroll:document.documentElement.scrollWidth
    }));
    assert.ok(fit.scroll <= fit.viewport + 2, "Horizontal overflow at mobile viewport: " + JSON.stringify(fit));
    await mobile.locator(".company-card").first().click();
    await mobile.locator(".project-card").first().click();
    await mobile.locator("#facet-discipline").selectOption({label:"Architecture"});
    assert.equal(await mobile.locator(".resource-line").count(),1);
    await mobile.locator(".resource-line").first().click();
    assert.match(await mobile.locator("#record-detail").innerText(),/Open original/);
    await mobile.goto(ROOT + "/workspaces.html", {waitUntil:"domcontentloaded"});
    const workspaceFit = await mobile.evaluate(() => ({viewport:document.documentElement.clientWidth, scroll:document.documentElement.scrollWidth}));
    assert.ok(workspaceFit.scroll <= workspaceFit.viewport + 2, "Workspaces mobile overflow");
    await mobile.goto(ROOT + "/field.html", {waitUntil:"domcontentloaded"});
    const fieldFit = await mobile.evaluate(() => ({viewport:document.documentElement.clientWidth, scroll:document.documentElement.scrollWidth}));
    assert.ok(fieldFit.scroll <= fieldFit.viewport + 2, "Field Resources mobile overflow");
    assert.equal(await mobile.locator('.field-record').count() >= 12, true);
    await mobile.goto(ROOT + "/money.html", {waitUntil:"domcontentloaded"});
    const moneyFit = await mobile.evaluate(() => ({viewport:document.documentElement.clientWidth, scroll:document.documentElement.scrollWidth}));
    assert.ok(moneyFit.scroll <= moneyFit.viewport + 2, "Money hub mobile overflow");
    await mobile.goto(ROOT + "/?company=display-example-construction-b&project=PRJ-000002", {waitUntil:"domcontentloaded"});
    await mobile.locator(".resource-line").first().waitFor();
    assert.match(await mobile.locator("#workspace").innerText(),/Site B/);
    await mobile.goto(ROOT + "/resources/project-documents.html?project=PRJ-000029", {waitUntil:"domcontentloaded"});
    await mobile.locator("#load-status").waitFor();
    await mobile.waitForFunction(() => document.getElementById("load-status").textContent.includes("Sheets readback"));
    assert.match(await mobile.locator("#project-name").textContent(),/Site C/);
    if (errors.length) throw new Error("Browser console errors: " + errors.join(" | "));
    console.log("Browser QA PASS: normalized empty slots, source-linked records, workspaces, finance boundaries, desktop/mobile overflow, legacy packet URL.");
  } finally {
    await browser.close();
  }
}
qa().catch(e => {console.error(e);process.exitCode=1;});
