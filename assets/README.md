# assets/

Coloque aqui os arquivos estáticos do projeto:

- `Aconchego.ttf` ou `Aconchego.woff2` — fonte display (se disponível localmente)
- Logotipo e ícones SVG

Se a fonte `Aconchego` estiver disponível, adicione o arquivo aqui e
atualize o bloco `@font-face` no `app.py`:

```css
@font-face {
  font-family: 'Aconchego';
  src: url('./assets/Aconchego.woff2') format('woff2'),
       url('./assets/Aconchego.ttf')   format('truetype');
}
```
