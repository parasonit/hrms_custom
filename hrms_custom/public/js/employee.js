frappe.ui.form.on("Employee", {
	refresh: function (frm) {

		setCannotAddDeleteRows(frm)
	
		handleRowButtons()
		frm.set_query("department", function () {
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


function moveButtons(row, fieldName) {
	let $col = $(row).find(`div.col.grid-static-col[data-fieldname="${fieldName}"]`);

	// Clicking the column to focus the row dynamically because the button is initially added when the row is focused
	$col.trigger('click');

	// Move buttons of type Button outside the div to prevent issues with display none
	// This prevents the buttons from disappearing due to certain core events adding display none
	$col.find('div.form-group[data-fieldtype="Button"]').appendTo($col);

	$('div.form-group.frappe-control.input-max-width[data-fieldtype="Button"]').each(function() {
		$(this).css({
			'display': 'flex',
			'justify-content': 'center',
		});
	});
}


// Function to display buttons in child table list-view for existing and newly added rows
function handleRowButtons() {

	// Move buttons for existing rows in the grid body
	$('div.grid-body div.grid-row').each(function () {
		// moveButtons(this, 'view');
		moveButtons(this, 'download');
	});

	// Move buttons for newly added rows when 'grid-add-row' is clicked
	$('.grid-add-row').on('click', function () {
		let $tableContainer = $(this).closest('.frappe-control[data-fieldtype="Table"]');
		let newRow = $tableContainer.find('.grid-row').last();
		moveButtons(newRow, 'view');
		moveButtons(newRow, 'download');
	});
}

frappe.ui.form.on('Form 16', {
    download: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		let URL = '/private/files/random/form-16/'+row.year+"/"+row.name1
		window.open(URL, "_blank");
    }
});

frappe.ui.form.on('Increment Letter', {
    download: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn]
		let URL = '/private/files/random/increment_letter/'+row.year+"/"+row.name1
		window.open(URL, "_blank");
    }
});

function setCannotAddDeleteRows(frm) {
	 let fields = [
        'custom_form_16',
        'custom_increment_letter',
        'custom_attached_documents'
    ];
	fields.forEach(field => {
        frm.set_df_property(field, 'cannot_add_rows', 1);
        frm.set_df_property(field, 'cannot_delete_rows', 1);
    });

}