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
    await page.locator(".resource-line").first().click();
    assert.match(await page.locator("#record-detail").innerText(),/Source register/);
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
    await page.locator("#source-results .source-card").first().waitFor();

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
    await mobile.locator(".resource-line").first().click();
    assert.match(await mobile.locator("#record-detail").innerText(),/Open original/);
    await mobile.goto(ROOT + "/?company=display-example-construction-b&project=PRJ-000002", {waitUntil:"domcontentloaded"});
    await mobile.locator(".resource-line").first().waitFor();
    assert.match(await mobile.locator("#workspace").innerText(),/Site B/);
    await mobile.goto(ROOT + "/resources/project-documents.html?project=PRJ-000029", {waitUntil:"domcontentloaded"});
    await mobile.locator("#load-status").waitFor();
    await mobile.waitForFunction(() => document.getElementById("load-status").textContent.includes("Sheets readback"));
    assert.match(await mobile.locator("#project-name").textContent(),/Site C/);
    if (errors.length) throw new Error("Browser console errors: " + errors.join(" | "));
    console.log("Browser QA PASS: desktop 1366px, mobile 390px, directory navigation, company/project grouping, record provenance, edit links, custody, legacy packet URL, deep links.");
  } finally {
    await browser.close();
  }
}
qa().catch(e => {console.error(e);process.exitCode=1;});
