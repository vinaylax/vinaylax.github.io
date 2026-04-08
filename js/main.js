/* ============================================
   Vinay Lakshman — main.js
   Stars · Accordion Boxes · Fade-in · Form
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Animated star canvas ─────────────────────
  const canvas = document.getElementById('stars-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let stars = [];

    function resize() {
      canvas.width  = window.innerWidth;
      canvas.height = window.innerHeight;
      buildStars();
    }

    function buildStars() {
      stars = [];
      const n = Math.floor((canvas.width * canvas.height) / 5500);
      for (let i = 0; i < n; i++) {
        stars.push({
          x:     Math.random() * canvas.width,
          y:     Math.random() * canvas.height,
          r:     Math.random() * 1.5 + 0.2,
          alpha: Math.random() * 0.6 + 0.2,
          speed: Math.random() * 0.003 + 0.001,
          phase: Math.random() * Math.PI * 2,
        });
      }
    }

    function draw(ts) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      stars.forEach(s => {
        const a = s.alpha + Math.sin(ts * s.speed + s.phase) * 0.15;
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255,255,255,${Math.min(1, Math.max(0.05, a))})`;
        ctx.fill();
      });
      requestAnimationFrame(draw);
    }

    resize();
    window.addEventListener('resize', resize);
    requestAnimationFrame(draw);
  }

  // ── Fade-in on scroll ────────────────────────
  const fadeEls = document.querySelectorAll('.fade-in');
  if (fadeEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e, i) => {
        if (e.isIntersecting) {
          setTimeout(() => e.target.classList.add('visible'), (i % 4) * 90);
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });
    fadeEls.forEach(el => io.observe(el));
  }

  // ── Accordion boxes ──────────────────────────
  const triggers = document.querySelectorAll('.box-trigger');

  triggers.forEach(trigger => {
    trigger.addEventListener('click', () => {
      const targetId = trigger.dataset.target;
      const panel    = document.getElementById(targetId);
      const isOpen   = trigger.classList.contains('active');

      // Close all first
      triggers.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.box-panel').forEach(p => p.classList.remove('open'));

      // If wasn't open, open this one
      if (!isOpen) {
        trigger.classList.add('active');
        panel.classList.add('open');
        // Smooth scroll to the panel after a brief delay for animation
        setTimeout(() => {
          panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 80);
      }
    });
  });

  // ── Photo upload (click placeholder to upload) ──
  const photoBox     = document.getElementById('hero-photo-box');
  const heroImg      = document.getElementById('hero-img');
  const placeholder  = document.getElementById('photo-placeholder');

  if (photoBox && heroImg && placeholder) {
    photoBox.style.cursor = 'pointer';
    photoBox.title = 'Click to upload your photo';

    photoBox.addEventListener('click', () => {
      const input = document.createElement('input');
      input.type  = 'file';
      input.accept = 'image/*';
      input.onchange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (ev) => {
          heroImg.src = ev.target.result;
          heroImg.style.display = 'block';
          placeholder.style.display = 'none';
          photoBox.style.border = 'none';
          photoBox.style.cursor = 'default';
          photoBox.title = '';
        };
        reader.readAsDataURL(file);
      };
      input.click();
    });
  }

});
