#!/usr/bin/env python3
"""
Credit Union Reconciliation Legend and Workflow
Based on OP-NCB Reconciliation training document
"""

# CREDIT UNION RECONCILIATION LEGEND
RECONCILIATION_LEGEND = {
    "document_types": {
        "gl_activity": {
            "name": "05 May 2025 Reconciliation and Flex GL Activity.xlsx",
            "description": "GL Accounting Activity - Contains individual GL sheets (74400-74570)",
            "purpose": "Internal general ledger activity from Flex system",
            "sheets": ["74400", "74505", "74510", "74515", "74520", "74525", "74530", "74535", "74540", "74550", "74560", "74570"]
        },
        "bank_statement": {
            "name": "NCB Bank Activity 5-1 to 5-31 Support for May 2025 Rec.xls",
            "description": "Bank Statement - NCB (National Cooperative Bank) activity",
            "purpose": "External bank statement showing actual bank transactions",
            "account": "CB Interest Settlement"
        },
        "reconciliation_template": {
            "name": "May 2025 Reconciliation_Final",
            "description": "Reconciliation Template - Matches GL activity with bank statement",
            "purpose": "Reconciliation worksheet showing adjustments and timing differences"
        }
    },
    
    "gl_accounts": {
        "74400": {
            "name": "RBC Activity",
            "bank_activities": [
                "RBC activity",
                "EFUNDS Corp – FEE SETTLE",
                "Withdrawal Coin or Withdrawal Currency",
                "Currency Exchange Payment",
                "CRIF Select Corp",
                "Withdrawal Outgoing Wire or Deposit Incoming Wire",
                "OCUL SERVICES CO - ACH Collec NW Fees",
                "CRIF SELECT CORP - EOM",
                "OCUL SERVICES CO - ACH Collec SB Transaction Fees",
                "Analysis Service Charge",
                "COOPERATIVE BUSI - ACH",
                "VISA U.S.A., INC IB241000 - VGBP_COL"
            ]
        },
        "74505": {
            "name": "CNS Settlement",
            "bank_activities": [
                "CNS Settlement activity",
                "PULSE FEES activity"
            ]
        },
        "74510": {
            "name": "EFUNDS Corp Daily Settlement",
            "bank_activities": [
                "EFUNDS Corp – DLY SETTLE activity"
            ]
        },
        "74515": {
            "name": "Cash Letter Corrections",
            "bank_activities": [
                "Cash Letter Corr activity"
            ]
        },
        "74520": {
            "name": "Image Check Presentment",
            "bank_activities": [
                "1591 Image CL Presentment activity"
            ]
        },
        "74525": {
            "name": "Returned Drafts",
            "bank_activities": [
                "1590 Image CL Presentment activity (returns)"
            ]
        },
        "74530": {
            "name": "ACH Activity",
            "bank_activities": [
                "ACH ADV File activity"
            ]
        },
        "74535": {
            "name": "ICUL Services",
            "bank_activities": [
                "ICUL ServCorp activity"
            ]
        },
        "74540": {
            "name": "CRIF Loans",
            "bank_activities": [
                "ACH ADV FILE - Orig CR activity (CRIF loans)"
            ]
        },
        "74550": {
            "name": "Cooperative Business",
            "bank_activities": [
                "Cooperative Business activity"
            ]
        },
        "74560": {
            "name": "Check Deposits",
            "bank_activities": [
                "1590 Image CL Presentment activity (deposits)"
            ]
        },
        "74570": {
            "name": "ACH Returns",
            "bank_activities": [
                "ACH ADV FILE - Orig DB activity (ACH returns)"
            ]
        }
    },
    
    "reconciliation_workflow": {
        "step_1": {
            "action": "Extract GL Balances",
            "description": "Get month-end balances from Flex system for each GL (74400-74570)",
            "source": "GL Activity file",
            "target": "Column O in reconciliation template"
        },
        "step_2": {
            "action": "Get Bank Statement Balance",
            "description": "Extract ending balance from NCB statement",
            "source": "NCB Bank Statement",
            "target": "Balance per Statement in reconciliation"
        },
        "step_3": {
            "action": "Match Bank Activities to GL Accounts",
            "description": "Reconcile each bank transaction with corresponding GL activity",
            "mapping": "Use GL-Bank Activity legend above"
        },
        "step_4": {
            "action": "Identify Timing Differences",
            "description": "Find items posted by bank but not in GL, and vice versa",
            "categories": [
                "Items added by bank but not yet on books of C.U.",
                "Items deducted by bank but not yet entered on books of C.U.",
                "Items deducted by C.U. but not yet entered on bank records",
                "Items added by C.U. but not yet entered on bank records"
            ]
        },
        "step_5": {
            "action": "Calculate Adjusted Balances",
            "description": "Ensure Balance per Books = Balance per Statement",
            "formula": "Adjusted Total (Books) = Adjusted Total (Statement)"
        }
    },
    
    "timing_differences": {
        "atm_settlement": {
            "gl_account": "74505",
            "description": "ATM settlement activity posted to GL on last day of month",
            "bank_timing": "Not posted at bank yet",
            "reconciliation_entry": "Negative amount in 'Items deducted by C.U. but not yet entered on bank records'"
        },
        "shared_branching": {
            "gl_account": "74510",
            "description": "Shared Branching activity recorded in GL on last day of month",
            "bank_timing": "Not posted at bank yet",
            "reconciliation_entry": "Negative in top right or positive in bottom right depending on amount difference"
        },
        "check_deposits": {
            "gl_account": "74560",
            "description": "Check deposit activity at branches posted to GL on last day of month",
            "bank_timing": "Not posted at bank yet",
            "reconciliation_entry": "Positive amount in 'Items added by C.U. but not yet entered on bank records'"
        },
        "gift_cards": {
            "gl_account": "74535",
            "description": "Gift Card activity posted to GL on last day of month",
            "bank_timing": "Not posted at bank yet",
            "reconciliation_entry": "Negative amount in 'Items deducted by C.U. but not yet entered on bank records'"
        },
        "cbs_activity": {
            "gl_account": "74550",
            "description": "CBS activity posted to GL on last day of month",
            "bank_timing": "Not posted at bank yet",
            "reconciliation_entry": "Positive amount in 'Items added by C.U. but not yet entered on bank records'"
        },
        "crif_loans": {
            "gl_account": "74540",
            "description": "CRIF indirect loan activity posted to GL on last day of month",
            "bank_timing": "Not posted at bank yet",
            "reconciliation_entry": "Negative amount in 'Items added by C.U. but not yet entered on bank records'"
        }
    }
}

def get_reconciliation_legend():
    """Get the complete reconciliation legend"""
    return RECONCILIATION_LEGEND

def get_gl_bank_mapping():
    """Get mapping between GL accounts and bank activities"""
    mapping = {}
    for gl, info in RECONCILIATION_LEGEND["gl_accounts"].items():
        mapping[gl] = {
            "name": info["name"],
            "bank_activities": info["bank_activities"]
        }
    return mapping

def get_timing_differences():
    """Get common timing differences for reconciliation"""
    return RECONCILIATION_LEGEND["timing_differences"]

def get_workflow_steps():
    """Get the reconciliation workflow steps"""
    return RECONCILIATION_LEGEND["reconciliation_workflow"]

if __name__ == "__main__":
    print("🏦 CREDIT UNION RECONCILIATION LEGEND")
    print("=" * 50)
    
    legend = get_reconciliation_legend()
    
    print("\n📋 DOCUMENT TYPES:")
    for doc_type, info in legend["document_types"].items():
        print(f"   {doc_type}: {info['name']}")
        print(f"      Purpose: {info['description']}")
    
    print("\n💰 GL ACCOUNTS AND BANK ACTIVITIES:")
    for gl, info in legend["gl_accounts"].items():
        print(f"   GL {gl}: {info['name']}")
        for activity in info['bank_activities']:
            print(f"      - {activity}")
    
    print("\n🔄 RECONCILIATION WORKFLOW:")
    for step, info in legend["reconciliation_workflow"].items():
        print(f"   {step}: {info['action']}")
        print(f"      {info['description']}")
    
    print("\n⏰ TIMING DIFFERENCES:")
    for diff_type, info in legend["timing_differences"].items():
        print(f"   {diff_type}: GL {info['gl_account']}")
        print(f"      {info['description']}")
