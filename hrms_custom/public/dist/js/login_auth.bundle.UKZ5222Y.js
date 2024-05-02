(() => {
  // ../hrms_custom/hrms_custom/public/js/login_auth.bundle.js
  console.log("Working....");
  if (frappe.session.user == "Guest" || frappe.session.user === void 0) {
    setTimeout(() => {
      $(".sign-up-message").css("display", "none");
    }, 100);
    frappe.call("parason.utils.auth_url").then((r) => {
      if (r.message) {
        window.location.replace(r.message);
      }
    });
  }
})();
//# sourceMappingURL=login_auth.bundle.UKZ5222Y.js.map
