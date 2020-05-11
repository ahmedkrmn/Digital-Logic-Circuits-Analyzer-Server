const express = require("express");
const apiResponse = require("../helpers/apiResponse");
const path = require("path");
const spawn = require("child_process").spawn;
const router = express.Router();
const multer = require("multer");

// Configure the storage object for multer
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, path.join(__dirname, "../uploads"));
  },
  // Use dynamic file name instead of this
  // filename: (req, file, cb) => {
  //   let image_type;
  //   // If uploaded by user or sent as blob json
  //   if (file.mimetype.split("/")[0] == "image")
  //     image_type = file.mimetype.split("/")[1];
  //   else image_type = "png";
  //   cb(null, "image" + image_type);
  // },
});
const upload = multer({ storage });

/* GET home page. */
router.get("/", (req, res) => {
  return apiResponse.successResponse(res, "You've reached the API!");
});

router.get("/test", (req, res) => {
  const process = spawn("python", [
    path.join(__dirname, "../controllers/test.py"),
  ]);

  process.stdout.on("data", function (out) {
    return apiResponse.successResponseWithData(
      res,
      "Analysis Success",
      JSON.parse(out.toString())
    );
  });
});

router.post("/analyze", upload.single("image_file"), (req, res) => {
  const type = req.body.type;
  const image = req.file.filename;

  let process;

  if (type == "upload") {
    process = spawn("python", [path.join(__dirname, "../controllers/test.py")]);
  } else if (type == "online") {
    process = spawn("python", [
      path.join(__dirname, "../controllers/image_to_truthtable.py"),
      image,
    ]);
  }

  process.stdout.on("data", function (out) {
    return apiResponse.successResponseWithData(
      res,
      "Analysis Success",
      JSON.parse(out.toString())
    );
  });

  process.stderr.on("data", function (err) {
    return apiResponse.ErrorResponse(res, err.toString());
  });
});

module.exports = router;
