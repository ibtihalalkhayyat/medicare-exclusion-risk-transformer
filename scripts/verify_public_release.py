#!/usr/bin/env python3
"""Verify PUBLIC synthetic demonstration package only (stdlib; no model weights)."""
import csv, hashlib, json, math, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
def stop(message):
    raise SystemExit('RELEASE VERIFICATION FAILED: ' + message)
def read(path): return (ROOT / path).read_bytes()
def load_json(path): return json.loads(read(path))
def sha(data): return hashlib.sha256(data).hexdigest()
def verify():
    manifest=load_json('PUBLIC_RELEASE_SHA256.json')
    if manifest.get('release_kind')!='PUBLIC_SYNTHETIC_RESEARCH_SOURCE_ONLY':stop('release kind')
    for path,expected in manifest['public_files_sha256'].items():
        file=ROOT/path
        if not file.is_file():stop('missing file '+path)
        if sha(read(path))!=expected:stop('SHA mismatch '+path)
    grid=load_json('demo/data/inference_grid.json')
    scenarios=load_json('demo/data/scenarios.json')
    schema=load_json('schema.json')
    if len(grid['scale_values'])!=21:stop('21 multiplier bins required')
    if len(scenarios)!=24 or len(grid['cases'])!=24:stop('24 rows required')
    if len(schema['columns'])!=141 or schema.get('model_inputs_per_record')!=140:stop('140 field schema required')
    ids=[x['synthetic_case_id'] for x in scenarios]
    if len(set(ids))!=24 or set(ids)!={x['synthetic_case_id'] for x in grid['cases']}:stop('scenario identity mismatch')
    cols=set(schema['columns'])
    if set(scenarios[0])!=cols:stop('synthetic schema mismatch')
    for row in scenarios:
        if set(row)!=cols or not row['synthetic_case_id'].startswith('SYNTHETIC_'):stop('invalid row schema')
    n=0
    for item in grid['cases']:
        vals=item['calibrated_outputs']
        if len(vals)!=21:stop('21 outputs per case')
        if any(not isinstance(v,(int,float)) or not math.isfinite(v) or v<0 or v>1 for v in vals):stop('invalid output')
        n+=len(vals)
    if n!=504:stop('504 outputs required')
    with (ROOT/'demo/data/synthetic_examples.csv').open(newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if set(reader.fieldnames)!=cols:stop('CSV schema mismatch')
        rows=list(reader)
    if len(rows)!=24 or {r['synthetic_case_id'] for r in rows}!=set(ids):stop('CSV count/IDs mismatch')
    forbidden=['.pt','.pth','.safetensors','.ckpt','.pem','.key']
    for p in ROOT.rglob('*'):
        if not p.is_file() or '.git' in p.parts:continue
        if p.suffix.lower() in forbidden:stop('prohibited private file '+str(p))
    prov=load_json('demo/data/model_output_provenance.json')
    if prov['frozen_model_modified'] is not False or prov['new_training_or_calibration'] is not False:stop('provenance contradiction')
    if prov['precomputed_outputs']!=504 or prov['synthetic_scenarios']!=24:stop('provenance count mismatch')
    print('PASS: public synthetic repository integrity verified: 24 cases, 140 inputs, 21 multipliers, 504 cached outputs.')
    print('PASS: public files SHA-256, frozen asset provenance, and absence of private weight types.')
    print('SCOPE: This does not validate real-provider scientific performance or independently reproduce model outputs.')
if __name__=='__main__':verify()
