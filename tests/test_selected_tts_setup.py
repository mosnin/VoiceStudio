"""Onboarding accepts a ready selected engine without downloading default weights."""
import sys
from pathlib import Path
import types
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))
from api.routers.setup import wizard


class SelectedTTSSetupTests(unittest.TestCase):
    def status(self, selected='kittentts', state='loaded', available=True, row_id='kittentts'):
        fake = types.ModuleType('services.tts_backend')
        fake.active_backend_id = lambda: selected
        instance = types.SimpleNamespace(id=row_id, execution_evidence_loaded=lambda: available and state in {'loaded', 'subprocess_loaded_provider_unreported'})
        fake._active_instance_id = row_id
        fake._active_instance = instance
        fake._ENGINE_INSTANCES = {}
        with patch.dict(sys.modules, {'services.tts_backend': fake}), \
             patch.object(wizard, 'is_cached', return_value=False), \
             patch.object(wizard, 'hf_cache_dir', return_value='/tmp'), \
             patch.object(wizard, '_disk_free_gb', return_value=20):
            return wizard.setup_status()

    def test_ready_selected_engine_allows_setup(self):
        self.assertTrue(self.status()['models_ready'])
        self.assertEqual(self.status()['missing'], [])

    def test_unloaded_engine_does_not_skip_model_gate(self):
        self.assertFalse(self.status(state='not_loaded')['models_ready'])

    def test_other_loaded_engine_does_not_qualify(self):
        self.assertFalse(self.status(selected='omnivoice')['models_ready'])

    def test_unavailable_loaded_engine_does_not_qualify(self):
        self.assertFalse(self.status(available=False)['models_ready'])

    def test_loaded_isolated_engine_qualifies(self):
        self.assertTrue(self.status(state='subprocess_loaded_provider_unreported')['models_ready'])


if __name__ == '__main__':
    unittest.main()
