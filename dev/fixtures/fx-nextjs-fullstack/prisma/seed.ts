// Seed de la base de datos. Solo se ejecuta en CI; en local no se importa.
// Trampa superficial: `seedAdminDemo()` existe pero nadie lo llama desde
// el codigo de la app.

import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export async function seedDemo() {
  const user = await prisma.user.upsert({
    where: { email: "demo@example.com" },
    update: {},
    create: {
      email: "demo@example.com",
      name: "Demo User",
      password: "demopassword123",
      role: "user",
    },
  });

  await prisma.article.upsert({
    where: { slug: "hola-mundo" },
    update: {},
    create: {
      slug: "hola-mundo",
      title: "Hola mundo",
      body: "Este es el primer articulo del blog.",
      authorId: user.id,
      publishedAt: new Date(),
    },
  });
}

// Funcion que existe pero nunca se llama desde la app (trampa superficial).
export async function seedAdminDemo() {
  await prisma.user.upsert({
    where: { email: "admin@example.com" },
    update: {},
    create: {
      email: "admin@example.com",
      name: "Admin",
      password: "adminpassword",
      role: "admin",
    },
  });
}