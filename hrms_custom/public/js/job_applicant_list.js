frappe.listview_settings['Job Applicant'] = {
	get_indicator: function(doc) {
		var colors = {
			'Job Offer Sent': 'blue',
			'Job Offer Approved': 'blue',
			'Open': 'orange',
			'Joined': 'green',
			'Hold': 'orange',
			'Rejected': 'red'
		};
		let status = doc.status;
		return [__(status), colors[status], 'status,=,' + doc.status];
	},
	hide_name_column: true
};
