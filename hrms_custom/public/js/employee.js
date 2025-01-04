frappe.ui.form.on("Employee", {
	onload(frm){
		if (!$("link[href='https://fonts.cdnfonts.com/css/Calibri']").length) {
            $("<link>", {
                rel: "stylesheet",
                href: "https://fonts.cdnfonts.com/css/Calibri"
            }).appendTo("head");
        }
	},
	
	refresh: function (frm) {
	    frm.fields_dict['custom_email_signature'].$wrapper.empty().append(generate_email_signatre(frm.doc));

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



function generate_email_signatre (doc){
	const full_name = `${doc.first_name} ${doc.last_name}`.toUpperCase();
	const designationDept = `${doc.designation}-${doc.department.replace(" - PMIPL", "")}`;
	let phone = '+91 (0) 240-6644 444';
	if (doc.custom_company_mobile) {
		phone = `${doc.custom_company_mobile}`;
	} else if (doc.custom_company_extension_no >= 200 && doc.custom_company_extension_no <= 499) {
		phone = `+91 (0) 240-6644 ${doc.custom_company_extension_no}`;
	} 

  return `
  
<div style="background-color: #ffffff;
                border-radius: 10px;
                height: 5.373cm;
                width: 8.501cm;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                padding: 10px;
                font-family: 'Calibri';">
    <table style="text-align: left;
                      width: 100%;margin: 0 15px; margin-top:15px;">
      <tr>
          <tr>
        <td style="width: 55%; padding: 15px 0;">
          <h1 style="color: #0033a0; font-size: 16px;  font-weight: 700; margin: 0; padding: 0; margin-bottom:5px;">${full_name}</h1>
          <p style="color: #0033a0; font-size: 12px; margin: 0; padding: 0; ">${designationDept}</p>
          <p style="color: #0033a0; font-size: 10px; margin: 0; padding: 0; ">Parason Machinery (I) Pvt Ltd</p>
      </td>
        <td style="width: 45%;
                           padding: 15px 0;
                           ">
          <div style="display: flex;
                                justify-content: start;
                                align-items: center;
                                ">
            <img src="https://cdn.prod.website-files.com/651bf456326f41a7abbd6228/67179a23d72eef013c7d35ae_phone-call%201.png"
              width="10px" height="10px">
            <a style="font-size: 10px;
                                   color: #0033a0;
                                   margin-left: 5px;">${phone}</a>
          </div>
		
          <div style="display: flex;
                                justify-content: start;
                                
                                align-items: center;">
            <img src="https://cdn.prod.website-files.com/651bf456326f41a7abbd6228/67179a23b623870f9f983e35_email.png"
              width="10px" height="10px">
            <a href="mailto:${doc.company_email}" style="font-size: 10px;
                                  color: #0033a0;
                                  text-decoration: none;
                                  margin-left: 5px;">${doc.company_email}</a>
          </div>
          <div style="display: flex;
                                

                                justify-content: start;
                                align-items: center;">
            <img src="https://cdn.prod.website-files.com/651bf456326f41a7abbd6228/67179a238cbf06271e9abd5a_web%20(1).png"
              width="10px" height="10px">
            <a href="https://parason.com" target="_blank" style="font-size: 10px;
                                  color: #0033a0;
                                  text-decoration: none;
                                  margin-left: 5px;">www.parason.com</a>
          </div>
        </td>
      </tr>
    </table>

    <hr style="height: 1px; width: 300px;
                   background-color: #e60000; margin:0" />

    <table style="width: 100%;
                      margin: 8px 15px; ;
                      color: #0033a0;">
      <tr>
       
          <a href="https://parason.com" target="_blank" style="
                                text-decoration: none;
                                ">
            <img src="https://cdn.prod.website-files.com/651bf456326f41a7abbd6228/6718929fc8da27b3a704da26_image.png" alt="Parason Logo" style="height: 60px; width: 302px;">
          </a>
       
      </tr>
    </table>
  </div>


<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>


<html>
<head>
<title>PARASON E-Mail Sign Templete</title>
<style type="text/css">
hr.new5 
{
  border: 1px solid #2a3c7e;
  border-radius: 5px;
}
.column 
{
	float: left;
	height: auto;
	line-height: 16.5px;
	border-left-width: 1px;
	border-left-style: solid;
	width: auto;
	border-left-color: #1D6CB0;
	padding-top: 0px;
	padding-right: 8px;
	padding-bottom: 8px;
	padding-left: 15px;
}
.row:after {
  content: "";
  display: table;
  clear: both;
  height: 90px;
}
</style>
</html>
</head>

<div class="row">
<div><span style="color: #2a3c7e; font-family: Calibri; font-size: medieum;"><strong>Thanks and Regards</strong></span></div>
<div><hr class="new5"></div>
<table style="border-collapse: collapse; width: 50%;" border="0">
<tbody>
<tr>
<td style="width: 13.471%;">
<center style="margin-top: 10px;">
<span style="color: #2a3c7e; font-family: sans-serif; font-size: xx-small;">
<!--  <a href="https://parason.com"><img src="https://parason.com/wp-content/uploads/2018/10/webLogo.png" alt="" width="170" height="40" /></a><br />  -->
<a href="https://parason.com"><img src="https://cdn.prod.website-files.com/651bf456326f41a7abbd6228/66fd14b418c4db12f40ccc65_FdYRGhoJ6ED44zMK1BiU9-transformed.png" alt="" width="170" height="40" /></a><br />
</span>
</center>
<center style="margin-top: 10px;">
<font color="#2a3c7e" font size="1" face="sans-serif">Follow us</font></br>
</center>

<center>
<a href="https://www.facebook.com/ParasonMachinery"><img src="https://parason.com/wp-content/uploads/2019/09/calpher-fb.png" width="20" height="20" /></a>
<a href="https://www.linkedin.com/company/parason"><img src="https://parason.com/wp-content/uploads/2019/09/calpher-linkedin.png" width="20" height="20" /></a>
<a href="https://twitter.com/parasongroup"><img src="https://parason.com/wp-content/uploads/2019/09/calpher-twitter.png" width="20" height="20" /></a>
<a href="https://www.youtube.com/channel/UCDx8c7x7gPsUGLd31ktlJuQ"><img src="https://parason.com/wp-content/uploads/2019/09/calpher-youtube.png" width="20" height="20" /></a>
</center>
</td>
<td style="width: 69.0083%; text-align: left;">
 <div class="column">
  <font color="#2a3c7e" font face="Calibri" size="2"><b>Umakanth Kaspa</b></font><br>   
<font color="#2a3c7e" font face="Calibri" size="1">Software Developer-IT</font>
<br />
<font color="#363636" font face="Calibri" size="1.5">
<img src="https://parason.com/wp-content/uploads/2019/09/parason-clpher-email.png" alt="" width="11" height="8" />&nbsp; kaspa.umakanth@parason.com &nbsp; &nbsp; 
<img src="https://parason.com/wp-content/uploads/2019/09/mobile-calpher.png" width="8" height="10">&nbsp; +91-9999999999<br>
<img src="https://parason.com/wp-content/uploads/2019/09/phone-calpher.png" width="8" height="10">&nbsp;&nbsp; +91 (0) 240-6644-444  &nbsp; | &nbsp; +91 (0) 240-6644 444
<br>
<img src="https://parason.com/wp-content/uploads/2019/09/office-calpher.png" width="10" height="10">&nbsp; Golden Dreams IT Park, 4th Floor, E-27, <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Chikalthana MIDC, Chh. Sambhajinagar (Aurangabad) — 431006
<br>
</font>
<img src="https://parason.com/wp-content/uploads/2019/09/calpher-web.png" width="10" height="10">&nbsp;
<a href="https://parason.com" style="font-family:Calibri; color:#2a3c7e; font-size:10px; text-decoration:none;">www.parason.com</a>&nbsp;&nbsp;
<img src="https://parason.com/wp-content/uploads/2019/09/parason-clpher-email.png" width="10" height="10">&nbsp;
<a href="mailto:info@parason.com" style="font-family: Calibri; color: #2a3c7e; font-size: 10px; text-decoration: none;">info@parason.com</a>&nbsp;&nbsp;

</div>
</td>
</tr>
</tbody>
</table>
</div>

`
}