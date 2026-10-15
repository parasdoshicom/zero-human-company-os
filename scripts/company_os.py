#!/usr/bin/env python3
"""Deterministic local teaching scaffold. No network, model calls, or live payments."""
import argparse
from contextlib import contextmanager
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
STAMP = '2026-10-15T12:00:00Z'
DRAFT = """# Fieldnotes Kit — local offer draft

## Before

A useful toolkit to help you conduct better interviews.

## After

Prepare your next customer interview with five practical questions, a planning sheet, and a debrief.

For independent consultants who want to understand a customer's workflow before pitching. Read the sample workbook before deciding whether the full kit would help.

Price hypothesis: $29 once. Includes a short workbook and sample. Excludes consulting, personalized research, and any guarantee of sales or validated demand.

Synthetic, deterministic teaching draft. No model generated this copy. Nothing was published and no customer outcome was observed.
"""



def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value, name):
    require(isinstance(value, str) and bool(value.strip()), f'{name} must be a nonempty string')
    return value


def integer(value, name, minimum=0):
    require(type(value) is int and value >= minimum, f'{name} must be an integer >= {minimum}')
    return value


def timestamp(value):
    nonempty(value, 'timestamp')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(parsed.tzinfo is not None and parsed.utcoffset() is not None, 'Timestamp must include timezone')
    return parsed


def window(value):
    require(isinstance(value, dict), 'Window must be an object')
    start, end = timestamp(value['start']), timestamp(value['end'])
    require(start < end, 'Window start must precede end')
    return start, end


def create_destination(path):
    path = Path(path).expanduser().resolve()
    require(path != ROOT and ROOT not in path.parents, 'Private workspace must be outside this public repository')
    path.mkdir(parents=True, exist_ok=False)
    return path


def initialize(path, name):
    nonempty(name, 'Company name')
    dest = create_destination(path)
    for folder in ('templates', 'examples', 'docs', 'principles'):
        shutil.copytree(ROOT / folder, dest / folder)
    for filename in ('AGENTS.md', 'CONTRIBUTING.md', 'SOURCES.md', 'SECURITY.md', 'LICENSE'):
        shutil.copy(ROOT / filename, dest / filename)
    shutil.copy(ROOT / 'templates/brief.md', dest / 'brief.md')
    (dest / 'START_HERE.md').write_text('''# Your private company workspace

Read [AGENTS.md](AGENTS.md), complete [brief.md](brief.md), and review permissions.json with the owner. Use [the lifecycle](docs/business-lifecycle.md), [principles](principles/README.md), and [templates](templates/README.md). Examples are fictional. Keep evidence and customer data private.

Required local setup: replace the five fields in setup.json (business_owner, customer, problem, product, budget_cents). Then run `python3 scripts/company_os.py check-workspace /path/to/this-workspace` from the original source checkout. Ready means ready for a local draft only. It never means permission to publish, spend, or operate live accounts.

The simulator and checker remain in the original source checkout. No runtime or integration is installed here. Before any real-world action, establish the exact owner-approved account, destination, scope, budget, expiry, and verification source. See [limitations](docs/limitations.md).
''')
    for folder in ('product', 'operations', 'evidence', 'learning'):
        (dest / folder).mkdir()
    (dest / 'PRIVATE.md').write_text('# Private company workspace\n\nCompany: ' + name + '\n\nKeep this directory private. Do not publish customer records, credentials, or live receipts.\n')
    (dest / '.gitignore').write_text('.env\n.env.*\nevidence/\nprivate/\n__pycache__/\n')
    write_json(dest / 'setup.json', {'business_owner': None, 'customer': None, 'problem': None, 'product': None, 'budget_cents': None})
    write_json(dest / 'permissions.json', {'status': 'draft', 'business_owner': None,
        'external_actions_allowed': False, 'approved_accounts': [], 'spend_limit_cents': 0,
        'approval_reference': None, 'expires_at': None})
    demo(dest / 'examples/completed-run')
    return dest


def check_workspace(path):
    dest = Path(path)
    setup = json.loads((dest / 'setup.json').read_text())
    missing = [key for key in ('business_owner', 'customer', 'problem', 'product')
               if not isinstance(setup.get(key), str) or not setup[key].strip() or setup[key].strip().upper() in {'TBD','REPLACE','UNKNOWN'}]
    if type(setup.get('budget_cents')) is not int or setup['budget_cents'] < 0:
        missing.append('budget_cents')
    permissions = json.loads((dest / 'permissions.json').read_text())
    result = {'status': 'needs_input' if missing else 'ready_for_local_draft', 'missing_fields': missing,
        'live_ready': False, 'account_scope': 'unconfigured' if not permissions.get('approved_accounts') else 'not_validated_by_this_checker',
        'next_action': 'Fill setup.json: ' + ', '.join(missing) if missing else 'Create one local draft task; no external actions are authorized by this check'}
    print(json.dumps(result, indent=2))
    return result


@contextmanager
def local_owner(path, owner):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, 'w') as handle:
            handle.write(owner)
        yield
    finally:
        Path(path).unlink()


def select_bottleneck(funnel):
    require(isinstance(funnel, dict), 'Funnel must be an object')
    for field in ('access_ok', 'measurement_valid'):
        require(type(funnel.get(field)) is bool, field + ' must be Boolean')
    threshold = integer(funnel.get('minimum_visits', 100), 'minimum_visits', 1)
    stages = ('qualified_visits', 'offer_interactions', 'checkout_intents', 'paid_orders')
    counts = [funnel.get(s) for s in stages]
    for stage, count in zip(stages, counts):
        if count is not None: integer(count, stage)
    if all(c is not None for c in counts):
        require(not any(b > a for a, b in zip(counts, counts[1:])), 'Example funnel requires nested counts within one cohort/window')
    if not funnel['access_ok']: return 'execution_access'
    if not funnel['measurement_valid'] or any(n is None for n in counts): return 'measurement'
    if counts[0] < threshold: return 'qualified_demand'
    for name, value in zip(stages[1:], counts[1:]):
        if value == 0: return name
    return 'delivery_and_learning'


def reconcile(ledger):
    require(isinstance(ledger, dict), 'Ledger must be an object')
    require(ledger.get('mode') == 'synthetic', 'This verifier accepts synthetic fixtures only')
    require(ledger.get('currency') == 'USD', 'Require USD fixture')
    nonempty(ledger['source'], 'source')
    business = nonempty(ledger['business_id'], 'business_id')
    start, end = window(ledger['window'])
    require(timestamp(ledger['observed_at']) >= end, 'Ledger observation must cover the window')
    require(isinstance(ledger['events'], list), 'Events must be a list')
    seen, purchases, refunds = set(), {}, {}
    gross = refund_total = fees = 0
    for row in ledger['events']:
        nonempty(row['id'], 'event ID')
        require(row['id'] not in seen, 'Duplicate event ID')
        seen.add(row['id'])
        require(row['business_id'] == business, 'Event belongs to another business')
        require(start <= timestamp(row['occurred_at']) < end, 'Event outside ledger window')
        amount = integer(row['amount_cents'], 'amount_cents')
        if row['type'] == 'purchase':
            require(amount > 0, 'Paid purchase must be positive')
            purchases[row['id']] = amount
            gross += amount
        elif row['type'] == 'refund':
            purchase = nonempty(row['purchase_id'], 'purchase_id')
            refunds[purchase] = refunds.get(purchase, 0) + amount
            refund_total += amount
        elif row['type'] == 'fee': fees += amount
        else: raise ValueError('Unknown event type')
    require(not any(key not in purchases or value > purchases[key] for key, value in refunds.items()), 'Refund must refer to a purchase and not exceed it')
    return {'mode': 'synthetic', 'business_id': business, 'window': ledger['window'], 'currency': 'USD',
        'gross_cents': gross, 'refund_cents': refund_total, 'fee_cents': fees,
        'net_after_fees_cents': gross - refund_total - fees, 'settlement': 'unknown', 'profit': 'unknown', 'real_sales_verified': 0}


def verify_claim(claim, ledger):
    reconcile(ledger)
    if claim.get('mode') != 'synthetic': return {'accepted': False, 'reason': 'Synthetic evidence cannot verify a real sale'}
    if claim['business_id'] != ledger['business_id']: return {'accepted': False, 'reason': 'Claim belongs to another business'}
    start, end = window(claim['window'])
    require(timestamp(claim['observed_at']) >= end, 'Claim observation must cover decision window')
    integer(claim['amount_cents'], 'claim amount_cents', 1)
    nonempty(claim['purchase_id'], 'purchase_id')
    matches = [e for e in ledger['events'] if e['type'] == 'purchase' and e['id'] == claim['purchase_id']]
    if not matches: return {'accepted': False, 'reason': 'No matching purchase in the ledger'}
    event = matches[0]
    if not start <= timestamp(event['occurred_at']) < end: return {'accepted': False, 'reason': 'Purchase outside claim decision window'}
    if event['amount_cents'] != claim['amount_cents']: return {'accepted': False, 'reason': 'Claim amount does not match the ledger'}
    return {'accepted': True, 'reason': 'Synthetic purchase event matched; not a live sale'}


def fixture(name):
    return json.loads((ROOT / 'examples/fieldnotes-kit' / name).read_text())


def inspect_draft(text):
    revision = text.split('## After\n', 1)[-1]
    return {'source':'deterministic content checks; not audience validation',
        'criteria':{'before_and_after': '## Before' in text and '## After' in text,
            'named_buyer': 'independent consultants' in revision,
            'concrete_deliverable': 'five practical questions, a planning sheet, and a debrief' in revision,
            'price_hypothesis':'Price hypothesis: $29 once' in revision,
            'exclusions_and_no_guarantee':'Excludes consulting, personalized research, and any guarantee of sales or validated demand' in revision,
            'no_customer_outcome_claim':'no customer outcome was observed' in revision},
        'limitations':'Text checks establish only the fixed local demo criteria, not persuasiveness, demand, or truthful arbitrary marketing copy'}


def draft_proof():
    return {'mode':'synthetic', 'artifact':'draft.md', 'sha256':hashlib.sha256(DRAFT.encode()).hexdigest(),
        'source':'local deterministic artifact readback', 'observed_at':STAMP, 'claim':'Local draft exists only; no publication or customer outcome'}


def expected_task(funnel):
    return {'id':'demo-offer-001', 'mode':'synthetic', 'owner':'demo-worker', 'verifier':'local-artifact-check',
        'business_id':funnel['business_id'], 'cohort':funnel['cohort'], 'window':funnel['window'],
        'bottleneck':select_bottleneck(funnel), 'action':'Write one deterministic local offer draft',
        'allowed_actions':['local_draft'], 'budget_cents':0, 'time_budget_minutes':15,
        'expires_at':'2026-10-15T12:15:00Z', 'source':'synthetic funnel fixture', 'observed_at':STAMP,
        'required_proof':'Artifact readback, declared content criteria, and SHA-256; local creation only',
        'acceptance_criteria':['before_and_after','named_buyer','concrete_deliverable','price_hypothesis','exclusions_and_no_guarantee','no_customer_outcome_claim'],
        'stop_rule':'Stop after one draft or 15 minutes; no external action',
        'status':'verified_local', 'terminal_evidence':'artifact-proof.json'}


def expected_learning():
    return {'source':'synthetic verifier and local artifact readback', 'observed_at':STAMP,
        'observation':'Unsupported sale rejected; deterministic local draft verified',
        'rule':'Require scoped source purchase evidence for sale claims; artifact proof establishes only local work',
        'regression_test':'test_claim_without_receipt_is_rejected', 'commercial_outcome':'none: simulation only',
        'next_action':'Owner reviews draft before any separately authorized publishing experiment'}


def run_controls(dest, funnel, ledger, claim):
    checks = {'access_failure_routes_to_repair':select_bottleneck(dict(funnel, access_ok=False)) == 'execution_access',
        'missing_measurement_stays_unknown':select_bottleneck(dict(funnel, qualified_visits=None)) == 'measurement',
        'unsupported_sale_rejected':not verify_claim(claim, ledger)['accepted']}
    # Probe lock is isolated from production ownership and always released on normal exit.
    with local_owner(dest / '.control-probe.lock', 'probe-owner'):
        try:
            with local_owner(dest / '.control-probe.lock', 'duplicate-worker'): checks['duplicate_owner_denied'] = False
        except FileExistsError: checks['duplicate_owner_denied'] = True
    require(all(checks.values()), 'A structural control failed')
    return checks


def demo(output):
    dest = Path(output).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=False)
    with local_owner(dest / '.owner.lock', 'demo-controller'):
        ledger, funnel, claim = fixture('ledger.json'), fixture('funnel.json'), fixture('claim.json')
        for name,data in [('ledger',ledger),('funnel',funnel)]: write_json(dest / (name+'.json'),data)
        write_json(dest / 'claim-rejected.json', {'claim':claim,'verification':verify_claim(claim,ledger)})
        (dest / 'draft.md').write_text(DRAFT)
        write_json(dest / 'artifact-proof.json', draft_proof())
        inspection = inspect_draft((dest / 'draft.md').read_text())
        require(all(inspection['criteria'].values()), 'Draft criteria failed')
        write_json(dest / 'inspection.json', inspection)
        write_json(dest / 'task.json', expected_task(funnel))
        report = reconcile(ledger)
        write_json(dest / 'report.json', report)
        write_json(dest / 'checks.json', run_controls(dest,funnel,ledger,claim))
        write_json(dest / 'learning.json', expected_learning())
    print('SIMULATED DEMO — no model, external actions, or real sales')
    print('PASS: unsupported sale rejected; access repair, unknown measurement, duplicate-owner controls passed')
    print('Bottleneck:',select_bottleneck(funnel))
    print('PASS: draft.md created, hashed, and task closed as verified_local')
    money=lambda key: f"${report[key]/100:.2f}"
    print(f"Separate synthetic accounting window: {money('gross_cents')} gross - {money('refund_cents')} refunds - {money('fee_cents')} fees = {money('net_after_fees_cents')} after fees")
    print('Settlement: unknown. Profit: unknown. Real sales verified: 0.')
    print('Evidence:',dest)
    return dest


def exact_json(actual, expected):
    """JSON value equality that preserves scalar types, including bool vs int."""
    if type(actual) is not type(expected):
        return False
    if isinstance(actual, dict):
        return actual.keys() == expected.keys() and all(exact_json(actual[key], expected[key]) for key in actual)
    if isinstance(actual, list):
        return len(actual) == len(expected) and all(exact_json(a, b) for a, b in zip(actual, expected))
    return actual == expected


def verify_directory(path):
    dest = Path(path)
    read=lambda name: json.loads((dest / (name+'.json')).read_text())
    # This is a deterministic fixture replay, not a live or tamper-proof verifier.
    ledger,funnel,claim_record=read('ledger'),read('funnel'),read('claim-rejected')
    require(exact_json(funnel, fixture('funnel.json')), 'Funnel changed from declared demo cohort/window')
    require(exact_json(ledger, fixture('ledger.json')), 'Ledger changed from declared demo accounting fixture')
    claim=claim_record['claim']
    require(exact_json(claim, fixture('claim.json')), 'Demo claim scope changed')
    expected=reconcile(ledger)
    require(exact_json(read('report'), expected), 'Report does not match source ledger')
    result=verify_claim(claim,ledger)
    require(exact_json(claim_record['verification'], result) and not result['accepted'], 'False-success rejection not preserved')
    require(exact_json(read('task'), expected_task(funnel)), 'Task contract, routing, or terminal state changed')
    require((dest/'draft.md').read_bytes() == DRAFT.encode(), 'Draft artifact changed')
    require(exact_json(read('artifact-proof'), draft_proof()), 'Artifact proof changed')
    inspection = inspect_draft((dest / 'draft.md').read_text())
    require(all(inspection['criteria'].values()) and exact_json(read('inspection'), inspection), 'Draft content inspection failed or changed')
    require(hashlib.sha256((dest/'draft.md').read_bytes()).hexdigest() == read('artifact-proof')['sha256'], 'Artifact hash mismatch')
    require(exact_json(read('checks'), run_controls(dest,funnel,ledger,claim)), 'Structural checks changed')
    require(exact_json(read('learning'), expected_learning()), 'Learning record changed')
    print('PASS: fixture scopes, task, local draft proof, structural checks, learning, and synthetic ledger verified')
    return expected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest='command',required=True)
    init=subs.add_parser('init'); init.add_argument('--workspace',required=True); init.add_argument('--name',required=True)
    run=subs.add_parser('demo'); run.add_argument('--output',default='demo-output')
    verify=subs.add_parser('verify'); verify.add_argument('path')
    check=subs.add_parser('check-workspace'); check.add_argument('path')
    args=parser.parse_args()
    try:
        if args.command=='init': print('Created private starter:',initialize(args.workspace,args.name))
        elif args.command=='demo': demo(args.output)
        elif args.command=='check-workspace': check_workspace(args.path)
        else: verify_directory(args.path)
    except (ValueError,OSError,KeyError,TypeError,AttributeError) as error:
        parser.exit(1,f'FAIL: {error}\n')


if __name__=='__main__': main()
