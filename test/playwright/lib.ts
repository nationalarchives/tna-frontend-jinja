import { expect, test, Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { HtmlValidate, ConfigData } from "html-validate";

export const expectFormFailure = async (page: Page) => {
  await expect(page.getByRole("main")).toHaveText(/There is a problem/);
  await expect(page.getByRole("main")).toHaveText(/Form contains errors/);
};
export const expectFormSuccess = async (page: Page) => {
  await expect(page.getByRole("main")).not.toHaveText(/There is a problem/);
  await expect(page.getByRole("main")).toHaveText(
    /Form submitted successfully/,
  );
};

export const expectSingleFieldValue = async (
  page: Page,
  expectedValue: string | number | boolean | Array<any> | null,
) => {
  const json = JSON.parse(
    (await page.getByTestId("form_data").textContent()) || "{}",
  );
  await expect(json.field).toEqual(expectedValue);
};

export const expectSingleFieldKeyValue = async (
  page: Page,
  key: string,
  expectedValue: string,
) => {
  const json = JSON.parse(
    (await page.getByTestId("form_data").textContent()) || "{}",
  );
  await expect(json.field).toHaveProperty(key);
  await expect(json.field[key]).toEqual(expectedValue);
};

export const checkAccessibility: (
  page: Page,
  disableRule?: Array<string>,
) => void = async (page, disableRules = []) => {
  await test.step("Check page accessibility", async () => {
    /* Ignore skip links */
    const accessibilityScanResults = await new AxeBuilder({ page })
      .exclude(".tna-skip-link")
      .disableRules(disableRules)
      .analyze();
    const accessibilityScanViolations = accessibilityScanResults.violations;
    expect(accessibilityScanViolations).toEqual([]);
  });
};

const htmlvalidateConfig: ConfigData = {
  extends: ["html-validate:recommended"],
  rules: {
    "attribute-empty-style": ["off", { style: "omit" }],
    "attribute-boolean-style": ["off", { style: "omit" }],
    "no-trailing-whitespace": "off",
    "form-dup-name": ["error", { shared: ["radio", "checkbox"] }],
  },
};

const htmlvalidate = new HtmlValidate(htmlvalidateConfig);

export const validateHtml: (
  page: Page,
  additionalRules?: object,
) => void = async (page, additionalRules = {}) => {
  await test.step("Validate HTML", async () => {
    const html = await page.content();

    let htmlvalidateInstance = htmlvalidate;
    if (Object.keys(additionalRules).length > 0) {
      console.log(
        "Applying additional HTML validation rules:",
        additionalRules,
      );
      const tempConfig = {
        ...htmlvalidateConfig,
        rules: {
          ...htmlvalidateConfig.rules,
          ...additionalRules,
        },
      };
      htmlvalidateInstance = new HtmlValidate(tempConfig);
    }

    const report = await htmlvalidateInstance.validateString(html);

    const errors =
      report.results[0]?.messages.filter((message) => message.severity === 2) ||
      [];
    await expect(errors).toEqual([]);

    const warnings =
      report.results[0]?.messages.filter((message) => message.severity === 1) ||
      [];
    if (report.warningCount) {
      console.log(`${report.warningCount} warnings`);
      warnings.forEach((message) => {
        console.log(message);
      });
    }
    await expect(report.warningCount).toBeLessThanOrEqual(10);

    await expect(report.valid).toBeTruthy();
  });
};
