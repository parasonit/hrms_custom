frappe.ui.form.on("Employee", {
	refresh: function(frm) {
		frm.set_query("department", function() {
			return {
				filters: [
					["Department","is_group", "=", 1]
				]
			}
		});
        if(frm.doc.department){
            frm.events.filter_sub_department(frm);
        }
	},
    department: function(frm) {
		frm.events.filter_sub_department(frm)
	},
    filter_sub_department: function(frm){
        frm.set_query("custom_sub_department", function() {
			return {
				filters: [
					["Department","parent_department", "=", frm.doc.department]
				]
			}
		});
    }
});