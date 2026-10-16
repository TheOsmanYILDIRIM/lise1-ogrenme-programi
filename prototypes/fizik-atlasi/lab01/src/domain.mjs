/**
 * Fizik Atlası — öğrenme alanı, deneyler ve değerlendirme.
 * Bağımsız saf fonksiyonlar; DOM yok, ağ yok, kalıcı öğrenci sistemi yok.
 */
export const VERSION = '1.1.0';
export const STORAGE_KEY = 'fizik-atlasi-lab01-v1';
export const FIELDS = [
  {id:'mekanik',name:'Mekanik',short:'Hareket',symbol:'◈',color:'#73e5ca',description:'Kuvvet, hareket ve dengeyi araştırır.'},
  {id:'optik',name:'Optik',short:'Işık',symbol:'◇',color:'#b1a5ff',description:'Işığın yayılmasını ve maddeyle etkileşimini inceler.'},
  {id:'elektromanyetizma',name:'Elektromanyetizma',short:'Alanlar',symbol:'⌁',color:'#ffd486',description:'Elektrik yükleri, akımlar ve manyetik alanları inceler.'},
  {id:'termodinamik',name:'Termodinamik',short:'Isı',symbol:'≋',color:'#ff9f84',description:'Isı, enerji aktarımı ve sıcaklık değişimlerini araştırır.'},
  {id:'atom',name:'Atom Fiziği',short:'Atom',symbol:'◎',color:'#80cfff',description:'Atomların yapısını ve elektronların enerji düzeylerini inceler.'},
  {id:'nukleer',name:'Nükleer Fizik',short:'Çekirdek',symbol:'✳',color:'#eea6d8',description:'Atom çekirdeğini, bozunmayı ve çekirdek tepkimelerini araştırır.'},
  {id:'katihal',name:'Katıhal Fiziği',short:'Malzeme',symbol:'▦',color:'#b3e78a',description:'Kristalleri, yarıiletkenleri ve katıların özelliklerini inceler.'},
  {id:'plazma',name:'Yüksek Enerji ve Plazma Fiziği',short:'Plazma',symbol:'✺',color:'#ffb973',description:'Plazmaları ve çok yüksek enerjili parçacık olaylarını araştırır.'}
];
export const LABS = [
  {
    id:'mechanics',field:'mekanik',chapter:'01',title:'Eğim İstasyonu',caption:'Kuvvet ve hareket',
    mission:'Bir cismin eğimli yolda hareketini kontrol et. Aynı cismi farklı koşullarda dene.',
    question:'Rampanın eğimi artarsa, aynı yüzeyde cisim genellikle nasıl hareket eder?',
    options:['Daha hızlı ivmelenir','Mutlaka durur','Eğim hareketi etkilemez'],answer:0,
    explainQuestion:'Bu deneyde hangi ilişkiyi kanıtlarla araştırdın?',
    explainOptions:['Yüzeyin renk değişimini','Eğim ve sürtünmenin harekete etkisini','Işığın kırılmasını'],explainAnswer:1,
    science:'Eğim arttıkça yerçekiminin rampaya paralel bileşeni büyür. Sürtünme harekete karşı koyar. Bu laboratuvar, mekanik ile ilgilidir.',
    adjustment:'Eğimi ve yüzey türünü değiştirerek iki farklı ölçüm kaydet.',
    tag:'Hareket · Mekanik', concept:'Mekanik'
  },
  {
    id:'optics',field:'optik',chapter:'02',title:'Işık Odası',caption:'Işığı ayrıştır',
    mission:'Prizmadan geçen ışığı gözlemle. Beyaz ve tek renkli ışığı karşılaştır.',
    question:'Beyaz ışık uygun bir prizmadan geçtiğinde ne gözlenebilir?',
    options:['Her zaman karanlığa dönüşür','Farklı renklere ayrılabilir','Manyetik alana dönüşür'],answer:1,
    explainQuestion:'Prizmanın yarattığı olayı hangi fizik alanı inceler?',
    explainOptions:['Optik: ışığın kırılması ve renklerine ayrılması','Nükleer fizik: çekirdek bozunması','Mekanik: cismin hızlanması'],explainAnswer:0,
    science:'Prizmada farklı dalga boylarındaki ışık farklı miktarlarda kırılır. Beyaz ışığın ayrılması bir optik olayıdır; temsili çizim gerçek kırılma açılarını ölçekle göstermez.',
    adjustment:'Beyaz ışığı kırmızı veya mavi ışıkla karşılaştır. Giriş açısını değiştir.',
    tag:'Işık · Optik', concept:'Optik'
  },
  {
    id:'magnet',field:'elektromanyetizma',chapter:'03',title:'Manyetik Alan',caption:'Görünmeyen kuvvet',
    mission:'Mıknatısı demir bilyeye yaklaştır. Alan gücünü değiştir, tahta ile karşılaştır.',
    question:'Mıknatıs yaklaştırıldığında hangi nesnenin etkilenmesi beklenir?',
    options:['Tahta blok','Demir bilye','İkisi de eşit biçimde'],answer:1,
    explainQuestion:'Mıknatısın demiri çekmesini doğrudan hangi alan açıklar?',
    explainOptions:['Termodinamik','Optik','Elektromanyetizma'],explainAnswer:2,
    science:'Demir gibi ferromanyetik maddeler mıknatıstan güçlü biçimde etkilenebilir; tahta bu deneyde böyle tepki vermez. Tüm metaller manyetik değildir. Çekim animasyonu kavramsaldır.',
    adjustment:'Mıknatısı sürükle veya konumunu kaydır, alan gücünü değiştir ve yeniden ölç.',
    tag:'Manyetizma · Elektromanyetizma', concept:'Elektromanyetizma'
  },
  {
    id:'thermal',field:'termodinamik',chapter:'04',title:'Isı Laboratuvarı',caption:'Enerjiyi izle',
    mission:'Aynı ısı kaynağıyla iki malzemenin ısı iletimini karşılaştır.',
    question:'Benzer koşullarda metal ve ahşap çubuklardan hangisi genellikle ısıyı daha hızlı iletir?',
    options:['Ahşap çubuk','İkisi her zaman eşit','Metal çubuk'],answer:2,
    explainQuestion:'Gözlediğin değişim en çok hangi fizik alanıyla ilişkilidir?',
    explainOptions:['Termodinamik: ısı aktarımı','Optik: ışığın dağılması','Nükleer fizik: çekirdek tepkimesi'],explainAnswer:0,
    science:'Metaller genellikle ahşaba göre daha iyi ısı iletkenidir. Gösterimde çubuğa yayılan renk temsili bir göstergedir; sıcaklık dağılımı gerçek bir ölçüm değildir.',
    adjustment:'Malzemeyi ve kaynak sıcaklığını değiştirip iki sonuç kaydet.',
    tag:'Isı · Termodinamik', concept:'Termodinamik'
  }
];
export const CLASS_CARDS=[
  {title:'Kaykay pistinde hızlanma',body:'Sporcu eğimli bir rampada hızlanıyor. Kuvvet ve hareket açıklanmak isteniyor.',field:'mekanik',tip:'İvme ve kuvvet araştırması.'},
  {title:'Gökkuşağını oluşturan damlalar',body:'Güneş ışığı su damlalarında kırılıp renklere ayrılıyor.',field:'optik',tip:'Işığın kırılması ve dağılımı.'},
  {title:'Demiri kaldıran elektromıknatıs',body:'Hurda tesisinde elektrik akımıyla çalışan dev bir mıknatıs var.',field:'elektromanyetizma',tip:'Akım ve manyetik alan.'},
  {title:'Sıcaklığı koruyan termos',body:'İçeceğin çevreyle ısı alışverişi azaltılıyor.',field:'termodinamik',tip:'Isı aktarımı ve yalıtım.'},
  {title:'Atomların çizgi tayfı',body:'Uyarılmış atomlar belirli dalga boylarında ışık yayıyor; enerji düzeyleri inceleniyor.',field:'atom',tip:'Atomdaki elektron düzeyleri.'},
  {title:'Radyoaktif izotopun bozunması',body:'Bir atom çekirdeği bozunuyor ve ışıma yayıyor.',field:'nukleer',tip:'Çekirdekle ilgili olay.'},
  {title:'Mikroçipte yarıiletken',body:'Silisyum kristalinin elektriksel özellikleriyle transistör tasarlanıyor.',field:'katihal',tip:'Katı madde ve yarıiletken özellikleri.'},
  {title:'Yıldızdaki iyonlaşmış gaz',body:'Güneş atmosferindeki elektrik yüklü plazma davranışı inceleniyor.',field:'plazma',tip:'Plazma ve yüksek enerjili ortam.'}
];
export const TRANSFER_CARDS=[
  {title:'Uyduyu yörüngede tutmak',body:'Bir uyduya etki eden kuvvetler ile yörüngesel hareket hesaplanıyor.',field:'mekanik'},
  {title:'Fiber optik kablo',body:'Işık, camın içinde tam yansıma ile iletiliyor.',field:'optik'},
  {title:'LED ekranın ışığı',body:'Yarıiletken malzemenin elektronik özellikleri kullanılarak bir ekran geliştiriliyor.',field:'katihal'},
  {title:'Kanser tedavisinde radyoizotop',body:'Atom çekirdeğinin radyoaktif bozunması tedavide kullanılıyor.',field:'nukleer'}
];
export const START_SETTINGS={
  mechanics:{angle:22,surface:'smooth'}, optics:{beam:'white',angle:0},
  magnet:{position:40,power:60},thermal:{material:'metal',temperature:80}
};
export function calcMechanics({angle,surface}){
  const theta=Number(angle)*Math.PI/180;
  const mu=surface==='rough'?0.28:0.04;
  const a=Math.max(0,9.81*(Math.sin(theta)-mu*Math.cos(theta)));
  const t=1.5;
  return {a,velocity:a*t,distance:0.5*a*t*t, label:a<0.01?'Kayma gözlenmedi':`İvme ${a.toFixed(2)} m/s²`,value:a.toFixed(2)+' m/s²'};
}
/** Snell's law ray trace through an equilateral-like triangular prism. Screen y points down. */
export function tracePrism(angle=0, index=1.52){
 const vertices=[[440,128],[580,385],[300,385]];
 const cross=(a,b)=>a[0]*b[1]-a[1]*b[0];
 const norm=v=>{const n=Math.hypot(...v);return v.map(x=>x/n)};
 const hit=(p,d,edge)=>{const q=edge[0],e=[edge[1][0]-q[0],edge[1][1]-q[1]],v=[q[0]-p[0],q[1]-p[1]],den=cross(d,e);if(Math.abs(den)<1e-8)return null;const t=cross(v,e)/den,u=cross(v,d)/den;return t>1e-4&&u>=0&&u<=1?{p:[p[0]+t*d[0],p[1]+t*d[1]],t,edge}:null};
 const edges=[[vertices[0],vertices[1]],[vertices[1],vertices[2]],[vertices[2],vertices[0]]];
 const input=[Math.cos(angle*Math.PI/180),Math.sin(angle*Math.PI/180)];
 const source=[80,270];let entries=edges.map(e=>hit(source,input,e)).filter(Boolean).sort((x,y)=>x.t-y.t);
 if(!entries.length)return {source,miss:true,input};
 let entry=entries[0], d=input;
 // normal facing the incoming ray; refract into higher-index glass
 let e=entry.edge,face=norm([-(e[1][1]-e[0][1]),e[1][0]-e[0][0]]);
 if(d[0]*face[0]+d[1]*face[1]>0)face=face.map(x=>-x);
 const refract=(direction,normal,n1,n2)=>{const cosine=-(direction[0]*normal[0]+direction[1]*normal[1]),eta=n1/n2,k=1-eta*eta*(1-cosine*cosine);return k<0?null:norm([eta*direction[0]+(eta*cosine-Math.sqrt(k))*normal[0],eta*direction[1]+(eta*cosine-Math.sqrt(k))*normal[1]])};
 d=refract(d,face,1,index);if(!d)return {source,entry:entry.p,miss:true,input};
 let exits=edges.filter(e=>e!==entry.edge).map(e=>hit([entry.p[0]+d[0]*0.02,entry.p[1]+d[1]*0.02],d,e)).filter(Boolean).sort((a,b)=>a.t-b.t);
 if(!exits.length)return {source,entry:entry.p,inside:d,miss:true,input};
 const exit=exits[0],edge=exit.edge;let normal=norm([-(edge[1][1]-edge[0][1]),edge[1][0]-edge[0][0]]);if(d[0]*normal[0]+d[1]*normal[1]>0)normal=normal.map(x=>-x);
 const outside=refract(d,normal,index,1);
 return {source,entry:entry.p,exit:exit.p,inside:d,outside,internalReflection:!outside,index};
}
export function calcOptics({beam,angle}){
 const rays=beam==='white'?[['red',1.513],['orange',1.516],['yellow',1.519],['green',1.522],['blue',1.529],['violet',1.536]]:[[beam,beam==='red'?1.513:1.529]];
 const paths=rays.map(([color,n])=>({color,...tracePrism(Number(angle),n)}));
 return {colors:rays.length,paths,caption:paths.every(x=>x.miss)?'Işın prizmayı ıskaladı; açıyı değiştir.':'Giriş açısı ve renge göre kırılma yolu değişir.',value:paths.every(x=>x.miss)?'Prizmaya temas yok':`${rays.length} dalga boyu · Snell modeli`};
}
/** Relative force on an iron sphere, dipole-inspired 1/r^4 gradient; not calibrated to newtons. */
export function calcMagnet({position,power}){
 const gap=Math.max(.08,(697-(80+7.4*Number(position))-95)/420); // dimensionless center-to-center gap
 const raw=(Number(power)/100)**2/(1+gap*4)**4;
 const strength=Math.min(1,raw*13);
 return {distance:gap,strength,affected:strength>.02,value:`Bağıl çekim ${Math.round(strength*100)} / 100`};
}
/** Illustrative 1D transient diffusion timescale, far-tip temperature. Same dimensions in both runs. */
export function thermalAtTime({material,temperature},t){
 const rate=material==='metal'?.25:.018;
 const tip=20+(Number(temperature)-20)*(1-Math.exp(-rate*Math.max(0,t)));
 return {tip,rate,source:Number(temperature),ambient:20};
}
export function calcThermal(s){
 const t=thermalAtTime(s,8);
 return {transfer:t.tip-20,tip:t.tip,materialName:s.material==='metal'?'Metal':'Ahşap',value:`8. saniyede uç: ${t.tip.toFixed(1)} °C (model)`};
}
export function calcExperiment(id,settings){
  switch(id){case 'mechanics':return calcMechanics(settings);case 'optics':return calcOptics(settings);case 'magnet':return calcMagnet(settings);case 'thermal':return calcThermal(settings);default:throw new RangeError('Bilinmeyen deney: '+id);}
}
export function settingSignature(id,s){switch(id){
  case 'mechanics':return `${s.angle}|${s.surface}`;
  case 'optics':return `${s.beam}|${s.angle}`;
  case 'magnet':return `${s.position}|${s.power}`;
  case 'thermal':return `${s.material}|${s.temperature}`;
  default:throw new RangeError('Bilinmeyen deney');
}}
/** Require visibly different conditions before claiming a comparative experiment. */
export function meaningfulDifference(id,a,b){
 if(!a||!b)return false;
 switch(id){
  case 'mechanics': return a.surface!==b.surface||Math.abs(Number(a.angle)-Number(b.angle))>=6;
  case 'optics': return a.beam!==b.beam||Math.abs(Number(a.angle)-Number(b.angle))>=8;
  case 'magnet': return Math.abs(Number(a.position)-Number(b.position))>=12||Math.abs(Number(a.power)-Number(b.power))>=25;
  case 'thermal': return a.material!==b.material||Math.abs(Number(a.temperature)-Number(b.temperature))>=20;
  default: throw new RangeError('Bilinmeyen deney');
 }
}
export function newProgress(){return {version:1,view:'explore',activeLab:'mechanics',settings:structuredClone(START_SETTINGS),labs:Object.fromEntries(LABS.map(x=>[x.id,{prediction:null,measurements:[],reason:null,reasonAttempts:0,completed:false}])),classIndex:0,classAnswers:[],classMistakes:0,classCurrentMistake:false,classCurrentHint:false,transferIndex:0,transferAnswers:[],transferMistakes:0,transferCurrentMistake:false,hints:0,missionStarted:false};}
export function safeProgress(p){if(!p||p.version!==1||!p.labs||!p.settings)return newProgress();const valid=newProgress();for(const lab of LABS){const src=p.labs?.[lab.id];if(src&&typeof src==='object'){const dest=valid.labs[lab.id];dest.prediction=Number.isInteger(src.prediction)&&src.prediction>=0&&src.prediction<3?src.prediction:null;dest.measurements=Array.isArray(src.measurements)?src.measurements.filter(x=>x&&typeof x.key==='string'&&typeof x.result==='string'&&x.settings&&typeof x.settings==='object').slice(-12):[];dest.reason=Number.isInteger(src.reason)?src.reason:null;dest.reasonAttempts=Number(src.reasonAttempts)||0;dest.completed=!!src.completed&&dest.measurements.length>=2&&dest.measurements.some((x,i)=>dest.measurements.some((y,j)=>i!==j&&meaningfulDifference(lab.id,x.settings,y.settings)))&&dest.reason===lab.explainAnswer;}
  const settings=p.settings[lab.id];if(settings&&typeof settings==='object'){for(const k of Object.keys(valid.settings[lab.id])){if(typeof settings[k]===typeof valid.settings[lab.id][k])valid.settings[lab.id][k]=settings[k]}}}
 valid.activeLab=LABS.some(x=>x.id===p.activeLab)?p.activeLab:'mechanics';valid.view=['explore','classify','transfer','report'].includes(p.view)?p.view:'explore';
 valid.classAnswers=Array.isArray(p.classAnswers)?p.classAnswers.slice(0,CLASS_CARDS.length).filter((a,i)=>a&&a.field===CLASS_CARDS[i].field):[];
 valid.classIndex=valid.classAnswers.length;valid.classCurrentMistake=!!p.classCurrentMistake;valid.classCurrentHint=!!p.classCurrentHint;
 valid.classMistakes=Math.max(0,Math.min(999,Number(p.classMistakes)||0));
 valid.transferAnswers=Array.isArray(p.transferAnswers)?p.transferAnswers.slice(0,TRANSFER_CARDS.length).filter((a,i)=>a&&a.field===TRANSFER_CARDS[i].field):[];
 valid.transferIndex=valid.transferAnswers.length;valid.transferCurrentMistake=!!p.transferCurrentMistake;valid.transferMistakes=Math.max(0,Math.min(999,Number(p.transferMistakes)||0));valid.hints=Math.max(0,Math.min(999,Number(p.hints)||0));valid.missionStarted=!!p.missionStarted;
 return valid;
}
export function labCount(p){return LABS.filter(x=>p.labs[x.id].completed).length;}
export function firstPassCount(answers){return answers.filter(x=>x.firstPass).length;}
export function mastery(p){const count=labCount(p);const classified=firstPassCount(p.classAnswers);const transferred=firstPassCount(p.transferAnswers);return {count,classified,transferred,pass:count===4&&p.classAnswers.length===8&&p.transferAnswers.length===4&&classified>=6&&transferred>=3&&p.hints<=3};}
export function documentEvidence(p){const m=mastery(p);return {format:'fizik-atlasi-educational-evidence-v1',outcome:'FİZ.9.1.2',units:['FİZ.9.1.1','FİZ.9.1.2'],finishedLabs:m.count,classificationFirstPass:m.classified,totalClassified:p.classAnswers.length,transferFirstPass:m.transferred,totalTransfer:p.transferAnswers.length,hints:p.hints,learningEvidence:m.pass?'strong-candidate':'practice-needed',note:'Bu prototip performans göstergesi resmî kazanım belgesi değildir; sadece bu cihaza kaydedilir.'};}
