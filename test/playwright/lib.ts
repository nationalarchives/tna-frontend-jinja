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
