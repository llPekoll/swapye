import { expect, test } from "@playwright/test";

function makeid(length: number) {
    var result = "";
    var characters =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(
            Math.floor(Math.random() * charactersLength)
        );
    }
    return result;
}
const jose = makeid(7);
const url = "https://dash.swapye.work";
// const url = ""

test("Game Creation", async ({ page }) => {
    await page.goto(`${url}/play/{game}`);
    await page.locator("data-test=email").fill(`${jose}@test.com`);
    await page.locator("data-test=password").fill("sakorizcoko");
    await page.locator("data-test=password_confirm").fill("sakorizcoko");
    await page.locator("data-test=submit").click();
    expect(await page.locator("data-test=email-log"));
});
test("Login", async ({ page }) => {
    await page.goto(`${url}/login`);
    await page.locator("data-test=email-log").fill(`${jose}@test.com`);
    await page.locator("data-test=password").fill("sakorizcoko");
    await page.locator("data-test=submit").click();
    expect(await page.locator("data-test=game-menu"));
});

test("create Game", async ({ page }) => {
    await page.goto(`${url}/login`);
    await page.locator("data-test=email-log").fill(`${jose}@test.com`);
    await page.locator("data-test=password").fill("sakorizcoko");
    await page.locator("data-test=submit").click();
    await page.locator("data-test=add-new").click();
    await page.locator("data-test=name").fill("Ils ricannent");
    await page.locator("data-test=submit").click();
    expect(await page.locator("data-test=game-menu"));
});

test("Edit Game", async ({ page }) => {
    await page.goto(`${url}/login`);
    await page.locator("data-test=email-log").fill(`${jose}@test.com`);
    await page.locator("data-test=password").fill("sakorizcoko");
    await page.locator("data-test=submit").click();
    await page.locator("data-test=add-new").click();
    await page.locator("data-test=name").fill("Ils ricannent");
    await page.locator("data-test=submit").click();
    await page.locator("data-test=account-1").click();
    await page.locator("data-test=menu-game-basics").click();
});
