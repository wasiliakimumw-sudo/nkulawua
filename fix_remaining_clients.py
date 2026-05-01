#!/usr/bin/env python
"""
Fix all remaining client references in views.py
"""
import re

def fix_remaining_clients(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix 1: form = ClientForm(instance=client) -> form = BeneficiaryForm(instance=beneficiary)
    content = content.replace("form = ClientForm(instance=client)", "form = BeneficiaryForm(instance=beneficiary)")
    
    # Fix 2: if invoice.client: -> if invoice.beneficiary:
    content = content.replace('if invoice.client:', 'if invoice.beneficiary:')
    content = content.replace('pre_selected_client = pre_selected_invoice.client', 
                        'pre_selected_beneficiary = pre_selected_invoice.beneficiary')
    content = content.replace("form.initial['client'] = pre_selected_client", 
                        "form.initial['beneficiary'] = pre_selected_beneficiary")
    
    # Fix 3: client = form.cleaned_data['client'] -> beneficiary = form.cleaned_data['beneficiary']
    content = content.replace("client = form.cleaned_data['client']", 
                        "beneficiary = form.cleaned_data['beneficiary']")
    
    # Fix 4: invoice = Invoice.objects.get(pk=invoice_id, client=client) 
    #         -> invoice = Invoice.objects.get(pk=invoice_id, beneficiary=beneficiary)
    content = content.replace('client=client)', 'beneficiary=beneficiary)')
    
    # Fix 5: client.recalculate_totals() -> beneficiary.recalculate_totals()
    content = re.sub(r'\bbeneficiary\.recalculate_totals\(\)', 'beneficiary.recalculate_totals()', content)
    # But also fix if it's still client.recalculate_totals()
    content = content.replace('client.recalculate_totals()', 'beneficiary.recalculate_totals()')
    
    # Fix 6: model_type == 'client' -> model_type == 'beneficiary'
    content = content.replace("model_type == 'client'", "model_type == 'beneficiary'")
    content = content.replace('model_type == "client"', 'model_type == "beneficiary"')
    
    # Fix 7: row_data.get('client', '') -> row_data.get('beneficiary', '')
    content = content.replace("row_data.get('client', '')", "row_data.get('beneficiary', '')")
    content = content.replace('row_data.get("client", "")', 'row_data.get("beneficiary", "")')
    
    # Fix 8: 'client': existing_client -> 'beneficiary': existing_beneficiary
    content = content.replace("'client': existing_client", "'beneficiary': existing_beneficiary")
    content = content.replace('"client": existing_client', '"beneficiary": existing_beneficiary')
    
    # Fix 9: headers with 'client' -> 'beneficiary'
    content = content.replace("'client', 'amount'", "'beneficiary', 'amount'")
    content = content.replace("'client', 'issue_date'", "'beneficiary', 'issue_date'")
    content = content.replace("'client', 'payment_date'", "'beneficiary', 'payment_date'")
    
    # Fix 10: request.GET.get('type', 'client') -> request.GET.get('type', 'beneficiary')
    content = content.replace("request.GET.get('type', 'client')", "request.GET.get('type', 'beneficiary')")
    
    # Fix 11: request.POST.get('type', 'client') -> request.POST.get('type', 'beneficiary')
    content = content.replace("request.POST.get('type', 'client')", "request.POST.get('type', 'beneficiary')")
    
    # Fix 12: Please select a client -> Please select a beneficiary
    content = content.replace('Please select a client', 'Please select a beneficiary')
    
    # Fix 13: Please select at least one client -> Please select at least one beneficiary
    content = content.replace('Please select at least one client', 'Please select at least one beneficiary')
    
    # Fix 14: Client name is required -> Beneficiary name is required
    content = content.replace('Client name is required', 'Beneficiary name is required')
    
    # Fix 15: Client "{client_name}" not found -> Beneficiary "{beneficiary_name}" not found
    content = content.replace('Client "{client_name}" not found', 'Beneficiary "{beneficiary_name}" not found')
    
    # Fix 16: headers for excel export
    content = content.replace("'invoice_number', 'client',", "'invoice_number', 'beneficiary',")
    content = content.replace("'client', 'amount',", "'beneficiary', 'amount',")
    
    # Fix 17: # Calculate balance_before: ... same client -> same beneficiary
    content = content.replace('same client', 'same beneficiary')
    content = content.replace('for same client', 'for same beneficiary')
    
    # Fix 18: total_with_opening: client.get_total_balance_with_opening(fiscal_year)
    # This should now be beneficiary.get_total_balance_with_opening(fiscal_year)
    content = content.replace('client.get_total_balance_with_opening', 'beneficiary.get_total_balance_with_opening')
    
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
    fix_remaining_clients(filepath)
    print("Done!")
