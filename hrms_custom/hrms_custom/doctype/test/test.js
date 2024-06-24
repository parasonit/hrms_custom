// Copyright (c) 2024, 8848 and contributors
// For license information, please see license.txt

frappe.ui.form.on("test", {
	refresh(frm) {
        $('div.col.grid-static-col[data-fieldname="view"]').each(function() {
            $(this).click(); 
        });
        $('div.col.grid-static-col[data-fieldname="download"]').each(function() {
            $(this).click(); 
        });
        $('div.col.grid-static-col[data-fieldname="view"]').each(function() {
            var nestedDiv = $(this).find('div.form-group[data-fieldtype="Button"]').detach();
            
            
            $(this).append(nestedDiv);
        });
        $('div.col.grid-static-col[data-fieldname="download"]').each(function() {
            var nestedDiv = $(this).find('div.form-group[data-fieldtype="Button"]').detach();
            
            
            $(this).append(nestedDiv);
        });



        $('div.grid-bodydiv.grid-row').each(function(){
            console.log(this)
        })


        $('.grid-add-row').on('click', function() {
            var newRow = $('div.grid-row').last();
        
            moveButton(newRow, 'view');
            moveButton(newRow, 'download');
        });
        
        function moveButton(row, fieldName) {
            var col = row.find('div.col.grid-static-col[data-fieldname="' + fieldName + '"]');
            col.click();
            var nestedDiv = col.find('div.form-group[data-fieldtype="Button"]').detach();
            col.append(nestedDiv);
        }
        
        
        
    
	},
});
