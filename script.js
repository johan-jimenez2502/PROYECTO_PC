window.addEventListener('load', () => {
  const splash = document.querySelector('.splash');
  const contenido = document.querySelector('.contenido');

  setTimeout(() => {
    splash.style.display = 'none';
    contenido.style.display = 'block';
  }, 4000);
});
