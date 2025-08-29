/// <reference lib="dom"/>

import { test, expect } from "@playwright/test";
import { expectFormFailure, expectFormSuccess } from "./lib";
import path from "path";
import { readFileSync } from "fs";

test("file input", async ({ page }) => {
  await page.goto("/forms/file-input/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - heading "File" [level=1]
  - paragraph: Upload a file
  - button "File"
  - button "Submit"`);
  const describedByLabelId = await page
    .getByLabel("File")
    .getAttribute("aria-describedby");
  await expect(page.locator(`#${describedByLabelId}`)).toContainText(
    "Upload a file",
  );
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Select a file to upload/);
  await page.getByRole("link", { name: "Select a file to upload" }).click();
  await expect(page.getByLabel("File")).toBeFocused();
  const fileChooserPromise = page.waitForEvent("filechooser");
  await page.getByLabel("File").click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles(path.join(__dirname, "../../README.md"));
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /File type not allowed. Only JSON files are accepted./,
  );
  const fileChooserPromise2 = page.waitForEvent("filechooser");
  await page.getByLabel("File").click();
  const fileChooser2 = await fileChooserPromise2;
  await fileChooser2.setFiles(path.join(__dirname, "../../package-lock.json"));
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /File size must be less than 20 KB./,
  );
  const fileChooserPromise3 = page.waitForEvent("filechooser");
  await page.getByLabel("File").click();
  const fileChooser3 = await fileChooserPromise3;
  await fileChooser3.setFiles(path.join(__dirname, "../../package.json"));
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
});

test("multiple file input", async ({ page }) => {
  await page.goto("/forms/files-input/");
  await expect(await page.getByTestId("form")).toMatchAriaSnapshot(`
  - heading "Files" [level=1]
  - paragraph: Upload a set of files
  - button "Files"
  - button "Submit"`);
  const describedByLabelId = await page
    .getByLabel("Files")
    .getAttribute("aria-describedby");
  await expect(page.locator(`#${describedByLabelId}`)).toContainText(
    "Upload a set of files",
  );
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(/Select files to upload/);
  await page.getByRole("link", { name: "Select files to upload" }).click();
  await expect(page.getByLabel("Files")).toBeFocused();
  const fileChooserPromise = page.waitForEvent("filechooser");
  await page.getByLabel("Files").click();
  const fileChooser = await fileChooserPromise;
  await fileChooser.setFiles([
    path.join(__dirname, "../../package.json"),
    path.join(__dirname, "../../README.md"),
  ]);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /File type not allowed. Only JSON files are accepted./,
  );
  const fileChooserPromise2 = page.waitForEvent("filechooser");
  await page.getByLabel("Files").click();
  const fileChooser2 = await fileChooserPromise2;
  await fileChooser2.setFiles([
    path.join(__dirname, "../../package.json"),
    path.join(__dirname, "../../package-lock.json"),
  ]);
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormFailure(page);
  await expect(page.getByRole("main")).toHaveText(
    /Each file size must be less than 20 KB./,
  );
  const fileChooserPromise3 = page.waitForEvent("filechooser");
  await page.getByLabel("Files").click();
  const fileChooser3 = await fileChooserPromise3;
  await fileChooser3.setFiles(path.join(__dirname, "../../package.json"));
  await page.getByRole("button", { name: "Submit" }).click();

  await expectFormSuccess(page);
});

// test("droppable file input", async ({ page }) => {
//   await page.goto("/forms/file-input-droppable/");

//   const buffer = readFileSync(
//     path.join(__dirname, "../../package.json"),
//   ).toString("base64");
//   const dataTransfer = await page.evaluateHandle(
//     async ({ bufferData, localFileName, localFileType }) => {
//       const dt = new DataTransfer();
//       const blobData = await fetch(bufferData).then((res) => res.blob());
//       const file = new File([blobData], localFileName, { type: localFileType });
//       dt.items.add(file);
//       return dt;
//     },
//     {
//       bufferData: `data:application/octet-stream;base64,${buffer}`,
//       localFileName: "package.json",
//       localFileType: "text/json",
//     },
//   );

//   await page.evaluate(
//     () => (document.getElementById("field").style.opacity = "1"),
//   );

//   const $droppableArea = await page.locator(".tna-file-input__droppable");

//   await expect($droppableArea).not.toContainClass(
//     "tna-file-input__droppable--over",
//   );
//   await page.getByLabel("File").dispatchEvent("dragenter", { dataTransfer });
//   await expect($droppableArea).toContainClass(
//     "tna-file-input__droppable--over",
//   );
//   await page.getByLabel("File").dispatchEvent("dragleave", { dataTransfer });
//   await expect($droppableArea).not.toContainClass(
//     "tna-file-input__droppable--over",
//   );
//   await page.getByLabel("File").dispatchEvent("dragenter", { dataTransfer });
//   await expect($droppableArea).toContainClass(
//     "tna-file-input__droppable--over",
//   );
//   await page.getByLabel("File").dispatchEvent("drop", { dataTransfer });
//   await expect($droppableArea).not.toContainClass(
//     "tna-file-input__droppable--over",
//   );

//   await page.getByRole("button", { name: "Submit" }).click();

//   await expectFormSuccess(page);
// });

// test("droppable multiple file input", async ({ page }) => {
//   await page.goto("/forms/files-input-droppable/");
// });
