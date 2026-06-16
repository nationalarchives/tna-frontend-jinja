/* eslint-disable no-console, max-statements, no-magic-numbers, max-lines-per-function, no-ternary */

import fs from "fs";

import { diffChars } from "diff";
import { globSync } from "glob";
/* eslint-disable-next-line camelcase */
import { html_beautify } from "js-beautify/js/lib/beautify-html.js";
import fetch from "node-fetch";

const pass = (message) => {
  console.log("\x1b[42m%s\x1b[0m", " PASS ", "\x1b[0m", message);
};

const fail = (message) => {
  console.error("\x1b[41m%s\x1b[0m", " FAIL ", "\x1b[0m", message);
};

console.log("Running tests...");
const testEndpoint = "http://127.0.0.1:5001/";
const standardiseHtml = (html) =>
  html_beautify(
    html
      .replace(/(\n\s*){1,}/g, "")
      .replace(/\s{2,}/g, " ")
      .replace(/(\w+)="([^"]*)\s+"/g, '$1="$2"')
      .replace(/(\w+)="\s+([^"]*)"/g, '$1="$2"')
      .replace(/&quot;/g, "&#34;"),
    {
      "wrap-attributes": "force",
      "preserve-newlines": false,
    },
  );

const tnaFrontendDirectory = "node_modules/@nationalarchives/frontend";
const fixturesDirectory = `${tnaFrontendDirectory}/nationalarchives/components/`;
const utilitiesFixturesDirectory = `${tnaFrontendDirectory}/nationalarchives/utilities/`;

const components = globSync(`${fixturesDirectory}*/fixtures.json`)
  .map((componentFixtureFile) => {
    const name = componentFixtureFile
      .replace(new RegExp(`^${fixturesDirectory}`), "")
      .replace(new RegExp(/\/fixtures.json$/), "");
    return {
      name,
      testUrl: `${testEndpoint}components/${name}`,
      fixtures: [],
    };
  })
  .map((component) => {
    const { fixtures } = JSON.parse(
      fs.readFileSync(
        `${fixturesDirectory}${component.name}/fixtures.json`,
        "utf8",
      ),
    );
    return {
      ...component,
      fixtures,
    };
  })
  .reverse();

for (
  let intComponent = 0;
  intComponent < components.length;
  intComponent += 1
) {
  const component = components[intComponent];
  console.log(`\nComponent: ${component.name}`);
  // const { fixtures } = JSON.parse(
  //   fs.readFileSync(
  //     `${fixturesDirectory}${component.name}/fixtures.json`,
  //     "utf8",
  //   ),
  // );

  for (
    let intFixture = 0;
    intFixture < component.fixtures.length;
    intFixture += 1
  ) {
    const fixture = component.fixtures[intFixture];
    const testUrl = `${component.testUrl}?params=${encodeURIComponent(
      JSON.stringify(fixture.options),
    )}`;
    /* eslint-disable-next-line no-await-in-loop */
    const response = await fetch(testUrl)
      .then((fetchResponse) => {
        if (fetchResponse.status >= 400 && fetchResponse.status < 600) {
          fail(`${fixture.name}\n`);
          throw new Error("Bad response from server");
        }
        return fetchResponse;
      })
      .catch((err) => {
        fail(`${fixture.name}\n`);
        console.error(err, testUrl);
      });
    /* eslint-disable-next-line no-await-in-loop */
    const body = await response.text();
    const bodyPretty = standardiseHtml(body);
    const fixturePretty = standardiseHtml(fixture.html);
    const mismatch = bodyPretty !== fixturePretty;
    if (mismatch) {
      fail(`${fixture.name}\n`);
      console.error(testUrl);
      const diff = diffChars(bodyPretty, fixturePretty)
        .map(
          (part) =>
            `${
              /* eslint-disable-next-line no-nested-ternary */
              part.added ? "\x1b[32m" : part.removed ? "\x1b[31m" : "\x1b[0m"
            }${part.value === " " ? "█" : part.value}`,
        )
        .join("");
      console.log(diff);
      console.log("\n");
      console.log("GREEN text shows expected content that wasn't rendered");
      console.log("RED text shows rendered content that wasn't expected");
      /* eslint-disable-next-line no-undef */
      process.exitCode = 1;
      throw new Error("Fixtures tests failed");
    } else {
      pass(fixture.name);
    }
  }
}

const utilities = globSync(`${utilitiesFixturesDirectory}*/fixtures.json`)
  .map((utilitiesFixtureFile) => {
    const name = utilitiesFixtureFile
      .replace(new RegExp(`^${utilitiesFixturesDirectory}`), "")
      .replace(new RegExp(/\/fixtures.json$/), "");
    return {
      name,
      testUrl: `${testEndpoint}utilities/${name}`,
      fixtures: [],
    };
  })
  .map((utility) => {
    const { fixtures } = JSON.parse(
      fs.readFileSync(
        `${utilitiesFixturesDirectory}${utility.name}/fixtures.json`,
        "utf8",
      ),
    );
    return {
      ...utility,
      fixtures,
    };
  })
  .reverse();

for (let intUtility = 0; intUtility < utilities.length; intUtility += 1) {
  const utility = utilities[intUtility];
  console.log(`\nUtility: ${utility.name}`);
  // const { fixtures } = JSON.parse(
  //   fs.readFileSync(
  //     `${utilitiesFixturesDirectory}${utility.name}/fixtures.json`,
  //     "utf8",
  //   ),
  // );

  for (
    let intFixture = 0;
    intFixture < utility.fixtures.length;
    intFixture += 1
  ) {
    const fixture = utility.fixtures[intFixture];
    const testUrl = `${utility.testUrl}?params=${encodeURIComponent(
      JSON.stringify(fixture.options),
    )}`;
    /* eslint-disable-next-line no-await-in-loop */
    const response = await fetch(testUrl)
      .then((fetchResponse) => {
        if (fetchResponse.status >= 400 && fetchResponse.status < 600) {
          fail(`${fixture.name}\n`);
          throw new Error("Bad response from server");
        }
        return fetchResponse;
      })
      .catch((err) => {
        fail(`${fixture.name}\n`);
        console.error(err, testUrl);
      });
    /* eslint-disable-next-line no-await-in-loop */
    const body = await response.text();
    const bodyPretty = standardiseHtml(body);
    const fixturePretty = standardiseHtml(fixture.html);
    const mismatch = bodyPretty !== fixturePretty;
    if (mismatch) {
      fail(`${fixture.name}\n`);
      console.error(testUrl);
      const diff = diffChars(bodyPretty, fixturePretty)
        .map(
          (part) =>
            `${
              /* eslint-disable-next-line no-nested-ternary */
              part.added ? "\x1b[32m" : part.removed ? "\x1b[31m" : "\x1b[0m"
            }${part.value === " " ? "█" : part.value}`,
        )
        .join("");
      console.log(diff);
      console.log("\n");
      console.log("GREEN text shows expected content that wasn't rendered");
      console.log("RED text shows rendered content that wasn't expected");
      /* eslint-disable-next-line no-undef */
      process.exitCode = 1;
      throw new Error("Fixtures tests failed");
    } else {
      pass(fixture.name);
    }
  }
}

console.log("\nTemplates");
const templatesDirectory = `${tnaFrontendDirectory}/nationalarchives/templates/`;
const { fixtures } = JSON.parse(
  fs.readFileSync(`${templatesDirectory}fixtures.json`, "utf8"),
);
await fixtures
  .filter((fixture) => fixture.template !== "layouts/_generic.njk")
  .forEach(async (fixture) => {
    const fixtureHtml = fixture.html;
    const testUrl = `${testEndpoint}templates/${fixture.template.replace(/\.njk/, ".html")}?params=${encodeURIComponent(
      JSON.stringify(fixture.options),
    )}`;
    const response = await fetch(testUrl)
      .then((fetchResponse) => {
        if (fetchResponse.status >= 400 && fetchResponse.status < 600) {
          fail(`${fixture.name}\n`);
          throw new Error("Bad response from server");
        }
        return fetchResponse;
      })
      .catch((err) => {
        fail(`${fixture.name}\n`);
        console.error(err, testUrl);
      });
    const body = await response.text();
    const bodyPretty = standardiseHtml(body);
    const fixturePretty = standardiseHtml(fixtureHtml);
    const mismatch = bodyPretty !== fixturePretty;
    if (mismatch) {
      // if (bodyPretty.length > 10000 || fixturePretty.length > 10000) {
      //   console.warn(
      //     "Output is too long to show a diff, but the test has failed because the rendered output doesn't match the expected output. Showing the first 10,000 characters of each for debugging purposes...",
      //   );
      //   bodyPretty = bodyPretty.substring(0, 10000);
      //   fixturePretty = fixturePretty.substring(0, 10000);
      // }
      fail(`${fixture.name}\n`);
      console.error(testUrl);
      const diff = diffChars(bodyPretty, fixturePretty)
        .map(
          (part) =>
            `${
              /* eslint-disable-next-line no-nested-ternary */
              part.added ? "\x1b[32m" : part.removed ? "\x1b[31m" : "\x1b[0m"
            }${part.value === " " ? "█" : part.value}`,
        )
        .join("");
      console.log(diff);
      console.log("\n");
      console.log("GREEN text shows expected content that wasn't rendered");
      console.log("RED text shows rendered content that wasn't expected");
      /* eslint-disable-next-line no-undef */
      process.exitCode = 1;
      throw new Error("Fixtures tests failed");
    } else {
      pass(fixture.name);
    }
  });
