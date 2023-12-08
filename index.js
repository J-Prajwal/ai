const { dockStart } = require("@nlpjs/basic");
const express = require("express");
const cors = require("cors");
const csv = require("csv-parser");
const fs = require("fs");
const { exec } = require("child_process");
const corpus = require("./corpus.json");

const app = express();

app.use(express.json());
app.use(cors());

function getDistinctValuesExcludingColumns(
  csvFilePaths,
  excludedColumns,
  callback
) {
  const distinctValues = {};

  let processedFiles = 0;

  csvFilePaths.forEach((csvFilePath, index) => {
    fs.createReadStream(csvFilePath)
      .pipe(csv())
      .on("data", (row) => {
        Object.keys(row).forEach((column) => {
          if (!excludedColumns.includes(column)) {
            if (!distinctValues[column]) {
              distinctValues[column] = new Set();
            }
            distinctValues[column].add(row[column]);
          }
        });
      })
      .on("end", () => {
        processedFiles++;
        if (processedFiles === csvFilePaths.length) {
          callback(null, distinctValues);
        }
      })
      .on("error", (error) => {
        callback(error, null);
      });
  });
}

app.listen(4000, () => {
  console.log("Server listening at port: http://localhost:4000");
});

(async () => {
  const dock = await dockStart({
    settings: {
      nlp: {
        forceNER: true,
        languages: ["en"],
        corpora: [corpus],
      },
    },
    use: ["Basic", "LangEn"],
  });
  const manager = dock.get("nlp");

  await manager.train();

  app.get("/makeQuery", async (req, res) => {
    const userQuery = req.query.query;
    const pythonScript = "csv_query.py";

    exec(`python ${pythonScript} ${userQuery}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        return res.status(500).json({
          error: "An error occurred while running the Python script.",
        });
      }

      let response;
      try {
        response = eval("(" + stdout + ")");
      } catch (e) {
        console.error("Error in converting string to JSON: " + e);
      }
      return res.status(200).json({
        message: "Python script executed successfully.",
        output: response,
      });
    });
  });

  app.get("/getOverview", async (req, res) => {
    const pythonScript2 = "overview.py";
    exec(`python ${pythonScript2}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        return res.status(500).json({
          error: "An error occurred while running the Python script.",
        });
      }

      let response;
      try {
        response = eval("(" + stdout + ")");
      } catch (e) {
        console.error("Error in converting string to JSON: " + e);
      }
      return res.status(200).json({
        message: "Python script executed successfully.",
        output: response,
      });
    });
  });
  
  app.get("/getRecords", async (req, res) => {
    const pythonScript = "records.py";
    const userQuery = req.query.query;
    exec(`python ${pythonScript} ${userQuery}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        return res.status(500).json({
          error: "An error occurred while running the Python script.",
        });
      }

      let response;
      try {
        response = eval("(" + stdout + ")");
      } catch (e) {
        console.error("Error in converting string to JSON: " + e);
      }
      return res.status(200).json({
        message: "Python script executed successfully.",
        output: response,
      });
    });
  });

  app.get("/getInfo", async (req, res) => {
    try {
      const userQuery = req.query.query;
      const response = await manager.process(userQuery);
      res.status(200).send(response);
    } catch (e) {
      res.status(404).send({ message: "error", e });
    }
  });

  app.get("/processCSV", async (req, res) => {
    try {
      const csvFiles = [
        "./data/transfer_action.csv",
        "./data/site_accepted_for_filing.csv",
      ];

      // columns to be ignored
      const excludedColumns = [
        "unique_column_id",
        "commencement_date",
        "area_op",
      ];

      getDistinctValuesExcludingColumns(
        csvFiles,
        excludedColumns,
        (error, distinctValues) => {
          if (error) {
            console.error("Error:", error);
            return res.status(500).json({
              error: "An error occurred while processing the CSV files.",
            });
          }

          const corpus = JSON.parse(fs.readFileSync("./corpus.json", "utf-8"));

          Object.keys(distinctValues).forEach((column) => {
            if (!corpus.entities[column]) {
              corpus.entities[column] = { options: {} };
            }
            distinctValues[column].forEach((value) => {
              if (value.trim() !== "") {
                if (!corpus.entities[column].options[value]) {
                  corpus.entities[column].options[value] = [value];
                }
              }
            });
          });

          fs.writeFileSync("./corpus.json", JSON.stringify(corpus, null, 2));

          console.log(
            "Distinct Values excluding specified columns and empty strings:",
            distinctValues
          );
          res.status(200).json({
            message:
              "CSV files processed successfully excluding specified columns and empty strings.",
            distinctValues,
          });
        }
      );
    } catch (e) {
      res.status(404).send({ message: "Error", e });
    }
  });
})();


