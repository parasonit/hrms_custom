frappe.pages['pms'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Performance Management',
		single_column: true
	});
}