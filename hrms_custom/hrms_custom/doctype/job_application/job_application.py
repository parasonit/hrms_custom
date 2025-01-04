import frappe
from frappe.model.document import Document
from frappe.utils import get_url
from frappe.model.mapper import get_mapped_doc

class JobApplication(Document):
    
    @frappe.whitelist()
    def send_application_link(self):
        try:
            if not frappe.db.exists("User", self.email_id):
                message = self.create_user_and_send_password_reset()
            else:
                self.add_role_if_user_exists()
                message = "Existing user. Email sent."
            return {"status": "success", "message": message}
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Error in send_application_link")
            return {"status": "error", "message": str(e)}

    def create_user_and_send_password_reset(self):
        user = frappe.get_doc({
            "doctype": 'User',
            "email": self.email_id,
            "first_name": self.applicant_name,
            "send_welcome_email": 0,
            "redirect_url": f'job-application-form/{self.name}',
            "user_type": 'Website User'
        }).insert(ignore_permissions=True)

        user.add_roles('Job Applicant')
        frappe.db.commit()
        self.send_login_link(user.reset_password())
        return "New user created. Email sent."

    def add_role_if_user_exists(self):
        user = frappe.get_doc("User", self.email_id)
        user.add_roles('Job Applicant')
        frappe.db.commit()
        self.send_login_link()

    def send_login_link(self, password_link=None):
        login_url = password_link if password_link else get_url(f"/login?redirect-to=/job-application-form/{self.name}")
        action_text = "Set your password" if password_link else "Log in to your account"

        message = f"""
            <p>Dear {self.applicant_name},</p>
            <p>Your job application has been created.</p>
            <p>You can complete your job application by clicking the button below:</p>
            <p>
                <a href="{login_url}" style="display: inline-block; padding: 10px 20px; font-size: 16px; color: white; background-color: #007bff; text-decoration: none; border-radius: 5px;">
                    {action_text}
                </a>
            </p>
            <p>Best regards,<br>HR Team</p>
        """


        

        frappe.sendmail(
            recipients=[self.email_id],
            subject="Job Application Link",
            message=message,
            now=True,
            reference_doctype=self.doctype,
            reference_name=self.name,
        )

    @frappe.whitelist()
    def convert_to_job_applicant(self):
        try:
            job_applicant = get_mapped_doc(
                "Job Application",
                self.name,
                {
                    "Job Application": {
                        "doctype": "Job Applicant",
                    }
                }
            )
            job_applicant.insert(ignore_permissions=True)
            frappe.db.commit()
            return {"status": "success"}
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), 'Job Application Conversion Failed')
            return {"status": "error", "error": str(e)}

    