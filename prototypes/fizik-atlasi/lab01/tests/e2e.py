from pathlib import Path
from playwright.sync_api import sync_playwright

html=Path(__file__).resolve().parents[1].joinpath('dist/index.html').read_text()
LABS=[('mechanics',0,1,'angle','34'),('optics',1,0,'angle','13'),('magnet',1,2,'power','90'),('thermal',2,0,'temperature','100')]
FIELDS=['mekanik','optik','elektromanyetizma','termodinamik','atom','nukleer','katihal','plazma']
TRANSFERS=['mekanik','optik','katihal','nukleer']
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for_timeout_marker = None
 for width in (360,390,1280):
  page=browser.new_page(viewport={'width':width,'height':800},device_scale_factor=1);page.set_default_timeout(2800); print('START',width,flush=True)
  errors=[]
  page.on('pageerror', lambda err: errors.append(str(err)))
  page.set_content(html)
  page.get_by_role('button',name='Laboratuvara gir').click()
  assert page.get_by_text('Keşif istasyonları').is_visible()
  assert page.evaluate('document.documentElement.scrollWidth')<=width, 'horizontal overflow on initial screen'
  for id,pred,reason,slider,new_value in LABS:
   print('  LAB',id,flush=True)
   page.locator(f'button[data-lab="{id}"]').click()
   page.locator(f'button[data-predict="{pred}"]').click()
   page.get_by_role('button',name='Deneyi çalıştır').click()
   assert '1/2 farklı koşul' in page.locator('.measure-summary').inner_text()
   if id=='mechanics':
    page.get_by_role('button',name='Deneyi çalıştır').click()
    assert '1/2 farklı koşul' in page.locator('.measure-summary').inner_text(),'duplicate run counted'
   element=page.locator(f'input[data-control="{slider}"]')
   element.evaluate('''(el,value) => { el.value=value;el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true})); }''',new_value)
   page.get_by_role('button',name='Deneyi çalıştır').click()
   assert '2/2 farklı koşul' in page.locator('.measure-summary').inner_text()
   page.locator(f'button[data-reason="{reason}"]').click()
   page.get_by_role('button',name='Açıklamamı doğrula').click()
   assert 'Keşif kaydedildi' in page.locator('.reason-step').inner_text(),f'not completed {id}'
  assert '4 / 4 istasyon tamamlandı' in page.locator('.unlock-strip').inner_text()
  page.locator('.unlock-strip button[data-view="classify"]').click()
  print('CLASSIFY START',flush=True)
  for i,f in enumerate(FIELDS):
   print('  CARD',i,f,flush=True)
   assert f'OLAY KARTI {i+1:02}' in page.locator('.case-panel').inner_text()
   if i==0:
    page.locator('button[data-class="optik"]').click()
    assert 'Henüz değil.' in page.locator('#answer-feedback').inner_text()
   page.locator(f'button[data-class="{f}"]').click()
  assert '7/8' in page.locator('.score-tiles').inner_text()
  page.locator('.congrats button[data-view="transfer"]').click()
  print('TRANSFER START',flush=True)
  for f in TRANSFERS:
   print('  TRANS',f,flush=True)
   page.locator(f'button[data-transfer="{f}"]').click()
  assert '4 / 4' in page.locator('.transfer-finish').inner_text()
  page.locator('.transfer-finish button[data-view="report"]').click()
  assert 'Güçlü öğrenme kanıtı' in page.locator('.report-header').inner_text()
  assert 'FİZ.9.1.2' in page.locator('.report-header').inner_text()
  scroll=page.evaluate('document.documentElement.scrollWidth')
  assert scroll<=width,f'overflow on report: {width} => {scroll}'
  if errors:raise AssertionError(f'{width}px browser errors: {errors}')
  page.screenshot(path=str(Path(__file__).with_name(f'report_{width}.png')),full_page=True)
  print(f'PASS e2e {width}px: 4 live labs, duplication prevention, 8 classifications, 4 transfers, report, no errors/overflow')
  page.close()
 browser.close()
