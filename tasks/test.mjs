import fetch from "node-fetch";
import fs from "fs";
import { diffChars } from "diff";
import { globSync } from "glob";
import { html_beautify } from "js-beautify/js/lib/beautify-html.js";

console.log("Running tests...");
const testEndpoint = "http://127.0.0.1:5000/";
const standardiseHtml = (html) =>
  html_beautify(
    html
      .replace(/(\n\s*){1,}/g, "")
      .replace(/\s{2,}/g, " ")
      .replace(/(\w+)="([^"]*)\s+"/g, '$1="$2"')
      .replace(/(\w+)="\s+([^"]*)"/g, '$1="$2"'),
    {
      "wrap-attributes": "force",
      "preserve-newlines": false,
    }
  );
const fixturesDirectory = `../tna-frontend/src/nationalarchives/components/`;
const components = globSync(`${fixturesDirectory}*/fixtures.json`)
  .map((componentFixtureFile) => {
    const name = componentFixtureFile
      .replace(new RegExp(`^${fixturesDirectory}`), "")
      .replace(new RegExp(/\/fixtures.json$/), "");
    return {
      name,
      testUrl: `${testEndpoint}${name}`,
      fixtures: [],
    };
  })
  .map((component) => {
    const { fixtures } = JSON.parse(
      fs.readFileSync(
        `${fixturesDirectory}${component.name}/fixtures.json`,
        "utf8"
      )
    );
    return {
      ...component,
      fixtures,
    };
  });

for (let i = 0; i < components.length; i++) {
  const component = components[i];
  console.log(`------------------------------------------`);
  console.log(`Component: ${component.name}`);
  const { fixtures } = JSON.parse(
    fs.readFileSync(
      `${fixturesDirectory}${component.name}/fixtures.json`,
      "utf8"
    )
  );

  for (let j = 0; j < component.fixtures.length; j++) {
    const fixture = component.fixtures[j];
    const testUrl = `${component.testUrl}?params=${encodeURIComponent(
      JSON.stringify(fixture.options)
    )}`;
    const response = await fetch(testUrl)
      .then((response) => {
        if (response.status >= 400 && response.status < 600) {
          throw new Error("Bad response from server");
        }
        return response;
      })
      .catch((e) => console.error(e, testUrl));
    const body = await response.text();
    const bodyPretty = standardiseHtml(body);
    const fixturePretty = standardiseHtml(fixture.html);
    const mismatch = bodyPretty !== fixturePretty;
    if (mismatch) {
      console.error(`  🔴 [FAIL] ${fixture.name}\n`);
      console.error(testUrl);
      const diff = diffChars(bodyPretty, fixturePretty)
        .map(
          (part) =>
            `${
              part.added ? "\x1b[32m" : part.removed ? "\x1b[31m" : "\x1b[0m"
            }${part.value === " " ? "█" : part.value}`
        )
        .join("");
      console.log(diff);
      console.log("\n");
      process.exitCode = 1;
      throw new Error("Fixtures tests failed");
    } else {
      console.log(`  🟢 [PASS] ${fixture.name}`);
    }
  }
}
