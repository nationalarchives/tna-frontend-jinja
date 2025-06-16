import { expect } from "@playwright/test";

export const expectFormFailure = async (page) => {
  await expect(page.getByRole("main")).toHaveText(/There is a problem/);
  await expect(page.getByRole("main")).toHaveText(/Form contains errors/);
};
export const expectFormSuccess = async (page) => {
  await expect(page.getByRole("main")).not.toHaveText(/There is a problem/);
  await expect(page.getByRole("main")).toHaveText(
    /Form submitted successfully/,
  );
};

export const expectSingleFieldValue = async (page, expectedValue) => {
  console.log(await page.getByTestId("form_data"));
  console.log(await page.getByTestId("form_data").textContent());
  const json = JSON.parse(await page.getByTestId("form_data").textContent());
  await expect(json.field).toEqual(expectedValue);
};
