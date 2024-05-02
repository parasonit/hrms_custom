console.log("Working....")
if(frappe.session.user == 'Guest' || frappe.session.user === undefined){
    setTimeout(() => {
        $('.sign-up-message').css('display', 'none');
    }, 100);
    frappe.call("hrms_custom.utils.auth_url")
    .then(r => {
        if(r.message){
            window.location.replace(r.message);
        }
    })
}