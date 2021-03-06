/**
 * Import axios from this module when making a POST request to the Django API.
 */

import axios from "axios";

// Include the CSRF token from the cookie supplied by Django.
// Create custom instance to avoid polluting global settings.
const axiosWithoutAuth = axios.create({
  xsrfHeaderName: "X-CSRFToken",
  xsrfCookieName: "csrftoken",
  withCredentials: false,
});

export default axiosWithoutAuth;
