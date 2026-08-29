export async function onRequest(context) {
  const response = await context.next();

  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("text/html")) {

    const metaTags = `
    <meta property="og:site_name" content="GUENESI">
    <meta property="og:title" content="Сайт с проектами (моими)">
    <meta property="og:description" content="[ВСТАВИТЬ_СЮДА_ТЕКСТ]">
    <meta property="og:url" content="https://quenesi.pages.dev/">
    <meta property="og:type" content="website">

    <meta property="og:image" content="https://quenesi.pages.dev/tg.png">
    <meta property="og:image:secure_url" content="https://quenesi.pages.dev/tg.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:type" content="image/png">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Сайт с проектами (моими)">
    <meta name="twitter:description" content="[ВСТАВИТЬ_СЮДА_ТЕКСТ]">
    <meta name="twitter:image" content="https://quenesi.pages.dev/tg.png">
    `;

    return new HTMLRewriter()
      .on("head", {
        element(el) {
          el.append(metaTags, { html: true });
        },
      })
      .transform(response);
  }

  return response;
}
