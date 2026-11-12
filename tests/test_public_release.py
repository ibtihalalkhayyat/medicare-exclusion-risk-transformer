import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestPublicSyntheticRelease(unittest.TestCase):
    def test_immutable_space_content_counts(self):
        g=json.loads((ROOT/'demo/data/inference_grid.json').read_text())
        self.assertEqual((len(g['cases']),len(g['scale_values'])),(24,21))
        self.assertEqual(sum(len(c['calibrated_outputs']) for c in g['cases']),504)
    def test_synthetic_feature_count(self):
        data=json.loads((ROOT/'demo/data/scenarios.json').read_text())
        self.assertEqual(len(data),24)
        self.assertTrue(all(len(r)==141 and str(r['synthetic_case_id']).startswith('SYNTHETIC_') for r in data))
    def test_no_training_or_real_data(self):
        prov=json.loads((ROOT/'demo/data/model_output_provenance.json').read_text())
        self.assertFalse(prov['new_training_or_calibration'])
        self.assertFalse(prov['real_cms_or_leie_rows_processed'])
        self.assertFalse(prov['final_2023_outcome_access'])
        self.assertFalse(prov['model_or_fitted_assets_exported_publicly'])
if __name__=='__main__':unittest.main()
