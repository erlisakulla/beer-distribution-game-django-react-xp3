/**
 * Import the required modules for UserAPI.js
 */
const { auth, authAdmin } = require("../middlewares/Auth");
const express = require("express");
const router = express.Router();
const { register, login } = require("../controllers/UserController");


// /user/ route

/**
 * Post request that routes to /signup page
 */
router.post("/signup", async (req, res) => {
  const mutedData = await register(req.body);
  res.status(mutedData.status).send(mutedData);
});

/**
 * Post request that routes to /login page
 */
router.post("/login", async (req, res) => {
  const mutedData = await login(req.body);
  res.status(mutedData.status).send(mutedData);
});

module.exports = router;