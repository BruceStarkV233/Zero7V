/**
 * thumb-lightbox.js
 *
 * 功能：
 * 1. 自动把页面中所有指向 images/ 目录下图片的 <img>，
 *    替换成对应的缩略图（images/thumbs/.../xxx.jpg）。
 * 2. 懒加载：图片滚动到视口附近才真正下载。
 * 3. 点击缩略图时，弹出灯箱（lightbox）显示原图大图。
 *
 * 使用方法：
 *   1. 把这个文件放到仓库里，例如 js/thumb-lightbox.js
 *   2. 在每个用到画廊的 html 页面的 </body> 前加一行：
 *        <script src="js/thumb-lightbox.js" defer></script>
 *      （路径根据你实际放置位置调整）
 *
 * 注意：
 *   - 已经在 src 里包含 "thumbs/" 的图片会被跳过，不会重复处理。
 *   - 如果某张图片不想被处理（比如 logo、头像），给它加上
 *     class="no-thumb" 即可跳过。
 */

(function () {
  "use strict";

  // 根据原图路径计算对应缩略图路径
  // images/场景/xxx.png  ->  images/thumbs/场景/xxx.jpg
  function toThumbSrc(src) {
    var marker = "images/";
    var idx = src.indexOf(marker);
    if (idx === -1) return null;

    var prefix = src.substring(0, idx);
    var rest = src.substring(idx + marker.length);

    if (rest.indexOf("thumbs/") === 0) return null; // 已经是缩略图了

    var dotIdx = rest.lastIndexOf(".");
    var noExt = dotIdx === -1 ? rest : rest.substring(0, dotIdx);

    return prefix + "images/thumbs/" + noExt + ".jpg";
  }

  function createLightbox() {
    var overlay = document.createElement("div");
    overlay.id = "tlb-overlay";
    overlay.innerHTML =
      '<img id="tlb-img" alt="" />' +
      '<div id="tlb-close" aria-label="close">&times;</div>';

    var style = document.createElement("style");
    style.textContent =
      "#tlb-overlay{position:fixed;inset:0;background:rgba(0,0,0,.88);" +
      "display:none;align-items:center;justify-content:center;" +
      "z-index:99999;cursor:zoom-out;padding:24px;box-sizing:border-box;}" +
      "#tlb-overlay.open{display:flex;}" +
      "#tlb-overlay img{max-width:100%;max-height:100%;" +
      "object-fit:contain;box-shadow:0 0 40px rgba(0,0,0,.6);}" +
      "#tlb-close{position:absolute;top:16px;right:24px;color:#fff;" +
      "font-size:32px;line-height:1;cursor:pointer;" +
      "font-family:sans-serif;}";

    document.head.appendChild(style);
    document.body.appendChild(overlay);

    function close() {
      overlay.classList.remove("open");
      document.getElementById("tlb-img").src = "";
    }

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay || e.target.id === "tlb-close") close();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });

    return function open(fullSrc, altText) {
      var img = document.getElementById("tlb-img");
      img.src = fullSrc;
      img.alt = altText || "";
      overlay.classList.add("open");
    };
  }

  function init() {
    var openLightbox = createLightbox();

    var imgs = Array.prototype.slice.call(document.querySelectorAll("img"));

    var observer = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var img = entry.target;
          var realSrc = img.getAttribute("data-src");
          if (realSrc) {
            img.src = realSrc;
            img.removeAttribute("data-src");
          }
          obs.unobserve(img);
        });
      },
      { rootMargin: "300px 0px" }
    );

    imgs.forEach(function (img) {
      if (img.classList.contains("no-thumb")) return;

      var fullSrc = img.getAttribute("src");
      if (!fullSrc) return;

      var thumbSrc = toThumbSrc(fullSrc);
      if (!thumbSrc) return; // 不是 images/ 下的图，跳过

      // 点击看大图
      img.style.cursor = "zoom-in";
      img.addEventListener("click", function () {
        openLightbox(fullSrc, img.alt);
      });

      // 懒加载：先用占位，真正的缩略图地址放到 data-src
      img.setAttribute("data-src", thumbSrc);
      img.setAttribute("loading", "lazy"); // 浏览器原生懒加载兜底
      img.src = thumbSrc; // 也直接设置一遍，避免某些浏览器不支持时图片消失

      observer.observe(img);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
