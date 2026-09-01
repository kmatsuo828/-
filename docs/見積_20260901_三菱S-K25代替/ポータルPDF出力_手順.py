import base64,json,subprocess,time,sys,os
SP='/tmp/claude-0/-home-user--/bdd2ed83-699d-5548-985c-f70774d98b1a/scratchpad'
q=json.load(open(SP+'/quote.json'))
frag=base64.urlsafe_b64encode(json.dumps(q,ensure_ascii=False).encode()).decode().rstrip('=')
LIB=open(SP+'/package/dist/html2pdf.bundle.min.js','rb').read()
srv=subprocess.Popen([sys.executable,'-m','http.server','8768','--bind','127.0.0.1','-d','/home/user/-'],
                     stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
time.sleep(1.5)
from playwright.sync_api import sync_playwright
try:
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
                            args=['--no-sandbox'])
        ctx=b.new_context(viewport={'width':1280,'height':1000}, accept_downloads=True)
        # cdnjs はプロキシで遮断されるので、npm から取得した同一版をローカルで返す
        ctx.route('https://cdnjs.cloudflare.com/**',
                  lambda route: route.fulfill(status=200, body=LIB,
                                              headers={'content-type':'application/javascript'}))
        pg=ctx.new_page()
        pg.on('console', lambda m: print('C:',m.type,m.text[:120]) if m.type=='error' else None)
        pg.goto('http://127.0.0.1:8768/zaiko-kanri.html#quote='+frag, wait_until='load')
        pg.wait_for_function("typeof quoteLines!=='undefined' && quoteLines.length===2", timeout=60000)
        pg.wait_for_timeout(600)
        pg.screenshot(path=SP+'/portal_ui_1_modal.png')          # 見積モーダル
        pg.evaluate("generateQuotePdf()")
        pg.wait_for_function("document.getElementById('pdf-preview').style.display==='block'", timeout=30000)
        pg.wait_for_timeout(1200)
        pg.screenshot(path=SP+'/portal_ui_2_preview.png')        # PDFプレビュー画面
        with pg.expect_download(timeout=180000) as dl:
            pg.click('.pdf-download-btn')                        # ポータルの「⬇ PDFダウンロード」
        d=dl.value
        out=os.path.join(SP, d.suggested_filename)
        d.save_as(out)
        print('DOWNLOADED:', out, os.path.getsize(out))
        b.close()
finally:
    srv.terminate()
