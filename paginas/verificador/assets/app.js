document.addEventListener('DOMContentLoaded', () => {
  // Atualiza dinamicamente o status no console do terminal
  const statusEl = document.getElementById('live-status');
  if (statusEl) {
    const timeString = new Date().toLocaleTimeString('pt-BR');
    statusEl.textContent = `[ONLINE · ${timeString}] Engine Operacional`;
  }

  // Efeito interativo suave nos cards de arquitetura
  const cards = document.querySelectorAll('.triad-card, .case-card');
  cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.borderColor = 'rgba(56, 189, 248, 0.4)';
    });
    card.addEventListener('mouseleave', () => {
      card.style.borderColor = '';
    });
  });
});
