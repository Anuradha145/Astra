# apps/astra/astra/events/sales_partner.py

import frappe
import traceback

def after_insert_customer(doc, method):
    frappe.msgprint("✅ Hook triggered for Sales Partner after_insert")

    try:
        customer_name = doc.partner_name or doc.name

        if not frappe.db.exists("Customer", {"customer_name": customer_name}):
            customer = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": customer_name,
                "customer_type": "Company",
                "customer_group": "Commercial",
                "territory": "All Territories"
            })
            customer.insert()
            frappe.msgprint(f"Customer {customer.name} created for Sales Partner {doc.name}")

            # Optional: Contact from HTML
            if doc.get("contact_html"):
                contact = frappe.get_doc({
                    "doctype": "Contact",
                    "first_name": customer_name,
                    "links": [{
                        "link_doctype": "Customer",
                        "link_name": customer.name
                    }],
                    "notes": doc.contact_html
                })
                contact.insert()
                frappe.msgprint("Contact created.")

            # Optional: Address from HTML
            if doc.get("address_html"):
                address = frappe.get_doc({
                    "doctype": "Address",
                    "address_title": customer_name,
                    "address_type": "Billing",
                    "links": [{
                        "link_doctype": "Customer",
                        "link_name": customer.name
                    }],
                    "notes": doc.address_html
                })
                address.insert()
                frappe.msgprint("Address created.")

    except Exception as e:
        frappe.log_error(traceback.format_exc(), f"Error in Sales Partner after_insert: {doc.name}")
        frappe.msgprint(f"⚠️ Error: {str(e)}", alert=True)
