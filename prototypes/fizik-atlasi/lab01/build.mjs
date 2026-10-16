/** Simple deterministic bundler for two authored ES modules; output offline single HTML. */
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {join,resolve} from 'node:path';
const root=resolve(import.meta.dirname);
const css=readFileSync(join(root,'src/styles.css'),'utf8');
let domain=readFileSync(join(root,'src/domain.mjs'),'utf8');
let app=readFileSync(join(root,'src/app.mjs'),'utf8');
const importLine=/^import\s+\{[^\n]+\}\s+from\s+'\.\/domain\.mjs';\s*$/m;
if(!importLine.test(app))throw new Error('Unexpected module import graph; build closed.');
app=app.replace(importLine,'');
if(/^import\s/m.test(app)||/^import\s/m.test(domain))throw new Error('Unknown module import; build closed.');
domain=domain.replace(/^export\s+(?=(const|function|class)\s)/gm,'');
const code=`(() => {\n'use strict';\n${domain}\n${app}\n})();`;
if(code.includes('</script'))throw new Error('Unexpected script closing text');
const html=readFileSync(join(root,'src/index.tpl.html'),'utf8')
 .replace('/*__CSS_BUNDLE__*/',css.replace(/<\/style/gi,'<\\/style'))
 .replace('/*__JS_BUNDLE__*/',code);
if(html.includes('__CSS_BUNDLE__')||html.includes('__JS_BUNDLE__'))throw new Error('Missing template substitution');
mkdirSync(join(root,'dist'),{recursive:true});writeFileSync(join(root,'dist/index.html'),html);
console.log(JSON.stringify({bytes:Buffer.byteLength(html),mode:'single-file-offline',modules:2,css:Buffer.byteLength(css)}));
