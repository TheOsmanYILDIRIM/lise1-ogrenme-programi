import test from 'node:test';
import assert from 'node:assert/strict';
import {LABS,FIELDS,CLASS_CARDS,TRANSFER_CARDS,calcExperiment,meaningfulDifference,newProgress,safeProgress,mastery,settingSignature} from '../src/domain.mjs';

test('curriculum pilot covers four labs, eight unique disciplines',()=>{
 assert.equal(LABS.length,4);assert.equal(FIELDS.length,8);assert.equal(new Set(FIELDS.map(x=>x.id)).size,8);
 for(const l of LABS)assert.ok(FIELDS.find(f=>f.id===l.field));
 assert.equal(CLASS_CARDS.length,8);assert.equal(TRANSFER_CARDS.length,4);
});
test('ramp acceleration increases with angle and roughness reduces it',()=>{
 const slow=calcExperiment('mechanics',{angle:14,surface:'smooth'});
 const fast=calcExperiment('mechanics',{angle:35,surface:'smooth'});
 const rough=calcExperiment('mechanics',{angle:35,surface:'rough'});
 assert.ok(fast.a>slow.a);assert.ok(fast.a>rough.a);assert.ok(fast.distance>slow.distance);
});
test('white light dispersion is a qualitative model; monochromatic stays one',()=>{
 assert.equal(calcExperiment('optics',{beam:'white',angle:0}).colors,6);
 assert.equal(calcExperiment('optics',{beam:'red',angle:10}).colors,1);
});
test('magnetic attraction increases near iron; zero field does not attract',()=>{
 const close=calcExperiment('magnet',{position:55,power:80});
 const far=calcExperiment('magnet',{position:14,power:80});
 const off=calcExperiment('magnet',{position:55,power:0});
 assert.ok(close.strength>far.strength);assert.equal(off.strength,0);
});
test('metal conducts faster than wood in model',()=>{
 const metal=calcExperiment('thermal',{material:'metal',temperature:90});
 const wood=calcExperiment('thermal',{material:'wood',temperature:90});
 assert.ok(metal.transfer>wood.transfer);
});
test('comparisons must change settings meaningfully',()=>{
 assert.equal(meaningfulDifference('mechanics',{angle:22,surface:'smooth'},{angle:23,surface:'smooth'}),false);
 assert.equal(meaningfulDifference('mechanics',{angle:22,surface:'smooth'},{angle:29,surface:'smooth'}),true);
 assert.equal(meaningfulDifference('optics',{beam:'white',angle:0},{beam:'red',angle:0}),true);
 assert.equal(meaningfulDifference('magnet',{position:30,power:50},{position:35,power:60}),false);
 assert.equal(meaningfulDifference('thermal',{material:'wood',temperature:80},{material:'metal',temperature:80}),true);
});
test('corrupt progress cannot grant completion; report gate checks all proof',()=>{
 const p=newProgress();
 const unsafe=structuredClone(p);unsafe.labs.mechanics.completed=true;
 assert.equal(safeProgress(unsafe).labs.mechanics.completed,false);
 assert.equal(mastery(p).pass,false);
 assert.equal(settingSignature('optics',{beam:'red',angle:4}),'red|4');
});
