#!/usr/bin/env python
"""
Script to fix all remaining client references in views.py
Uses regex to make precise replacements while preserving indentation
"""

import re

def fix_views_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix 1: Replace Client. with Beneficiary. (for model references)
    content = re.sub(r'\bClient\.', 'Beneficiary.', content)
    
    # Fix 2: Replace Client( with Beneficiary( (for constructor calls)
    content = re.sub(r'\bClient\(', 'Beneficiary(', content)
    
    # Fix 3: Replace client_id with beneficiary_id (variable names)
    content = re.sub(r'\bclient_id\b', 'beneficiary_id', content)
    
    # Fix 4: Replace 'client' in function params (careful with word boundaries)
    # Replace: def xxx(request, client_id): -> def xxx(request, beneficiary_id):
    content = re.sub(r'def (\w+)\(request,\s*client_id\)', r'def \1(request, beneficiary_id)', content)
    
    # Fix 5: Replace client variable names (but not beneficiary)
    # Pattern: spaces/tabs followed by 'client' as a word
    # We need to be careful not to replace parts of 'beneficiary'
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_line = line
        
        # Replace variable assignments and function calls like: client = get_object...
        # But only if it's the full word 'client' not part of 'beneficiary'
        # Use negative lookbehind to avoid 'beneficiary'
        # Replace: client =  -> beneficiary =
        # Replace: for client in -> for beneficiary in
        # Replace: client.delete() -> beneficiary.delete()
        # Replace: client.is_active -> beneficiary.is_active
        # etc.
        
        # Skip lines that already have 'beneficiary'
        if 'beneficiary' in new_line:
            new_lines.append(new_line)
            continue
        
        # Replace patterns where 'client' is used as a variable
        # Pattern: word boundary client word boundary, not preceded by 'beneficiary'
        # This is tricky with regex, so let's do simple replacements for common patterns
        
        # client = get_object_or_404(Client, pk=pk) -> beneficiary = get_object_or_404(Beneficiary, pk=pk)
        new_line = re.sub(r'\bclient\s*=\s*get_object_or_404\(Client,\s*pk=(\w+)\)', 
                        r'beneficiary = get_object_or_404(Beneficiary, pk=\1)', new_line)
        
        # client = get_object_or_404(Client, pk=pk) (already handled by Fix 1)
        new_line = re.sub(r'\bclient\s*=\s*get_object_or_404\(Beneficiary,\s*pk=(\w+)\)',
                        r'beneficiary = get_object_or_404(Beneficiary, pk=\1)', new_line)
        
        # for client in clients: -> for beneficiary in beneficiaries:
        new_line = re.sub(r'\bfor\s+client\s+in\s+clients:', 
                        'for beneficiary in beneficiaries:', new_line)
        
        # client.delete() -> beneficiary.delete()
        new_line = re.sub(r'\bclient\.delete\(\)', 'beneficiary.delete()', new_line)
        
        # client.is_active -> beneficiary.is_active
        new_line = re.sub(r'\bclient\.is_active', 'beneficiary.is_active', new_line)
        
        # client.save() -> beneficiary.save()
        new_line = re.sub(r'\bclient\.save\(\)', 'beneficiary.save()', new_line)
        
        # client.name -> beneficiary.name
        new_line = re.sub(r'\bclient\.name\b', 'beneficiary.name', new_line)
        
        # client.total_outstanding -> beneficiary.total_outstanding
        new_line = re.sub(r'\bclient\.total_outstanding\b', 'beneficiary.total_outstanding', new_line)
        
        # client.invoices.all() -> beneficiary.invoices.all()
        new_line = re.sub(r'\bclient\.invoices\.all\(\)', 'beneficiary.invoices.all()', new_line)
        
        # client.payments.all() -> beneficiary.payments.all()
        new_line = re.sub(r'\bclient\.payments\.all\(\)', 'beneficiary.payments.all()', new_line)
        
        # client.opening_balances -> beneficiary.opening_balances
        new_line = re.sub(r'\bclient\.opening_balances\b', 'beneficiary.opening_balances', new_line)
        
        # client.household_count -> beneficiary.household_count
        new_line = re.sub(r'\bclient\.household_count\b', 'beneficiary.household_count', new_line)
        
        # client.beneficiary_type -> beneficiary.beneficiary_type (already fixed)
        # client.client_type -> beneficiary.beneficiary_type
        new_line = re.sub(r'\bclient\.client_type\b', 'beneficiary.beneficiary_type', new_line)
        
        # "client": client -> "beneficiary": beneficiary (in render calls)
        new_line = re.sub(r'"client"\s*:\s*client\b', '"beneficiary": beneficiary', new_line)
        new_line = re.sub(r"'client'\s*:\s*client\b", "'beneficiary': beneficiary", new_line)
        
        # messages.success(request, "Client ..." -> messages.success(request, "Beneficiary ...")
        new_line = re.sub(r'messages\.success\(request,\s*"Client\s+', 'messages.success(request, "Beneficiary ', new_line)
        new_line = re.sub(r"messages\.success\(request,\s*'Client\s+", "messages.success(request, 'Beneficiary ", new_line)
        
        # messages.error(request, "Client ..." -> messages.error(request, "Beneficiary ...")
        new_line = re.sub(r'messages\.error\(request,\s*"Client\s+', 'messages.error(request, "Beneficiary ', new_line)
        new_line = re.sub(r"messages\.error\(request,\s*'Client\s+", "messages.error(request, 'Beneficiary ", new_line)
        
        new_lines.append(new_line)
    
    content = '\n'.join(new_lines)
    
    # Fix 6: Replace function names
    function_mappings = [
        ('def client_list(', 'def beneficiary_list('),
        ('def client_create(', 'def beneficiary_create('),
        ('def client_edit(', 'def beneficiary_edit('),
        ('def client_delete(', 'def beneficiary_delete('),
        ('def client_toggle_status(', 'def beneficiary_toggle_status('),
        ('def client_detail(', 'def beneficiary_detail('),
        ('def bulk_client_create(', 'def bulk_beneficiary_create('),
        ('def bulk_client_import(', 'def bulk_beneficiary_import('),
        ('def download_client_template(', 'def download_beneficiary_template('),
        ('def client_pdf_report(', 'def beneficiary_pdf_report('),
        ('def client_invoices_json(', 'def beneficiary_invoices_json('),
    ]
    
    for old, new in function_mappings:
        content = content.replace(old, new)
    
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
    print(f"Fixing {filepath}...")
    fix_views_file(filepath)
    print("Done!")
