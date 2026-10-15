import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('company_os', ROOT / 'scripts/company_os.py')
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class CompanyTests(unittest.TestCase):
    def setUp(self):
        self.ledger = json.loads((ROOT / 'examples/fieldnotes-kit/ledger.json').read_text())
        self.funnel = {'access_ok': True, 'measurement_valid': True, 'qualified_visits':120,
            'offer_interactions':0, 'checkout_intents':0, 'paid_orders':0}

    def test_claim_without_receipt_is_rejected(self):
        self.assertFalse(app.verify_claim({'mode':'synthetic','purchase_id':'missing','amount_cents':2900}, self.ledger)['accepted'])

    def test_synthetic_evidence_cannot_prove_real_sale(self):
        self.assertFalse(app.verify_claim({'mode':'live','purchase_id':'demo-order-1','amount_cents':2900}, self.ledger)['accepted'])

    def test_wrong_amount_rejected(self):
        self.assertFalse(app.verify_claim({'mode':'synthetic','purchase_id':'demo-order-1','amount_cents':1}, self.ledger)['accepted'])

    def test_reconciliation_retains_financial_distinctions(self):
        result = app.reconcile(self.ledger)
        self.assertEqual((result['gross_cents'], result['refund_cents'], result['fee_cents'], result['net_after_fees_cents']), (5800,2900,200,2700))
        self.assertEqual(result['settlement'], 'unknown')
        self.assertEqual(result['profit'], 'unknown')

    def test_duplicate_event_rejected(self):
        self.ledger['events'].append(self.ledger['events'][0])
        with self.assertRaises(ValueError): app.reconcile(self.ledger)

    def test_refund_over_purchase_rejected(self):
        self.ledger['events'][2]['amount_cents'] = 3000
        with self.assertRaises(ValueError): app.reconcile(self.ledger)

    def test_unknown_not_zero(self):
        self.funnel['qualified_visits'] = None
        self.assertEqual(app.select_bottleneck(self.funnel), 'measurement')

    def test_access_failure_takes_priority(self):
        self.funnel['access_ok'] = False
        self.assertEqual(app.select_bottleneck(self.funnel), 'execution_access')

    def test_zero_interaction_routes_to_offer(self):
        self.assertEqual(app.select_bottleneck(self.funnel), 'offer_interactions')

    def test_invalid_nested_funnel_rejected(self):
        self.funnel['checkout_intents'] = 2
        with self.assertRaises(ValueError): app.select_bottleneck(self.funnel)

    def test_initializer_refuses_existing_and_inside_repo(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(FileExistsError): app.initialize(temp, 'Test')
        with self.assertRaises(ValueError): app.initialize(ROOT / 'unsafe-private', 'Test')

    def test_initializer_creates_private_safe_defaults(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = app.initialize(Path(temp) / 'new', 'Test')
            permissions = json.loads((dest / 'permissions.json').read_text())
            self.assertFalse(permissions['external_actions_allowed'])
            self.assertEqual(permissions['spend_limit_cents'],0)
            self.assertTrue((dest / 'START_HERE.md').is_file())
            self.assertEqual((dest / 'docs/limitations.md').read_text(), (ROOT / 'docs/limitations.md').read_text())

    def test_exclusive_owner_and_exception_release(self):
        with tempfile.TemporaryDirectory() as temp:
            lock = Path(temp) / 'lock'
            with self.assertRaises(RuntimeError):
                with app.local_owner(lock, 'first'):
                    with self.assertRaises(FileExistsError):
                        with app.local_owner(lock, 'second'): pass
                    self.assertEqual(lock.read_text(), 'first')
                    raise RuntimeError('worker failed')
            self.assertFalse(lock.exists())

    def test_demo_roundtrip_and_tampered_report(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = app.demo(Path(temp) / 'demo')
            app.verify_directory(dest)
            result = json.loads((dest / 'report.json').read_text())
            result['gross_cents'] = 999999
            (dest / 'report.json').write_text(json.dumps(result))
            with self.assertRaises(ValueError): app.verify_directory(dest)
            with self.assertRaises(FileExistsError): app.demo(dest)


if __name__ == '__main__': unittest.main()
