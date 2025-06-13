import { test, expect } from "@playwright/test";
import { expectFormFailure, expectFormSuccess } from "./lib";

test("select", async ({ page }) => {
  await page.goto("/forms/select");
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Select an order/);
  await expect(page.getByLabel("Order")).toHaveValue("");
  await page.getByLabel("Order").selectOption({ label: "Relevance" });
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
  await expect(page.getByLabel("Order")).toHaveValue("relevance");
});
