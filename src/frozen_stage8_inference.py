"""Private research inference only: Original frozen Stage8 Transformer weights.
No training, no public API or real person inference permission granted by this module.
"""
import os, json, math, hashlib
from pathlib import Path
import numpy as np
import torch
from torch import nn

MODEL_SHA = '6f671f6c72445cdb06fbd7b580e99aa0dd4000d38fc8024c11b22b52e636d34d'
PREP_FILE_SHA = 'b18637de8c41aa044ca4da5a92e2d9da1ec7b401178bddaef497d62577782343'
PREP_EMBED_SHA = '48fe517e8738908d622f2b87d5f62e1b4f4d2ebc7c20e4c1ce3ba5f52c3c010e'
PLATT_FILE_SHA = '7a44b21502e7b24ec309f6bfe937cd772b21e339628dc9344cdf7041d6f46568'
DEPENDENCY_SHA = '4f8b0f09ac4578dd649769523daf7feed31911da18bbc775004a7b3085fc708a'
LAGS=(4,3,2,1,0)

def sha_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(4<<20),b''):h.update(chunk)
    return h.hexdigest()

def content_hash(payload):
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str).encode('utf8')).hexdigest()

class Stage8Architecture(nn.Module):
    def __init__(self,num_numeric,num_categories):
        super().__init__()
        d=64
        self.provider_embedding=nn.Embedding(num_categories,8)
        self.projection=nn.Linear(num_numeric+8,d)
        positions=torch.arange(5,dtype=torch.float32)[:,None]
        radians=torch.exp(-math.log(10000.0)*torch.arange(0,d,2,dtype=torch.float32)/d)
        pe=torch.zeros((5,d),dtype=torch.float32)
        pe[:,0::2]=torch.sin(positions*radians)
        pe[:,1::2]=torch.cos(positions*radians)
        self.register_buffer('fixed_sinusoidal_positions',pe.unsqueeze(0),persistent=True)
        layer=nn.TransformerEncoderLayer(d_model=d,nhead=4,dim_feedforward=4*d,
               dropout=0.1,activation='gelu',batch_first=True,norm_first=True)
        self.encoder=nn.TransformerEncoder(layer,num_layers=1,enable_nested_tensor=False)
        self.norm=nn.LayerNorm(d)
        self.classifier=nn.Linear(d,1)
    def forward(self,numeric,categorical):
        projected=self.projection(torch.cat([numeric,self.provider_embedding(categorical)],-1))
        encoded=self.encoder(projected+self.fixed_sinusoidal_positions)
        return self.classifier(self.norm(encoded[:,-1,:])).squeeze(-1)

class FrozenStage8Predictor:
    def __init__(self,package_dir):
        self.root=Path(package_dir)
        files={'model':self.root/'Transformer_full_refit_2017_2020.pt',
               'preproc':self.root/'FULL_DEVELOPMENT_2017_2019_SEQUENCE_sequence_preprocessor.json',
               'platt':self.root/'temporal_oof_platt_2018_2020.json'}
        sha={'model':MODEL_SHA,'preproc':PREP_FILE_SHA,'platt':PLATT_FILE_SHA}
        for k,path in files.items():
            if not path.is_file() or sha_file(path)!=sha[k]:raise RuntimeError('Immutable artifact identity failure: '+k)
        self.p=json.loads(files['preproc'].read_text());self.c=json.loads(files['platt'].read_text())
        data=dict(self.p);v=data.pop('preprocessor_sha256')
        if v!=PREP_EMBED_SHA or content_hash(data)!=v:raise RuntimeError('Preprocessor inner SHA failure')
        if self.c['dependency_sha256']!=DEPENDENCY_SHA or self.c['fit_years']!=[2018,2019,2020]:raise RuntimeError('Calibration provenance failure')
        self.f=list(self.p['active_numeric_features']);self.vocab=list(self.p['provider_type_vocabulary'])
        if len(self.f)!=27 or len(self.vocab)!=126 or list(self.p['sequence_order'])!=list(LAGS):raise RuntimeError('Schema drift')
        self.mapping={name:i for i,name in enumerate(self.vocab)}
        if len(self.mapping)!=126 or self.p['unknown_token'] not in self.mapping:raise RuntimeError('Categorical vocabulary invalid')
        self.cols={f'lag{k}_{feature}' for k in LAGS for feature in self.f}|{f'lag{k}_provider_type_mode' for k in LAGS}
        cp=torch.load(files['model'],map_location='cpu',weights_only=True)
        if cp['dependency_sha256']!=DEPENDENCY_SHA or cp['preprocessor_sha256']!=PREP_EMBED_SHA or cp['epochs']!=12:
            raise RuntimeError('Stage8 checkpoint governance mismatch')
        if cp['config']['config_id']!='TRF_d64_h4_l1_p0.1_lr1e-3' or cp['train_years']!=[2017,2018,2019,2020]:
            raise RuntimeError('Frozen model protocol mismatch')
        self.model=Stage8Architecture(len(self.f),len(self.vocab)).cpu()
        self.model.load_state_dict(cp['state_dict'],strict=True)
        self.model.eval()
    def preprocess(self,rows):
        if not isinstance(rows,list) or not (1<=len(rows)<=1000):raise ValueError('1..1000 input vectors required')
        x=np.empty((len(rows),5,len(self.f)),dtype=np.float32)
        c=np.empty((len(rows),5),dtype=np.int64)
        for i,row in enumerate(rows):
            if not isinstance(row,dict) or set(row)!=self.cols:raise ValueError('Schema mismatch: only frozen exact columns allowed')
            for j,name in enumerate(self.f):
                v=np.asarray([row[f'lag{k}_{name}'] for k in LAGS],dtype=np.float32)
                v[~np.isfinite(v)]=np.float32(self.p['medians'][name])
                if name in self.p['log1p_base_features']:
                    if (v<0).any():raise ValueError('Negative log1p feature: '+name)
                    v=np.log1p(v)
                v=(v-np.float32(self.p['means'][name]))/np.float32(self.p['stds'][name])
                if not np.isfinite(v).all():raise ValueError('Nonfinite normalized feature: '+name)
                x[i,:,j]=v
            for j,k in enumerate(LAGS):
                val=row[f'lag{k}_provider_type_mode']
                val=self.p['missing_token'] if val is None else str(val)
                c[i,j]=self.mapping.get(val,self.mapping[self.p['unknown_token']])
        return x,c
    def predict_transformed(self,x,c):
        a=np.asarray(x,dtype=np.float32);b=np.asarray(c,dtype=np.int64)
        if a.ndim!=3 or a.shape[1:]!=(5,27) or b.shape!=a.shape[:2]:raise ValueError('Transformed vector shape mismatch')
        if len(a)>1000 or len(a)<1 or not np.isfinite(a).all() or (b<0).any() or (b>=126).any():raise ValueError('Invalid transformed input')
        with torch.inference_mode():
            z=self.model(torch.from_numpy(a),torch.from_numpy(b)).numpy().astype(np.float64)
        calibrated=self.calibrate(z)
        return z,calibrated
    def predict(self,rows):
        return self.predict_transformed(*self.preprocess(rows))
    def calibrate(self,z):
        t=float(self.c['intercept'])+float(self.c['slope'])*np.asarray(z,dtype=np.float64)
        t=np.clip(t,-700,700)
        return np.where(t>=0,1/(1+np.exp(-t)),np.exp(t)/(1+np.exp(t)))
