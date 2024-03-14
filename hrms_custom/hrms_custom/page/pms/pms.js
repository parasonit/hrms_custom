frappe.pages["pms"].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("PMS Dashboard"),
		single_column: true,
	});
	frappe.breadcrumbs.add("pms");

	page.company_field = page.add_field({
		fieldname: 'company',
		label: __('Company'),
		fieldtype: 'Link',
		options: 'Company',
		reqd: 1,
		default: frappe.defaults.get_default("company"),
		change: function() {
			page.capacity_dashboard.refresh();
		}
	});

	page.appraisal_cycle_field = page.add_field({
		fieldname: 'appraisal_cycle',
		label: __('Appraisal Cycle'),
		fieldtype: 'Link',
		options: 'Appraisal Cycle',
		change: function() {
			var appraisal_cycle = this.get_value()
			reset_pms_dashboard(page, appraisal_cycle);
		}
	});

	$(frappe.render_template("pms")).appendTo(page.body.addClass("no-border"));

};

function reset_pms_dashboard(page, appraisal_cycle){
	frappe.call({
		method: "hrms_custom.hrms_custom.page.pms.pms.get_cards",
		type: "GET",
		args: {
			appraisal_cycle: appraisal_cycle,
		},
		callback: function(r) {
			if(r.message){
				update_cards(page, r.message)
			}
		}
	})
}

function update_cards(page, resp){
	$(".card-container").remove();
	let wrapper = '<div class="row card-container">';
	resp.forEach(card => {
		wrapper += `
			<div class="widget number-widget-box" style="width: 22%; margin: 10px 5px;" data-widget-name="Total Employees">
				<div class="widget-head">
					<div class="widget-label">
						<div class="widget-title">
							<span class="ellipsis" title="Total Employees">
								${card.name}
							</span>
						</div>
						<div class="widget-subtitle"></div>
					</div>
				</div>
				<a href="${card.route}" target="_blank">
					<div class="widget-body">
						<div class="widget-content">
							<div class="number">
							${card.total} <!-- Dynamic value, change it according to your requirement -->
							</div>
							<div class="card-stats grey-stat">
								<!-- <span class="percentage-stat-area">
									0  % since last month
								</span> -->
							</div>
						</div>
					</div>
				</a>
				<div class="widget-footer"></div>
			</div>
		`;
	})

	wrapper += '</div>';

	$(wrapper).appendTo(page.body.addClass("no-border"));
}