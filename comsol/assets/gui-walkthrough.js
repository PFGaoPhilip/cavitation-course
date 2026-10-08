
(() => {
  document.querySelectorAll('.gui-walkthrough td code, .copy-block').forEach(node => {
    const value=node.textContent;
    if(!value.trim())return;
    const button=document.createElement('button');button.type='button';button.className='copy-value';button.textContent='Copy / 复制';
    button.setAttribute('aria-label','Copy exact field value');
    button.onclick=async()=>{try{if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(value)}else{
      const area=document.createElement('textarea');area.value=value;area.style.position='fixed';area.style.top='-1000px';document.body.append(area);area.select();
      if(!document.execCommand('copy'))throw new Error('copy');area.remove();}
      button.textContent='Copied / 已复制';setTimeout(()=>button.textContent='Copy / 复制',1400);
    }catch(e){button.textContent='Select text / 选中文本';const range=document.createRange();range.selectNodeContents(node);const sel=window.getSelection();sel.removeAllRanges();sel.addRange(range)}};
    node.after(button);
  });
})();
