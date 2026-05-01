#!/usr/bin/env python
"""
Script to refactor Client to Beneficiary in the Django project.
This script makes systematic replacements in views.py
"""

import re
import sys

def refactor_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Store original for comparison
    original = content
    
    # 1. Class name: Client -> Beneficiary
    content = content.replace('Client.', 'Beneficiary.')
    content = content.replace('Client(', 'Beneficiary(')
    content = content.replace('from .models import ', 'from .models import Beneficiary, ')
    # Fix the import line to avoid duplicate
    content = content.replace('from .models import Beneficiary, Beneficiary, ', 'from .models import Beneficiary, ')
    
    # 2. Field names: client -> beneficiary (but careful with beneficiary itself)
    # We need to replace field references like client= -> beneficiary=
    # Use word boundaries to avoid replacing parts of other words
    content = re.sub(r'\bclient_id\b', 'beneficiary_id', content)
    content = re.sub(r'\bclient\b(?!\s*_)', 'beneficiary', content)  # Replace client but not client_something patterns
    
    # 3. Field name: client_type -> beneficiary_type
    content = content.replace('client_type', 'beneficiary_type')
    
    # 4. URL names: client_list -> beneficiary_list, etc.
    url_mappings = [
        ('client_list', 'beneficiary_list'),
        ('client_detail', 'beneficiary_detail'),
        ('client_edit', 'beneficiary_edit'),
        ('client_delete', 'beneficiary_delete'),
        ('client_create', 'beneficiary_create'),
        ('client_toggle_status', 'beneficiary_toggle_status'),
        ('client_pdf_report', 'beneficiary_pdf_report'),
        ('bulk_client_create', 'bulk_beneficiary_create'),
        ('bulk_client_import', 'bulk_beneficiary_import'),
        ('download_client_template', 'download_beneficiary_template'),
        ('client_invoices_json', 'beneficiary_invoices_json'),
        ('send_sms_to_client', 'send_sms_to_beneficiary'),
    ]
    
    for old, new in url_mappings:
        content = content.replace(old, new)
    
    # 5. Model choices: Client.SCHEME_CHOICES -> Beneficiary.SCHEME_CHOICES
    content = content.replace('Client.SCHEME_CHOICES', 'Beneficiary.SCHEME_CHOICES')
    
    # 6. Exception handling: Client.DoesNotExist -> Beneficiary.DoesNotExist
    content = content.replace('Client.DoesNotExist', 'Beneficiary.DoesNotExist')
    content = content.replace('Client.MultipleObjectsReturned', 'Beneficiary.MultipleObjectsReturned')
    
    # 7. Template references
    content = content.replace('client_list.html', 'beneficiary_list.html')
    content = content.replace('client_form.html', 'beneficiary_form.html')
    content = content.replace('client_detail.html', 'beneficiary_detail.html')
    content = content.replace('client_delete.html', 'beneficiary_delete.html')
    content = content.replace('bulk_client_create.html', 'bulk_beneficiary_create.html')
    content = content.replace('bulk_client_import.html', 'bulk_beneficiary_import.html')
    
    # 8. Variable names in function parameters
    content = re.sub(r'def (\w+)\(request,\s*client_id\)', r'def \1(request, beneficiary_id)', content)
    
    # Write back if changes were made
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
        return True
    else:
        print(f"No changes needed: {filepath}")
        return False

if __name__ == '__main__':
    filepath = 'accounting_app/views.py'
    print(f"Refactoring {filepath}...")
    refactor_file(filepath)
    print("Done!")
