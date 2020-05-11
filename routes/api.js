const express = require("express");
const apiResponse = require("../helpers/apiResponse");
const path = require("path");
const router = express.Router();
const multer = require("multer");

// Configure the storage object for multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, "../uploads"));
  },
  filename: (req, file, cb) => {
    let image_type;
    // If uploaded by user or sent as blob json
    if (file.mimetype.split("/")[0] == "image")
      image_type = file.mimetype.split("/")[1];
    else image_type = "png";
    cb(null, "image");
  },
});
const upload = multer({ storage });

/* GET home page. */
router.get("/", (req, res) => {
  // Spawn the python process that handles ML and Image Processing
  var spawn = require("child_process").spawn;
  var process = spawn("python", [
    path.join(__dirname, "../controllers/image_to_truthtable.py"),
  ]);

  process.stdout.on("data", function (out) {
    return apiResponse.successResponse(res, out.toString());
  });

  process.stderr.on("data", function (err) {
    return apiResponse.ErrorResponse(res, err.toString());
  });
});

router.post("/analyze", upload.single("image_file"), (req, res) => {
  const type = req.body.type;
  // const image = req.file;

  // Spawn the python process that handles ML and Image Processing
  var spawn = require("child_process").spawn;
  var process = spawn("python", [
    path.join(__dirname, "../controllers/test.py"),
    type,
  ]);

  process.stdout.on("data", function (data) {
    return apiResponse.successResponseWithData(
      res,
      "analysis success",
      JSON.parse(data.toString())
    );
  });
});

module.exports = router;
