import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {createHash} from 'node:crypto';
const root=resolve(import.meta.dirname,'..');const site=join(root,'site');
test('manifest pins immutable filename to actual source digest',()=>{
 const info=JSON.parse(readFileSync(join(site,'version.json')));
 assert.match(info.sha256,/^[a-f0-9]{64}$/);
 assert.equal(info.asset,`atlas-${info.sha256.slice(0,16)}.html`);
 assert.ok(existsSync(join(site,info.asset)));
 assert.equal(createHash('sha256').update(readFileSync(join(site,info.asset))).digest('hex'),info.sha256);
});
test('entry is uncacheable and points at immutable content without erasing progress',()=>{
 const info=JSON.parse(readFileSync(join(site,'version.json')));
 const entry=readFileSync(join(site,'index.html'),'utf8');
 const rules=readFileSync(join(site,'_headers'),'utf8');
 assert.ok(entry.includes(info.asset));
 assert.match(entry,/location\.replace/);
 assert.match(rules,/\/index\.html\n  Cache-Control: no-store, max-age=0/);
 assert.match(rules,/\/version\.json\n  Cache-Control: no-store, max-age=0/);
 assert.ok(rules.includes(`/${info.asset}\n  Cache-Control: public, max-age=31536000, immutable`));
 assert.ok(!entry.includes('localStorage.clear'));
 assert.ok(!entry.includes('caches.delete'));
});
