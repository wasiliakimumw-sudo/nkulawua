#!/usr/bin/env python
"""
Safe script to refactor Client to Beneficiary in views.py
Only replaces specific patterns with word boundaries
"""

import re

def safe_refactor(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # Skip import lines to avoid breaking them
        if 'from .models import' in line or 'from .forms import' in line:
            new_lines.append(line)
            continue
        
        # Replace function definitions and calls
        new_line = line
        
        # Replace Client.SCHEME_CHOICES
        new_line = new_line.replace('Client.SCHEME_CHOICES', 'Beneficiary.SCHEME_CHOICES')
        
        # Replace Client.DoesNotExist
        new_line = new_line.replace('Client.DoesNotExist', 'Beneficiary.DoesNotExist')
        new_line = new_line.replace('Client.MultipleObjectsReturned', 'Beneficiary.MultipleObjectsReturned')
        
        # Replace URL names
        url_replacements = [
            ('"client_list"', '"beneficiary_list"'),
            ("'client_list'", "'beneficiary_list'"),
            ('"client_detail"', '"beneficiary_detail"'),
            ("'client_detail'", "'beneficiary_detail'"),
            ('"client_edit"', '"beneficiary_edit"'),
            ("'client_edit'", "'beneficiary_edit'"),
            ('"client_delete"', '"beneficiary_delete"'),
            ("'client_delete'", "'beneficiary_delete'"),
            ('"client_create"', '"beneficiary_create"'),
            ("'client_create'", "'beneficiary_create'"),
            ('"client_toggle_status"', '"beneficiary_toggle_status"'),
            ("'client_toggle_status'", "'beneficiary_toggle_status'"),
            ('"client_pdf_report"', '"beneficiary_pdf_report"'),
            ("'client_pdf_report'", "'beneficiary_pdf_report'"),
            ('"bulk_client_create"', '"bulk_beneficiary_create"'),
            ("'bulk_client_create'", "'bulk_beneficiary_create'"),
            ('"bulk_client_import"', '"bulk_beneficiary_import"'),
            ("'bulk_client_import'", "'bulk_beneficiary_import'"),
            ('"download_client_template"', '"download_beneficiary_template"'),
            ("'download_client_template'", "'download_beneficiary_template'"),
            ('"client_invoices_json"', '"beneficiary_invoices_json"'),
            ("'client_invoices_json'", "'beneficiary_invoices_json'"),
        ]
        
        for old, new in url_replacements:
            new_line = new_line.replace(old, new)
        
        # Replace template names
        template_replacements = [
            ('client_list.html', 'beneficiary_list.html'),
            ('client_form.html', 'beneficiary_form.html'),
            ('client_detail.html', 'beneficiary_detail.html'),
            ('client_delete.html', 'beneficiary_delete.html'),
            ('bulk_client_create.html', 'bulk_beneficiary_create.html'),
            ('bulk_client_import.html', 'bulk_beneficiary_import.html'),
        ]
        
        for old, new in template_replacements:
            new_line = new_line.replace(old, new)
        
        # Replace variable names (careful with word boundaries)
        # Replace client_id with beneficiary_id in function params
        new_line = re.sub(r'def (\w+)\(request,\s*client_id\)', r'def \1(request, beneficiary_id)', new_line)
        
        # Replace client= in function calls (like get_object_or_404, create, filter)
        new_line = new_line.replace('client=client,', 'beneficiary=beneficiary,')
        new_line = new_line.replace('client=beneficiary,', 'beneficiary=beneficiary,')
        new_line = new_line.replace('client=inv.client,', 'beneficiary=inv.beneficiary,')
        
        # Replace .client. with .beneficiary.
        new_line = new_line.replace('.client.', '.beneficiary.')
        new_line = new_line.replace('.client_id', '.beneficiary_id')
        
        # Replace client_type with beneficiary_type
        new_line = new_line.replace('client_type', 'beneficiary_type')
        
        # Replace "client" in redirect calls
        new_line = re.sub(r'redirect\("client', 'redirect("beneficiary', new_line)
        new_line = re.sub(r"redirect\('client", "redirect('beneficiary", new_line)
        
        new_lines.append(new_line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"Successfully refactored {filepath}")

if __name__ == '__main__':
    safe_refactor('accounting_app/views.py')
    print("Done!")
