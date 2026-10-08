
(() => {
 let pref='light';try{pref=localStorage.getItem('cavitation-course-theme')||'light'}catch(e){}
 const requested=new URLSearchParams(location.search).get('theme');if(requested==='light'||requested==='dark')pref=requested;const root=document.documentElement;root.dataset.theme=pref;
 const btn=document.getElementById('theme-toggle');
 const label=()=>{if(btn)btn.textContent=root.dataset.theme==='dark'?'Day / 日间':'Night / 夜间'};label();
 if(btn)btn.onclick=()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem('cavitation-course-theme',root.dataset.theme)}catch(e){}label()};
 if(window.renderMathInElement)renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\(',right:'\\)',display:false}],throwOnError:false});
 document.querySelectorAll('details').forEach(d=>{d.dataset.wasOpen=d.open?'1':'0'});
 window.addEventListener('beforeprint',()=>document.querySelectorAll('details').forEach(d=>{d.dataset.wasOpen=d.open?'1':'0';d.open=true}));
 window.addEventListener('afterprint',()=>document.querySelectorAll('details').forEach(d=>d.open=d.dataset.wasOpen==='1'));
})();
