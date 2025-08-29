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
  const json = JSON.parse(await page.getByTestId("form_data").textContent());
  await expect(json.field).toEqual(expectedValue);
};

export const expectSingleFieldKeyValue = async (page, key, expectedValue) => {
  const json = JSON.parse(await page.getByTestId("form_data").textContent());
  await expect(json.field).toHaveProperty(key);
  await expect(json.field[key]).toEqual(expectedValue);
};
