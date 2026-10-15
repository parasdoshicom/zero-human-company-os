#!/usr/bin/env python3
"""Local teaching scaffold. No network access, live payments, or agent execution."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
STAMP = '2026-10-15T12:00:00Z'  # fixed synthetic observation window


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def create_destination(path):
    path = Path(path).expanduser().resolve()
    if path == ROOT or ROOT in path.parents:
        raise ValueError('Private workspace must be outside this public repository')
    path.mkdir(parents=True, exist_ok=False)
    return path


def initialize(path, name):
    if not name.strip():
        raise ValueError('Company name must not be empty')
    dest = create_destination(path)
    shutil.copytree(ROOT / 'templates', dest / 'templates')
    shutil.copytree(ROOT / 'examples', dest / 'examples')
    shutil.copy(ROOT / 'AGENTS.md', dest / 'AGENTS.md')
    (dest / 'docs').mkdir()
    shutil.copy(ROOT / 'docs/limitations.md', dest / 'docs/limitations.md')
    shutil.copy(ROOT / 'templates/brief.md', dest / 'brief.md')
    (dest / 'START_HERE.md').write_text('# Your private company workspace\n\nRead AGENTS.md, fill brief.md, and review permissions.json with the business owner. Start with one task from templates/. Examples are fictional. Store evidence privately and keep uncertain outcomes explicit. The runnable simulator lives in your original public-source checkout; this private workspace contains operating records, not installed integrations.\n')
    for folder in ('product', 'operations', 'evidence', 'learning'):
        (dest / folder).mkdir()
    (dest / 'PRIVATE.md').write_text('# Private company workspace\n\n'
        + 'Company: ' + name + '\n\nKeep this directory private. Do not publish customer records, credentials, or live receipts.\n')
    (dest / '.gitignore').write_text('.env\n.env.*\nevidence/\nprivate/\n__pycache__/\n')
    write_json(dest / 'permissions.json', {'status': 'draft', 'business_owner': None,
        'external_actions_allowed': False, 'approved_accounts': [], 'spend_limit_cents': 0,
        'approval_reference': None, 'expires_at': None})
    return dest


@contextmanager
def local_owner(path, owner):
    """Fail closed on an existing lock. No automatic stale-lock deletion."""
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, 'w') as handle:
            handle.write(owner)
        yield
    finally:
        Path(path).unlink()


def select_bottleneck(funnel):
    if not funnel.get('access_ok'):
        return 'execution_access'
    stages = ('qualified_visits', 'offer_interactions', 'checkout_intents', 'paid_orders')
    if not funnel.get('measurement_valid') or any(funnel.get(s) is None for s in stages):
        return 'measurement'
    counts = [funnel[s] for s in stages]
    if any(type(n) is not int or n < 0 for n in counts):
        raise ValueError('Funnel counts must be nonnegative integers')
    if any(b > a for a, b in zip(counts, counts[1:])):
        raise ValueError('Example funnel requires nested counts within one cohort/window')
    if counts[0] < funnel.get('minimum_visits', 100):
        return 'qualified_demand'
    for name, value in zip(stages[1:], counts[1:]):
        if value == 0:
            return name
    return 'delivery_and_learning'


def reconcile(ledger):
    if ledger.get('mode') != 'synthetic':
        raise ValueError('This demo verifier accepts synthetic fixtures only')
    if ledger.get('currency') != 'USD' or not ledger.get('source') or not ledger.get('observed_at'):
        raise ValueError('Require USD fixture, source, and observation timestamp')
    datetime.fromisoformat(ledger['observed_at'].replace('Z', '+00:00'))
    seen, purchases, refunds = set(), {}, {}
    gross = refund_total = fees = 0
    for row in ledger['events']:
        if row['id'] in seen:
            raise ValueError('Duplicate event ID')
        seen.add(row['id'])
        amount = row['amount_cents']
        if type(amount) is not int or amount < 0:
            raise ValueError('Amounts must be nonnegative integer cents')
        if row['type'] == 'purchase':
            purchases[row['id']] = amount
            gross += amount
        elif row['type'] == 'refund':
            purchase = row['purchase_id']
            refunds[purchase] = refunds.get(purchase, 0) + amount
            refund_total += amount
        elif row['type'] == 'fee':
            fees += amount
        else:
            raise ValueError('Unknown event type')
    if any(key not in purchases or value > purchases[key] for key, value in refunds.items()):
        raise ValueError('Refund must refer to a purchase and not exceed it')
    return {'mode': 'synthetic', 'currency': 'USD', 'gross_cents': gross,
        'refund_cents': refund_total, 'fee_cents': fees,
        'net_after_fees_cents': gross - refund_total - fees,
        'settlement': 'unknown', 'profit': 'unknown', 'real_sales_verified': 0}


def verify_claim(claim, ledger):
    reconcile(ledger)
    if claim.get('mode') != 'synthetic':
        return {'accepted': False, 'reason': 'Synthetic evidence cannot verify a real sale'}
    matches = [e for e in ledger['events'] if e['type'] == 'purchase' and e['id'] == claim.get('purchase_id')]
    if not matches:
        return {'accepted': False, 'reason': 'No matching purchase in the ledger'}
    if matches[0]['amount_cents'] != claim.get('amount_cents'):
        return {'accepted': False, 'reason': 'Claim amount does not match the ledger'}
    return {'accepted': True, 'reason': 'Synthetic purchase event matched; not a live sale'}


def demo(output):
    dest = Path(output).expanduser().resolve()
    # Demo outputs may live in ignored demo-output; never reuse an existing directory.
    dest.mkdir(parents=True, exist_ok=False)
    with local_owner(dest / '.owner.lock', 'demo-controller'):
        ledger = json.loads((ROOT / 'examples/fieldnotes-kit/ledger.json').read_text())
        funnel = {'access_ok': True, 'measurement_valid': True, 'minimum_visits': 100,
            'qualified_visits': 120, 'offer_interactions': 0, 'checkout_intents': 0, 'paid_orders': 0}
        write_json(dest / 'funnel.json', funnel)
        write_json(dest / 'ledger.json', ledger)
        claim = {'mode': 'synthetic', 'purchase_id': 'missing-sale', 'amount_cents': 2900}
        rejected = verify_claim(claim, ledger)
        write_json(dest / 'claim-rejected.json', {'claim': claim, 'verification': rejected})
        task = {'id': 'demo-offer-001', 'mode': 'synthetic', 'owner': 'demo-worker',
            'verifier': 'ledger-and-destination-check', 'bottleneck': select_bottleneck(funnel),
            'action': 'Draft one clearer product promise; save locally for owner review',
            'allowed_actions': ['local_draft'], 'budget_cents': 0, 'time_budget_minutes': 15,
            'expires_at': '2026-10-15T12:15:00Z', 'source': 'synthetic funnel fixture',
            'observed_at': STAMP, 'required_proof': 'Local draft exists; no publication or demand claim',
            'stop_rule': 'Stop after one draft or 15 minutes; no external action', 'status': 'prepared'}
        write_json(dest / 'task.json', task)
        report = reconcile(ledger)
        write_json(dest / 'report.json', report)
        checks = {'access_failure_routes_to_repair': select_bottleneck(dict(funnel, access_ok=False)) == 'execution_access',
            'missing_measurement_stays_unknown': select_bottleneck(dict(funnel, qualified_visits=None)) == 'measurement',
            'unsupported_sale_rejected': not rejected['accepted']}
        try:
            with local_owner(dest / '.owner.lock', 'duplicate-worker'):
                checks['duplicate_owner_denied'] = False
        except FileExistsError:
            checks['duplicate_owner_denied'] = True
        if not all(checks.values()):
            raise ValueError('A structural control failed')
        write_json(dest / 'checks.json', checks)
        write_json(dest / 'learning.json', {'source': 'synthetic verifier', 'observed_at': STAMP,
            'observation': 'Unsupported sale claim was rejected',
            'rule': 'Require matching source purchase ID and amount',
            'regression_test': 'test_claim_without_receipt_is_rejected',
            'commercial_outcome': 'none: simulation only'})
    print('SIMULATED DEMO — no external actions, no real sales')
    print('PASS: unsupported sale claim rejected')
    print('PASS: access failure routed to repair; missing measurements remain unknown; duplicate owner denied')
    print('Bottleneck:', task['bottleneck'])
    print('Synthetic ledger: $58 gross - $29 refunds - $2 fees = $27 after fees')
    print('Settlement: unknown. Profit: unknown. Real sales verified: 0.')
    print('Evidence:', dest)
    return dest


def verify_directory(path):
    path = Path(path)
    expected = reconcile(json.loads((path / 'ledger.json').read_text()))
    actual = json.loads((path / 'report.json').read_text())
    if actual != expected:
        raise ValueError('Report does not match the source ledger')
    rejected = json.loads((path / 'claim-rejected.json').read_text())
    result = verify_claim(rejected['claim'], json.loads((path / 'ledger.json').read_text()))
    if result != rejected['verification'] or result['accepted']:
        raise ValueError('False-success rejection was not preserved')
    print('PASS: synthetic report reconciles and unsupported claim remains rejected')
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    init = subs.add_parser('init')
    init.add_argument('--workspace', required=True)
    init.add_argument('--name', required=True)
    run = subs.add_parser('demo')
    run.add_argument('--output', default='demo-output')
    verify = subs.add_parser('verify')
    verify.add_argument('path')
    args = parser.parse_args()
    try:
        if args.command == 'init':
            print('Created private starter:', initialize(args.workspace, args.name))
        elif args.command == 'demo':
            demo(args.output)
        else:
            verify_directory(args.path)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, f'FAIL: {error}\n')


if __name__ == '__main__':
    main()
