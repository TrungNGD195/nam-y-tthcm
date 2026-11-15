"""Independent numerical review. Requires numpy/scipy only for authoring, never for the site."""
import json, math, importlib, sys, copy, unicodedata
from pathlib import Path
import numpy as np
from scipy import ndimage, signal, fft
import calculations as calc

ROOT=Path(__file__).resolve().parents[3]
checks={'correlation':0,'morphology':0,'histogram':0,'dct':0,'lzw_roundtrip':0,'otsu':0,'isodata':0,'smooth':0,'ac_roundtrip':0,'serialized_solutions':0}
original_correlate=calc.correlate
def checked_correlate(a,h,valid=False):
    result=original_correlate(a,h,valid)
    expected=signal.correlate2d(np.array(a),np.array(h),mode='valid' if valid else 'same',boundary='fill',fillvalue=0)
    assert np.allclose(result,expected,atol=1e-9)
    checks['correlation']+=1
    return result
calc.correlate=checked_correlate

original_morph=calc.morph
def checked_morph(a,b,op='erode',standard=False):
    result=original_morph(a,b,op,standard)
    structure=np.array(b,dtype=bool)
    if op=='erode':expected=ndimage.binary_erosion(a,structure=structure,border_value=0)
    else:expected=ndimage.binary_dilation(a,structure=structure if standard else np.flip(structure),border_value=0)
    assert np.array_equal(result,expected)
    if op=='erode' and b[len(b)//2][len(b[0])//2]:assert np.all(np.array(result)<=np.array(a))
    checks['morphology']+=1
    return result
calc.morph=checked_morph

original_hist=calc.hist
def checked_hist(a,levels=None):
    result=original_hist(a,levels)
    expected=np.bincount(np.array(a).ravel(),minlength=levels or 0).tolist()
    assert result==expected and sum(result)==np.array(a).size
    checks['histogram']+=1
    return result
calc.hist=checked_hist

original_dct=calc.dct
def checked_dct(a):
    result=original_dct(a);expected=fft.dctn(a,type=2,norm='ortho')
    assert np.allclose(result,expected,atol=1e-9)
    assert np.allclose(fft.idctn(expected,type=2,norm='ortho'),a,atol=1e-9)
    checks['dct']+=1
    return result
calc.dct=checked_dct

original_decode=calc.lzw_decode
def checked_decode(codes,initial):
    result,trace=original_decode(codes,initial)
    # Separate string-dictionary decoder, including the KwKwK case.
    dictionary={i:chr(i) for i in range(initial)};word=dictionary[codes[0]];text=word
    for code in codes[1:]:
        entry=dictionary.get(code,word+word[0]);dictionary[len(dictionary)]=word+entry[0];text+=entry;word=entry
    assert result==list(map(ord,text))
    checks['lzw_roundtrip']+=1
    return result,trace
calc.lzw_decode=checked_decode

original_otsu=calc.otsu
def checked_otsu(h):
    result,opts=original_otsu(h)
    pixels=np.repeat(np.arange(len(h)),h)
    variance=[]
    for k in range(len(h)-1):
        low=pixels[pixels<=k];high=pixels[pixels>k]
        variance.append((len(low)/len(pixels))*(len(high)/len(pixels))*(low.mean()-high.mean())**2 if len(low) and len(high) else 0)
    assert np.allclose([r[-1] for r in result],variance,atol=1e-9)
    assert opts==np.flatnonzero(np.isclose(variance,max(variance),rtol=0,atol=1e-10)).tolist()
    checks['otsu']+=1
    return result,opts
calc.otsu=checked_otsu

original_iso=calc.isodata
def checked_iso(h,t,round_each=True):
    rows=original_iso(h,t,round_each)
    pixels=np.repeat(np.arange(len(h)),h)
    for current,mu1,mu2,nxt in rows:
        low=pixels[pixels<=current];high=pixels[pixels>current]
        assert np.isclose(mu1,low.mean()) and np.isclose(mu2,high.mean())
        mean=(low.mean()+high.mean())/2
        expected=np.floor(mean+0.5) if round_each else mean
        assert np.isclose(nxt,expected)
    assert np.isclose(rows[-1][0],rows[-1][-1])
    checks['isodata']+=1
    return rows
calc.isodata=checked_iso

original_smooth=calc.smooth
def checked_smooth(h,w):
    result=original_smooth(h,w)
    assert np.allclose(result,np.convolve(np.pad(h,(w//2,w//2)),np.ones(w)/w,mode='valid'))
    checks['smooth']+=1
    return result
calc.smooth=checked_smooth

original_pairs=calc.acpairs
def checked_pairs(seq):
    pairs=original_pairs(seq)
    decoded=[]
    for run,value in pairs:
        if (run,value)==(0,0):decoded.extend([0]*(len(seq)-len(decoded)))
        elif (run,value)==(15,0):decoded.extend([0]*16)
        else:decoded.extend([0]*run+[value])
    assert decoded==seq
    checks['ac_roundtrip']+=1
    return pairs
calc.acpairs=checked_pairs

import exercises as e

assert calc.hist(e.I,10)==[4,5,6,6,4,4,4,0,1,2]  # source answer key, PDF page 21
assert len(calc.huffman(e.HB1)[3])==87  # source key page 32
assert len(calc.huffman(e.HB2)[3])==85
for a in [e.HB1,e.HB2,e.HU1,e.HU2]:
    syms,freq,codes,bits,_=calc.huffman(a)
    assert all(not y.startswith(x) for s,x in codes.items() for t,y in codes.items() if s!=t)
    reverse={v:k for k,v in codes.items()};word='';decoded=[]
    for bit in bits:
        word+=bit
        if word in reverse:decoded.append(reverse[word]);word=''
    assert decoded==syms and word==''
assert e.syms==['A','B','A','C','A','A','B','E','C','B','A','D']
assert e.quant==[[11,0],[-2,1]] and e.dcbit+e.acbit=='011011101101001'
assert e.err==91 and e.energy==185012
assert e.components(e.b1,e.CROSS)==1 and e.components(e.b2,e.CROSS)==2
assert e.components(e.b1,e.SQUARE)==e.components(e.b2,e.SQUARE)==1
assert e.runs==[9,3,0,13,5,0,2,11]
assert np.allclose(e.restored,[[9,7],[13,15]]) and abs(e.rms-2.0)<1e-9
assert math.isclose(sum(x*x for row in e.JT for x in row),sum(x*x for row in fft.idctn(e.JT,norm='ortho') for x in row))

raw=json.loads((ROOT/'content/xu-ly-anh/source-prompts.json').read_text(encoding='utf-8'))
data=json.loads((ROOT/'src/subjects/xu-ly-anh/solutions.json').read_text(encoding='utf-8'))
assert {r['id'] for r in raw['records']}=={r['id'] for r in data['items']}
assert {r['id'] for r in raw['records'] if r['kind']=='exercise'}==set(e.SOLUTIONS)
assert len(data['items'])==168 and len(e.SOLUTIONS)==67
for item in data['items']:
    if item['kind']!='exercise':continue
    expected=copy.deepcopy(e.SOLUTIONS[item['id']]['steps'])
    for step in expected:
        if step.get('formula'):
            step['formula']=''.join(c for c in unicodedata.normalize('NFD',step['formula'].replace('đ','d').replace('Đ','D')) if not unicodedata.combining(c))
        if item['id']=='uyen-5-T6':
            for block in step.get('blocks',[]):
                if block['type']=='table' and 'h_s' in block['headers'][-1]:block['rows']=[[r[0],round(r[1],2)] for r in block['rows']]
    assert item['steps']==expected, f'{item["id"]}: serialized solution differs from independently checked calculations'
    checks['serialized_solutions']+=1
print(json.dumps({'result':'passed','sourceItems':168,'calculationItems':67,'independentChecks':checks},ensure_ascii=False))
