// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("Appraisal", {
	setup: function(frm) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","custom_pms_eligibility", "in", ["KRA", "Activity"]]
				]
			}
		});

		if(frm.doc.__islocal){
			frm.set_value("custom_is_final",1) 
		}
	},
	refresh(frm) {
		if (!frm.doc.__islocal) {
			frm.trigger("add_custom_buttons");
			frm.trigger("show_feedback_history");
			frm.trigger("setup_chart");
		}

		// don't allow removing image (fetched from employee)
		frm.sidebar.image_wrapper.find(".sidebar-image-actions").addClass("hide");

		// make field editable/readonly
		setTimeout(() => {
			if(frm.doc.workflow_state == 'Draft'){
				frappe.db.get_value('Employee', frm.doc.employee, 'user_id').then(r => {
					if(frappe.session.user == r.message.user_id){
						//goals
						frm.fields_dict.goals.grid.update_docfield_property("custom_self_score", "read_only", 0);
						frm.fields_dict.goals.grid.update_docfield_property("score", "read_only", 1);

						//activity
						frm.fields_dict.custom_activities.grid.update_docfield_property("self_score", "read_only", 0);
						frm.fields_dict.custom_activities.grid.update_docfield_property("score", "read_only", 1);
					}
					else{
						//goals
						frm.fields_dict.goals.grid.update_docfield_property("custom_self_score", "read_only", 1);

						//activity
						frm.fields_dict.custom_activities.grid.update_docfield_property("self_score", "read_only", 1);
					}
				})
			}
			else{
				//goals
				frm.fields_dict.goals.grid.update_docfield_property("custom_self_score", "read_only", 1);

				//activity
				frm.fields_dict.custom_activities.grid.update_docfield_property("custom_self_score", "read_only", 1);
			}
		}, 500);

		//remove self score column
		// setTimeout(() => {
		// 	removeColumns(frm, ['custom_self_score'], 'custom_self_appraisal_kra')
		// }, 500);
	},

	appraisal_template(frm) {
		if (frm.doc.appraisal_template) {
			frm.call("set_kras_and_rating_criteria", () => {
				frm.refresh_field("appraisal_kra");
				frm.refresh_field("feedback_ratings");
			});
		}
	},

	appraisal_cycle(frm) {
		if (frm.doc.appraisal_cycle) {
			frappe.run_serially([
				() => {
					if (frm.doc.__islocal && frm.doc.appraisal_cycle) {
						frappe.db.get_value("Appraisal Cycle", frm.doc.appraisal_cycle, "kra_evaluation_method", (r) => {
							if (r.kra_evaluation_method) {
								frm.set_value("rate_goals_manually", cint(r.kra_evaluation_method === "Manual Rating"));
							}
						});
					}
				},
				() => {
					frm.call({
						method: "set_appraisal_template",
						doc: frm.doc,
					});
				}
			]);
		}
	},

	add_custom_buttons(frm) {
		frm.add_custom_button(__("View Goals"), function() {
			frappe.route_options = {
				company: frm.doc.company,
				employee: frm.doc.employee,
				appraisal_cycle: frm.doc.appraisal_cycle,
			};
			frappe.set_route("Tree", "Goal");
		});
	},

	show_feedback_history(frm) {
		frappe.require("performance.bundle.js", () => {
			const feedback_history = new hrms.PerformanceFeedback({
				frm: frm,
				wrapper: $(frm.fields_dict.feedback_html.wrapper),
			});
			feedback_history.refresh();
		});
	},

	setup_chart(frm) {
		const labels = [];
		const maximum_scores = [];
		const scores = [];

		frm.doc.appraisal_kra.forEach((d) => {
			labels.push(d.kra);
			maximum_scores.push(d.per_weightage || 0);
			scores.push(d.goal_score || 0);
		});

		if (labels.length && maximum_scores.length && scores.length) {
			frm.dashboard.render_graph({
				data: {
					labels: labels,
					datasets: [
						{
							name: "Maximum Score",
							chartType: "bar",
							values: maximum_scores,
						},
						{
							name: "Score Obtained",
							chartType: "bar",
							values: scores,
						}
					]
				},
				title: __("Scores"),
				height: 250,
				type: "bar",
				barOptions: {
					spaceRatio: 0.7
				},
				colors: ["blue", "green"]
			});
		}
	},

	calculate_total(frm) {
		let total = 0;

		frm.doc.goals.forEach((d) => {
			total += flt(d.score);
		});

		frm.set_value("total_score", total);
	}
});


frappe.ui.form.on("Appraisal Goal", {
	score(frm, cdt, cdn) {
		let d = frappe.get_doc(cdt, cdn);

		if (flt(d.score) > flt(d.per_weightage)) {
			frappe.msgprint(__("Score must be less than or equal to weightage"));
			d.score = 0;
			refresh_field("score", d.name, "goals");
		} else {
			frm.trigger("set_score_earned", cdt, cdn);
		}
	},

	per_weightage(frm, cdt, cdn) {
		frm.trigger("set_score_earned", cdt, cdn);
	},

	goals_remove(frm, cdt, cdn) {
		frm.trigger("set_score_earned", cdt, cdn);
	},

	set_score_earned(frm, cdt, cdn) {
		let d = frappe.get_doc(cdt, cdn);

		let score_earned = flt(d.score) * flt(d.per_weightage) / 100;
		frappe.model.set_value(cdt, cdn, "score_earned", score_earned);

		frm.trigger("calculate_total");
	},
	custom_self_score(frm, cdt, cdn) {
		let d = frappe.get_doc(cdt, cdn);
		if (flt(d.custom_self_score) > flt(d.per_weightage)) {
			frappe.msgprint(__("Score must be less than or equal to weightage"));
			d.score = 0;
			refresh_field("score", d.name, "goals");
		} else {
			frm.trigger("set_score_earned", cdt, cdn);
		}
	},
});

// function removeColumns(frm, fields, table) {
//     let grid = frm.get_field(table).grid;
    
//     for (let field of fields) {
//         grid.fields_map[field].hidden = 1;
//     }
    
//     grid.visible_columns = undefined;
//     grid.setup_visible_columns();
    
//     grid.header_row.wrapper.remove();
//     delete grid.header_row;
//     grid.make_head();
    
//     for (let row of grid.grid_rows) {
//         if (row.open_form_button) {
//             row.open_form_button.parent().remove();
//             delete row.open_form_button;
//         }
        
//         for (let field in row.columns) {
//             if (row.columns[field] !== undefined) {
//                 row.columns[field].remove();
//             }
//         }
//         delete row.columns;
//         row.columns = [];
//         row.render_row();
//     }
// 	frm.refresh_field("custom_self_appraisal_kra")
// }