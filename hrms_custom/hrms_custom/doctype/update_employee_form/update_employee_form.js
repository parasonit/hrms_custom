// Copyright (c) 2024, 8848 and contributors
// For license information, please see license.txt

frappe.ui.form.on("Update Employee Form", {
	refresh(frm) {
        frm.add_custom_button(__("Upload"), function(){
            console.log("uploading...")
            frm.set_value('zip_file', '')
            frm.save()
        }).addClass("btn-warning").css({
            'background': 'cornflowerblue',
            'color': 'white',
            'font-weight': '500'
        })
	}
});
