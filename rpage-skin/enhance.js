/* ============================================================
   選用 — 捲動淡入效果（防禦性寫法）
   貼進後台：頁面頭部 HTML 欄位，包在 <script> 裡；或自訂 JS 欄位
   抓不到元素就安靜略過，不會弄壞頁面
   ============================================================ */
(function(){
  try{
    if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var targets = document.querySelectorAll('.module, .o-footer, .hr-stats');
    if(!targets.length || !('IntersectionObserver' in window)) return;
    targets.forEach(function(el){ el.classList.add('js-reveal'); });
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){ e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { threshold:.12 });
    targets.forEach(function(el){ io.observe(el); });
  }catch(err){ /* graceful skip */ }
})();
