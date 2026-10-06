// Constantes de tags para revalidateTag / next.tags.
// Trampa ecosistema #5: la app usa 'articles' para revalidar, pero
// la home page consume 'home' (en app/page.tsx). El tag 'articles'
// nunca invalida la home.

export const TAG_ARTICLES = "articles";
export const TAG_COMMENTS = "comments";
export const TAG_HOME = "home";
export const TAG_ARTICULO = (slug: string) => `articulo:${slug}`;

// El cookie de sesion vive en next/headers y es HTTPOnly (definido en
// auth.ts). El middleware lo lee por nombre.
export const SESSION_COOKIE = "fxnext-session";