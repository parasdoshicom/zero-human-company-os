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
        self.claim = {'observed_at':'2026-10-15T12:00:00Z','mode':'synthetic','business_id':self.ledger['business_id'],'window':self.ledger['window'],'purchase_id':'demo-order-1','amount_cents':2900}
        self.funnel = {'access_ok': True, 'measurement_valid': True, 'qualified_visits':120,
            'offer_interactions':0, 'checkout_intents':0, 'paid_orders':0}

    def test_claim_without_receipt_is_rejected(self):
        self.assertFalse(app.verify_claim(dict(self.claim,purchase_id='missing'), self.ledger)['accepted'])

    def test_synthetic_evidence_cannot_prove_real_sale(self):
        self.assertFalse(app.verify_claim(dict(self.claim,mode='live'), self.ledger)['accepted'])

    def test_wrong_amount_rejected(self):
        self.assertFalse(app.verify_claim(dict(self.claim,amount_cents=1), self.ledger)['accepted'])

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

    def test_stale_and_cross_business_claims_rejected(self):
        stale = dict(self.claim, window={'start':'2026-10-14T00:00:00Z','end':'2026-10-15T00:00:00Z'})
        self.assertFalse(app.verify_claim(stale,self.ledger)['accepted'])
        self.assertFalse(app.verify_claim(dict(self.claim,business_id='other'),self.ledger)['accepted'])
        self.assertTrue(app.verify_claim(self.claim,self.ledger)['accepted'])

    def test_strict_funnel_types(self):
        for key,value in [('access_ok','false'),('measurement_valid',1),('minimum_visits',True),('minimum_visits',-1),('qualified_visits',True),('paid_orders','0')]:
            with self.subTest(key=key,value=value):
                with self.assertRaises(ValueError): app.select_bottleneck(dict(self.funnel,**{key:value}))

    def test_aware_event_time_and_scope_required(self):
        for key,value in [('occurred_at','2026-10-02T12:00:00'),('occurred_at','2026-11-01T00:00:00Z'),('business_id','other'),('amount_cents',True)]:
            ledger=copy.deepcopy(self.ledger); ledger['events'][0][key]=value
            with self.subTest(key=key,value=value):
                with self.assertRaises(ValueError): app.reconcile(ledger)

    def test_task_proof_checks_and_learning_tamper(self):
        with tempfile.TemporaryDirectory() as temp:
            dest=app.demo(Path(temp)/'demo')
            for file,key,value in [('task.json','allowed_actions',['publish']),('task.json','budget_cents',1),('task.json','status','prepared'),('checks.json','unsupported_sale_rejected',False),('artifact-proof.json','sha256','wrong'),('learning.json','commercial_outcome','sale')]:
                path=dest/file; original=path.read_text(); data=json.loads(original); data[key]=value; path.write_text(json.dumps(data))
                with self.subTest(file=file,key=key):
                    with self.assertRaises(ValueError): app.verify_directory(dest)
                path.write_text(original)
            (dest/'draft.md').write_text('tampered')
            with self.assertRaises(ValueError): app.verify_directory(dest)

    def test_workspace_check_is_local_only_and_docs_portable(self):
        with tempfile.TemporaryDirectory() as temp:
            dest=app.initialize(Path(temp)/'private','Test')
            self.assertEqual(app.check_workspace(dest)['status'],'needs_input')
            self.assertTrue((dest/'principles/README.md').exists())
            self.assertTrue((dest/'docs/business-lifecycle.md').exists())
            setup={'business_owner':'Owner','customer':'Consultant','problem':'Interview planning','product':'Workbook','budget_cents':0}
            (dest/'setup.json').write_text(json.dumps(setup))
            result=app.check_workspace(dest)
            self.assertEqual(result['status'],'ready_for_local_draft')
            self.assertFalse(result['live_ready'])
            self.assertEqual(result['account_scope'],'unconfigured')

    def test_cli_invalid_json_has_clean_failure(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp)/'setup.json').write_text('{bad')
            result=subprocess.run([sys.executable,str(ROOT/'scripts/company_os.py'),'check-workspace',temp],capture_output=True,text=True)
            self.assertEqual(result.returncode,1)
            self.assertIn('FAIL:',result.stderr)
            self.assertNotIn('Traceback',result.stderr)

    def test_initialized_markdown_links_and_completed_example(self):
        import re
        with tempfile.TemporaryDirectory() as temp:
            dest=app.initialize(Path(temp)/'private','Test')
            app.verify_directory(dest/'examples/completed-run')
            for path in dest.rglob('*.md'):
                for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
                    if '://' in link or link.startswith(('#','mailto:')): continue
                    target=link.split('#')[0]
                    self.assertTrue((path.parent/target).exists(),f'{path.relative_to(dest)}: {target}')

    def test_draft_inspection_fails_missing_buyer_or_price(self):
        self.assertTrue(all(app.inspect_draft(app.DRAFT)['criteria'].values()))
        self.assertFalse(app.inspect_draft(app.DRAFT.replace('independent consultants','anyone'))['criteria']['named_buyer'])
        self.assertFalse(app.inspect_draft(app.DRAFT.replace('$29','$0'))['criteria']['price_hypothesis'])

    def test_json_contract_preserves_nested_scalar_types(self):
        self.assertFalse(app.exact_json({'nested':[{'budget':False}]},{'nested':[{'budget':0}]}))
        self.assertFalse(app.exact_json({'nested':[15.0]},{'nested':[15]}))
        self.assertTrue(app.exact_json({'a':[1,False],'b':2},{'b':2,'a':[1,False]}))

    def test_type_only_artifact_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            dest=app.demo(Path(temp)/'demo')
            for file,keys,value in [('task.json',['budget_cents'],False),('task.json',['time_budget_minutes'],15.0),('checks.json',['unsupported_sale_rejected'],1),('report.json',['real_sales_verified'],False),('report.json',['gross_cents'],5800.0),('inspection.json',['criteria','named_buyer'],1),('claim-rejected.json',['verification','accepted'],0),('funnel.json',['paid_orders'],False)]:
                path=dest/file; original=path.read_text(); data=json.loads(original); node=data
                for key in keys[:-1]: node=node[key]
                node[keys[-1]]=value; path.write_text(json.dumps(data))
                with self.subTest(file=file,keys=keys):
                    with self.assertRaises(ValueError): app.verify_directory(dest)
                path.write_text(original)


if __name__ == '__main__': unittest.main()
