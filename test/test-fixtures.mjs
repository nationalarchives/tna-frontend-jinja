import fetch from "node-fetch";
import fs from "fs";
import { diffChars } from "diff";
import { globSync } from "glob";
import { html_beautify } from "js-beautify/js/lib/beautify-html.js";

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
      .replace(/(\w+)="\s+([^"]*)"/g, '$1="$2"'),
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

for (let i = 0; i < components.length; i++) {
  const component = components[i];
  console.log(`\nComponent: ${component.name}`);
  const { fixtures } = JSON.parse(
    fs.readFileSync(
      `${fixturesDirectory}${component.name}/fixtures.json`,
      "utf8",
    ),
  );

  for (let j = 0; j < component.fixtures.length; j++) {
    const fixture = component.fixtures[j];
    const testUrl = `${component.testUrl}?params=${encodeURIComponent(
      JSON.stringify(fixture.options),
    )}`;
    const response = await fetch(testUrl)
      .then((response) => {
        if (response.status >= 400 && response.status < 600) {
          fail(`${fixture.name}\n`);
          throw new Error("Bad response from server");
        }
        return response;
      })
      .catch((e) => {
        fail(`${fixture.name}\n`);
        console.error(e, testUrl);
      });
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
              part.added ? "\x1b[32m" : part.removed ? "\x1b[31m" : "\x1b[0m"
            }${part.value === " " ? "█" : part.value}`,
        )
        .join("");
      console.log(diff);
      console.log("\n");
      console.log("GREEN text shows expected content that wasn't rendered");
      console.log("RED text shows rendered content that wasn't expected");
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

for (let i = 0; i < utilities.length; i++) {
  const utility = utilities[i];
  console.log(`\nUtility: ${utility.name}`);
  const { fixtures } = JSON.parse(
    fs.readFileSync(
      `${utilitiesFixturesDirectory}${utility.name}/fixtures.json`,
      "utf8",
    ),
  );

  for (let j = 0; j < utility.fixtures.length; j++) {
    const fixture = utility.fixtures[j];
    const testUrl = `${utility.testUrl}?params=${encodeURIComponent(
      JSON.stringify(fixture.options),
    )}`;
    const response = await fetch(testUrl)
      .then((response) => {
        if (response.status >= 400 && response.status < 600) {
          fail(`${fixture.name}\n`);
          throw new Error("Bad response from server");
        }
        return response;
      })
      .catch((e) => {
        fail(`${fixture.name}\n`);
        console.error(e, testUrl);
      });
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
              part.added ? "\x1b[32m" : part.removed ? "\x1b[31m" : "\x1b[0m"
            }${part.value === " " ? "█" : part.value}`,
        )
        .join("");
      console.log(diff);
      console.log("\n");
      console.log("GREEN text shows expected content that wasn't rendered");
      console.log("RED text shows rendered content that wasn't expected");
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
    let fixturePretty = fixture.html;
    const testUrl = `${testEndpoint}templates/${fixture.template.replace(/\.njk/, ".html")}?params=${encodeURIComponent(
      JSON.stringify(fixture.options),
    )}`;
    const response = await fetch(testUrl)
      .then((response) => {
        if (response.status >= 400 && response.status < 600) {
          fail(`${fixture.name}\n`);
          throw new Error("Bad response from server");
        }
        return response;
      })
      .catch((e) => {
        fail(`${fixture.name}\n`);
        console.error(e, testUrl);
      });
    const body = await response.text();
    let bodyPretty = body;
    if (bodyPretty.includes("/* COMPILED_EMAIL_CSS */")) {
      let emailCss = fs.readFileSync(
        "node_modules/@nationalarchives/frontend/nationalarchives/email.css",
        "utf8",
      );
      emailCss = emailCss
        .replace("/*# sourceMappingURL=email.css.map */", "")
        .trim();
      bodyPretty = bodyPretty.replace("/* COMPILED_EMAIL_CSS */", emailCss);
    }
    bodyPretty = standardiseHtml(bodyPretty);
    fixturePretty = standardiseHtml(fixturePretty);
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
              part.added ? "\x1b[32m" : part.removed ? "\x1b[31m" : "\x1b[0m"
            }${part.value === " " ? "█" : part.value}`,
        )
        .join("");
      console.log(diff);
      console.log("\n");
      console.log("GREEN text shows expected content that wasn't rendered");
      console.log("RED text shows rendered content that wasn't expected");
      process.exitCode = 1;
      throw new Error("Fixtures tests failed");
    } else {
      pass(fixture.name);
    }
  });
