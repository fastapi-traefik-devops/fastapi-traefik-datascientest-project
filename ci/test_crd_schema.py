"""Strict CRD schema generation and the committed operator schemas."""
import json
from pathlib import Path
import unittest
import crd_schema

CI = Path(__file__).resolve().parent


def crd(schema, served=True):
    return {'metadata': {'name': 'widgets.example.com'},
            'spec': {'group': 'example.com', 'names': {'kind': 'Widget'},
                     'versions': [{'name': 'v1', 'served': served, 'schema': {'openAPIV3Schema': schema}}]}}


class CrdSchemaTests(unittest.TestCase):
    def test_objects_with_properties_reject_unknown_fields_at_every_level(self):
        name, schema = crd_schema.convert(crd({'type': 'object', 'description': 'x', 'properties': {
            'spec': {'type': 'object', 'properties': {'size': {'type': 'string', 'description': 'y'}}}}}), 'v1')
        self.assertEqual(name, 'crd-example.com-widget-v1.json')
        self.assertIs(schema['additionalProperties'], False)
        self.assertIs(schema['properties']['spec']['additionalProperties'], False)
        self.assertNotIn('description', json.dumps({k: v for k, v in schema.items() if k != '$comment'}))

    def test_free_form_maps_and_preserved_fields_stay_open(self):
        _, schema = crd_schema.convert(crd({'type': 'object', 'properties': {
            'labels': {'type': 'object', 'additionalProperties': {'type': 'string'}},
            'raw': {'type': 'object', 'x-kubernetes-preserve-unknown-fields': True, 'properties': {'a': {}}}}}), 'v1')
        self.assertEqual(schema['properties']['labels']['additionalProperties'], {'type': 'string'})
        self.assertNotIn('additionalProperties', schema['properties']['raw'])

    def test_nullable_and_int_or_string(self):
        _, schema = crd_schema.convert(crd({'type': 'object', 'properties': {
            'n': {'type': 'string', 'nullable': True}, 'port': {'x-kubernetes-int-or-string': True}}}), 'v1')
        self.assertEqual(schema['properties']['n']['type'], ['string', 'null'])
        self.assertEqual(schema['properties']['port']['anyOf'], [{'type': 'integer'}, {'type': 'string'}])

    def test_unserved_or_missing_version_is_rejected(self):
        with self.assertRaises(ValueError):
            crd_schema.convert(crd({'type': 'object'}, served=False), 'v1')
        with self.assertRaises(ValueError):
            crd_schema.convert(crd({'type': 'object'}), 'v2')

    def test_committed_operator_schemas_are_strict_and_traceable(self):
        expected = {'crd-postgresql.cnpg.io-cluster-v1.json', 'crd-barmancloud.cnpg.io-objectstore-v1.json',
                    'crd-cert-manager.io-certificate-v1.json'}
        self.assertTrue(expected <= {p.name for p in CI.glob('crd-*.json')})
        for name in expected:
            schema = json.loads((CI / name).read_text())
            self.assertIs(schema['additionalProperties'], False, name)
            self.assertIs(schema['properties']['spec']['additionalProperties'], False, name)
            self.assertIn('source sha256', schema['$comment'])

    def test_validator_fails_closed_for_kinds_without_schema(self):
        script = (CI / 'validate.sh').read_text()
        self.assertIn('crd-{{.Group}}-{{.ResourceKind}}-{{.ResourceAPIVersion}}.json', script)
        for loophole in ('-ignore-missing-schemas', '-skip'):
            self.assertNotIn(loophole, script)


if __name__ == '__main__':
    unittest.main()
