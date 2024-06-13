frappe.listview_settings['Job Requisition'] = {
	hide_name_column: true,
	onload: function (listview) {
		listview.columns.unshift({
			type: "Subject",
			df: {
				label: __("ID"),
				fieldname: "name"
			}
		});
		listview.columns[1].type = 'Field';
		listview.refresh(true);
	}
}
